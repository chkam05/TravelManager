from __future__ import annotations

from collections import defaultdict
from contextlib import closing
import gzip
import json
import sqlite3
from threading import Lock

from resources.offline_maps import OfflineMapLayers
from services.offline_maps.errors import OfflineMapTileGenerationError
from storage.offline_maps import OfflineMapPaths


class OfflineMapOnDemandTiles:
    """Generates and permanently caches one detailed vector tile at a time."""

    def __init__(self, paths: OfflineMapPaths):
        self._paths = paths
        self._locks_guard = Lock()
        self._locks: dict[tuple[str, int, int, int], Lock] = {}

    def generate(
        self, map_id: str, file_name: str, zoom: int, column: int, row: int
    ) -> bytes | None:
        key = (map_id, zoom, column, row)
        with self._locks_guard:
            tile_lock = self._locks.setdefault(key, Lock())
        try:
            with tile_lock:
                cached = self._read_cached(file_name, zoom, column, row)
                if cached is not None:
                    return cached
                encoded = self._encode(map_id, zoom, column, row)
                if not encoded:
                    return None
                compressed = gzip.compress(encoded, compresslevel=6, mtime=0)
                self._store(file_name, zoom, column, row, compressed)
                return compressed
        finally:
            with self._locks_guard:
                if not tile_lock.locked():
                    self._locks.pop(key, None)

    def _encode(self, map_id, zoom, column, row):
        try:
            import mapbox_vector_tile
            import mercantile
            from mapbox_vector_tile.encoder import on_invalid_geometry_make_valid
            from shapely import box, from_wkb, transform

            feature_path = self._paths.map_features_path(map_id)
            if not feature_path.is_file():
                raise OfflineMapTileGenerationError(
                    'Ta mapa nie zawiera indeksu potrzebnego do szczegółowego przybliżenia.'
                )
            tile_bounds = mercantile.bounds(column, row, zoom)
            mercator_bounds = mercantile.xy_bounds(column, row, zoom)
            clipping_box = box(
                tile_bounds.west, tile_bounds.south,
                tile_bounds.east, tile_bounds.north,
            )
            layers: dict[str, list[dict]] = defaultdict(list)
            with closing(sqlite3.connect(
                f'file:{feature_path}?mode=ro', uri=True, timeout=30
            )) as connection:
                rows = connection.execute('''
                    SELECT f.osm_id, f.layer, f.geometry_wkb,
                           f.properties, f.priority
                    FROM feature_bounds AS b
                    JOIN features AS f ON f.id = b.id
                    WHERE f.min_zoom <= ?
                      AND b.min_lon <= ? AND b.max_lon >= ?
                      AND b.min_lat <= ? AND b.max_lat >= ?
                    ORDER BY f.priority, f.id
                ''', (
                    zoom, tile_bounds.east, tile_bounds.west,
                    tile_bounds.north, tile_bounds.south,
                )).fetchall()
            for osm_id, layer_id, geometry_wkb, properties, _priority in rows:
                definition = OfflineMapLayers.BY_ID.get(layer_id)
                if definition is None:
                    continue
                geometry = from_wkb(geometry_wkb).intersection(clipping_box)
                if geometry.is_empty:
                    continue
                geometry = transform(geometry, self._web_mercator_transform)
                tolerance = definition.simplification_for_zoom(zoom)
                if tolerance:
                    geometry = geometry.simplify(tolerance, preserve_topology=True)
                if geometry.is_empty:
                    continue
                layers[layer_id].append({
                    'id': int(osm_id),
                    'geometry': geometry,
                    'properties': json.loads(properties),
                })
            if not layers:
                return None
            payload = [
                {'name': layer_id, 'features': features}
                for layer_id, features in layers.items()
            ]
            return mapbox_vector_tile.encode(payload, default_options={
                'quantize_bounds': (
                    mercator_bounds.left, mercator_bounds.bottom,
                    mercator_bounds.right, mercator_bounds.top,
                ),
                'extents': 4096,
                'on_invalid_geometry': on_invalid_geometry_make_valid,
            })
        except OfflineMapTileGenerationError:
            raise
        except Exception as error:
            raise OfflineMapTileGenerationError(
                f'Nie udało się wygenerować szczegółowego kafelka: {error}'
            ) from error

    def _read_cached(self, file_name, zoom, column, row):
        path = self._paths.map_path(file_name)
        if not path.is_file():
            return None
        tms_row = (1 << zoom) - 1 - row
        with closing(sqlite3.connect(path, timeout=30)) as connection:
            result = connection.execute('''
                SELECT tile_data FROM tiles
                WHERE zoom_level = ? AND tile_column = ? AND tile_row = ?
            ''', (zoom, column, tms_row)).fetchone()
        return bytes(result[0]) if result else None

    def _store(self, file_name, zoom, column, row, payload):
        path = self._paths.map_path(file_name)
        tms_row = (1 << zoom) - 1 - row
        with closing(sqlite3.connect(path, timeout=30)) as connection:
            connection.execute('PRAGMA busy_timeout=30000')
            connection.execute('''
                INSERT OR IGNORE INTO tiles(
                    zoom_level, tile_column, tile_row, tile_data
                ) VALUES (?, ?, ?, ?)
            ''', (zoom, column, tms_row, payload))
            connection.commit()

    @staticmethod
    def _web_mercator_transform(coordinates):
        import numpy

        radius = 6378137.0
        result = numpy.array(coordinates, dtype=float, copy=True)
        result[:, 0] = numpy.radians(result[:, 0]) * radius
        latitude = numpy.clip(result[:, 1], -85.05112878, 85.05112878)
        result[:, 1] = radius * numpy.log(
            numpy.tan(numpy.pi / 4 + numpy.radians(latitude) / 2)
        )
        return result

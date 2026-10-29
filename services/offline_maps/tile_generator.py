from __future__ import annotations

from collections import defaultdict
from contextlib import closing
from datetime import datetime, timezone
import json
import sqlite3
from typing import Callable

from models.offline_maps import OfflineMapJob
from resources.offline_maps import OfflineMapLayers
from services.offline_maps.dependencies import OfflineMapDependencies
from services.offline_maps.errors import (
    OfflineMapTileGenerationCancelled,
    OfflineMapTileGenerationError,
)
from services.offline_maps.resource_guard import OfflineMapResourceGuard
from services.offline_maps.package_reuse import OfflineMapPackageReuse
from storage.offline_maps import (
    OfflineMapFeatureStorage,
    OfflineMapPaths,
    OfflineMapTileStorage,
)


class OfflineMapTileGenerator:
    """Builds MVT blobs in bounded batches from the normalized feature store."""

    FEATURE_BATCH_SIZE = 500
    ASSIGNMENT_BATCH_SIZE = 5000
    COMMIT_INTERVAL = 20
    # Dense local detail is unreadable at country-scale zooms and can put
    # hundreds of thousands of geometries into one MVT tile.
    DETAIL_MIN_ZOOM = {'water': 9, 'landuse': 11}
    LARGE_WATER_SPAN = 0.1

    def __init__(self, paths: OfflineMapPaths):
        self._paths = paths
        self._resources = OfflineMapResourceGuard(paths.root)
        self._reuse = OfflineMapPackageReuse(paths)

    def process(
        self,
        job: OfflineMapJob,
        cancelled: Callable[[], bool],
        progress: Callable[[OfflineMapJob, int, int], None] | None = None,
    ) -> str:
        OfflineMapDependencies.require()
        work = self._paths.job_work_path(job.id)
        features = OfflineMapFeatureStorage(work)
        if not features.path.is_file():
            raise OfflineMapTileGenerationError('Brak przeanalizowanych danych OSM.')
        self._resources.ensure_stage(features.path.stat().st_size, 'generowanie kafelków')
        tiles = OfflineMapTileStorage(work)
        try:
            tiles.create(features.path)
            bounds, feature_count = self._assign_tiles(
                features, tiles, job, cancelled, progress
            )
            reusable = self._reuse.reusable_maps(job)
            coverages = {
                region.id: region.coverage
                for region in self._paths.catalog.load()[1]
            }
            try:
                _copied, reused_layers = tiles.import_complete_tiles(
                    [
                        (
                            self._paths.map_path(item.file_name),
                            coverages[item.region_id],
                        )
                        for item in reusable
                        if coverages.get(item.region_id) is not None
                    ],
                    job.max_zoom,
                    cancelled,
                )
            except InterruptedError as error:
                raise OfflineMapTileGenerationCancelled(
                    'Ponowne użycie kafelków zostało anulowane.'
                ) from error
            tile_count = tiles.assignment_count()
            self._report(job, 0, tile_count, progress, phase='encoding')
            layer_ids = reused_layers | self._encode_tiles(
                tiles, job, tile_count, cancelled, progress
            )
            generated_count, min_zoom, max_zoom = tiles.generated_stats()
            if generated_count == 0:
                raise OfflineMapTileGenerationError(
                    'Generator nie utworzył żadnego kafelka mapy.'
                )
            tiles.set_metadata('bounds', bounds)
            tiles.set_metadata('min_zoom', min_zoom)
            tiles.set_metadata('max_zoom', max_zoom)
            tiles.set_metadata('feature_count', feature_count)
            tiles.set_metadata('tile_count', generated_count)
            tiles.set_metadata('format', 'pbf')
            tiles.set_metadata('layers', sorted(layer_ids))
            tiles.finalize()
            tiles.commit()
            self._report(job, tile_count, tile_count, progress)
            return 'optimising'
        except OfflineMapTileGenerationCancelled:
            tiles.discard()
            raise
        except Exception as error:
            tiles.discard()
            if isinstance(error, OfflineMapTileGenerationError):
                raise
            raise OfflineMapTileGenerationError(
                f'Nie udało się wygenerować kafelków mapy: {error}'
            ) from error
        finally:
            tiles.close()

    def _assign_tiles(self, features, tiles, job, cancelled, progress):
        import mercantile

        with closing(sqlite3.connect(features.path)) as connection:
            bounds_row = connection.execute('''
                SELECT MIN(min_lon), MIN(min_lat), MAX(max_lon), MAX(max_lat),
                       COUNT(*)
                FROM features
                WHERE min_zoom <= ?
                  AND (layer NOT IN ('water', 'landuse')
                       OR (layer = 'water' AND ? >= ?)
                       OR (layer = 'landuse' AND ? >= ?)
                       OR (layer = 'water' AND geometry_type = 'polygon'
                           AND (max_lon - min_lon >= ? OR max_lat - min_lat >= ?)))
            ''', (job.max_zoom,
                  job.max_zoom, self.DETAIL_MIN_ZOOM['water'],
                  job.max_zoom, self.DETAIL_MIN_ZOOM['landuse'],
                  self.LARGE_WATER_SPAN, self.LARGE_WATER_SPAN)).fetchone()
            if not bounds_row or bounds_row[0] is None:
                raise OfflineMapTileGenerationError(
                    'Brak obiektów możliwych do umieszczenia na mapie.'
                )
            bounds = [float(value) for value in bounds_row[:4]]
            total_features = int(bounds_row[4])
            self._report(job, 0, total_features, progress, phase='assignment')
            cursor = connection.execute('''
                SELECT id, layer, geometry_type, min_zoom,
                       min_lon, min_lat, max_lon, max_lat
                FROM features
                WHERE min_zoom <= ?
                  AND (layer NOT IN ('water', 'landuse')
                       OR (layer = 'water' AND ? >= ?)
                       OR (layer = 'landuse' AND ? >= ?)
                       OR (layer = 'water' AND geometry_type = 'polygon'
                           AND (max_lon - min_lon >= ? OR max_lat - min_lat >= ?)))
                ORDER BY id
            ''', (job.max_zoom,
                  job.max_zoom, self.DETAIL_MIN_ZOOM['water'],
                  job.max_zoom, self.DETAIL_MIN_ZOOM['landuse'],
                  self.LARGE_WATER_SPAN, self.LARGE_WATER_SPAN))
            assignments: list[tuple[int, int, int, int]] = []
            processed = 0
            while True:
                rows = cursor.fetchmany(self.FEATURE_BATCH_SIZE)
                if not rows:
                    break
                for feature_id, layer, geometry_type, min_zoom, west, south, east, north in rows:
                    self._check_cancel(cancelled)
                    large_water = layer == 'water' and geometry_type == 'polygon' and (
                        east - west >= self.LARGE_WATER_SPAN
                        or north - south >= self.LARGE_WATER_SPAN
                    )
                    if not large_water:
                        min_zoom = max(min_zoom, self.DETAIL_MIN_ZOOM.get(layer, 0))
                    for tile in mercantile.tiles(
                        west, south, east, north,
                        range(min_zoom, job.max_zoom + 1),
                        truncate=True,
                    ):
                        self._check_cancel(cancelled)
                        assignments.append((tile.z, tile.x, tile.y, feature_id))
                        if len(assignments) >= self.ASSIGNMENT_BATCH_SIZE:
                            tiles.assign(assignments)
                            assignments.clear()
                            self._resources.ensure(
                                self._resources.MINIMUM_FREE_BYTES,
                                'przypisywanie kafelków',
                            )
                    processed += 1
                if assignments:
                    tiles.assign(assignments)
                    assignments.clear()
                self._report(job, processed, total_features, progress)
        return bounds, total_features

    def _encode_tiles(self, tiles, job, total, cancelled, progress):
        import mapbox_vector_tile
        import mercantile
        from mapbox_vector_tile.encoder import on_invalid_geometry_make_valid
        from shapely import box, from_wkb, transform

        completed = 0
        generated_layers: set[str] = set()
        for zoom, column, row in tiles.tile_coordinates():
            self._check_cancel(cancelled)
            if completed % 1000 == 0:
                self._resources.ensure(
                    self._resources.MINIMUM_FREE_BYTES,
                    'generowanie kafelków',
                )
            tile_bounds = mercantile.bounds(column, row, zoom)
            mercator_bounds = mercantile.xy_bounds(column, row, zoom)
            layers: dict[str, list[dict]] = defaultdict(list)
            clipping_box = box(
                tile_bounds.west, tile_bounds.south,
                tile_bounds.east, tile_bounds.north,
            )
            for osm_id, layer_id, geometry_wkb, properties, _priority in (
                tiles.tile_features(zoom, column, row)
            ):
                self._check_cancel(cancelled)
                definition = OfflineMapLayers.BY_ID.get(layer_id)
                if definition is None:
                    continue
                geometry = from_wkb(geometry_wkb)
                geometry = geometry.intersection(clipping_box)
                geometry = transform(geometry, self._web_mercator_transform)
                tolerance = definition.simplification_for_zoom(zoom)
                if tolerance:
                    geometry = geometry.simplify(
                        tolerance,
                        preserve_topology=True,
                    )
                if geometry.is_empty:
                    continue
                layers[layer_id].append({
                    'id': int(osm_id),
                    'geometry': geometry,
                    'properties': json.loads(properties),
                })
            if layers:
                generated_layers.update(layers)
                payload = [
                    {'name': layer_id, 'features': layer_features}
                    for layer_id, layer_features in layers.items()
                ]
                encoded = mapbox_vector_tile.encode(payload, default_options={
                    'quantize_bounds': (
                        mercator_bounds.left, mercator_bounds.bottom,
                        mercator_bounds.right, mercator_bounds.top,
                    ),
                    'extents': 4096,
                    'on_invalid_geometry': on_invalid_geometry_make_valid,
                })
                if encoded:
                    tiles.save_tile(zoom, column, row, encoded)
            completed += 1
            if completed % self.COMMIT_INTERVAL == 0:
                tiles.commit()
            self._report(job, completed, total, progress)
        tiles.commit()
        return generated_layers

    @staticmethod
    def _web_mercator_transform(coordinates):
        """Transforms a Shapely coordinate array from WGS84 to EPSG:3857."""
        import numpy

        radius = 6378137.0
        result = numpy.array(coordinates, dtype=float, copy=True)
        result[:, 0] = numpy.radians(result[:, 0]) * radius
        latitude = numpy.clip(result[:, 1], -85.05112878, 85.05112878)
        result[:, 1] = radius * numpy.log(
            numpy.tan(numpy.pi / 4 + numpy.radians(latitude) / 2)
        )
        return result

    @staticmethod
    def _check_cancel(cancelled):
        if cancelled():
            raise OfflineMapTileGenerationCancelled(
                'Generowanie kafelków zostało anulowane.'
            )

    def _report(self, job, current, total, callback, phase=None):
        work = self._paths.job_work_path(job.id, create=False)
        artifacts_size = sum(
            path.stat().st_size for path in work.iterdir() if path.is_file()
        ) if work.is_dir() else 0
        self._resources.ensure_stage(artifacts_size, 'generowanie kafelków', 1)
        job.status = 'running'
        job.stage = 'building_tiles'
        if phase is not None:
            job.phase = phase
        job.current = current
        job.total = total
        job.updated_at = datetime.now(timezone.utc).isoformat()
        self._paths.jobs.upsert(job)
        if callback:
            callback(job, current, total)

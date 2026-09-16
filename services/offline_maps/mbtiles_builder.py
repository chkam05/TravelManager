from __future__ import annotations

from contextlib import closing
from datetime import datetime, timezone
import gzip
import json
from pathlib import Path
import sqlite3
from typing import Callable

from config import APP_NAME, APP_VERSION
from models.offline_maps import OfflineMap, OfflineMapJob
from services.offline_maps.errors import (
    OfflineMapInstallationCancelled,
    OfflineMapInstallationError,
)
from storage.offline_maps import OfflineMapPaths, OfflineMapTileStorage
from services.offline_maps.resource_guard import OfflineMapResourceGuard


class OfflineMapMbtilesBuilder:
    """Builds, validates and atomically installs one standards-based MBTiles."""

    BATCH_SIZE = 500
    SCHEMA_VERSION = 1
    REQUIRED_METADATA = frozenset({
        'name', 'type', 'version', 'description', 'format', 'bounds',
        'center', 'minzoom', 'maxzoom', 'attribution', 'compression', 'json',
    })

    def __init__(self, paths: OfflineMapPaths):
        self._paths = paths
        self._resources = OfflineMapResourceGuard(paths.root)

    def process(
        self, job: OfflineMapJob, cancelled: Callable[[], bool]
    ) -> str:
        work = self._paths.job_work_path(job.id)
        generated = OfflineMapTileStorage(work).path
        if not generated.is_file():
            raise OfflineMapInstallationError('Brak wygenerowanych kafelków mapy.')
        self._resources.ensure_stage(generated.stat().st_size, 'instalacja')
        region = self._region(job.region_id)
        final_path = self._paths.map_path(f'{job.map_id}.mbtiles')
        partial_path = work / 'package.mbtiles.part'
        replacing = final_path.exists()
        if replacing and not job.is_update:
            raise OfflineMapInstallationError('Docelowa mapa już istnieje.')
        if job.is_update and not replacing:
            raise OfflineMapInstallationError('Brak mapy źródłowej do aktualizacji.')
        self._remove(partial_path)
        installed_file_created = False
        try:
            self._build(generated, partial_path, region.name, job, cancelled)
            self._check_cancel(cancelled)
            self._validate(partial_path)
            self._optimise(partial_path)
            self._check_cancel(cancelled)
            self._set_progress(job, 'installing', 1, 1)
            installed = self._installed_model(partial_path, generated, region, job)
            partial_path.replace(final_path)
            installed_file_created = not replacing
            try:
                self._paths.maps.upsert(installed)
            except Exception:
                if installed_file_created:
                    self._remove(final_path)
                raise
            return 'installing'
        except OfflineMapInstallationCancelled:
            self._remove(partial_path)
            raise
        except Exception as error:
            self._remove(partial_path)
            if installed_file_created:
                self._remove(final_path)
            if isinstance(error, OfflineMapInstallationError):
                raise
            raise OfflineMapInstallationError(
                f'Nie udało się zainstalować mapy MBTiles: {error}'
            ) from error

    def _build(self, generated, destination, name, job, cancelled):
        with closing(sqlite3.connect(generated)) as source, closing(
            sqlite3.connect(destination)
        ) as target:
            metadata = {
                key: json.loads(value)
                for key, value in source.execute('SELECT key, value FROM metadata')
            }
            bounds = self._bounds(metadata.get('bounds'))
            minimum = int(metadata.get('min_zoom'))
            maximum = int(metadata.get('max_zoom'))
            tile_count = int(metadata.get('tile_count') or 0)
            if not 0 <= minimum <= maximum <= 22 or tile_count < 1:
                raise OfflineMapInstallationError('Nieprawidłowe metadane kafelków.')
            target.executescript('''
                PRAGMA journal_mode=DELETE;
                PRAGMA synchronous=FULL;
                CREATE TABLE metadata (
                    name TEXT PRIMARY KEY,
                    value TEXT NOT NULL
                );
                CREATE TABLE tiles (
                    zoom_level INTEGER NOT NULL,
                    tile_column INTEGER NOT NULL,
                    tile_row INTEGER NOT NULL,
                    tile_data BLOB NOT NULL
                );
                CREATE UNIQUE INDEX tile_index ON tiles (
                    zoom_level, tile_column, tile_row
                );
            ''')
            center = [
                (bounds[0] + bounds[2]) / 2,
                (bounds[1] + bounds[3]) / 2,
                minimum,
            ]
            layers = metadata.get('layers') or []
            if not isinstance(layers, list) or not all(
                isinstance(layer, str) and layer for layer in layers
            ):
                raise OfflineMapInstallationError(
                    'Nieprawidłowa lista warstw kafelków.'
                )
            vector_layers = [
                {'id': layer, 'minzoom': minimum, 'maxzoom': maximum}
                for layer in layers
            ]
            values = {
                'name': name,
                'type': 'baselayer',
                'version': str(self.SCHEMA_VERSION),
                'description': f'{APP_NAME} offline map',
                'format': 'pbf',
                'bounds': ','.join(self._number(value) for value in bounds),
                'center': ','.join(self._number(value) for value in center),
                'minzoom': str(minimum),
                'maxzoom': str(maximum),
                'attribution': '© OpenStreetMap contributors',
                'compression': 'gzip',
                'generator': f'{APP_NAME} {APP_VERSION}',
                'json': json.dumps({'vector_layers': vector_layers}),
            }
            target.executemany(
                'INSERT INTO metadata(name, value) VALUES (?, ?)', values.items()
            )

            cursor = source.execute('''
                SELECT zoom_level, tile_column, tile_row, tile_data
                FROM generated_tiles
                ORDER BY zoom_level, tile_column, tile_row
            ''')
            completed = 0
            while True:
                rows = cursor.fetchmany(self.BATCH_SIZE)
                if not rows:
                    break
                self._check_cancel(cancelled)
                output = []
                for zoom, column, xyz_row, data in rows:
                    tms_row = (1 << zoom) - 1 - xyz_row
                    output.append((
                        zoom, column, tms_row,
                        gzip.compress(bytes(data), compresslevel=6, mtime=0),
                    ))
                target.executemany('''
                    INSERT INTO tiles(
                        zoom_level, tile_column, tile_row, tile_data
                    ) VALUES (?, ?, ?, ?)
                ''', output)
                target.commit()
                completed += len(output)
                self._resources.ensure_stage(
                    generated.stat().st_size, 'instalacja'
                )
                self._set_progress(job, 'optimising', completed, tile_count)
            if completed != tile_count:
                raise OfflineMapInstallationError(
                    'Liczba zapisanych kafelków nie zgadza się z metadanymi.'
                )

    def _validate(self, path: Path) -> None:
        import mapbox_vector_tile

        with closing(sqlite3.connect(f'file:{path}?mode=ro', uri=True)) as connection:
            integrity = connection.execute('PRAGMA quick_check').fetchone()
            if integrity != ('ok',):
                raise OfflineMapInstallationError('Kontrola integralności MBTiles nie powiodła się.')
            metadata = dict(connection.execute('SELECT name, value FROM metadata'))
            if not self.REQUIRED_METADATA.issubset(metadata):
                raise OfflineMapInstallationError('Baza MBTiles nie zawiera metadanych.')
            count, invalid = connection.execute('''
                SELECT COUNT(*), SUM(
                    zoom_level < 0 OR zoom_level > 22 OR
                    tile_column < 0 OR tile_column >= (1 << zoom_level) OR
                    tile_row < 0 OR tile_row >= (1 << zoom_level)
                ) FROM tiles
            ''').fetchone()
            if count < 1 or invalid:
                raise OfflineMapInstallationError('Baza zawiera nieprawidłowe kafelki.')
            samples = connection.execute('''
                SELECT tile_data FROM tiles
                ORDER BY zoom_level, tile_column, tile_row
                LIMIT 3
            ''').fetchall()
            for (compressed,) in samples:
                try:
                    decoded = gzip.decompress(compressed)
                    if not decoded or not mapbox_vector_tile.decode(decoded):
                        raise ValueError('empty tile')
                except Exception as error:
                    raise OfflineMapInstallationError(
                        'Nie udało się zweryfikować danych MVT.'
                    ) from error

    @staticmethod
    def _optimise(path: Path) -> None:
        with closing(sqlite3.connect(path)) as connection:
            connection.execute('ANALYZE')
            connection.commit()
            connection.execute('VACUUM')
            connection.commit()

    def _installed_model(self, package_path, generated, region, job):
        with closing(sqlite3.connect(generated)) as connection:
            metadata = {
                key: json.loads(value)
                for key, value in connection.execute('SELECT key, value FROM metadata')
            }
        return OfflineMap.from_dict({
            'id': job.map_id,
            'region_id': job.region_id,
            'name': region.name,
            'file_name': f'{job.map_id}.mbtiles',
            'size': package_path.stat().st_size,
            'bounds': self._bounds(metadata.get('bounds')),
            'min_zoom': int(metadata.get('min_zoom')),
            'max_zoom': int(metadata.get('max_zoom')),
            'installed_at': datetime.now(timezone.utc).isoformat(),
            'source_updated_at': region.source_updated_at,
            'schema_version': self.SCHEMA_VERSION,
        })

    def _region(self, identifier):
        _, regions = self._paths.catalog.load()
        region = next((item for item in regions if item.id == identifier), None)
        if region is None:
            raise OfflineMapInstallationError('Region zniknął z katalogu map.')
        return region

    def _set_progress(self, job, stage, current, total):
        job.status = 'running'
        job.stage = stage
        job.current = current
        job.total = total
        job.updated_at = datetime.now(timezone.utc).isoformat()
        self._paths.jobs.upsert(job)

    @staticmethod
    def _bounds(value):
        if (
            not isinstance(value, list) or len(value) != 4
            or any(type(item) not in (int, float) for item in value)
        ):
            raise OfflineMapInstallationError('Nieprawidłowy zakres mapy.')
        west, south, east, north = [float(item) for item in value]
        if not (-180 <= west <= east <= 180 and -90 <= south <= north <= 90):
            raise OfflineMapInstallationError('Nieprawidłowy zakres mapy.')
        return [west, south, east, north]

    @staticmethod
    def _number(value: float) -> str:
        return f'{value:.7f}'.rstrip('0').rstrip('.')

    @staticmethod
    def _check_cancel(cancelled):
        if cancelled():
            raise OfflineMapInstallationCancelled(
                'Instalowanie mapy zostało anulowane.'
            )

    @staticmethod
    def _remove(path: Path) -> None:
        try:
            path.unlink()
        except FileNotFoundError:
            pass

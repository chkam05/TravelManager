from __future__ import annotations

from contextlib import closing
import gzip
import json
import sqlite3
from tempfile import TemporaryDirectory
import unittest

import mapbox_vector_tile
from shapely import Point

from models.offline_maps import OfflineMap, OfflineMapJob, OfflineMapRegion
from services.offline_maps import OfflineMapMbtilesBuilder
from services.offline_maps.errors import (
    OfflineMapInstallationCancelled,
    OfflineMapInstallationError,
)
from storage.offline_maps import OfflineMapPaths, OfflineMapTileStorage


NOW = '2026-09-14T12:00:00+00:00'


def job():
    return OfflineMapJob.from_dict({
        'id': 'install-job', 'region_id': 'fixture', 'map_id': 'fixture-map',
        'status': 'queued', 'stage': 'optimising',
        'downloaded_bytes': 100, 'total_bytes': 100,
        'current': 0, 'total': 0, 'max_zoom': 14,
        'cancel_requested': False, 'created_at': NOW, 'updated_at': NOW,
        'error': '',
    })


class OfflineMapMbtilesBuilderTests(unittest.TestCase):
    def setUp(self):
        self.temporary = TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.paths = OfflineMapPaths(self.temporary.name)
        self.current_job = job()
        self.paths.jobs.save([self.current_job])
        self.paths.catalog.save(NOW, [OfflineMapRegion.from_dict({
            'id': 'fixture', 'name': 'Obszar testowy', 'parent_id': 'europe',
            'country_codes': [], 'region_codes': [],
            'pbf_url': 'https://download.geofabrik.de/fixture.osm.pbf',
            'pbf_size': 100, 'source_updated_at': NOW,
            'bounds': [18.0, 49.0, 20.0, 51.0], 'children': [],
        })])
        self.work = self.paths.job_work_path(self.current_job.id)

    def _create_tiles(self, payload=None, coordinates=None):
        if payload is None:
            payload = mapbox_vector_tile.encode([{
                'name': 'places',
                'features': [{
                    'id': 1, 'geometry': Point(2048, 2048),
                    'properties': {'name': 'Testowo'},
                }],
            }])
        path = OfflineMapTileStorage(self.work).path
        with closing(sqlite3.connect(path)) as connection:
            connection.executescript('''
                CREATE TABLE generated_tiles (
                    zoom_level INTEGER NOT NULL,
                    tile_column INTEGER NOT NULL,
                    tile_row INTEGER NOT NULL,
                    tile_data BLOB NOT NULL,
                    PRIMARY KEY (zoom_level, tile_column, tile_row)
                );
                CREATE TABLE metadata (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL
                );
            ''')
            coordinates = coordinates or [(2, 2, 1)]
            connection.executemany(
                'INSERT INTO generated_tiles VALUES (?, ?, ?, ?)',
                ((*coordinate, payload) for coordinate in coordinates),
            )
            metadata = {
                'bounds': [0.0, 0.0, 10.0, 10.0],
                'min_zoom': min(row[0] for row in coordinates),
                'max_zoom': max(row[0] for row in coordinates),
                'tile_count': len(coordinates),
                'format': 'pbf', 'layers': ['places'],
            }
            connection.executemany(
                'INSERT INTO metadata VALUES (?, ?)',
                ((key, json.dumps(value)) for key, value in metadata.items()),
            )
            connection.commit()
        return path

    def test_builds_valid_tms_mbtiles_and_registers_only_after_validation(self):
        self._create_tiles()
        result = OfflineMapMbtilesBuilder(self.paths).process(
            self.current_job, lambda: False
        )
        self.assertEqual(result, 'installing')
        installed = self.paths.maps.load()
        self.assertEqual(len(installed), 1)
        self.assertEqual(installed[0].id, 'fixture-map')
        package = self.paths.map_path(installed[0].file_name)
        self.assertEqual(installed[0].size, package.stat().st_size)

        with closing(sqlite3.connect(package)) as connection:
            metadata = dict(connection.execute(
                'SELECT name, value FROM metadata'
            ))
            zoom, column, tms_row, compressed = connection.execute(
                'SELECT zoom_level, tile_column, tile_row, tile_data FROM tiles'
            ).fetchone()
            integrity = connection.execute('PRAGMA quick_check').fetchone()[0]
        self.assertEqual((zoom, column, tms_row), (2, 2, 2))
        decoded = mapbox_vector_tile.decode(gzip.decompress(compressed))
        self.assertIn('places', decoded)
        self.assertEqual(metadata['format'], 'pbf')
        self.assertEqual(metadata['compression'], 'gzip')
        self.assertIn('OpenStreetMap contributors', metadata['attribution'])
        self.assertEqual(integrity, 'ok')

    def test_converts_xyz_rows_to_tms_for_top_middle_and_bottom_tiles(self):
        self._create_tiles(coordinates=[(3, 1, 0), (3, 1, 3), (3, 1, 7)])
        OfflineMapMbtilesBuilder(self.paths).process(
            self.current_job, lambda: False
        )

        package = self.paths.map_path('fixture-map.mbtiles')
        with closing(sqlite3.connect(package)) as connection:
            rows = connection.execute('''
                SELECT tile_row FROM tiles
                WHERE zoom_level = 3 AND tile_column = 1
                ORDER BY tile_row
            ''').fetchall()
        self.assertEqual(rows, [(0,), (4,), (7,)])

    def test_invalid_mvt_never_becomes_an_installed_map(self):
        self._create_tiles(b'not-a-vector-tile')
        with self.assertRaisesRegex(
            OfflineMapInstallationError, 'zweryfikować danych MVT'
        ):
            OfflineMapMbtilesBuilder(self.paths).process(
                self.current_job, lambda: False
            )
        self.assertEqual(self.paths.maps.load(), [])
        self.assertFalse(self.paths.map_path('fixture-map.mbtiles').exists())
        self.assertFalse((self.work / 'package.mbtiles.part').exists())

    def test_cancel_removes_partial_package_but_keeps_generated_tiles(self):
        generated = self._create_tiles()
        with self.assertRaises(OfflineMapInstallationCancelled):
            OfflineMapMbtilesBuilder(self.paths).process(
                self.current_job, lambda: True
            )
        self.assertTrue(generated.exists())
        self.assertFalse((self.work / 'package.mbtiles.part').exists())
        self.assertEqual(self.paths.maps.load(), [])

    def test_existing_package_is_never_overwritten(self):
        self._create_tiles()
        package = self.paths.map_path('fixture-map.mbtiles')
        package.write_bytes(b'keep')
        with self.assertRaisesRegex(OfflineMapInstallationError, 'już istnieje'):
            OfflineMapMbtilesBuilder(self.paths).process(
                self.current_job, lambda: False
            )
        self.assertEqual(package.read_bytes(), b'keep')

    def _register_old_map(self):
        package = self.paths.map_path('fixture-map.mbtiles')
        package.write_bytes(b'old-working-map')
        self.paths.maps.save([OfflineMap.from_dict({
            'id': 'fixture-map', 'region_id': 'fixture', 'name': 'Old map',
            'file_name': package.name, 'size': package.stat().st_size,
            'bounds': [0.0, 0.0, 1.0, 1.0], 'min_zoom': 0,
            'max_zoom': 14, 'installed_at': NOW, 'source_updated_at': '',
            'schema_version': 1,
        })])
        self.current_job.is_update = True
        self.paths.jobs.upsert(self.current_job)
        return package

    def test_successful_update_atomically_replaces_map_and_metadata(self):
        package = self._register_old_map()
        self._create_tiles()

        OfflineMapMbtilesBuilder(self.paths).process(
            self.current_job, lambda: False
        )

        self.assertNotEqual(package.read_bytes(), b'old-working-map')
        installed = self.paths.maps.load()
        self.assertEqual(len(installed), 1)
        self.assertEqual(installed[0].name, 'Obszar testowy')
        self.assertEqual(installed[0].bounds, [0.0, 0.0, 10.0, 10.0])

    def test_failed_update_preserves_the_old_working_map(self):
        package = self._register_old_map()
        self._create_tiles(b'not-a-vector-tile')

        with self.assertRaises(OfflineMapInstallationError):
            OfflineMapMbtilesBuilder(self.paths).process(
                self.current_job, lambda: False
            )

        self.assertEqual(package.read_bytes(), b'old-working-map')
        self.assertEqual(self.paths.maps.load()[0].name, 'Old map')


if __name__ == '__main__':
    unittest.main()

from __future__ import annotations

from contextlib import closing
import gzip
from pathlib import Path
import sqlite3
from tempfile import TemporaryDirectory
import unittest

from flask import Flask
import mapbox_vector_tile
from shapely import Point

from controllers.offline_map_controller import OfflineMapController
from models.offline_maps import OfflineMap
from storage.offline_maps import OfflineMapPaths


NOW = '2026-09-14T12:00:00+00:00'


class OfflineMapTileApiTests(unittest.TestCase):
    def setUp(self):
        self.temporary = TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        directory = Path(self.temporary.name)

        class Storage:
            pass

        Storage.directory = directory
        self.paths = OfflineMapPaths(directory)
        self.app = Flask(__name__)
        self.app.register_blueprint(OfflineMapController(Storage()))
        self.client = self.app.test_client()
        self.vector_tile = mapbox_vector_tile.encode([{
            'name': 'places',
            'features': [{
                'id': 1, 'geometry': Point(2048, 2048),
                'properties': {'name': 'Testowo'},
            }],
        }])
        self.compressed = gzip.compress(self.vector_tile, mtime=0)
        self._register_map('fixture-map', 'fixture.mbtiles')
        self._create_mbtiles('fixture.mbtiles')

    def _register_map(self, map_id, file_name):
        maps = self.paths.maps.load()
        maps.append(OfflineMap.from_dict({
            'id': map_id, 'region_id': 'fixture', 'name': 'Fixture',
            'file_name': file_name, 'size': len(self.compressed),
            'bounds': [-180.0, -85.0, 180.0, 85.0],
            'min_zoom': 2, 'max_zoom': 2, 'installed_at': NOW,
            'source_updated_at': NOW, 'schema_version': 1,
        }))
        self.paths.maps.save(maps)

    def _create_mbtiles(self, file_name):
        path = self.paths.map_path(file_name)
        with closing(sqlite3.connect(path)) as connection:
            connection.execute('''
                CREATE TABLE tiles (
                    zoom_level INTEGER, tile_column INTEGER,
                    tile_row INTEGER, tile_data BLOB
                )
            ''')
            # XYZ row 1 at zoom 2 is TMS row 2.
            connection.execute(
                'INSERT INTO tiles VALUES (2, 2, 2, ?)',
                (self.compressed,),
            )
            connection.commit()

    def test_returns_decoded_vector_tile_with_cache_headers(self):
        response = self.client.get(
            '/api/offline-maps/fixture-map/tiles/2/2/1.pbf'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.content_type, 'application/vnd.mapbox-vector-tile'
        )
        self.assertNotIn('Content-Encoding', response.headers)
        self.assertIn('max-age=3600', response.headers['Cache-Control'])
        self.assertEqual(response.data, self.vector_tile)
        self.assertTrue(response.headers.get('ETag'))

        cached = self.client.get(
            '/api/offline-maps/fixture-map/tiles/2/2/1.pbf',
            headers={'If-None-Match': response.headers['ETag']},
        )
        self.assertEqual(cached.status_code, 304)

    def test_missing_tile_returns_empty_204(self):
        response = self.client.get(
            '/api/offline-maps/fixture-map/tiles/2/1/1.pbf'
        )
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.data, b'')

    def test_corrupted_tile_is_not_sent_to_the_renderer(self):
        path = self.paths.map_path('fixture.mbtiles')
        with closing(sqlite3.connect(path)) as connection:
            connection.execute('UPDATE tiles SET tile_data = ?', (b'invalid',))
            connection.commit()
        response = self.client.get('/api/offline-maps/fixture-map/tiles/2/2/1.pbf')
        self.assertEqual(response.status_code, 500)

    def test_rejects_zoom_and_coordinates_outside_valid_range(self):
        for url in (
            '/api/offline-maps/fixture-map/tiles/1/1/1.pbf',
            '/api/offline-maps/fixture-map/tiles/2/4/1.pbf',
            '/api/offline-maps/fixture-map/tiles/2/1/4.pbf',
        ):
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url).status_code, 400)

    def test_unregistered_map_is_not_addressable(self):
        response = self.client.get(
            '/api/offline-maps/unknown/tiles/2/2/1.pbf'
        )
        self.assertEqual(response.status_code, 404)

    def test_missing_registered_file_is_reported_without_creating_database(self):
        self._register_map('missing-map', 'missing.mbtiles')
        path = self.paths.map_path('missing.mbtiles')
        response = self.client.get(
            '/api/offline-maps/missing-map/tiles/2/2/1.pbf'
        )
        self.assertEqual(response.status_code, 500)
        self.assertFalse(path.exists())

    def test_corrupt_registered_database_has_controlled_error(self):
        self._register_map('corrupt-map', 'corrupt.mbtiles')
        self.paths.map_path('corrupt.mbtiles').write_bytes(b'broken')
        response = self.client.get(
            '/api/offline-maps/corrupt-map/tiles/2/2/1.pbf'
        )
        self.assertEqual(response.status_code, 500)
        self.assertIn('MBTiles', response.get_json()['message'])


if __name__ == '__main__':
    unittest.main()

from __future__ import annotations

from contextlib import closing
import json
import sqlite3
from tempfile import TemporaryDirectory
import unittest

import mapbox_vector_tile
from shapely import LineString, Point, Polygon, to_wkb

from models.offline_maps import OfflineMapJob
from resources.offline_maps import OfflineMapLayers
from services.offline_maps import (
    OfflineMapTileGenerator,
)
from services.offline_maps.errors import OfflineMapTileGenerationCancelled
from storage.offline_maps import (
    OfflineMapFeatureStorage,
    OfflineMapPaths,
    OfflineMapTileStorage,
)


NOW = '2026-09-14T12:00:00+00:00'


def job():
    return OfflineMapJob.from_dict({
        'id': 'tile-job', 'region_id': 'fixture', 'map_id': 'fixture-map',
        'status': 'queued', 'stage': 'building_tiles',
        'downloaded_bytes': 100, 'total_bytes': 100,
        'current': 0, 'total': 0, 'max_zoom': 13,
        'cancel_requested': False, 'created_at': NOW, 'updated_at': NOW,
        'error': '',
    })


class OfflineMapTileGeneratorTests(unittest.TestCase):
    def setUp(self):
        self.temporary = TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.paths = OfflineMapPaths(self.temporary.name)
        self.current_job = job()
        self.paths.jobs.save([self.current_job])
        self.work = self.paths.job_work_path(self.current_job.id)
        self._write_features()

    def _write_features(self):
        storage = OfflineMapFeatureStorage(self.work)
        storage.create()
        entries = (
            ('node', 1, 'places', 'point', Point(19.0, 50.0), 7,
             {'name': 'Testowo', 'place': 'city'}),
            ('way', 2, 'roads', 'line',
             LineString([(18.99, 49.99), (19.01, 50.01)]), 7,
             {'name': 'Główna', 'highway': 'primary'}),
            ('way', 3, 'buildings', 'polygon', Polygon([
                (18.999, 49.999), (19.001, 49.999),
                (19.001, 50.001), (18.999, 50.001), (18.999, 49.999),
            ]), 13, {'name': 'Ratusz', 'building': 'yes'}),
        )
        rows = []
        for osm_type, osm_id, layer, geometry_type, geometry, zoom, props in entries:
            definition = OfflineMapLayers.BY_ID[layer]
            rows.append((
                osm_type, osm_id, layer, geometry_type, to_wkb(geometry),
                zoom, definition.priority,
                json.dumps(props, ensure_ascii=False), *geometry.bounds,
            ))
        storage.insert_many(rows)
        storage.finalize()
        storage.close()

    def test_generates_decodable_mvt_in_bounded_staging_database(self):
        progress = []
        stage = OfflineMapTileGenerator(self.paths).process(
            self.current_job,
            lambda: False,
            lambda _job, current, total: progress.append((current, total)),
        )
        self.assertEqual(stage, 'optimising')
        tile_path = OfflineMapTileStorage(self.work).path
        self.assertTrue(tile_path.is_file())
        with closing(sqlite3.connect(tile_path)) as connection:
            rows = connection.execute('''
                SELECT zoom_level, tile_data FROM generated_tiles
                ORDER BY zoom_level
            ''').fetchall()
            metadata = {
                key: json.loads(value) for key, value in connection.execute(
                    'SELECT key, value FROM metadata'
                )
            }
            tables = {
                row[0] for row in connection.execute(
                    "SELECT name FROM sqlite_master WHERE type = 'table'"
                )
            }
        self.assertGreater(len(rows), 0)
        decoded_layers = set()
        decoded_names = set()
        for _zoom, payload in rows:
            decoded = mapbox_vector_tile.decode(payload)
            decoded_layers.update(decoded)
            for layer in decoded.values():
                decoded_names.update(
                    feature['properties'].get('name')
                    for feature in layer['features']
                )
        self.assertTrue({'places', 'roads', 'buildings'}.issubset(decoded_layers))
        self.assertTrue({'Testowo', 'Główna', 'Ratusz'}.issubset(decoded_names))
        self.assertNotIn('tile_features', tables)
        self.assertEqual(metadata['tile_count'], len(rows))
        self.assertEqual(metadata['min_zoom'], min(row[0] for row in rows))
        self.assertEqual(metadata['max_zoom'], 13)
        self.assertEqual(progress[-1], (progress[-1][0], progress[-1][0]))
        self.assertEqual(self.paths.jobs.find(self.current_job.id).phase, 'encoding')
        self.assertIn((0, 3), progress)
        self.assertTrue(any(current == 0 and total > 3 for current, total in progress))

    def test_cancellation_discards_all_partial_tile_output(self):
        with self.assertRaises(OfflineMapTileGenerationCancelled):
            OfflineMapTileGenerator(self.paths).process(
                self.current_job, lambda: True
            )
        self.assertFalse(OfflineMapTileStorage(self.work).path.exists())

    def test_dense_detail_is_not_encoded_at_country_scale(self):
        self.current_job.max_zoom = 8
        with closing(sqlite3.connect(OfflineMapFeatureStorage(self.work).path)) as connection:
            geometry = to_wkb(Polygon([
                (18.99, 49.99), (19.01, 49.99), (19.01, 50.01),
                (18.99, 50.01), (18.99, 49.99),
            ]))
            for layer, minimum in [('water', 5), ('landuse', 7)]:
                connection.execute('''
                    INSERT INTO features (
                        osm_type, osm_id, layer, geometry_type, geometry_wkb,
                        min_zoom, priority, properties,
                        min_lon, min_lat, max_lon, max_lat
                    ) VALUES ('way', 10, ?, 'polygon', ?, ?, 10, '{}',
                              18.99, 49.99, 19.01, 50.01)
                ''', (layer, geometry, minimum))
            connection.commit()
        OfflineMapTileGenerator(self.paths).process(self.current_job, lambda: False)
        with closing(sqlite3.connect(OfflineMapTileStorage(self.work).path)) as connection:
            layers = json.loads(connection.execute(
                "SELECT value FROM metadata WHERE key = 'layers'"
            ).fetchone()[0])
        self.assertNotIn('water', layers)
        self.assertNotIn('landuse', layers)
        self.assertIn('roads', layers)

    def test_large_water_area_remains_visible_at_country_scale(self):
        self.current_job.max_zoom = 8
        geometry = to_wkb(Polygon([
            (18.8, 49.8), (19.2, 49.8), (19.2, 50.2),
            (18.8, 50.2), (18.8, 49.8),
        ]))
        with closing(sqlite3.connect(OfflineMapFeatureStorage(self.work).path)) as connection:
            connection.execute('''
                INSERT INTO features (
                    osm_type, osm_id, layer, geometry_type, geometry_wkb,
                    min_zoom, priority, properties,
                    min_lon, min_lat, max_lon, max_lat
                ) VALUES ('way', 11, 'water', 'polygon', ?, 5, 10, '{}',
                          18.8, 49.8, 19.2, 50.2)
            ''', (geometry,))
            connection.commit()
        OfflineMapTileGenerator(self.paths).process(self.current_job, lambda: False)
        with closing(sqlite3.connect(OfflineMapTileStorage(self.work).path)) as connection:
            layers = json.loads(connection.execute(
                "SELECT value FROM metadata WHERE key = 'layers'"
            ).fetchone()[0])
        self.assertIn('water', layers)

    def test_missing_feature_database_has_clear_error(self):
        OfflineMapFeatureStorage(self.work).path.unlink()
        with self.assertRaisesRegex(Exception, 'przeanalizowanych danych'):
            OfflineMapTileGenerator(self.paths).process(
                self.current_job, lambda: False
            )


if __name__ == '__main__':
    unittest.main()

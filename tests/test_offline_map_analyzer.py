from __future__ import annotations

from contextlib import closing
import json
import sqlite3
from tempfile import TemporaryDirectory
import unittest

import osmium

from models.offline_maps import OfflineMapJob, OfflineMapRegion
from services.offline_maps import (
    OfflineMapAnalysisCancelled,
    OfflineMapPbfAnalyzer,
    OfflineMapMbtilesBuilder,
    OfflineMapTileGenerator,
)
from storage.offline_maps import OfflineMapFeatureStorage, OfflineMapPaths


NOW = '2026-09-14T12:00:00+00:00'


def job():
    return OfflineMapJob.from_dict({
        'id': 'analysis-job', 'region_id': 'fixture', 'map_id': 'fixture-map',
        'status': 'queued', 'stage': 'analysing', 'downloaded_bytes': 100,
        'total_bytes': 100, 'current': 0, 'total': 0, 'max_zoom': 14,
        'cancel_requested': False, 'created_at': NOW, 'updated_at': NOW,
        'error': '',
    })


class OfflineMapPbfAnalyzerTests(unittest.TestCase):
    def setUp(self):
        self.temporary = TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.paths = OfflineMapPaths(self.temporary.name)
        self.current_job = job()
        self.paths.jobs.save([self.current_job])
        self.source = self.paths.source_path(self.current_job.id)

    def _write_fixture(self):
        with osmium.SimpleWriter(str(self.source), overwrite=True) as writer:
            nodes = (
                (1, 19.00, 50.00), (2, 19.01, 50.00),
                (3, 19.01, 50.01), (4, 19.00, 50.01),
                (5, 19.02, 50.00), (6, 19.03, 50.01),
            )
            for identifier, lon, lat in nodes:
                tags = (
                    {'place': 'city', 'name': 'Testowo', 'phone': 'hidden'}
                    if identifier == 1 else {}
                )
                writer.add_node(osmium.osm.mutable.Node(
                    id=identifier,
                    location=osmium.osm.Location(lon, lat),
                    tags=tags,
                ))
            writer.add_way(osmium.osm.mutable.Way(
                id=10, nodes=[1, 2, 3, 4, 1],
                tags={'building': 'yes', 'name': 'Ratusz', 'phone': 'hidden'},
            ))
            writer.add_way(osmium.osm.mutable.Way(
                id=11, nodes=[5, 6],
                tags={'highway': 'primary', 'name': 'Główna'},
            ))
            writer.add_way(osmium.osm.mutable.Way(
                id=12, nodes=[2, 5], tags={'highway': 'construction'},
            ))

    def test_streams_nodes_lines_and_areas_into_indexed_sqlite(self):
        self._write_fixture()
        progress = []
        next_stage = OfflineMapPbfAnalyzer(self.paths).process(
            self.current_job,
            lambda: False,
            lambda _job, current, total: progress.append((current, total)),
        )
        self.assertEqual(next_stage, 'building_tiles')

        database = OfflineMapFeatureStorage(
            self.paths.job_work_path(self.current_job.id)
        )
        self.assertTrue(database.path.is_file())
        with closing(sqlite3.connect(database.path)) as connection:
            connection.row_factory = sqlite3.Row
            rows = connection.execute(
                'SELECT * FROM features ORDER BY layer, osm_id'
            ).fetchall()
            indexes = {
                row[1] for row in connection.execute(
                    "PRAGMA index_list('features')"
                ).fetchall()
            }
            metadata = {
                key: json.loads(value) for key, value in connection.execute(
                    'SELECT key, value FROM metadata'
                )
            }

        self.assertEqual({row['layer'] for row in rows}, {
            'buildings', 'places', 'roads'
        })
        self.assertNotIn(12, {row['osm_id'] for row in rows})
        road = next(row for row in rows if row['layer'] == 'roads')
        self.assertEqual(road['min_zoom'], 7)
        self.assertEqual(json.loads(road['properties'])['name'], 'Główna')
        place = next(row for row in rows if row['layer'] == 'places')
        self.assertNotIn('phone', json.loads(place['properties']))
        self.assertTrue({
            'features_layer_zoom', 'features_bounds', 'features_osm_object'
        }.issubset(indexes))
        self.assertEqual(metadata['stored_features'], len(rows))
        self.assertEqual(progress[-1][0], progress[-1][1])

    def test_cancellation_removes_incomplete_feature_database(self):
        self._write_fixture()
        with self.assertRaises(OfflineMapAnalysisCancelled):
            OfflineMapPbfAnalyzer(self.paths).process(
                self.current_job, lambda: True
            )
        database = OfflineMapFeatureStorage(
            self.paths.job_work_path(self.current_job.id)
        )
        self.assertFalse(database.path.exists())

    def test_periodic_progress_checks_the_source_without_failing(self):
        self._write_fixture()
        analyser = OfflineMapPbfAnalyzer(self.paths)
        analyser.PROGRESS_INTERVAL = 2
        updates = []

        next_stage = analyser.process(
            self.current_job,
            lambda: False,
            lambda _job, current, total: updates.append((current, total)),
        )

        self.assertEqual(next_stage, 'building_tiles')
        self.assertTrue(any(current >= 2 and total == 0 for current, total in updates))
        self.assertEqual(updates[-1][0], updates[-1][1])

    def test_small_pbf_continues_through_tiles_and_mbtiles_installation(self):
        self._write_fixture()
        self.paths.catalog.save(NOW, [OfflineMapRegion.from_dict({
            'id': 'fixture', 'name': 'Obszar testowy', 'parent_id': '',
            'country_codes': [], 'region_codes': [],
            'pbf_url': 'https://download.geofabrik.de/fixture.osm.pbf',
            'pbf_size': None, 'source_updated_at': NOW,
            'bounds': None, 'children': [],
        })])
        analyser = OfflineMapPbfAnalyzer(self.paths)
        analyser.PROGRESS_INTERVAL = 2

        self.assertEqual(analyser.process(self.current_job, lambda: False), 'building_tiles')
        self.assertEqual(
            OfflineMapTileGenerator(self.paths).process(self.current_job, lambda: False),
            'optimising',
        )
        self.assertEqual(
            OfflineMapMbtilesBuilder(self.paths).process(self.current_job, lambda: False),
            'installing',
        )
        installed = self.paths.maps.load()
        self.assertEqual(len(installed), 1)
        self.assertTrue(self.paths.map_path(installed[0].file_name).is_file())

    def test_missing_source_has_clear_diagnostic(self):
        with self.assertRaisesRegex(Exception, 'Brak pobranego pliku'):
            OfflineMapPbfAnalyzer(self.paths).process(
                self.current_job, lambda: False
            )


if __name__ == '__main__':
    unittest.main()

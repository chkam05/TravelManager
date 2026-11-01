from __future__ import annotations

from contextlib import closing
import gzip
import json
import sqlite3
from tempfile import TemporaryDirectory
import unittest

import mercantile

from models.offline_maps import OfflineMap, OfflineMapJob, OfflineMapRegion
from services.offline_maps import OfflineMapPackageReuse
from storage.offline_maps import (
    OfflineMapFeatureStorage, OfflineMapPaths, OfflineMapTileStorage,
)


NOW = '2026-10-29T10:00:00+00:00'


def region(identifier, parent='', children=None):
    return OfflineMapRegion.from_dict({
        'id': identifier, 'name': identifier, 'parent_id': parent,
        'country_codes': ['PL'], 'region_codes': [],
        'pbf_url': f'https://download.geofabrik.de/{identifier}.osm.pbf',
        'pbf_size': 100, 'source_updated_at': NOW,
        'bounds': [14.0, 49.0, 24.5, 55.0], 'children': children or [],
    })


def installed(identifier, region_id, updated=NOW):
    return OfflineMap.from_dict({
        'id': identifier, 'region_id': region_id, 'name': identifier,
        'file_name': f'{identifier}.mbtiles', 'size': 10,
        'bounds': [18.0, 49.0, 20.0, 51.0],
        'min_zoom': 3, 'max_zoom': 10, 'installed_at': NOW,
        'source_updated_at': updated, 'schema_version': 1,
    })


class OfflineMapReuseTests(unittest.TestCase):
    def setUp(self):
        self.temporary = TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.paths = OfflineMapPaths(self.temporary.name)
        self.paths.catalog.save(NOW, [
            region('europe', children=['poland']),
            region('poland', 'europe', ['poland/slaskie']),
            region('poland/slaskie', 'poland'),
        ])

    def test_detects_only_fresh_installed_descendants_with_artifacts(self):
        child = installed('slaskie', 'poland/slaskie')
        unrelated = installed('europe-map', 'europe')
        self.paths.maps.save([child, unrelated])
        self.paths.map_path(child.file_name).write_bytes(b'map')
        self.paths.map_features_path(child.id).write_bytes(b'features')
        service = OfflineMapPackageReuse(self.paths)
        job = OfflineMapJob.from_dict({
            'id': 'job-poland', 'region_id': 'poland', 'map_id': 'poland-map',
            'status': 'queued', 'stage': 'analysing', 'max_zoom': 10,
            'created_at': NOW, 'updated_at': NOW,
        })

        self.assertEqual([item.id for item in service.covered_maps('poland')], ['slaskie'])
        self.assertEqual([item.id for item in service.reusable_maps(job)], ['slaskie'])

    def test_feature_import_deduplicates_osm_object_and_layer(self):
        child_dir = self.paths.job_work_path('child')
        child = OfflineMapFeatureStorage(child_dir)
        child.create()
        row = ('way', 42, 'roads', 'line', b'geometry', 7, 1, '{"name":"old"}',
               18.0, 50.0, 18.1, 50.1)
        child.insert_many([row])
        child.close()

        parent_dir = self.paths.job_work_path('parent')
        parent = OfflineMapFeatureStorage(parent_dir)
        parent.create()
        self.assertEqual(parent.import_from([child.path]), 1)
        self.assertTrue(parent.contains_reused_object('way', 42))
        self.assertFalse(parent.contains_reused_object('node', 42))
        parent.insert_many([(
            'way', 42, 'roads', 'line', b'other', 7, 1, '{"name":"duplicate"}',
            18.0, 50.0, 18.1, 50.1,
        )])
        self.assertEqual(parent.count(), 1)
        parent.close()

    def test_complete_child_tile_is_copied_and_removed_from_build_queue(self):
        work = self.paths.job_work_path('tile-reuse')
        feature_path = OfflineMapFeatureStorage(work).path
        with closing(sqlite3.connect(feature_path)) as connection:
            connection.execute('CREATE TABLE features(id INTEGER PRIMARY KEY)')
        target = OfflineMapTileStorage(work)
        target.create(feature_path)
        zoom, column, row = 10, 565, 347
        target.assign([(zoom, column, row, 1)])

        package = self.paths.map_path('child.mbtiles')
        tms_row = (1 << zoom) - 1 - row
        with closing(sqlite3.connect(package)) as connection:
            connection.executescript('''
                CREATE TABLE metadata(name TEXT PRIMARY KEY, value TEXT);
                CREATE TABLE tiles(zoom_level INTEGER, tile_column INTEGER,
                                   tile_row INTEGER, tile_data BLOB);
            ''')
            connection.execute(
                'INSERT INTO metadata VALUES (?, ?)',
                ('json', json.dumps({'vector_layers': [{'id': 'roads'}]})),
            )
            connection.execute(
                'INSERT INTO tiles VALUES (?, ?, ?, ?)',
                (zoom, column, tms_row, gzip.compress(b'mvt')),
            )
            connection.commit()
        bounds = mercantile.bounds(column, row, zoom)
        coverage = {
            'type': 'Polygon',
            'coordinates': [[
                [bounds.west, bounds.south], [bounds.east, bounds.south],
                [bounds.east, bounds.north], [bounds.west, bounds.north],
                [bounds.west, bounds.south],
            ]],
        }
        copied, layers = target.import_complete_tiles(
            [(package, coverage)],
            10, lambda: False,
        )

        self.assertEqual(copied, 1)
        self.assertEqual(layers, {'roads'})
        self.assertEqual(target.assignment_count(), 0)
        self.assertEqual(target.generated_stats()[0], 1)
        target.close()


if __name__ == '__main__':
    unittest.main()

from datetime import datetime, timezone
from pathlib import Path
import sqlite3
from tempfile import TemporaryDirectory
import unittest

from models.offline_maps import OfflineMap
from services.offline_maps import OfflineMapTransfer
from storage.offline_maps import OfflineMapPaths


class OfflineMapTransferTests(unittest.TestCase):
    def test_round_trip_preserves_package_and_feature_index(self):
        with TemporaryDirectory() as source_root, TemporaryDirectory() as target_root:
            source = OfflineMapPaths(source_root)
            current = OfflineMap.from_dict({
                'id': 'test-map', 'region_id': 'test-region', 'name': 'Test map',
                'file_name': 'test-map.mbtiles', 'size': 1,
                'bounds': [18, 49, 20, 51], 'min_zoom': 3, 'max_zoom': 10,
                'installed_at': datetime.now(timezone.utc).isoformat(),
                'source_updated_at': '', 'schema_version': 1,
            })
            with sqlite3.connect(source.map_path(current.file_name)) as connection:
                connection.executescript('CREATE TABLE metadata(name TEXT, value TEXT); CREATE TABLE tiles(zoom_level INTEGER);')
            with sqlite3.connect(source.map_features_path(current.id)) as connection:
                connection.executescript('CREATE TABLE features(id INTEGER); CREATE VIRTUAL TABLE feature_bounds USING rtree(id,min_lon,max_lon,min_lat,max_lat);')
            source.maps.add(current)
            archive = Path(source_root) / 'map.tmmap'
            OfflineMapTransfer(source).export(current.id, archive)

            target = OfflineMapPaths(target_root)
            imported = OfflineMapTransfer(target).import_file(archive)

            self.assertEqual(imported.id, current.id)
            self.assertTrue(target.map_path(current.file_name).is_file())
            self.assertTrue(target.map_features_path(current.id).is_file())
            self.assertEqual(target.maps.load()[0].name, current.name)

    def test_import_rejects_incomplete_archive(self):
        with TemporaryDirectory() as root:
            archive = Path(root) / 'broken.tmmap'
            import zipfile
            with zipfile.ZipFile(archive, 'w') as package:
                package.writestr('manifest.json', '{}')
            with self.assertRaisesRegex(ValueError, 'strukturę'):
                OfflineMapTransfer(OfflineMapPaths(root)).import_file(archive)


if __name__ == '__main__':
    unittest.main()

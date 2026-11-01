from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from models.offline_maps import OfflineMap, OfflineMapJob, OfflineMapRegion
from storage.offline_maps import OfflineMapPaths


NOW = '2026-09-14T12:00:00+00:00'


def region_payload(**changes):
    return {
        'id': 'europe/poland/slaskie',
        'name': 'Śląskie',
        'parent_id': 'europe/poland',
        'country_codes': ['PL'],
        'region_codes': ['PL-24'],
        'pbf_url': 'https://download.geofabrik.de/europe/poland/slaskie-latest.osm.pbf',
        'pbf_size': 123456,
        'source_updated_at': NOW,
        'bounds': [18.0, 49.3, 19.9, 51.1],
        'children': [],
        **changes,
    }


def map_payload(**changes):
    return {
        'id': 'europe-poland-slaskie',
        'region_id': 'europe/poland/slaskie',
        'name': 'Śląskie',
        'file_name': 'europe-poland-slaskie.mbtiles',
        'size': 987654,
        'bounds': [18.0, 49.3, 19.9, 51.1],
        'min_zoom': 0,
        'max_zoom': 14,
        'installed_at': NOW,
        'source_updated_at': NOW,
        'schema_version': 1,
        **changes,
    }


def job_payload(**changes):
    return {
        'id': 'job-123',
        'region_id': 'europe/poland/slaskie',
        'map_id': 'europe-poland-slaskie',
        'status': 'running',
        'stage': 'downloading',
        'downloaded_bytes': 120,
        'total_bytes': 1000,
        'current': 120,
        'total': 1000,
        'max_zoom': 14,
        'cancel_requested': False,
        'created_at': NOW,
        'updated_at': NOW,
        'error': '',
        **changes,
    }


class OfflineMapModelTests(unittest.TestCase):
    def test_models_round_trip_without_losing_resume_metadata(self):
        for model, payload in (
            (OfflineMapRegion, region_payload()),
            (OfflineMap, map_payload()),
            (OfflineMapJob, job_payload()),
        ):
            self.assertEqual(model.from_dict(payload).to_dict(), payload)

    def test_region_rejects_insecure_urls_ids_and_invalid_bounds(self):
        for change in (
            {'id': '../poland'},
            {'id': 'europe/../secret'},
            {'pbf_url': 'http://download.geofabrik.de/map.osm.pbf'},
            {'pbf_url': 'https://user:pass@example.test/map.osm.pbf'},
            {'bounds': [20, 50, 10, 51]},
            {'country_codes': ['poland']},
        ):
            with self.assertRaises(ValueError):
                OfflineMapRegion.from_dict(region_payload(**change))

    def test_installed_map_rejects_unsafe_files_and_zoom(self):
        for change in (
            {'file_name': '../map.mbtiles'},
            {'file_name': 'map.sqlite3'},
            {'max_zoom': 23},
            {'min_zoom': 15, 'max_zoom': 14},
            {'size': -1},
        ):
            with self.assertRaises(ValueError):
                OfflineMap.from_dict(map_payload(**change))

    def test_job_rejects_unknown_state_and_non_boolean_cancel_flag(self):
        for change in (
            {'status': 'paused'},
            {'stage': 'extracting'},
            {'cancel_requested': 1},
            {'id': '../../job'},
        ):
            with self.assertRaises(ValueError):
                OfflineMapJob.from_dict(job_payload(**change))


class OfflineMapStorageTests(unittest.TestCase):
    def setUp(self):
        self.temporary = TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.paths = OfflineMapPaths(self.temporary.name)

    def test_initialization_creates_isolated_directory_structure(self):
        self.assertEqual(self.paths.root, Path(self.temporary.name) / 'offline_maps')
        for path in (
            self.paths.root, self.paths.sources_directory,
            self.paths.work_directory, self.paths.maps_directory,
        ):
            self.assertTrue(path.is_dir())
        self.assertEqual(self.paths.catalog.load(), ('', []))
        self.assertEqual(self.paths.maps.load(), [])
        self.assertEqual(self.paths.jobs.load(), [])

    def test_catalog_maps_and_jobs_survive_new_storage_instance(self):
        region = OfflineMapRegion.from_dict(region_payload())
        installed = OfflineMap.from_dict(map_payload())
        job = OfflineMapJob.from_dict(job_payload())
        self.paths.catalog.save(NOW, [region])
        self.paths.maps.save([installed])
        self.paths.jobs.save([job])

        restored = OfflineMapPaths(self.temporary.name)
        self.assertEqual(restored.catalog.load()[1][0].to_dict(), region.to_dict())
        self.assertEqual(restored.maps.load()[0].to_dict(), installed.to_dict())
        self.assertEqual(restored.jobs.load()[0].to_dict(), job.to_dict())
        for name in ('catalog.json', 'installed_maps.json', 'jobs.json'):
            self.assertTrue((restored.root / name).is_file())

    def test_failed_atomic_catalog_replace_preserves_previous_file(self):
        original = OfflineMapRegion.from_dict(region_payload(name='Poprzednia nazwa'))
        replacement = OfflineMapRegion.from_dict(region_payload(name='Nowa nazwa'))
        self.paths.catalog.save(NOW, [original])

        with patch.object(Path, 'replace', side_effect=OSError('disk failure')):
            with self.assertRaisesRegex(OSError, 'disk failure'):
                self.paths.catalog.save(NOW, [replacement])

        restored = OfflineMapPaths(self.temporary.name)
        self.assertEqual(restored.catalog.load()[1][0].name, 'Poprzednia nazwa')
        temporary_files = [
            item for item in self.paths.root.iterdir()
            if item.name not in {
                'catalog.json', 'installed_maps.json', 'jobs.json',
                'sources', 'work', 'maps',
            }
        ]
        self.assertEqual(temporary_files, [])

    def test_duplicate_registry_entries_are_rejected_before_write(self):
        installed = OfflineMap.from_dict(map_payload())
        job = OfflineMapJob.from_dict(job_payload())
        with self.assertRaises(ValueError):
            self.paths.maps.save([installed, installed])
        with self.assertRaises(ValueError):
            self.paths.jobs.save([job, job])
        self.assertFalse(self.paths.maps.file_path.exists())
        self.assertFalse(self.paths.jobs.file_path.exists())

    def test_paths_reject_traversal_wrong_extensions_and_symlink_escape(self):
        for value in ('../job', 'a/b', '', '.hidden'):
            with self.assertRaises(ValueError):
                self.paths.source_path(value)
        with self.assertRaises(ValueError):
            self.paths.map_path('map.sqlite3')
        with self.assertRaises(ValueError):
            self.paths.map_path('../map.mbtiles')

        outside = Path(self.temporary.name) / 'outside.mbtiles'
        outside.write_bytes(b'outside')
        link = self.paths.maps_directory / 'linked.mbtiles'
        try:
            link.symlink_to(outside)
        except (OSError, NotImplementedError):
            self.skipTest('Symbolic links are unavailable on this platform.')
        with self.assertRaises(ValueError):
            self.paths.map_path('linked.mbtiles')

    def test_job_cleanup_and_map_deletion_touch_only_registered_locations(self):
        source = self.paths.source_path('job-123', partial=True)
        source.write_bytes(b'partial')
        work = self.paths.job_work_path('job-123')
        (work / 'tile.tmp').write_bytes(b'tile')
        unrelated = Path(self.temporary.name) / 'keep.txt'
        unrelated.write_text('keep', encoding='utf-8')
        self.paths.clear_job_files('job-123')
        self.assertFalse(source.exists())
        self.assertFalse(work.exists())
        self.assertTrue(unrelated.exists())

        installed = OfflineMap.from_dict(map_payload())
        package = self.paths.map_path(installed.file_name)
        package.write_bytes(b'mbtiles')
        self.assertTrue(self.paths.delete_map_file(installed))
        self.assertFalse(package.exists())
        self.assertFalse(self.paths.delete_map_file(installed))


if __name__ == '__main__':
    unittest.main()

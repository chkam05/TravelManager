from __future__ import annotations

from tempfile import TemporaryDirectory
import unittest

from models.offline_maps import OfflineMap, OfflineMapJob
from services.offline_maps import OfflineMapCleanupService
from storage.offline_maps import OfflineMapPaths


NOW = '2026-09-14T12:00:00+00:00'


def job(identifier, status='failed', stage='failed'):
    return OfflineMapJob.from_dict({
        'id': identifier, 'region_id': 'poland',
        'map_id': f'{identifier}-map', 'status': status, 'stage': stage,
        'downloaded_bytes': 5, 'total_bytes': 10,
        'current': 5, 'total': 10, 'max_zoom': 14,
        'cancel_requested': status == 'cancelled',
        'created_at': NOW, 'updated_at': NOW, 'error': '',
    })


def installed(current_job):
    return OfflineMap.from_dict({
        'id': current_job.map_id, 'region_id': current_job.region_id,
        'name': 'Polska', 'file_name': f'{current_job.map_id}.mbtiles',
        'size': 7, 'bounds': [14.0, 49.0, 24.2, 54.9],
        'min_zoom': 3, 'max_zoom': 14, 'installed_at': NOW,
        'source_updated_at': NOW, 'schema_version': 1,
    })


class OfflineMapCleanupServiceTests(unittest.TestCase):
    def setUp(self):
        self.temporary = TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.paths = OfflineMapPaths(self.temporary.name)
        self.cleanup = OfflineMapCleanupService(self.paths)

    def _work_files(self, current_job):
        self.paths.source_path(current_job.id).write_bytes(b'pbf')
        work = self.paths.job_work_path(current_job.id)
        (work / 'features.sqlite3').write_bytes(b'features')
        (work / 'tiles.sqlite3').write_bytes(b'tiles')
        (work / 'node-locations.idx').write_bytes(b'index')
        (work / 'package.mbtiles.part').write_bytes(b'partial')
        return work

    def test_installed_job_cleanup_removes_sources_and_work_not_map(self):
        current = job('installed-job', 'running', 'installing')
        package = installed(current)
        self.paths.jobs.save([current])
        self.paths.maps.save([package])
        map_path = self.paths.map_path(package.file_name)
        map_path.write_bytes(b'mbtiles')
        work = self._work_files(current)

        self.assertIsNone(self.cleanup.process(current, lambda: False))
        self.assertFalse(self.paths.source_path(current.id).exists())
        self.assertFalse(work.exists())
        self.assertEqual(map_path.read_bytes(), b'mbtiles')

    def test_cleanup_refuses_to_remove_work_for_uninstalled_map(self):
        current = job('unfinished-job', 'running', 'installing')
        work = self._work_files(current)
        with self.assertRaisesRegex(RuntimeError, 'niezainstalowanej'):
            self.cleanup.process(current, lambda: False)
        self.assertTrue(work.exists())
        self.assertTrue(self.paths.source_path(current.id).exists())

    def test_startup_removes_only_provably_orphaned_files(self):
        failed = job('failed-job')
        cancelled = job('cancelled-job', 'cancelled', 'cancelled')
        self.paths.jobs.save([failed, cancelled])
        failed_work = self._work_files(failed)
        cancelled_partial = self.paths.source_path(cancelled.id, partial=True)
        cancelled_partial.write_bytes(b'partial')
        orphan_source = self.paths.source_path('orphan-job', partial=True)
        orphan_source.write_bytes(b'orphan')
        orphan_work = self.paths.job_work_path('orphan-job')
        orphan_features = self.paths.map_features_path('orphan-map')
        orphan_features.write_bytes(b'index')
        (orphan_work / 'data.tmp').write_bytes(b'orphan')
        unrelated = self.paths.sources_directory / 'readme.txt'
        unrelated.write_text('keep', encoding='utf-8')

        result = self.cleanup.cleanup_orphans()
        self.assertEqual(result, {
            'sources': 1, 'work_directories': 1, 'feature_indexes': 1,
        })
        self.assertFalse(orphan_source.exists())
        self.assertFalse(orphan_work.exists())
        self.assertFalse(orphan_features.exists())
        self.assertEqual(result['feature_indexes'], 1)
        self.assertTrue(failed_work.exists())
        self.assertTrue(cancelled_partial.exists())
        self.assertEqual(unrelated.read_text(encoding='utf-8'), 'keep')

    def test_startup_finishes_cleanup_interrupted_after_completion(self):
        completed = job('completed-job', 'completed', 'completed')
        self.paths.jobs.save([completed])
        work = self._work_files(completed)
        result = self.cleanup.cleanup_orphans()
        self.assertFalse(work.exists())
        self.assertFalse(self.paths.source_path(completed.id).exists())
        self.assertEqual(result, {
            'sources': 1, 'work_directories': 1, 'feature_indexes': 0,
        })


if __name__ == '__main__':
    unittest.main()

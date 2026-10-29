from __future__ import annotations

from contextlib import closing
from datetime import datetime, timezone
import sqlite3
from tempfile import TemporaryDirectory
from threading import Lock
from time import monotonic, sleep
import unittest

from models.offline_maps import OfflineMap, OfflineMapJob, OfflineMapRegion
from services.offline_maps import OfflineMapJobManager
from storage.offline_maps import OfflineMapPaths


NOW = '2026-09-14T12:00:00+00:00'


def region(identifier):
    return OfflineMapRegion.from_dict({
        'id': identifier, 'name': identifier.title(), 'parent_id': 'europe',
        'country_codes': [], 'region_codes': [],
        'pbf_url': f'https://download.geofabrik.de/europe/{identifier}.osm.pbf',
        'pbf_size': 10, 'source_updated_at': '', 'bounds': None,
        'children': [],
    })


def persisted_job(identifier='job-recovered', status='running'):
    return OfflineMapJob.from_dict({
        'id': identifier, 'region_id': 'poland', 'map_id': 'poland-map',
        'status': status, 'stage': 'downloading', 'downloaded_bytes': 4,
        'total_bytes': 10, 'current': 4, 'total': 10, 'max_zoom': 14,
        'cancel_requested': False, 'created_at': NOW, 'updated_at': NOW,
        'error': '',
    })


class CompletingDownloader:
    def __init__(self, paths, delay=0):
        self.paths = paths
        self.delay = delay
        self.calls = []
        self.active = 0
        self.maximum_active = 0
        self.lock = Lock()

    def download(self, job, cancelled):
        with self.lock:
            self.active += 1
            self.maximum_active = max(self.maximum_active, self.active)
        try:
            deadline = monotonic() + self.delay
            while monotonic() < deadline:
                if cancelled():
                    raise AssertionError('Unexpected cancellation')
                sleep(0.002)
            self.calls.append(job.id)
            job.status = 'running'
            job.stage = 'analysing'
            job.downloaded_bytes = 10
            job.current = 10
            job.total_bytes = 10
            job.total = 10
            job.updated_at = datetime.now(timezone.utc).isoformat()
            self.paths.jobs.upsert(job)
            return self.paths.source_path(job.id)
        finally:
            with self.lock:
                self.active -= 1


class OfflineMapJobManagerTests(unittest.TestCase):
    def setUp(self):
        self.temporary = TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.paths = OfflineMapPaths(self.temporary.name)
        self.paths.catalog.save(NOW, [region('poland'), region('germany')])
        self.managers = []

    def tearDown(self):
        for manager in self.managers:
            manager.stop()

    def manager(self, downloader):
        manager = OfflineMapJobManager(self.paths, downloader=downloader)
        self.managers.append(manager)
        return manager

    def wait_for(self, predicate, timeout=3):
        deadline = monotonic() + timeout
        while monotonic() < deadline:
            if predicate():
                return
            sleep(0.01)
        self.fail('Timed out waiting for offline map job state.')

    def test_worker_processes_only_one_map_at_a_time(self):
        downloader = CompletingDownloader(self.paths, delay=0.04)
        manager = self.manager(downloader)
        first = manager.create('poland')
        second = manager.create('germany')
        self.wait_for(lambda: (
            len(downloader.calls) == 2
            and all(
                job.status == 'queued' and job.stage == 'analysing'
                for job in manager.list()
            )
        ))
        self.assertEqual(downloader.maximum_active, 1)
        self.assertEqual(set(downloader.calls), {first.id, second.id})
        self.assertTrue(all(
            job.status == 'queued' and job.stage == 'analysing'
            for job in manager.list()
        ))

    def test_restart_recovers_running_download_as_queued_and_resumes_it(self):
        recovered = persisted_job()
        self.paths.jobs.save([recovered])
        downloader = CompletingDownloader(self.paths)
        manager = self.manager(downloader)
        manager.start()
        self.wait_for(lambda: downloader.calls == [recovered.id])
        saved = manager.find(recovered.id)
        self.assertEqual((saved.status, saved.stage), ('queued', 'analysing'))

    def test_duplicate_region_job_is_rejected(self):
        downloader = CompletingDownloader(self.paths, delay=0.1)
        manager = self.manager(downloader)
        manager.create('poland')
        with self.assertRaisesRegex(ValueError, 'już istnieje'):
            manager.create('poland')

    def test_update_job_keeps_map_id_zoom_and_persisted_update_flag(self):
        installed = OfflineMap.from_dict({
            'id': 'poland-map', 'region_id': 'poland', 'name': 'Poland',
            'file_name': 'poland-map.mbtiles', 'size': 10,
            'bounds': [14.0, 49.0, 24.0, 55.0], 'min_zoom': 0,
            'max_zoom': 12, 'installed_at': NOW, 'source_updated_at': NOW,
            'schema_version': 1,
        })
        self.paths.maps.save([installed])
        manager = self.manager(CompletingDownloader(self.paths, delay=1))
        manager.start = lambda: None

        current = manager.create_update('poland-map')

        self.assertEqual(current.map_id, installed.id)
        self.assertEqual(current.max_zoom, installed.max_zoom)
        self.assertTrue(current.is_update)
        self.assertTrue(manager.find(current.id).is_update)

    def test_update_job_can_increase_zoom_without_replacing_installed_map_first(self):
        installed = OfflineMap.from_dict({
            'id': 'poland-map', 'region_id': 'poland', 'name': 'Poland',
            'file_name': 'poland-map.mbtiles', 'size': 10,
            'bounds': [14.0, 49.0, 24.0, 55.0], 'min_zoom': 0,
            'max_zoom': 12, 'installed_at': NOW, 'source_updated_at': NOW,
            'schema_version': 1,
        })
        self.paths.maps.save([installed])
        manager = self.manager(CompletingDownloader(self.paths, delay=1))
        manager.start = lambda: None

        current = manager.create_update('poland-map', max_zoom=19)

        self.assertEqual(current.max_zoom, 19)
        self.assertTrue(current.is_update)
        self.assertEqual(self.paths.maps.load()[0].max_zoom, 12)
        with self.assertRaisesRegex(ValueError, 'przybliżenia'):
            manager.create_update('poland-map', max_zoom=23)

    def test_cancel_is_persisted_even_before_worker_observes_it(self):
        downloader = CompletingDownloader(self.paths, delay=0.1)
        manager = self.manager(downloader)
        current = manager.create('poland')
        cancelled = manager.cancel(current.id)
        self.assertTrue(cancelled.cancel_requested)
        self.assertTrue(manager.find(current.id).cancel_requested)

    def test_user_cancel_removes_download_and_all_work_files(self):
        current = persisted_job('cancel-and-clean', status='queued')
        self.paths.jobs.save([current])
        partial = self.paths.source_path(current.id, partial=True)
        partial.write_bytes(b'partial')
        work = self.paths.job_work_path(current.id)
        (work / 'features.sqlite3').write_bytes(b'features')
        (work / 'tiles.sqlite3').write_bytes(b'tiles')
        manager = self.manager(CompletingDownloader(self.paths))

        manager.cancel(current.id)
        manager._run_job(current.id)

        saved = manager.find(current.id)
        self.assertEqual((saved.status, saved.stage), ('cancelled', 'cancelled'))
        self.assertFalse(partial.exists())
        self.assertFalse(work.exists())
        self.assertEqual((saved.current, saved.total), (0, 0))

    def test_map_identifier_is_stable_and_safe_for_long_region_ids(self):
        value = 'europe/' + ('very-long-region-' * 10)
        first = OfflineMapJobManager.map_id(value)
        self.assertEqual(first, OfflineMapJobManager.map_id(value))
        self.assertLessEqual(len(first), 128)
        self.assertNotIn('/', first)

    def test_resume_selects_latest_safe_persisted_stage(self):
        stages = (
            ('partial-only', 'downloading'),
            ('downloaded', 'analysing'),
            ('analysed', 'building_tiles'),
            ('generated', 'optimising'),
        )
        for identifier, expected in stages:
            with self.subTest(expected=expected):
                current = persisted_job(identifier, status='cancelled')
                current.cancel_requested = True
                self.paths.jobs.save([current])
                work = self.paths.job_work_path(identifier)
                if expected == 'downloading':
                    self.paths.source_path(identifier, partial=True).write_bytes(b'x')
                elif expected == 'analysing':
                    self.paths.source_path(identifier).write_bytes(b'x')
                elif expected == 'building_tiles':
                    (work / 'features.sqlite3').write_bytes(b'x')
                else:
                    with closing(sqlite3.connect(work / 'tiles.sqlite3')) as connection:
                        connection.executescript('''
                            CREATE TABLE generated_tiles (tile_data BLOB);
                            INSERT INTO generated_tiles VALUES (X'01');
                            CREATE TABLE metadata (key TEXT, value TEXT);
                            INSERT INTO metadata VALUES ('tile_count', '1');
                        ''')
                manager = self.manager(CompletingDownloader(self.paths, delay=1))
                # Inspect the selected stage before the worker can consume it.
                manager.start = lambda: None
                resumed = manager.resume(identifier)
                self.assertEqual(resumed.stage, expected)
                self.assertEqual(resumed.status, 'queued')
                self.assertFalse(resumed.cancel_requested)
                self.paths.clear_job_files(identifier)

    def test_partial_tile_database_resumes_generation_not_installation(self):
        current = persisted_job('partial-tiles', status='cancelled')
        self.paths.jobs.save([current])
        work = self.paths.job_work_path(current.id)
        (work / 'features.sqlite3').write_bytes(b'x')
        with closing(sqlite3.connect(work / 'tiles.sqlite3')) as connection:
            connection.executescript('''
                CREATE TABLE tile_features (feature_id INTEGER);
                CREATE TABLE generated_tiles (tile_data BLOB);
                CREATE TABLE metadata (key TEXT, value TEXT);
            ''')
        manager = self.manager(CompletingDownloader(self.paths, delay=1))
        manager.start = lambda: None
        resumed = manager.resume(current.id)
        self.assertEqual(resumed.stage, 'building_tiles')


if __name__ == '__main__':
    unittest.main()

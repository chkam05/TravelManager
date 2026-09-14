"""Tests for source-level railway downloads and atomic GTFS caches."""
from concurrent.futures import CancelledError, ThreadPoolExecutor
from pathlib import Path
import sqlite3
from tempfile import TemporaryDirectory
from threading import Event
from time import monotonic, sleep
import unittest
from unittest.mock import patch
from urllib.error import URLError
from zipfile import ZIP_DEFLATED, ZipFile
from io import BytesIO

from core.gtfs_database import GtfsDatabase
from resources.public_transport.public_transport_messages import PublicTransportValueError
from tests.test_rail_gtfs_fixture import fixture_payload
from utils.public_transport.rail_gtfs_cache import RailGtfsCache
from utils.public_transport.download_progress import PublicTransportDownloadProgress
from utils.public_transport.rail_gtfs_repository import RailGtfsRepository


class RailGtfsCacheTests(unittest.TestCase):
    def setUp(self):
        self.directory = TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        root = Path(self.directory.name)
        paths = {
            'polish_trains': root / 'polish_trains.sqlite3',
            'wkd': root / 'wkd.sqlite3'
        }
        path_patch = patch.object(RailGtfsCache, '_DATABASE_PATHS', paths)
        path_patch.start()
        self.addCleanup(path_patch.stop)

    def test_concurrent_consumers_build_one_shared_source_cache(self):
        with patch.object(
            RailGtfsCache,
            '_download',
            return_value=fixture_payload()
        ) as download:
            with ThreadPoolExecutor(max_workers=2) as executor:
                paths = list(executor.map(
                    lambda _: RailGtfsCache.ensure_database('polish_trains'),
                    range(2)
                ))
        self.assertEqual(paths[0], paths[1])
        self.assertEqual(download.call_count, 1)

    def test_shared_update_broadcasts_progress_to_both_consumers(self):
        started = Event()
        release = Event()
        received = [[], []]

        def download(_source_id):
            started.set()
            self.assertTrue(release.wait(timeout=5))
            PublicTransportDownloadProgress.report('shared', 1, 2)
            return fixture_payload()

        def consume(index):
            with PublicTransportDownloadProgress.bind(
                lambda item, *_: received[index].append(item)
            ):
                return RailGtfsCache.ensure_database('polish_trains')

        with patch.object(RailGtfsCache, '_download', side_effect=download):
            with ThreadPoolExecutor(max_workers=2) as executor:
                first = executor.submit(consume, 0)
                self.assertTrue(started.wait(timeout=5))
                second = executor.submit(consume, 1)
                deadline = monotonic() + 5
                while monotonic() < deadline:
                    flight = RailGtfsCache._FLIGHTS.get('polish_trains')
                    if flight:
                        with flight.condition:
                            if len(flight.subscribers) == 2:
                                break
                    sleep(0.01)
                else:
                    self.fail('Both consumers did not join the shared update')
                release.set()
                first.result(timeout=5)
                second.result(timeout=5)
        self.assertIn('shared', received[0])
        self.assertIn('shared', received[1])

    def test_cancelling_one_waiter_does_not_cancel_shared_build(self):
        started = Event()
        release = Event()
        cancel_first = Event()

        def download(_source_id):
            started.set()
            self.assertTrue(release.wait(timeout=5))
            return fixture_payload()

        with patch.object(RailGtfsCache, '_download', side_effect=download) as call:
            with ThreadPoolExecutor(max_workers=2) as executor:
                first = executor.submit(
                    RailGtfsCache.ensure_database,
                    'polish_trains',
                    False,
                    cancel_first.is_set
                )
                self.assertTrue(started.wait(timeout=5))
                second = executor.submit(
                    RailGtfsCache.ensure_database,
                    'polish_trains'
                )
                cancel_first.set()
                with self.assertRaises(CancelledError):
                    first.result(timeout=5)
                release.set()
                result = second.result(timeout=5)
        self.assertTrue(result.exists())
        self.assertEqual(call.call_count, 1)

    def test_sources_use_independent_database_files(self):
        self.assertNotEqual(
            RailGtfsCache.database_path('polish_trains'),
            RailGtfsCache.database_path('wkd')
        )

    def test_interrupted_archive_resumes_with_http_range(self):
        partial = RailGtfsCache.database_path('polish_trains').with_suffix('.zip.part')
        partial.write_bytes(b'abc')
        requests = []

        class Response:
            headers = {'Content-Length': '3'}
            def __enter__(self): return self
            def __exit__(self, *_): return False
            def getcode(self): return 206
            def read(self, _size):
                if hasattr(self, 'done'): return b''
                self.done = True
                return b'def'

        def open_response(request, **_kwargs):
            requests.append(request)
            return Response()

        with patch('utils.public_transport.rail_gtfs_cache.urlopen', side_effect=open_response):
            payload = RailGtfsCache._download('polish_trains')
        self.assertEqual(payload, b'abcdef')
        self.assertEqual(requests[0].get_header('Range'), 'bytes=3-')
        self.assertFalse(partial.exists())

    def test_partial_archive_is_discovered_for_next_launch(self):
        partial = RailGtfsCache.database_path('wkd').with_suffix('.zip.part')
        self.assertFalse(RailGtfsCache.has_partial_download('wkd'))
        partial.write_bytes(b'partial')
        self.assertTrue(RailGtfsCache.has_partial_download('wkd'))

    def test_two_polish_operators_share_one_build_while_wkd_is_independent(self):
        with patch.object(RailGtfsCache, '_download', return_value=fixture_payload()) as download:
            intercity = RailGtfsRepository('rail_pkp_intercity')._path()
            polregio = RailGtfsRepository('rail_polregio')._path()
            wkd = RailGtfsRepository('rail_wkd')._path()
        self.assertEqual(intercity, polregio)
        self.assertNotEqual(intercity, wkd)
        self.assertEqual(download.call_count, 2)

    def test_failed_refresh_keeps_last_valid_database(self):
        path = RailGtfsCache.database_path('polish_trains')
        with patch.object(
            RailGtfsCache,
            '_download',
            return_value=fixture_payload()
        ):
            RailGtfsCache.ensure_database('polish_trains')
        original = path.read_bytes()
        with patch.object(RailGtfsCache, '_download', return_value=b'bad zip'):
            with self.assertRaises(Exception):
                RailGtfsCache.ensure_database('polish_trains', refresh=True)
        self.assertEqual(path.read_bytes(), original)
        self.assertTrue(GtfsDatabase.is_valid_cache(path))

    def test_network_failure_keeps_previous_database_available(self):
        path = RailGtfsCache.database_path('polish_trains')
        with patch.object(RailGtfsCache, '_download', return_value=fixture_payload()):
            RailGtfsCache.ensure_database('polish_trains')
        original = path.read_bytes()
        with patch.object(RailGtfsCache, '_download', side_effect=URLError('offline')):
            with self.assertRaises(URLError):
                RailGtfsCache.ensure_database('polish_trains', refresh=True)
        self.assertEqual(path.read_bytes(), original)

    def test_zip_missing_required_file_does_not_replace_database(self):
        path = RailGtfsCache.database_path('polish_trains')
        with patch.object(RailGtfsCache, '_download', return_value=fixture_payload()):
            RailGtfsCache.ensure_database('polish_trains')
        original = path.read_bytes()
        source = BytesIO()
        with ZipFile(source, 'w', ZIP_DEFLATED) as archive:
            archive.writestr('agency.txt', 'agency_id,agency_name\nIC,Incomplete\n')
        with patch.object(RailGtfsCache, '_download', return_value=source.getvalue()):
            with self.assertRaises(Exception):
                RailGtfsCache.ensure_database('polish_trains', refresh=True)
        self.assertEqual(path.read_bytes(), original)

    def test_new_feed_version_atomically_replaces_metadata(self):
        path = RailGtfsCache.database_path('polish_trains')
        first = fixture_payload()
        with patch.object(RailGtfsCache, '_download', return_value=first):
            RailGtfsCache.ensure_database('polish_trains')
        changed = BytesIO()
        with ZipFile(BytesIO(first)) as source, ZipFile(changed, 'w', ZIP_DEFLATED) as target:
            for name in source.namelist():
                payload = source.read(name)
                if name == 'feed_info.txt':
                    payload = payload.replace(b'synthetic-1', b'synthetic-2')
                target.writestr(name, payload)
        with patch.object(RailGtfsCache, '_download', return_value=changed.getvalue()):
            RailGtfsCache.ensure_database('polish_trains', refresh=True)
        self.assertEqual(RailGtfsCache.source_metadata('polish_trains')['feed_version'], 'synthetic-2')

    def test_source_metadata_exposes_version_and_validity(self):
        with patch.object(
            RailGtfsCache,
            '_download',
            return_value=fixture_payload()
        ):
            RailGtfsCache.ensure_database('polish_trains')
        metadata = RailGtfsCache.source_metadata('polish_trains')
        self.assertEqual(metadata['feed_version'], 'synthetic-1')
        self.assertEqual(metadata['source_coverage_from'], '2020-01-01')
        self.assertEqual(metadata['source_coverage_to'], '2099-12-31')
        self.assertIn('built_at', metadata)

    def test_date_availability_distinguishes_range_and_no_service(self):
        from datetime import date

        with patch.object(
            RailGtfsCache,
            '_download',
            return_value=fixture_payload()
        ):
            RailGtfsCache.ensure_database('polish_trains')

        available = RailGtfsCache.schedule_availability(
            'polish_trains', date(2030, 1, 1)
        )
        no_service = RailGtfsCache.schedule_availability(
            'polish_trains', date(2030, 1, 5)
        )
        outside = RailGtfsCache.schedule_availability(
            'polish_trains', date(2100, 1, 1)
        )
        self.assertTrue(available.available)
        self.assertEqual(no_service.status, 'no_service')
        self.assertEqual(
            no_service.message.key,
            'PUBLIC_TRANSPORT_ERROR.RAIL_SCHEDULE_DATE_UNAVAILABLE'
        )
        self.assertEqual(outside.status, 'outside_range')
        with self.assertRaises(PublicTransportValueError) as raised:
            RailGtfsCache.require_service_date(
                'polish_trains', date(2100, 1, 1)
            )
        self.assertEqual(
            raised.exception.translation.key,
            'PUBLIC_TRANSPORT_ERROR.RAIL_SCHEDULE_DATE_OUTSIDE_RANGE'
        )

    def test_available_date_carries_stale_feed_warning(self):
        from datetime import date

        with patch.object(
            RailGtfsCache,
            '_download',
            return_value=fixture_payload()
        ):
            path = RailGtfsCache.ensure_database('polish_trains')
        connection = sqlite3.connect(path)
        try:
            connection.execute(
                "UPDATE feed_info SET start_date = ?, end_date = ?",
                ('20200101', '20200103')
            )
            connection.commit()
        finally:
            connection.close()
        availability = RailGtfsCache.require_service_date(
            'polish_trains', date(2020, 1, 2)
        )
        self.assertTrue(availability.available)
        self.assertTrue(availability.stale)
        self.assertEqual(
            availability.message.key,
            'PUBLIC_TRANSPORT_ERROR.RAIL_SCHEDULE_STALE'
        )

    def test_missing_cache_has_explicit_status(self):
        from datetime import date

        availability = RailGtfsCache.schedule_availability(
            'polish_trains', date.today()
        )
        self.assertEqual(availability.status, 'missing')
        self.assertFalse(availability.available)


if __name__ == '__main__':
    unittest.main()

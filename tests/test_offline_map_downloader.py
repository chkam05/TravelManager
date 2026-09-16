from __future__ import annotations

from tempfile import TemporaryDirectory
from threading import Event
from hashlib import md5
import unittest
from urllib.error import URLError

from models.offline_maps import OfflineMapJob, OfflineMapRegion
from services.offline_maps import (
    OfflineMapDownloadCancelled,
    OfflineMapDownloadError,
    OfflineMapPbfDownloader,
)
from storage.offline_maps import OfflineMapPaths


NOW = '2026-09-14T12:00:00+00:00'


def region(url='https://download.geofabrik.de/europe/poland-latest.osm.pbf'):
    return OfflineMapRegion.from_dict({
        'id': 'poland', 'name': 'Poland', 'parent_id': 'europe',
        'country_codes': ['PL'], 'region_codes': [], 'pbf_url': url,
        'pbf_size': None, 'source_updated_at': '', 'bounds': None,
        'children': [],
    })


def job(identifier='map-job'):
    return OfflineMapJob.from_dict({
        'id': identifier, 'region_id': 'poland', 'map_id': 'poland',
        'status': 'queued', 'stage': 'preparing', 'downloaded_bytes': 0,
        'total_bytes': 0, 'current': 0, 'total': 0, 'max_zoom': 14,
        'cancel_requested': False, 'created_at': NOW, 'updated_at': NOW,
        'error': '',
    })


class Response:
    def __init__(self, chunks, status=200, headers=None, url=None):
        self._chunks = iter(chunks)
        self._status = status
        self.headers = headers or {}
        self._url = url

    def __enter__(self):
        return self

    def __exit__(self, *_):
        return False

    def getcode(self):
        return self._status

    def read(self, _size):
        return next(self._chunks, b'')

    def geturl(self):
        return self._url or 'https://download.geofabrik.de/europe/poland-latest.osm.pbf'


class OfflineMapPbfDownloaderTests(unittest.TestCase):
    def setUp(self):
        self.temporary = TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.paths = OfflineMapPaths(self.temporary.name)
        self.paths.catalog.save(NOW, [region()])

    def test_download_uses_identifiable_headers_and_installs_source_atomically(self):
        requests = []

        def opener(request, **_options):
            requests.append(request)
            return Response([b'abc', b'def'], headers={'Content-Length': '6'})

        current_job = job()
        progress = []
        result = OfflineMapPbfDownloader(
            self.paths, opener=opener
        ).download(current_job, progress=lambda _job, current, total: (
            progress.append((current, total))
        ))

        self.assertEqual(result.read_bytes(), b'abcdef')
        self.assertFalse(self.paths.source_path(current_job.id, True).exists())
        self.assertIn('TravelManager', requests[0].get_header('User-agent'))
        self.assertEqual(progress[-1], (6, 6))
        saved = self.paths.jobs.find(current_job.id)
        self.assertEqual(saved.stage, 'analysing')
        self.assertEqual(saved.downloaded_bytes, 6)

    def test_existing_partial_is_resumed_with_validated_content_range(self):
        current_job = job()
        self.paths.source_path(current_job.id, True).write_bytes(b'abc')
        requests = []

        def opener(request, **_options):
            requests.append(request)
            return Response(
                [b'def'], status=206,
                headers={
                    'Content-Length': '3', 'Content-Range': 'bytes 3-5/6'
                },
            )

        result = OfflineMapPbfDownloader(
            self.paths, opener=opener
        ).download(current_job)
        self.assertEqual(requests[0].get_header('Range'), 'bytes=3-')
        self.assertEqual(result.read_bytes(), b'abcdef')

    def test_server_ignoring_range_restarts_instead_of_duplicating_bytes(self):
        current_job = job()
        self.paths.source_path(current_job.id, True).write_bytes(b'old')

        result = OfflineMapPbfDownloader(
            self.paths,
            opener=lambda *_args, **_kwargs: Response(
                [b'new'], status=200, headers={'Content-Length': '3'}
            ),
        ).download(current_job)
        self.assertEqual(result.read_bytes(), b'new')

    def test_cancel_keeps_resumable_partial_and_persists_state(self):
        cancellation = Event()
        current_job = job()

        def progress(*_args):
            cancellation.set()

        downloader = OfflineMapPbfDownloader(
            self.paths,
            opener=lambda *_args, **_kwargs: Response(
                [b'abc', b'def'], headers={'Content-Length': '6'}
            ),
        )
        with self.assertRaises(OfflineMapDownloadCancelled):
            downloader.download(current_job, cancellation.is_set, progress)

        self.assertEqual(
            self.paths.source_path(current_job.id, True).read_bytes(), b'abc'
        )
        saved = self.paths.jobs.find(current_job.id)
        self.assertEqual((saved.status, saved.stage), ('cancelled', 'cancelled'))
        self.assertTrue(saved.cancel_requested)

    def test_transient_failure_retries_and_preserves_partial(self):
        calls = []
        delays = []

        def opener(_request, **_options):
            calls.append(True)
            if len(calls) == 1:
                raise URLError('temporary')
            return Response([b'ok'], headers={'Content-Length': '2'})

        result = OfflineMapPbfDownloader(
            self.paths, opener=opener, sleeper=delays.append
        ).download(job())
        self.assertEqual(result.read_bytes(), b'ok')
        self.assertEqual(len(calls), 2)
        self.assertEqual(delays, [1.0])

    def test_url_must_come_from_saved_geofabrik_catalog(self):
        self.paths.catalog.save(NOW, [region('https://example.test/map.osm.pbf')])
        with self.assertRaisesRegex(OfflineMapDownloadError, 'Geofabrik'):
            OfflineMapPbfDownloader(self.paths).download(job())

    def test_unknown_region_is_rejected_before_any_request(self):
        current_job = job()
        current_job.region_id = 'germany'
        with self.assertRaisesRegex(OfflineMapDownloadError, 'katalogu'):
            OfflineMapPbfDownloader(self.paths).download(current_job)

    def test_available_geofabrik_checksum_is_verified_before_installing_source(self):
        payload = b'verified-pbf'
        checksum = md5(payload, usedforsecurity=False).hexdigest().encode()
        result = OfflineMapPbfDownloader(
            self.paths,
            opener=lambda *_args, **_kwargs: Response(
                [payload], headers={'Content-Length': str(len(payload))}
            ),
            checksum_opener=lambda *_args, **_kwargs: Response(
                [checksum + b'  poland.osm.pbf\n'],
                url='https://download.geofabrik.de/europe/poland-latest.osm.pbf.md5',
            ),
        ).download(job())
        self.assertEqual(result.read_bytes(), payload)

    def test_checksum_mismatch_keeps_untrusted_source_as_partial(self):
        payload = b'corrupted-pbf'
        downloader = OfflineMapPbfDownloader(
            self.paths,
            opener=lambda *_args, **_kwargs: Response(
                [payload], headers={'Content-Length': str(len(payload))}
            ),
            checksum_opener=lambda *_args, **_kwargs: Response(
                [b'00000000000000000000000000000000  map.osm.pbf\n'],
                url='https://download.geofabrik.de/map.osm.pbf.md5',
            ),
        )
        with self.assertRaisesRegex(OfflineMapDownloadError, 'sumą kontrolną'):
            downloader.download(job())
        self.assertFalse(self.paths.source_path('map-job').exists())
        self.assertEqual(
            self.paths.source_path('map-job', partial=True).read_bytes(), payload
        )

    def test_redirect_outside_geofabrik_is_rejected(self):
        downloader = OfflineMapPbfDownloader(
            self.paths,
            opener=lambda *_args, **_kwargs: Response(
                [b'data'], headers={'Content-Length': '4'},
                url='https://example.test/stolen.osm.pbf',
            ),
        )
        with self.assertRaisesRegex(OfflineMapDownloadError, 'zaufane źródło'):
            downloader.download(job())


if __name__ == '__main__':
    unittest.main()

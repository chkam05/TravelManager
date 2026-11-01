from collections import namedtuple
from pathlib import Path
import unittest

from services.offline_maps import OfflineMapResourceError, OfflineMapResourceGuard


Usage = namedtuple('Usage', 'total used free')


class OfflineMapResourceGuardTests(unittest.TestCase):
    def guard(self, free):
        return OfflineMapResourceGuard(
            Path('/tmp/offline-map-test'),
            disk_usage=lambda _path: Usage(free * 2, free, free),
        )

    def test_download_estimate_uses_four_times_source_with_minimum_reserve(self):
        guard = self.guard(10**12)
        self.assertEqual(
            guard.required_for_download(200 * 1024 * 1024),
            800 * 1024 * 1024,
        )
        self.assertEqual(
            guard.required_for_download(None), guard.MINIMUM_FREE_BYTES
        )

    def test_insufficient_space_stops_stage_with_diagnostic_values(self):
        guard = self.guard(100)
        with self.assertRaisesRegex(
            OfflineMapResourceError, 'wymagane.*dostępne'
        ):
            guard.ensure_download(1024)

    def test_sufficient_space_allows_pipeline_stage(self):
        self.guard(2 * 1024**3).ensure_stage(
            300 * 1024**2, 'generowanie', multiplier=2
        )


if __name__ == '__main__':
    unittest.main()

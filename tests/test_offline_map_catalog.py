from __future__ import annotations

import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from flask import Flask, g

from controllers.offline_map_controller import OfflineMapController
from core.language_service import LanguageService
from models.offline_maps import OfflineMap, OfflineMapJob, OfflineMapRegion
from services.offline_maps.catalog_service import (
    OfflineMapCatalogError,
    OfflineMapCatalogService,
)
from services.offline_maps.dependencies import (
    OfflineMapDependencies,
    OfflineMapDependencyError,
)
from services.offline_maps.pbf_metadata import pbf_metadata
from storage.offline_maps import OfflineMapPaths


NOW = '2026-09-14T12:00:00+00:00'


def geofabrik_catalog(pbf_url=None):
    return {
        'type': 'FeatureCollection',
        'features': [
            {
                'type': 'Feature',
                'properties': {
                    'id': 'europe', 'parent': None, 'name': 'Europe',
                    'urls': {},
                },
            },
            {
                'type': 'Feature',
                'properties': {
                    'id': 'europe/poland', 'parent': 'europe',
                    'name': 'Poland', 'iso3166-1:alpha2': ['PL'],
                    'urls': {'pbf': pbf_url or (
                        'https://download.geofabrik.de/europe/'
                        'poland-latest.osm.pbf'
                    )},
                },
            },
            {
                'type': 'Feature',
                'properties': {
                    'id': 'europe/poland/slaskie',
                    'parent': 'europe/poland', 'name': 'Slaskie',
                    'iso3166-1:alpha2': 'PL', 'iso3166-2': ['PL-24'],
                    'urls': {'pbf': (
                        'https://download.geofabrik.de/europe/poland/'
                        'slaskie-latest.osm.pbf'
                    )},
                },
            },
        ],
    }


class FakeResponse:
    def __init__(self, payload):
        self.payload = json.dumps(payload).encode()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def read(self):
        return self.payload


class OfflineMapCatalogTests(unittest.TestCase):
    def setUp(self):
        self.temporary = TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.paths = OfflineMapPaths(self.temporary.name)

    def test_parser_builds_real_hierarchy_and_normalizes_iso_codes(self):
        regions = OfflineMapCatalogService.parse(geofabrik_catalog())
        indexed = {region.id: region for region in regions}
        self.assertEqual(indexed['europe'].children, ['europe/poland'])
        self.assertEqual(
            indexed['europe/poland'].children, ['europe/poland/slaskie']
        )
        self.assertEqual(
            indexed['europe/poland/slaskie'].country_codes, ['PL']
        )
        self.assertEqual(
            indexed['europe/poland/slaskie'].region_codes, ['PL-24']
        )

    def test_region_names_are_plain_text_even_for_cached_geofabrik_markup(self):
        payload = geofabrik_catalog()
        payload['features'][2]['properties']['name'] = 'Śląskie</br> Górny Śląsk &amp; Zagłębie'
        region = OfflineMapCatalogService.parse(payload)[2]
        self.assertEqual(region.name, 'Śląskie Górny Śląsk & Zagłębie')

        region.name = 'Śląskie</br> Górny Śląsk &amp; Zagłębie'
        self.paths.catalog.save(NOW, [region])
        self.assertEqual(self.paths.catalog.load()[1][0].name, region.name)

    def test_pbf_headers_provide_size_and_file_modification_date(self):
        url = 'https://download.geofabrik.de/europe/poland-latest.osm.pbf'

        class Response:
            headers = {
                'Content-Length': '123456',
                'Last-Modified': 'Wed, 16 Sep 2026 08:30:00 GMT',
            }

            def __enter__(self):
                return self

            def __exit__(self, *_):
                return False

            def geturl(self):
                return url

        def opener(request, **options):
            self.assertEqual(request.get_method(), 'HEAD')
            self.assertEqual(request.full_url, url)
            self.assertEqual(options['timeout'], 5)
            return Response()

        self.assertEqual(pbf_metadata(url, opener=opener), {
            'source_size': 123456,
            'source_modified_at': '2026-09-16T08:30:00+00:00',
        })

    def test_pbf_metadata_rejects_redirect_outside_geofabrik(self):
        class Response:
            headers = {'Content-Length': '123456'}

            def __enter__(self):
                return self

            def __exit__(self, *_):
                return False

            def geturl(self):
                return 'https://example.test/map.osm.pbf'

        url = 'https://download.geofabrik.de/europe/poland-latest.osm.pbf'
        self.assertEqual(pbf_metadata(url, opener=lambda *_args, **_kwargs: Response()), {
            'source_size': None, 'source_modified_at': '',
        })

    def test_untrusted_download_url_is_not_saved(self):
        regions = OfflineMapCatalogService.parse(
            geofabrik_catalog('https://example.test/poland.osm.pbf')
        )
        self.assertNotIn('europe/poland', {region.id for region in regions})

    def test_refresh_persists_catalog_and_network_failure_uses_cache(self):
        service = OfflineMapCatalogService(
            self.paths.catalog,
            opener=lambda *args, **kwargs: FakeResponse(geofabrik_catalog()),
        )
        fresh = service.refresh()
        self.assertEqual(fresh['source'], 'current')
        self.assertEqual(len(fresh['regions']), 3)

        def fail(*args, **kwargs):
            raise OSError('offline')

        cached = OfflineMapCatalogService(
            self.paths.catalog, opener=fail
        ).refresh()
        self.assertEqual(cached['source'], 'cache')
        self.assertEqual(cached['warning'], 'offline')
        self.assertEqual(len(cached['regions']), 3)

    def test_network_failure_without_cache_has_clear_error(self):
        def fail(*args, **kwargs):
            raise OSError('offline')

        service = OfflineMapCatalogService(self.paths.catalog, opener=fail)
        with self.assertRaisesRegex(
            OfflineMapCatalogError, 'Nie udało się pobrać katalogu'
        ):
            service.get()

    def test_dependency_diagnostic_names_every_missing_package(self):
        original = OfflineMapDependencies.MODULES
        try:
            OfflineMapDependencies.MODULES = {'test-package': 'module_that_is_absent'}
            with self.assertRaisesRegex(
                OfflineMapDependencyError, 'test-package.*requirements.txt'
            ):
                OfflineMapDependencies.require()
        finally:
            OfflineMapDependencies.MODULES = original


class OfflineMapCatalogApiTests(unittest.TestCase):
    def setUp(self):
        self.temporary = TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        paths = OfflineMapPaths(self.temporary.name)
        paths.catalog.save(NOW, OfflineMapCatalogService.parse(geofabrik_catalog()))

        class Storage:
            directory = Path(self.temporary.name)

        self.app = Flask(__name__)
        language = LanguageService()
        self.app.extensions[LanguageService.EXTENSION_KEY] = language

        @self.app.before_request
        def language_for_request():
            g.language = 'pl_PL'

        self.app.register_blueprint(OfflineMapController(Storage()))

    def _controller(self):
        return next(
            blueprint for blueprint in self.app.blueprints.values()
            if isinstance(blueprint, OfflineMapController)
        )

    def test_catalog_endpoint_returns_localized_cached_hierarchy(self):
        response = self.app.test_client().get('/api/offline-maps/catalog')
        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertEqual(payload['source'], 'cache')
        indexed = {row['id']: row for row in payload['regions']}
        self.assertEqual(indexed['europe/poland']['name'], 'Polska')
        self.assertEqual(indexed['europe/poland']['source_name'], 'Poland')
        self.assertEqual(
            indexed['europe/poland']['children'],
            ['europe/poland/slaskie'],
        )

    def test_catalog_endpoint_cleans_names_from_existing_cache(self):
        controller = self._controller()
        updated_at, regions = controller._paths.catalog.load()
        regions[-1].name = 'Śląskie</br> Katowice &amp; okolice'
        controller._paths.catalog.save(updated_at, regions)

        rows = self.app.test_client().get('/api/offline-maps/catalog').get_json()['regions']
        item = next(row for row in rows if row['id'] == 'europe/poland/slaskie')
        self.assertEqual(item['name'], 'Śląskie Katowice & okolice')

    def test_explicit_refresh_is_accepted_without_waiting_for_network(self):
        controller = self._controller()
        controller._catalog.refresh_async = lambda: True
        response = self.app.test_client().post(
            '/api/offline-maps/catalog/refresh'
        )
        self.assertEqual(response.status_code, 202)
        self.assertEqual(response.get_json()['status'], 'started')

    def test_download_preflight_reports_storage_and_duplicate_state(self):
        self._controller()._pbf_metadata = lambda _url: {
            'source_size': 1024, 'source_modified_at': NOW,
        }
        client = self.app.test_client()
        response = client.get('/api/offline-maps/preflight/europe/poland')

        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertEqual(payload['status'], 'ok')
        self.assertGreater(payload['available_space'], 0)
        self.assertEqual(payload['source_size'], 1024)
        self.assertEqual(payload['source_modified_at'], NOW)
        self.assertEqual(payload['estimated_map_size'], 2560)
        self.assertTrue(payload['enough_space'])
        self.assertFalse(payload['installed'])
        self.assertFalse(payload['active_job'])

    def test_download_preflight_rejects_unknown_region(self):
        response = self.app.test_client().get(
            '/api/offline-maps/preflight/europe/unknown'
        )
        self.assertEqual(response.status_code, 404)

    def test_installed_map_list_metadata_and_safe_deletion(self):
        controller = self._controller()
        installed = OfflineMap.from_dict({
            'id': 'poland', 'region_id': 'poland', 'name': 'Polska',
            'file_name': 'poland.mbtiles', 'size': 7,
            'bounds': [14.0, 49.0, 24.2, 54.9],
            'min_zoom': 0, 'max_zoom': 14, 'installed_at': NOW,
            'source_updated_at': NOW, 'schema_version': 1,
        })
        controller._paths.maps.save([installed])
        controller._paths.map_path(installed.file_name).write_bytes(b'mbtiles')
        controller._paths.map_features_path(installed.id).write_bytes(b'index')
        client = self.app.test_client()

        listing = client.get('/api/offline-maps').get_json()
        self.assertEqual(listing['maps'][0]['id'], 'poland')
        metadata = client.get('/api/offline-maps/poland/metadata')
        self.assertEqual(metadata.status_code, 200)
        self.assertEqual(metadata.get_json()['map']['max_zoom'], 14)

        response = client.delete('/api/offline-maps/poland')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(controller._paths.maps.load(), [])
        self.assertFalse(controller._paths.map_path('poland.mbtiles').exists())
        self.assertFalse(controller._paths.map_features_path('poland').exists())

    def test_active_map_job_blocks_deletion(self):
        controller = self._controller()
        installed = OfflineMap.from_dict({
            'id': 'poland', 'region_id': 'poland', 'name': 'Polska',
            'file_name': 'poland.mbtiles', 'size': 7,
            'bounds': [14.0, 49.0, 24.2, 54.9],
            'min_zoom': 0, 'max_zoom': 14, 'installed_at': NOW,
            'source_updated_at': '', 'schema_version': 1,
        })
        job = OfflineMapJob.from_dict({
            'id': 'job-poland', 'region_id': 'poland', 'map_id': 'poland',
            'status': 'running', 'stage': 'building_tiles',
            'downloaded_bytes': 1, 'total_bytes': 1,
            'current': 1, 'total': 2, 'max_zoom': 14,
            'cancel_requested': False, 'created_at': NOW,
            'updated_at': NOW, 'error': '',
        })
        controller._paths.maps.save([installed])
        controller._paths.jobs.save([job])
        response = self.app.test_client().delete('/api/offline-maps/poland')
        self.assertEqual(response.status_code, 409)
        self.assertEqual(len(controller._paths.maps.load()), 1)


if __name__ == '__main__':
    unittest.main()

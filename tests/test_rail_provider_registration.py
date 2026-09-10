"""Registration and ordering tests for railway public transport providers."""
import unittest

from flask import Flask, g

from core.language_service import LanguageService
from resources.public_transport.public_transport_providers import PublicTransportProviders
from resources.public_transport.rail_gtfs_sources import RailGtfsSources
from controllers.public_transport_controller import PublicTransportController
from utils.public_transport.rail_downloader import RailDownloader


class RailProviderRegistrationTests(unittest.TestCase):
    def test_line_numbers_use_natural_numeric_order(self):
        values = ['1012/3 Bocian', '1003 Zamenhof', '1000/2 Narew',
                  '101 Moravia', '1000/1 Narew', '100 Moravia', '1000 Narew']
        self.assertEqual(sorted(
            values, key=PublicTransportController._natural_line_key
        ), [
            '100 Moravia', '101 Moravia', '1000 Narew', '1000/1 Narew',
            '1000/2 Narew', '1003 Zamenhof', '1012/3 Bocian'
        ])

    def groups(self, locale):
        app = Flask(__name__)
        app.extensions[LanguageService.EXTENSION_KEY] = LanguageService()
        with app.test_request_context('/'):
            g.language = locale
            return PublicTransportProviders.options_by_region()

    def test_all_providers_are_registered_with_shared_downloader_base(self):
        for mapping in RailGtfsSources.PROVIDERS:
            with self.subTest(provider=mapping.provider_id):
                downloader = PublicTransportProviders.downloader(
                    mapping.provider_id
                )
                self.assertTrue(issubclass(downloader, RailDownloader))
                self.assertEqual(downloader.PROVIDER_ID, mapping.provider_id)
                self.assertFalse(
                    PublicTransportProviders.uses_settings_cache(
                        mapping.provider_id
                    )
                )

    def test_rail_providers_are_grouped_by_service_area(self):
        for locale, label in [
            ('pl_PL', 'Ogólnopolscy i dalekobieżni'),
            ('en_US', 'National and long-distance')
        ]:
            with self.subTest(locale=locale):
                groups = self.groups(locale)
                self.assertEqual(groups[0]['region'], label)
                by_region = {
                    group['region']: {item['id'] for item in group['providers']}
                    for group in groups
                }
                self.assertEqual(
                    by_region[label],
                    {
                        'rail_pkp_intercity', 'rail_polregio',
                        'rail_regiojet', 'rail_leo_express'
                    }
                )
                self.assertIn('rail_arriva', by_region['kujawsko-pomorskie'])

    def test_existing_municipal_providers_remain_registered(self):
        groups = self.groups('pl_PL')
        municipal = {
            item['id']
            for group in groups
            for item in group['providers']
            if item['mode'] == 'city'
        }
        self.assertIn(PublicTransportProviders.GZM, municipal)
        self.assertIn(PublicTransportProviders.WARSAW, municipal)
        self.assertIn(PublicTransportProviders.KRAKOW, municipal)

    def test_regiojet_leo_and_two_skm_entries_stay_distinct(self):
        rail = [
            item
            for group in self.groups('pl_PL')
            for item in group['providers']
            if item['mode'] == 'rail'
        ]
        names = {item['id']: item['name'] for item in rail}
        self.assertEqual(names['rail_regiojet'], 'RegioJet')
        self.assertEqual(names['rail_leo_express'], 'Leo Express')
        self.assertNotEqual(
            names['rail_skm_tricity'], names['rail_skm_warsaw']
        )


if __name__ == '__main__':
    unittest.main()

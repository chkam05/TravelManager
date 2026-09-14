"""Contract tests for the audited Polish railway GTFS mapping."""
import unittest

from resources.public_transport.rail_gtfs_sources import RailGtfsSources


class RailGtfsSourcesTests(unittest.TestCase):
    def test_all_rail_providers_have_stable_unique_ids(self):
        providers = RailGtfsSources.PROVIDERS
        self.assertEqual(len(providers), 14)
        self.assertEqual(len({item.provider_id for item in providers}), 14)

    def test_thirteen_providers_share_polish_trains_and_wkd_is_separate(self):
        providers = RailGtfsSources.PROVIDERS
        self.assertEqual(
            sum(item.source_id == RailGtfsSources.POLISH_TRAINS
                for item in providers),
            13
        )
        self.assertEqual(
            RailGtfsSources.provider('rail_wkd').source_id,
            RailGtfsSources.WKD
        )

    def test_current_source_agencies_are_explicit_and_not_shared(self):
        agencies = [
            agency
            for provider in RailGtfsSources.PROVIDERS
            for agency in provider.agency_ids
        ]
        self.assertEqual(len(agencies), 14)
        self.assertEqual(len(set(agencies)), 14)
        self.assertEqual(
            RailGtfsSources.provider('rail_regiojet').agency_ids,
            ('RJ',)
        )
        self.assertEqual(
            RailGtfsSources.provider('rail_leo_express').agency_ids,
            ('LEO',)
        )

    def test_unknown_provider_does_not_fall_back_to_another_agency(self):
        with self.assertRaises(KeyError):
            RailGtfsSources.provider('rail_unknown')

    def test_ui_order_and_polregio_spelling_are_stable(self):
        self.assertEqual(
            [provider.provider_id for provider in RailGtfsSources.PROVIDERS],
            [
                'rail_pkp_intercity', 'rail_polregio', 'rail_arriva',
                'rail_kd', 'rail_kmal', 'rail_km', 'rail_ks', 'rail_kw',
                'rail_lka', 'rail_skm_tricity', 'rail_regiojet',
                'rail_leo_express', 'rail_skm_warsaw', 'rail_wkd'
            ]
        )
        self.assertEqual(
            RailGtfsSources.provider('rail_polregio').display_name,
            'POLREGIO'
        )


if __name__ == '__main__':
    unittest.main()

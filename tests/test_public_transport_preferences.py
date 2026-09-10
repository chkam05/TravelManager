"""Persistence tests for independent city and railway panel choices."""
import unittest

from models.settings_data_model import SettingsDataModel


class PublicTransportPreferenceTests(unittest.TestCase):
    def test_legacy_provider_is_migrated_to_its_transport_mode(self):
        settings = SettingsDataModel.from_dict({
            'selected_public_transport_provider': 'rail_pkp_intercity'
        })
        self.assertEqual(settings.selected_public_transport_mode, 'rail')
        self.assertEqual(
            settings.selected_public_transport_providers['rail'],
            'rail_pkp_intercity'
        )

    def test_both_providers_and_mode_survive_serialization(self):
        settings = SettingsDataModel.from_dict({
            'selected_public_transport_provider': 'rail_polregio',
            'selected_public_transport_providers': {
                'city': 'gzm', 'rail': 'rail_polregio'
            },
            'selected_public_transport_mode': 'city'
        })
        restored = SettingsDataModel.from_dict(settings.to_dict())
        self.assertEqual(restored.selected_public_transport_mode, 'city')
        self.assertEqual(restored.selected_public_transport_providers, {
            'city': 'gzm', 'rail': 'rail_polregio'
        })


if __name__ == '__main__':
    unittest.main()

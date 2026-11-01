import unittest

from models.settings.ui_settings import UiSettings


class OfflineMapUiSettingsTests(unittest.TestCase):
    def test_offline_map_mode_defaults_to_online_only(self):
        settings = UiSettings.from_dict({})

        self.assertEqual(settings.offline_map_mode, 'online_only')
        self.assertEqual(settings.to_dict()['offline_map_mode'], 'online_only')

    def test_supported_offline_map_modes_round_trip(self):
        for mode in UiSettings.OFFLINE_MAP_MODES:
            with self.subTest(mode=mode):
                settings = UiSettings.from_dict({'offline_map_mode': mode})
                self.assertEqual(settings.to_dict()['offline_map_mode'], mode)

    def test_unknown_offline_map_mode_is_rejected_to_safe_default(self):
        settings = UiSettings.from_dict({'offline_map_mode': 'unexpected'})

        self.assertEqual(settings.offline_map_mode, 'online_only')

    def test_dynamic_zoom_defaults_to_19_and_accepts_only_supported_levels(self):
        self.assertEqual(UiSettings.from_dict({}).offline_map_max_dynamic_zoom, 19)
        for zoom in range(14, 20):
            with self.subTest(zoom=zoom):
                settings = UiSettings.from_dict({
                    'offline_map_max_dynamic_zoom': str(zoom)
                })
                self.assertEqual(settings.offline_map_max_dynamic_zoom, zoom)
                self.assertEqual(
                    settings.to_dict()['offline_map_max_dynamic_zoom'], zoom
                )
        for invalid in (0, 13, 20, 'invalid'):
            with self.subTest(invalid=invalid):
                self.assertEqual(UiSettings.from_dict({
                    'offline_map_max_dynamic_zoom': invalid
                }).offline_map_max_dynamic_zoom, 19)


if __name__ == '__main__':
    unittest.main()

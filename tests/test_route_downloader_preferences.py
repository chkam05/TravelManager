from unittest.mock import patch
import unittest

from utils.data.route_downloader import RouteDownloader


CONVERTED_ROUTE = {
    'distance': 1000,
    'duration': 100,
    'geometry': {'type': 'LineString', 'coordinates': []},
    'legs': [],
    'waypoints': []
}


class RouteDownloaderPreferenceTests(unittest.TestCase):
    @patch('utils.data.route_downloader.ValhallaRouteConverter.convert', return_value=CONVERTED_ROUTE)
    @patch('utils.data.route_downloader.MapDataDownloader.post_json', return_value={'trip': {}})
    def test_nature_bicycle_uses_mountain_bike_and_tracks(self, post_json, _convert):
        RouteDownloader._download_valhalla(
            [{'latitude': 52.0, 'longitude': 21.0}, {'latitude': 52.1, 'longitude': 21.1}],
            'bicycle',
            True,
            'nature'
        )
        payload = post_json.call_args.args[1]
        self.assertEqual(payload['costing'], 'bicycle')
        self.assertEqual(payload['costing_options']['bicycle']['bicycle_type'], 'mountain')
        self.assertEqual(payload['costing_options']['bicycle']['use_tracks'], 1)

    @patch('utils.data.route_downloader.ValhallaRouteConverter.convert', return_value=CONVERTED_ROUTE)
    @patch('utils.data.route_downloader.MapDataDownloader.post_json', return_value={'trip': {}})
    def test_highway_car_prefers_highways(self, post_json, _convert):
        RouteDownloader._download_valhalla(
            [{'latitude': 52.0, 'longitude': 21.0}, {'latitude': 52.1, 'longitude': 21.1}],
            'car',
            True,
            'highways'
        )
        options = post_json.call_args.args[1]['costing_options']['auto']
        self.assertEqual(options['use_highways'], 1)
        self.assertEqual(options['use_tracks'], 0)


if __name__ == '__main__':
    unittest.main()

from unittest.mock import patch
import unittest

from flask import Flask

from controllers.map_controller import MapController
from models.route.route_data_model import RouteDataModel


def route(distance):
    return RouteDataModel.from_dict({
        'distance': distance,
        'duration': distance / 15,
        'geometry': {'coordinates': [], 'type': 'LineString'},
        'legs': [],
        'waypoints': []
    })


class RandomRouteApiTests(unittest.TestCase):
    def setUp(self):
        app = Flask(__name__)
        app.register_blueprint(MapController())
        self.client = app.test_client()

    @patch('controllers.map_controller.RouteDownloader.download')
    def test_returns_closed_candidate_closest_to_requested_length(self, download):
        download.side_effect = [route(45_000), route(79_000), route(110_000), route(65_000)]

        response = self.client.post('/api/map/random-route', json={
            'start': {'latitude': 52.2297, 'longitude': 21.0122},
            'area_km': 25,
            'length_km': 80,
            'transport': 'car'
        })

        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertEqual(payload['route']['distance'], 79_000)
        self.assertEqual(payload['points'][0], payload['points'][-1])
        self.assertEqual(download.call_count, 4)

    @patch('controllers.map_controller.LanguageService.translate_current', return_value='Invalid configuration')
    def test_rejects_configuration_outside_limits(self, _translate):
        response = self.client.post('/api/map/random-route', json={
            'start': {'latitude': 52.2297, 'longitude': 21.0122},
            'area_km': 0,
            'length_km': 80
        })
        self.assertEqual(response.status_code, 400)


if __name__ == '__main__':
    unittest.main()

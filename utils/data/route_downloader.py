from __future__ import annotations
from typing import Any
from urllib.parse import urlencode

from models.route.route_data_model import RouteDataModel
from resources.map_sources import MapSources
from utils.converters.valhalla_route_converter import ValhallaRouteConverter
from utils.data.map_data_downloader import MapDataDownloader


class RouteDownloader:
    """Downloads routes from OSRM-compatible services or Valhalla."""

    @classmethod
    def download(
        cls,
        points: list[dict[str, float]],
        transport: str,
        include_toll_roads: bool
    ) -> RouteDataModel:
        if transport == 'car' and not include_toll_roads:
            return cls._download_valhalla(points)
        return cls._download_osrm(points, transport)

    @staticmethod
    def _download_osrm(points: list[dict[str, float]], transport: str) -> RouteDataModel:
        base_url, profile = MapSources.ROUTE_PROFILES.get(
            transport,
            MapSources.ROUTE_PROFILES['car']
        )
        coordinates = ';'.join(
            f'{point["longitude"]},{point["latitude"]}'
            for point in points
        )
        params = {'overview': 'full', 'geometries': 'geojson', 'steps': 'true'}
        data = MapDataDownloader.get_json(
            f'{base_url}/route/v1/{profile}/{coordinates}?{urlencode(params)}'
        )

        if data.get('code') != 'Ok' or not data.get('routes'):
            raise ValueError(data.get('message') or 'No route found.')

        selected = data['routes'][0]
        return RouteDataModel.from_dict({
            'distance': selected.get('distance'),
            'duration': selected.get('duration'),
            'geometry': selected.get('geometry'),
            'legs': selected.get('legs', []),
            'waypoints': data.get('waypoints', []),
            'toll_exclusion_requested': False,
            'toll_exclusion_applied': False,
            'toll_exclusion_warning': None
        })

    @staticmethod
    def _download_valhalla(points: list[dict[str, float]]) -> RouteDataModel:
        data = MapDataDownloader.post_json(f'{MapSources.VALHALLA_URL}/route', {
            'locations': [
                {'lat': point['latitude'], 'lon': point['longitude']}
                for point in points
            ],
            'costing': 'auto',
            'costing_options': {'auto': {'use_tolls': 0}},
            'directions_options': {'units': 'kilometers'}
        })
        return RouteDataModel.from_dict(ValhallaRouteConverter.convert(data))

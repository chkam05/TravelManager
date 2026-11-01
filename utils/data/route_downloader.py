from __future__ import annotations
from typing import Any
from urllib.parse import urlencode

from models.route.route_data_model import RouteDataModel
from core.language_service import LanguageService
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
        include_toll_roads: bool,
        preference: str = 'standard'
    ) -> RouteDataModel:
        if (transport == 'car' and not include_toll_roads) or preference != 'standard':
            return cls._download_valhalla(points, transport, include_toll_roads, preference)
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
            raise ValueError(LanguageService.translate_current('ROUTE_ERROR.ROUTE_NOT_FOUND'))

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
    def _download_valhalla(
        points: list[dict[str, float]],
        transport: str = 'car',
        include_toll_roads: bool = False,
        preference: str = 'standard'
    ) -> RouteDataModel:
        costing = {'car': 'auto', 'bicycle': 'bicycle', 'foot': 'pedestrian'}.get(transport, 'auto')
        options: dict[str, float | str] = {}
        if costing == 'auto':
            options['use_tolls'] = 1 if include_toll_roads else 0
            if preference == 'highways':
                options.update({'use_highways': 1, 'use_living_streets': 0.1, 'use_tracks': 0})
            elif preference == 'urban':
                options.update({'use_highways': 0.05, 'use_living_streets': 0.8, 'use_tracks': 0.1})
            elif preference == 'nature':
                options.update({'use_highways': 0, 'use_living_streets': 0.5, 'use_tracks': 0.9})
        elif costing == 'bicycle':
            if preference == 'urban':
                options.update({'bicycle_type': 'road', 'use_roads': 0.7, 'use_tracks': 0.1})
            elif preference == 'nature':
                options.update({'bicycle_type': 'mountain', 'use_roads': 0.15, 'use_tracks': 1})
        elif costing == 'pedestrian':
            if preference == 'urban':
                options.update({'use_living_streets': 1, 'use_tracks': 0.1})
            elif preference == 'nature':
                options.update({'walkway_factor': 0.6, 'use_living_streets': 0.4, 'use_tracks': 1})

        data = MapDataDownloader.post_json(f'{MapSources.VALHALLA_URL}/route', {
            'locations': [
                {'lat': point['latitude'], 'lon': point['longitude']}
                for point in points
            ],
            'costing': costing,
            'costing_options': {costing: options},
            'directions_options': {'units': 'kilometers'}
        })
        converted = ValhallaRouteConverter.convert(data, LanguageService.translate_current)
        converted['toll_exclusion_requested'] = costing == 'auto' and not include_toll_roads
        converted['toll_exclusion_applied'] = costing == 'auto' and not include_toll_roads
        if costing != 'auto' or include_toll_roads:
            converted['toll_exclusion_warning'] = None
        return RouteDataModel.from_dict(converted)

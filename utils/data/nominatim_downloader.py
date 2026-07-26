from __future__ import annotations
from typing import Any

from models.map.map_element_data_model import MapElementDataModel
from resources.map_sources import MapSources
from utils.data.map_data_downloader import MapDataDownloader


class NominatimDownloader:
    """Downloads and converts Nominatim search and reverse-geocoding data."""

    @classmethod
    def reverse(cls, latitude: str | float, longitude: str | float) -> MapElementDataModel:
        data = MapDataDownloader.get_json_with_params(MapSources.NOMINATIM_URL, '/reverse', {
            'format': 'jsonv2',
            'lat': latitude,
            'lon': longitude,
            'addressdetails': 1,
            'extratags': 1,
            'namedetails': 1
        })
        return MapElementDataModel.from_dict(data)

    @classmethod
    def search(
        cls,
        query: str,
        limit: int = 5,
        viewbox: str | None = None
    ) -> list[MapElementDataModel]:
        params: dict[str, Any] = {
            'format': 'jsonv2',
            'q': query,
            'limit': limit,
            'addressdetails': 1,
            'extratags': 1,
            'namedetails': 1
        }

        if viewbox:
            params['viewbox'] = viewbox
            params['bounded'] = 1

        data = MapDataDownloader.get_json_with_params(MapSources.NOMINATIM_URL, '/search', params)
        return [
            MapElementDataModel.from_dict(item)
            for item in data
            if isinstance(item, dict)
        ]

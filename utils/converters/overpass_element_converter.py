from __future__ import annotations
from typing import Any

from models.map.map_element_data_model import MapElementDataModel


class OverpassElementConverter:
    """Converts Overpass nodes, ways and relations to map element models."""

    _MAIN_KEYS = ('amenity', 'shop', 'tourism', 'leisure', 'healthcare', 'office', 'landuse', 'boundary', 'sport')

    @classmethod
    def convert(cls, item: dict[str, Any]) -> MapElementDataModel | None:
        tags = dict(item.get('tags') or {})
        latitude = item.get('lat', item.get('center', {}).get('lat'))
        longitude = item.get('lon', item.get('center', {}).get('lon'))

        try:
            lat = float(latitude)
            lon = float(longitude)
        except (TypeError, ValueError):
            return None

        if not -90 <= lat <= 90 or not -180 <= lon <= 180:
            return None

        category, element_type = cls.tagged_value(tags)
        return MapElementDataModel.from_dict({
            'place_id': f'overpass:{item.get("type")}:{item.get("id")}',
            'osm_type': item.get('type'),
            'osm_id': item.get('id'),
            'category': category,
            'type': element_type,
            'display_name': cls.display_name(tags, lat, lon),
            'coordinates': {'latitude': lat, 'longitude': lon},
            'address': tags,
            'name': tags,
            'annotations': tags,
            'properties': tags,
            'references': tags,
            'restrictions': tags,
            'primary_features': tags,
            'raw_data': {**item, 'source': 'overpass_advanced_search'}
        })

    @classmethod
    def tagged_value(cls, tags: dict[str, Any]) -> tuple[str | None, str | None]:
        for key in cls._MAIN_KEYS:
            if tags.get(key):
                return key, str(tags[key])
        return None, None

    @staticmethod
    def display_name(tags: dict[str, Any], latitude: float, longitude: float) -> str:
        address = ', '.join(str(value) for value in (
            tags.get('addr:street'),
            tags.get('addr:housenumber'),
            tags.get('addr:city')
        ) if value)
        name = tags.get('name') or tags.get('brand') or tags.get('operator')

        if name and address:
            return f'{name}, {address}'
        if name:
            return str(name)
        if address:
            return address
        return f'{latitude:.6f}, {longitude:.6f}'

from __future__ import annotations
from typing import Any

from resources.map_legend import MapLegend


class MapLegendConverter:
    """Converts static map legend resources to the frontend response shape."""

    @classmethod
    def convert_item(cls, key: str, data: dict[str, Any]) -> dict[str, Any]:
        icon_type = data.get(MapLegend.FIELD_ICON)
        return {
            'id': key,
            'title': data.get(MapLegend.FIELD_TITLE, key),
            'icon_type': icon_type,
            'image': f'/assets/images/legend/{key}.{icon_type}' if icon_type else None,
            'requirements': data.get(MapLegend.FIELD_REQUIREMENTS, [])
        }

    @classmethod
    def convert_group(cls, key: str, items: dict[str, Any]) -> dict[str, Any]:
        return {
            'id': key,
            'title': key.replace('_', ' ').title(),
            'items': [cls.convert_item(item_key, data) for item_key, data in items.items()]
        }

    @classmethod
    def convert_tab(cls, tab_id: str, label: str, groups: dict[str, Any]) -> dict[str, Any]:
        return {
            'id': tab_id,
            'label': label,
            'groups': [cls.convert_group(key, items) for key, items in groups.items()]
        }

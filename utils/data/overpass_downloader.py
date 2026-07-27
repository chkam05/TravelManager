from __future__ import annotations
from typing import Any, Callable

from models.map.map_element_data_model import MapElementDataModel
from resources.map_search import MapSearchConfig
from resources.map_sources import MapSources
from utils.converters.overpass_element_converter import OverpassElementConverter
from utils.data.map_data_downloader import MapDataDownloader


class OverpassDownloader:
    """Downloads map elements matching configured OpenStreetMap tags."""

    @classmethod
    def search(
        cls,
        category_id: str,
        subcategory_id: str,
        keyword: str,
        limit: int,
        bbox: str | None
    ) -> list[MapElementDataModel]:
        if not bbox:
            return []

        filters = cls.filters(category_id, subcategory_id)
        if not filters:
            return []

        query = cls.query(filters, bbox)
        data = cls.download_query(query)
        results: list[MapElementDataModel] = []
        seen: set[tuple[str, Any]] = set()

        for item in data.get('elements', []):
            if not isinstance(item, dict):
                continue
            key = (str(item.get('type')), item.get('id'))
            tags = dict(item.get('tags') or {})

            if key in seen or not cls.text_matches_keyword(tags, keyword):
                continue

            model = OverpassElementConverter.convert(item)
            if not model:
                continue

            seen.add(key)
            results.append(model)
            if len(results) >= limit:
                break

        return results

    @staticmethod
    def filters(
        category_id: str,
        subcategory_id: str
    ) -> list[dict[str, str | tuple[str, ...] | None]]:
        if subcategory_id in MapSearchConfig.FILTERS:
            return MapSearchConfig.FILTERS[subcategory_id]

        result: list[dict[str, str | tuple[str, ...] | None]] = []
        for item in MapSearchConfig.GROUPS.get(category_id, ()):
            result.extend(MapSearchConfig.FILTERS.get(item, []))
        return result

    @classmethod
    def query(
        cls,
        filters: list[dict[str, str | tuple[str, ...] | None]],
        bbox: str
    ) -> str:
        lines = ['[out:json][timeout:12];', '(']
        for tags in filters:
            selector = cls.selector(tags)
            lines.extend((
                f'  node{selector}({bbox});',
                f'  way{selector}({bbox});',
                f'  relation{selector}({bbox});'
            ))
        lines.extend((');', 'out center;'))
        return '\n'.join(lines)

    @classmethod
    def selector(cls, tags: dict[str, str | tuple[str, ...] | None]) -> str:
        parts: list[str] = []
        for key, value in tags.items():
            escaped_key = cls.escape(key)
            if value is None:
                parts.append(f'["{escaped_key}"]')
            elif isinstance(value, tuple):
                pattern = '|'.join(cls.escape(item) for item in value)
                parts.append(f'["{escaped_key}"~"^({pattern})$"]')
            else:
                parts.append(f'["{escaped_key}"="{cls.escape(value)}"]')
        return ''.join(parts)

    @staticmethod
    def escape(value: str) -> str:
        return value.replace('\\', '\\\\').replace('"', '\\"')

    @staticmethod
    def text_matches_keyword(tags: dict[str, Any], keyword: str) -> bool:
        phrase = keyword.strip().lower()
        if not phrase:
            return True
        return any(
            phrase in str(tags.get(key) or '').lower()
            for key in (
                'name', 'official_name', 'short_name', 'brand', 'operator',
                'addr:street', 'addr:city', 'cuisine', 'description'
            )
        )

    @classmethod
    def download_query(
        cls,
        query: str,
        attempt_callback: Callable[[int, int], None] | None = None
    ) -> dict[str, Any]:
        """Executes an arbitrary Overpass query with configured fallbacks."""
        last_error: Exception | None = None
        urls = (
            MapSources.OVERPASS_URL,
            *MapSources.OVERPASS_FALLBACK_URLS
        )[:3]
        for attempt, url in enumerate(urls, start=1):
            if attempt_callback:
                attempt_callback(attempt, len(urls))
            try:
                data = MapDataDownloader.post_form_json(url, {'data': query})
                return data if isinstance(data, dict) else {}
            except Exception as error:
                last_error = error
        raise last_error or RuntimeError('Overpass request failed.')

    @classmethod
    def _download(cls, query: str) -> dict[str, Any]:
        """Keeps compatibility with the original internal query method."""
        return cls.download_query(query)

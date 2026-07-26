from __future__ import annotations
import math
from typing import Any

from models.map.map_element_data_model import MapElementDataModel
from models.map.map_place_data_model import MapPlaceDataModel
from resources.map_search import MapSearchConfig
from utils.data.nominatim_downloader import NominatimDownloader
from utils.data.overpass_downloader import OverpassDownloader


class MapSearchService:
    """Coordinates Nominatim and Overpass map searches."""

    @classmethod
    def search(cls, query: str, limit: int = 5) -> MapPlaceDataModel:
        elements = NominatimDownloader.search(query, limit)
        return cls._place(query, 'nominatim_search', elements)

    @classmethod
    def advanced_search(
        cls,
        query: str,
        keyword: str,
        category_id: str,
        subcategory_id: str,
        limit: int,
        bounds: dict[str, Any]
    ) -> MapPlaceDataModel:
        viewbox = cls.viewbox(bounds)

        if not category_id and not subcategory_id:
            elements = NominatimDownloader.search(query, limit, viewbox)
            return cls._place(query, 'nominatim_advanced_search', elements)

        inferred = subcategory_id or cls.subcategory_from_keyword(keyword, category_id)
        try:
            elements = OverpassDownloader.search(
                category_id,
                inferred,
                cls.effective_keyword(keyword, inferred),
                limit,
                cls.bbox(viewbox)
            )
        except Exception as error:
            try:
                elements = cls._category_fallback(query, keyword, category_id, inferred, limit, viewbox)
            except Exception:
                raise RuntimeError(f'Could not search OpenStreetMap tags: {error}') from error

        if not elements:
            elements = cls._category_fallback(query, keyword, category_id, inferred, limit, viewbox)

        return cls._place(query, 'advanced_search', elements)

    @staticmethod
    def _place(query: str, source: str, elements: list[MapElementDataModel]) -> MapPlaceDataModel:
        return MapPlaceDataModel(
            query=query,
            source=source,
            selected=elements[0] if elements else None,
            elements=elements
        )

    @classmethod
    def _category_fallback(
        cls,
        query: str,
        keyword: str,
        category_id: str,
        subcategory_id: str,
        limit: int,
        viewbox: str | None
    ) -> list[MapElementDataModel]:
        base_terms = MapSearchConfig.FALLBACK_QUERIES.get(
            subcategory_id,
            MapSearchConfig.FALLBACK_QUERIES.get(category_id, (query,))
        )
        terms = tuple(dict.fromkeys((
            *([keyword.strip()] if keyword.strip() else []),
            *base_terms
        )))
        results: list[MapElementDataModel] = []
        seen: set[str] = set()

        for term in terms:
            if not term:
                continue
            try:
                elements = NominatimDownloader.search(term, max(1, min(limit, 10)), viewbox)
            except Exception:
                continue
            for element in elements:
                key = str(element.place_id or '')
                if not key:
                    key = f'{element.coordinates}:{element.display_name}'
                if key in seen:
                    continue
                seen.add(key)
                results.append(element)
                if len(results) >= limit:
                    return results
        return results

    @staticmethod
    def subcategory_from_keyword(keyword: str, category_id: str) -> str:
        normalized = ' '.join(keyword.strip().lower().split())
        subcategory = MapSearchConfig.KEYWORD_ALIASES.get(normalized, '')
        return subcategory if subcategory in MapSearchConfig.GROUPS.get(category_id, ()) else ''

    @staticmethod
    def effective_keyword(keyword: str, subcategory_id: str) -> str:
        normalized = ' '.join(keyword.strip().lower().split())
        if subcategory_id and MapSearchConfig.KEYWORD_ALIASES.get(normalized) == subcategory_id:
            return ''
        return keyword

    @staticmethod
    def bbox(viewbox: str | None) -> str | None:
        if not viewbox:
            return None
        try:
            west, north, east, south = [float(item) for item in viewbox.split(',')]
        except ValueError:
            return None
        return f'{south},{west},{north},{east}'

    @staticmethod
    def viewbox(params: dict[str, Any]) -> str | None:
        try:
            radius = float(params.get('radius_km', 0) or 0)
            center_lat = float(params.get('center_lat'))
            center_lon = float(params.get('center_lon'))
        except (TypeError, ValueError):
            radius = center_lat = center_lon = 0

        if radius > 0 and -90 <= center_lat <= 90 and -180 <= center_lon <= 180:
            lat_delta = radius / 111.32
            lon_delta = radius / max(1.0, 111.32 * math.cos(math.radians(center_lat)))
            return (
                f'{max(-180, center_lon - lon_delta)},'
                f'{min(90, center_lat + lat_delta)},'
                f'{min(180, center_lon + lon_delta)},'
                f'{max(-90, center_lat - lat_delta)}'
            )

        try:
            west, east = float(params.get('west')), float(params.get('east'))
            south, north = float(params.get('south')), float(params.get('north'))
        except (TypeError, ValueError):
            return None

        if not (-180 <= west <= 180 and -180 <= east <= 180 and -90 <= south <= 90 and -90 <= north <= 90):
            return None

        if abs(east - west) > 0.9 or abs(north - south) > 0.7:
            try:
                center_lat = float(params.get('center_lat'))
                center_lon = float(params.get('center_lon'))
            except (TypeError, ValueError):
                return f'{west},{north},{east},{south}'
            if -90 <= center_lat <= 90 and -180 <= center_lon <= 180:
                lat_delta = 20.0 / 111.32
                lon_delta = 20.0 / max(1.0, 111.32 * math.cos(math.radians(center_lat)))
                west, east = max(-180, center_lon - lon_delta), min(180, center_lon + lon_delta)
                south, north = max(-90, center_lat - lat_delta), min(90, center_lat + lat_delta)

        return f'{west},{north},{east},{south}'

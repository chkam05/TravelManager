from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Any, ClassVar, Dict

from core.data.base_data_model import BaseDataModel
from models.offline_maps.validation import (
    bounds, https_url, iso_datetime, optional_text, region_id,
    required_text, string_list, non_negative_integer,
)


@dataclass
class OfflineMapRegion(BaseDataModel):
    """One downloadable region exposed by an audited map source."""

    FIELD_ID: ClassVar[str] = 'id'
    FIELD_NAME: ClassVar[str] = 'name'
    FIELD_PARENT_ID: ClassVar[str] = 'parent_id'
    FIELD_COUNTRY_CODES: ClassVar[str] = 'country_codes'
    FIELD_REGION_CODES: ClassVar[str] = 'region_codes'
    FIELD_PBF_URL: ClassVar[str] = 'pbf_url'
    FIELD_PBF_SIZE: ClassVar[str] = 'pbf_size'
    FIELD_SOURCE_UPDATED_AT: ClassVar[str] = 'source_updated_at'
    FIELD_BOUNDS: ClassVar[str] = 'bounds'
    FIELD_CHILDREN: ClassVar[str] = 'children'
    FIELD_COVERAGE: ClassVar[str] = 'coverage'

    id: str
    name: str
    parent_id: str
    country_codes: list[str]
    region_codes: list[str]
    pbf_url: str
    pbf_size: int | None
    source_updated_at: str
    bounds: list[float] | None
    children: list[str]
    coverage: dict | None

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> OfflineMapRegion:
        if not isinstance(d, dict):
            raise ValueError('Invalid offline map region.')
        parent = optional_text(d.get(cls.FIELD_PARENT_ID), 'parent id', 200)
        if parent:
            parent = region_id(parent, 'parent id')
        url = optional_text(d.get(cls.FIELD_PBF_URL), 'PBF URL', 2048)
        return cls(
            id=region_id(d.get(cls.FIELD_ID)),
            name=required_text(d.get(cls.FIELD_NAME), 'region name'),
            parent_id=parent,
            country_codes=string_list(
                d.get(cls.FIELD_COUNTRY_CODES), 'country codes',
                re.compile(r'^[A-Z]{2}$')
            ),
            region_codes=string_list(
                d.get(cls.FIELD_REGION_CODES), 'region codes',
                re.compile(r'^[A-Z]{2}-[A-Z0-9]{1,6}$')
            ),
            pbf_url=https_url(url, 'PBF URL') if url else '',
            pbf_size=non_negative_integer(
                d.get(cls.FIELD_PBF_SIZE), 'PBF size', allow_none=True
            ),
            source_updated_at=iso_datetime(
                d.get(cls.FIELD_SOURCE_UPDATED_AT), 'source update date'
            ),
            bounds=bounds(d.get(cls.FIELD_BOUNDS)),
            children=[
                region_id(item, 'child id')
                for item in string_list(d.get(cls.FIELD_CHILDREN), 'children')
            ],
            coverage=cls._coverage(d.get(cls.FIELD_COVERAGE)),
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            self.FIELD_ID: self.id,
            self.FIELD_NAME: self.name,
            self.FIELD_PARENT_ID: self.parent_id,
            self.FIELD_COUNTRY_CODES: list(self.country_codes),
            self.FIELD_REGION_CODES: list(self.region_codes),
            self.FIELD_PBF_URL: self.pbf_url,
            self.FIELD_PBF_SIZE: self.pbf_size,
            self.FIELD_SOURCE_UPDATED_AT: self.source_updated_at,
            self.FIELD_BOUNDS: list(self.bounds) if self.bounds else None,
            self.FIELD_CHILDREN: list(self.children),
            **({self.FIELD_COVERAGE: self.coverage} if self.coverage else {}),
        }

    @staticmethod
    def _coverage(value: object) -> dict | None:
        if value is None:
            return None
        if not isinstance(value, dict) or value.get('type') not in {
            'Polygon', 'MultiPolygon'
        }:
            raise ValueError('Invalid region coverage geometry.')
        coordinates = value.get('coordinates')
        polygons = [coordinates] if value['type'] == 'Polygon' else coordinates
        if not isinstance(polygons, list) or not polygons:
            raise ValueError('Invalid region coverage geometry.')
        clean_polygons = []
        for polygon in polygons:
            if not isinstance(polygon, list) or not polygon:
                raise ValueError('Invalid region coverage geometry.')
            clean_rings = []
            for ring in polygon:
                if not isinstance(ring, list) or len(ring) < 4:
                    raise ValueError('Invalid region coverage geometry.')
                clean_ring = []
                for point in ring:
                    if (
                        not isinstance(point, (list, tuple)) or len(point) < 2
                        or type(point[0]) not in (int, float)
                        or type(point[1]) not in (int, float)
                        or not -180 <= point[0] <= 180
                        or not -90 <= point[1] <= 90
                    ):
                        raise ValueError('Invalid region coverage geometry.')
                    clean_ring.append([float(point[0]), float(point[1])])
                if clean_ring[0] != clean_ring[-1]:
                    raise ValueError('Invalid region coverage geometry.')
                clean_rings.append(clean_ring)
            clean_polygons.append(clean_rings)
        return {
            'type': value['type'],
            'coordinates': clean_polygons[0]
            if value['type'] == 'Polygon' else clean_polygons,
        }

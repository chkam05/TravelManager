from __future__ import annotations

from dataclasses import dataclass
from pathlib import PurePath
from typing import Any, ClassVar, Dict

from core.data.base_data_model import BaseDataModel
from models.offline_maps.validation import (
    bounds, iso_datetime, local_id, non_negative_integer, region_id,
    required_text,
)


@dataclass
class OfflineMap(BaseDataModel):
    """Metadata for one completely installed MBTiles package."""

    FIELD_ID: ClassVar[str] = 'id'
    FIELD_REGION_ID: ClassVar[str] = 'region_id'
    FIELD_NAME: ClassVar[str] = 'name'
    FIELD_FILE_NAME: ClassVar[str] = 'file_name'
    FIELD_SIZE: ClassVar[str] = 'size'
    FIELD_BOUNDS: ClassVar[str] = 'bounds'
    FIELD_MIN_ZOOM: ClassVar[str] = 'min_zoom'
    FIELD_MAX_ZOOM: ClassVar[str] = 'max_zoom'
    FIELD_INSTALLED_AT: ClassVar[str] = 'installed_at'
    FIELD_SOURCE_UPDATED_AT: ClassVar[str] = 'source_updated_at'
    FIELD_SCHEMA_VERSION: ClassVar[str] = 'schema_version'

    id: str
    region_id: str
    name: str
    file_name: str
    size: int
    bounds: list[float]
    min_zoom: int
    max_zoom: int
    installed_at: str
    source_updated_at: str
    schema_version: int

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> OfflineMap:
        if not isinstance(d, dict):
            raise ValueError('Invalid offline map.')
        file_name = required_text(d.get(cls.FIELD_FILE_NAME), 'map file name', 180)
        if PurePath(file_name).name != file_name or not file_name.endswith('.mbtiles'):
            raise ValueError('Invalid map file name.')
        minimum = non_negative_integer(d.get(cls.FIELD_MIN_ZOOM), 'minimum zoom')
        maximum = non_negative_integer(d.get(cls.FIELD_MAX_ZOOM), 'maximum zoom')
        if minimum > maximum or maximum > 22:
            raise ValueError('Invalid zoom range.')
        schema_version = non_negative_integer(d.get(cls.FIELD_SCHEMA_VERSION), 'schema version')
        if schema_version < 1:
            raise ValueError('Invalid schema version.')
        return cls(
            id=local_id(d.get(cls.FIELD_ID), 'map id'),
            region_id=region_id(d.get(cls.FIELD_REGION_ID)),
            name=required_text(d.get(cls.FIELD_NAME), 'map name'),
            file_name=file_name,
            size=non_negative_integer(d.get(cls.FIELD_SIZE), 'map size'),
            bounds=bounds(d.get(cls.FIELD_BOUNDS), optional=False),
            min_zoom=minimum,
            max_zoom=maximum,
            installed_at=iso_datetime(d.get(cls.FIELD_INSTALLED_AT), 'installation date', optional=False),
            source_updated_at=iso_datetime(d.get(cls.FIELD_SOURCE_UPDATED_AT), 'source update date'),
            schema_version=schema_version,
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            self.FIELD_ID: self.id,
            self.FIELD_REGION_ID: self.region_id,
            self.FIELD_NAME: self.name,
            self.FIELD_FILE_NAME: self.file_name,
            self.FIELD_SIZE: self.size,
            self.FIELD_BOUNDS: list(self.bounds),
            self.FIELD_MIN_ZOOM: self.min_zoom,
            self.FIELD_MAX_ZOOM: self.max_zoom,
            self.FIELD_INSTALLED_AT: self.installed_at,
            self.FIELD_SOURCE_UPDATED_AT: self.source_updated_at,
            self.FIELD_SCHEMA_VERSION: self.schema_version,
        }

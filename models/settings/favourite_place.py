from __future__ import annotations

from dataclasses import dataclass
from typing import Any, ClassVar, Dict

from core.data.base_data_model import BaseDataModel


@dataclass
class FavouritePlace(BaseDataModel):
    """Stores a user-defined favourite map place."""

    # Default values

    # Field name declarations
    FIELD_ID: ClassVar[str] = 'id'
    FIELD_SOURCE_KEY: ClassVar[str] = 'source_key'
    FIELD_NAME: ClassVar[str] = 'name'
    FIELD_TAG_ID: ClassVar[str] = 'tag_id'
    FIELD_ICON: ClassVar[str] = 'icon'
    FIELD_LATITUDE: ClassVar[str] = 'latitude'
    FIELD_LONGITUDE: ClassVar[str] = 'longitude'
    FIELD_PLACE_DATA: ClassVar[str] = 'place_data'

    # Fields
    id: str
    source_key: str
    name: str
    tag_id: str
    icon: str | None
    latitude: float
    longitude: float
    place_data: Dict[str, Any]

    #region Serialization

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> FavouritePlace:
        """Deserializes favourite place data from a dictionary."""
        return cls(
            id=str(d.get(cls.FIELD_ID, '')),
            source_key=str(d.get(cls.FIELD_SOURCE_KEY, '')),
            name=str(d.get(cls.FIELD_NAME, '')),
            tag_id=str(d.get(cls.FIELD_TAG_ID, '')),
            icon=str(d.get(cls.FIELD_ICON)) if d.get(cls.FIELD_ICON) else None,
            latitude=float(d.get(cls.FIELD_LATITUDE, 0.0)),
            longitude=float(d.get(cls.FIELD_LONGITUDE, 0.0)),
            place_data=d.get(cls.FIELD_PLACE_DATA, {}) if isinstance(d.get(cls.FIELD_PLACE_DATA), dict) else {}
        )

    def to_dict(self) -> Dict[str, Any]:
        """Serializes favourite place data to a dictionary."""
        return {
            self.FIELD_ID: self.id,
            self.FIELD_SOURCE_KEY: self.source_key,
            self.FIELD_NAME: self.name,
            self.FIELD_TAG_ID: self.tag_id,
            self.FIELD_ICON: self.icon,
            self.FIELD_LATITUDE: self.latitude,
            self.FIELD_LONGITUDE: self.longitude,
            self.FIELD_PLACE_DATA: self.place_data
        }

    #endregion Serialization

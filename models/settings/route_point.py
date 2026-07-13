from __future__ import annotations

from dataclasses import dataclass
from typing import Any, ClassVar, Dict

from core.data.base_data_model import BaseDataModel


@dataclass
class RoutePoint(BaseDataModel):
    """Stores a single point used by a saved route."""

    # Default values

    # Field name declarations
    FIELD_ID: ClassVar[str] = 'id'
    FIELD_TITLE: ClassVar[str] = 'title'
    FIELD_LATITUDE: ClassVar[str] = 'latitude'
    FIELD_LONGITUDE: ClassVar[str] = 'longitude'

    # Fields
    id: str
    title: str
    latitude: float
    longitude: float

    #region Serialization

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> RoutePoint:
        """Deserializes route point data from a dictionary."""
        return cls(
            id=str(d.get(cls.FIELD_ID, '')),
            title=str(d.get(cls.FIELD_TITLE, '')),
            latitude=float(d.get(cls.FIELD_LATITUDE, 0.0)),
            longitude=float(d.get(cls.FIELD_LONGITUDE, 0.0))
        )

    def to_dict(self) -> Dict[str, Any]:
        """Serializes route point data to a dictionary."""
        return {
            self.FIELD_ID: self.id,
            self.FIELD_TITLE: self.title,
            self.FIELD_LATITUDE: self.latitude,
            self.FIELD_LONGITUDE: self.longitude
        }

    #endregion Serialization

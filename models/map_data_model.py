from __future__ import annotations
from dataclasses import dataclass
from typing import Any, ClassVar, Dict

from core.data.base_data_model import BaseDataModel
from models.map.map_place_data_model import MapPlaceDataModel


@dataclass
class MapDataModel(BaseDataModel):
    """Stores the complete map data payload returned by the Python API."""

    # https://wiki.openstreetmap.org/wiki/Map_features#Additional_properties
    # https://wiki.openstreetmap.org/w/index.php?title=Category:Key_descriptions
    # https://wiki.openstreetmap.org/wiki/Category:Tag_descriptions

    # Default values
    _DEFAULT_STATUS: ClassVar[str] = 'ok'
    _DEFAULT_MESSAGE: ClassVar[str | None] = None

    # Field name declarations
    FIELD_STATUS: ClassVar[str] = 'status'
    FIELD_MESSAGE: ClassVar[str] = 'message'
    FIELD_PLACE: ClassVar[str] = 'place'

    # Fields
    status: str
    message: str | None
    place: MapPlaceDataModel | None

    #region Serialization

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> MapDataModel:
        """Deserializes data from a dictionary in "attribute:value" format to an object."""
        place = d.get(cls.FIELD_PLACE)

        return cls(
            status=d.get(cls.FIELD_STATUS, cls._DEFAULT_STATUS),
            message=d.get(cls.FIELD_MESSAGE, cls._DEFAULT_MESSAGE),
            place=MapPlaceDataModel.from_dict(place) if place else None
        )

    def to_dict(self) -> Dict[str, Any]:
        """Serializes object to a dictionary in the format "attribute:value"."""
        return {
            self.FIELD_STATUS: self.status,
            self.FIELD_MESSAGE: self.message,
            self.FIELD_PLACE: self.place.to_dict() if self.place else None
        }

    #endregion Serialization

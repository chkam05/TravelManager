from __future__ import annotations
from dataclasses import dataclass
from typing import Any, ClassVar, Dict

from core.data.base_data_model import BaseDataModel
from models.public_transport.model_serialization import parse_coordinate


@dataclass
class PublicTransportCoordinate(BaseDataModel):
    """Stores one geographical point of a public transport route."""

    # Field name declarations
    FIELD_LATITUDE: ClassVar[str] = 'latitude'
    FIELD_LONGITUDE: ClassVar[str] = 'longitude'

    # Fields
    latitude: float
    longitude: float

    #region Serialization

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> PublicTransportCoordinate:
        """Deserializes a geographical point."""
        return cls(
            latitude=parse_coordinate(
                d.get(cls.FIELD_LATITUDE),
                -90,
                90
            ) or 0.0,
            longitude=parse_coordinate(
                d.get(cls.FIELD_LONGITUDE),
                -180,
                180
            ) or 0.0
        )

    def to_dict(self) -> Dict[str, Any]:
        """Serializes a geographical point."""
        return {
            self.FIELD_LATITUDE: self.latitude,
            self.FIELD_LONGITUDE: self.longitude
        }

    #endregion Serialization

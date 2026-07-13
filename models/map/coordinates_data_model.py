from __future__ import annotations
from dataclasses import dataclass
from typing import Any, ClassVar, Dict

from core.data.base_data_model import BaseDataModel


@dataclass
class CoordinatesDataModel(BaseDataModel):
    """Stores geographic coordinates for an OpenStreetMap element."""

    # Default values
    _DEFAULT_LATITUDE: ClassVar[float | None] = None
    _DEFAULT_LONGITUDE: ClassVar[float | None] = None

    # Field name declarations
    FIELD_LATITUDE: ClassVar[str] = 'latitude'
    FIELD_LONGITUDE: ClassVar[str] = 'longitude'

    # Fields
    latitude: float | None
    longitude: float | None

    #region Serialization

    @staticmethod
    def _to_float(value: Any) -> float | None:
        """Converts numeric API values to float while preserving missing values."""
        if value is None or value == '':
            return None

        return float(value)

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> CoordinatesDataModel:
        """Deserializes data from a dictionary in "attribute:value" format to an object."""
        return cls(
            latitude=cls._to_float(d.get(cls.FIELD_LATITUDE, d.get('lat', cls._DEFAULT_LATITUDE))),
            longitude=cls._to_float(d.get(cls.FIELD_LONGITUDE, d.get('lon', cls._DEFAULT_LONGITUDE)))
        )

    def to_dict(self) -> Dict[str, Any]:
        """Serializes object to a dictionary in the format "attribute:value"."""
        return {
            self.FIELD_LATITUDE: self.latitude,
            self.FIELD_LONGITUDE: self.longitude
        }

    #endregion Serialization

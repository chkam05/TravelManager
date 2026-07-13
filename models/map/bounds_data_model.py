from __future__ import annotations
from dataclasses import dataclass
from typing import Any, ClassVar, Dict

from core.data.base_data_model import BaseDataModel


@dataclass
class BoundsDataModel(BaseDataModel):
    """Stores geographic bounds for an OpenStreetMap element."""

    # Default values
    _DEFAULT_SOUTH: ClassVar[float | None] = None
    _DEFAULT_WEST: ClassVar[float | None] = None
    _DEFAULT_NORTH: ClassVar[float | None] = None
    _DEFAULT_EAST: ClassVar[float | None] = None

    # Field name declarations
    FIELD_SOUTH: ClassVar[str] = 'south'
    FIELD_WEST: ClassVar[str] = 'west'
    FIELD_NORTH: ClassVar[str] = 'north'
    FIELD_EAST: ClassVar[str] = 'east'

    # Fields
    south: float | None
    west: float | None
    north: float | None
    east: float | None

    #region Serialization

    @staticmethod
    def _to_float(value: Any) -> float | None:
        """Converts numeric API values to float while preserving missing values."""
        if value is None or value == '':
            return None

        return float(value)

    @classmethod
    def _from_nominatim_bounds(cls, value: Any) -> Dict[str, Any]:
        """Converts Nominatim boundingbox arrays to the local bounds dictionary shape."""
        if not isinstance(value, list) or len(value) != 4:
            return {}

        return {
            cls.FIELD_SOUTH: value[0],
            cls.FIELD_NORTH: value[1],
            cls.FIELD_WEST: value[2],
            cls.FIELD_EAST: value[3]
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> BoundsDataModel:
        """Deserializes data from a dictionary in "attribute:value" format to an object."""
        if 'boundingbox' in d:
            d = cls._from_nominatim_bounds(d.get('boundingbox'))

        return cls(
            south=cls._to_float(d.get(cls.FIELD_SOUTH, cls._DEFAULT_SOUTH)),
            west=cls._to_float(d.get(cls.FIELD_WEST, cls._DEFAULT_WEST)),
            north=cls._to_float(d.get(cls.FIELD_NORTH, cls._DEFAULT_NORTH)),
            east=cls._to_float(d.get(cls.FIELD_EAST, cls._DEFAULT_EAST))
        )

    def to_dict(self) -> Dict[str, Any]:
        """Serializes object to a dictionary in the format "attribute:value"."""
        return {
            self.FIELD_SOUTH: self.south,
            self.FIELD_WEST: self.west,
            self.FIELD_NORTH: self.north,
            self.FIELD_EAST: self.east
        }

    #endregion Serialization

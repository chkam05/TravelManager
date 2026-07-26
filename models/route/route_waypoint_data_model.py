from __future__ import annotations
from dataclasses import dataclass
from typing import Any, ClassVar, Dict, List

from core.data.base_data_model import BaseDataModel


@dataclass
class RouteWaypointDataModel(BaseDataModel):
    """Stores a waypoint returned by an OSRM-compatible router."""

    # Default values
    _DEFAULT_NAME: ClassVar[str] = ''
    _DEFAULT_DISTANCE: ClassVar[float] = 0.0

    # Field name declarations
    FIELD_NAME: ClassVar[str] = 'name'
    FIELD_LOCATION: ClassVar[str] = 'location'
    FIELD_DISTANCE: ClassVar[str] = 'distance'

    # Fields
    name: str
    location: List[float]
    distance: float

    #region Serialization

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> RouteWaypointDataModel:
        """Deserializes data from a dictionary in "attribute:value" format to an object."""
        location = d.get(cls.FIELD_LOCATION, [])
        return cls(
            name=str(d.get(cls.FIELD_NAME) or cls._DEFAULT_NAME),
            location=[
                float(value) for value in location[:2]
            ] if isinstance(location, (list, tuple)) else [],
            distance=max(0.0, float(d.get(cls.FIELD_DISTANCE) or cls._DEFAULT_DISTANCE))
        )

    def to_dict(self) -> Dict[str, Any]:
        """Serializes object to a dictionary in the format "attribute:value"."""
        return {
            self.FIELD_NAME: self.name,
            self.FIELD_LOCATION: list(self.location),
            self.FIELD_DISTANCE: self.distance
        }

    #endregion Serialization

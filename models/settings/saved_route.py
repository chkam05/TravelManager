from __future__ import annotations

from dataclasses import dataclass
from typing import Any, ClassVar, Dict, List

from core.data.base_data_model import BaseDataModel
from models.settings.route_point import RoutePoint


@dataclass
class SavedRoute(BaseDataModel):
    """Stores a user-defined route with route points and cached summary values."""

    # Default values
    DEFAULT_ICON: ClassVar[str] = '🚗'

    # Field name declarations
    FIELD_ID: ClassVar[str] = 'id'
    FIELD_NAME: ClassVar[str] = 'name'
    FIELD_ICON: ClassVar[str] = 'icon'
    FIELD_POINTS: ClassVar[str] = 'points'
    FIELD_DISTANCE: ClassVar[str] = 'distance'
    FIELD_DURATION: ClassVar[str] = 'duration'

    # Fields
    id: str
    name: str
    icon: str
    points: List[RoutePoint]
    distance: float
    duration: float

    #region Serialization

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> SavedRoute:
        """Deserializes saved route data from a dictionary."""
        points = d.get(cls.FIELD_POINTS, [])

        return cls(
            id=str(d.get(cls.FIELD_ID, '')),
            name=str(d.get(cls.FIELD_NAME, '')),
            icon=str(d.get(cls.FIELD_ICON, cls.DEFAULT_ICON) or cls.DEFAULT_ICON),
            points=RoutePoint.from_dict_list(points if isinstance(points, list) else []),
            distance=float(d.get(cls.FIELD_DISTANCE, 0.0) or 0.0),
            duration=float(d.get(cls.FIELD_DURATION, 0.0) or 0.0)
        )

    def to_dict(self) -> Dict[str, Any]:
        """Serializes saved route data to a dictionary."""
        return {
            self.FIELD_ID: self.id,
            self.FIELD_NAME: self.name,
            self.FIELD_ICON: self.icon,
            self.FIELD_POINTS: self.to_dict_list(self.points),
            self.FIELD_DISTANCE: self.distance,
            self.FIELD_DURATION: self.duration
        }

    #endregion Serialization

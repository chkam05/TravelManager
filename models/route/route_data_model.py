from __future__ import annotations
from dataclasses import dataclass
from typing import Any, ClassVar, Dict, List

from core.data.base_data_model import BaseDataModel
from models.route.route_geometry_data_model import RouteGeometryDataModel
from models.route.route_leg_data_model import RouteLegDataModel
from models.route.route_waypoint_data_model import RouteWaypointDataModel


@dataclass
class RouteDataModel(BaseDataModel):
    """Stores a route in the stable shape consumed by the frontend."""

    # Default values
    _DEFAULT_DISTANCE: ClassVar[float] = 0.0
    _DEFAULT_DURATION: ClassVar[float] = 0.0
    _DEFAULT_TOLL_EXCLUSION_REQUESTED: ClassVar[bool] = False
    _DEFAULT_TOLL_EXCLUSION_APPLIED: ClassVar[bool] = False
    _DEFAULT_TOLL_EXCLUSION_WARNING: ClassVar[str | None] = None

    # Field name declarations
    FIELD_DISTANCE: ClassVar[str] = 'distance'
    FIELD_DURATION: ClassVar[str] = 'duration'
    FIELD_GEOMETRY: ClassVar[str] = 'geometry'
    FIELD_LEGS: ClassVar[str] = 'legs'
    FIELD_WAYPOINTS: ClassVar[str] = 'waypoints'
    FIELD_TOLL_EXCLUSION_REQUESTED: ClassVar[str] = 'toll_exclusion_requested'
    FIELD_TOLL_EXCLUSION_APPLIED: ClassVar[str] = 'toll_exclusion_applied'
    FIELD_TOLL_EXCLUSION_WARNING: ClassVar[str] = 'toll_exclusion_warning'

    # Fields
    distance: float
    duration: float
    geometry: RouteGeometryDataModel
    legs: List[RouteLegDataModel]
    waypoints: List[RouteWaypointDataModel]
    toll_exclusion_requested: bool
    toll_exclusion_applied: bool
    toll_exclusion_warning: str | None

    #region Serialization

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> RouteDataModel:
        """Deserializes data from a dictionary in "attribute:value" format to an object."""
        return cls(
            distance=max(0.0, float(d.get(cls.FIELD_DISTANCE) or cls._DEFAULT_DISTANCE)),
            duration=max(0.0, float(d.get(cls.FIELD_DURATION) or cls._DEFAULT_DURATION)),
            geometry=RouteGeometryDataModel.from_dict(
                d.get(cls.FIELD_GEOMETRY) if isinstance(d.get(cls.FIELD_GEOMETRY), dict) else {}
            ),
            legs=RouteLegDataModel.from_dict_list(
                d.get(cls.FIELD_LEGS) if isinstance(d.get(cls.FIELD_LEGS), list) else []
            ),
            waypoints=RouteWaypointDataModel.from_dict_list(
                d.get(cls.FIELD_WAYPOINTS) if isinstance(d.get(cls.FIELD_WAYPOINTS), list) else []
            ),
            toll_exclusion_requested=bool(d.get(
                cls.FIELD_TOLL_EXCLUSION_REQUESTED,
                cls._DEFAULT_TOLL_EXCLUSION_REQUESTED
            )),
            toll_exclusion_applied=bool(d.get(
                cls.FIELD_TOLL_EXCLUSION_APPLIED,
                cls._DEFAULT_TOLL_EXCLUSION_APPLIED
            )),
            toll_exclusion_warning=d.get(
                cls.FIELD_TOLL_EXCLUSION_WARNING,
                cls._DEFAULT_TOLL_EXCLUSION_WARNING
            )
        )

    def to_dict(self) -> Dict[str, Any]:
        """Serializes object to a dictionary in the format "attribute:value"."""
        return {
            self.FIELD_DISTANCE: self.distance,
            self.FIELD_DURATION: self.duration,
            self.FIELD_GEOMETRY: self.geometry.to_dict(),
            self.FIELD_LEGS: self.to_dict_list(self.legs),
            self.FIELD_WAYPOINTS: self.to_dict_list(self.waypoints),
            self.FIELD_TOLL_EXCLUSION_REQUESTED: self.toll_exclusion_requested,
            self.FIELD_TOLL_EXCLUSION_APPLIED: self.toll_exclusion_applied,
            self.FIELD_TOLL_EXCLUSION_WARNING: self.toll_exclusion_warning
        }

    #endregion Serialization

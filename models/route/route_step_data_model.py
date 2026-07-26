from __future__ import annotations
from dataclasses import dataclass
from typing import Any, ClassVar, Dict

from core.data.base_data_model import BaseDataModel
from models.route.route_maneuver_data_model import RouteManeuverDataModel


@dataclass
class RouteStepDataModel(BaseDataModel):
    """Stores one frontend route instruction."""

    # Default values
    _DEFAULT_DISTANCE: ClassVar[float] = 0.0
    _DEFAULT_DURATION: ClassVar[float] = 0.0
    _DEFAULT_NAME: ClassVar[str] = ''
    _DEFAULT_INSTRUCTION: ClassVar[str] = ''

    # Field name declarations
    FIELD_DISTANCE: ClassVar[str] = 'distance'
    FIELD_DURATION: ClassVar[str] = 'duration'
    FIELD_NAME: ClassVar[str] = 'name'
    FIELD_INSTRUCTION: ClassVar[str] = 'instruction'
    FIELD_MANEUVER: ClassVar[str] = 'maneuver'

    # Fields
    distance: float
    duration: float
    name: str
    instruction: str
    maneuver: RouteManeuverDataModel

    #region Serialization

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> RouteStepDataModel:
        """Deserializes data from a dictionary in "attribute:value" format to an object."""
        maneuver = d.get(cls.FIELD_MANEUVER, {})
        return cls(
            distance=max(0.0, float(d.get(cls.FIELD_DISTANCE) or cls._DEFAULT_DISTANCE)),
            duration=max(0.0, float(d.get(cls.FIELD_DURATION) or cls._DEFAULT_DURATION)),
            name=str(d.get(cls.FIELD_NAME) or cls._DEFAULT_NAME),
            instruction=str(d.get(cls.FIELD_INSTRUCTION) or cls._DEFAULT_INSTRUCTION),
            maneuver=RouteManeuverDataModel.from_dict(maneuver if isinstance(maneuver, dict) else {})
        )

    def to_dict(self) -> Dict[str, Any]:
        """Serializes object to a dictionary in the format "attribute:value"."""
        return {
            self.FIELD_DISTANCE: self.distance,
            self.FIELD_DURATION: self.duration,
            self.FIELD_NAME: self.name,
            self.FIELD_INSTRUCTION: self.instruction,
            self.FIELD_MANEUVER: self.maneuver.to_dict()
        }

    #endregion Serialization

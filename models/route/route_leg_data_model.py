from __future__ import annotations
from dataclasses import dataclass
from typing import Any, ClassVar, Dict, List

from core.data.base_data_model import BaseDataModel
from models.route.route_step_data_model import RouteStepDataModel


@dataclass
class RouteLegDataModel(BaseDataModel):
    """Stores one leg between consecutive route points."""

    # Default values
    _DEFAULT_DISTANCE: ClassVar[float] = 0.0
    _DEFAULT_DURATION: ClassVar[float] = 0.0

    # Field name declarations
    FIELD_DISTANCE: ClassVar[str] = 'distance'
    FIELD_DURATION: ClassVar[str] = 'duration'
    FIELD_STEPS: ClassVar[str] = 'steps'

    # Fields
    distance: float
    duration: float
    steps: List[RouteStepDataModel]

    #region Serialization

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> RouteLegDataModel:
        """Deserializes data from a dictionary in "attribute:value" format to an object."""
        steps = d.get(cls.FIELD_STEPS, [])
        return cls(
            distance=max(0.0, float(d.get(cls.FIELD_DISTANCE) or cls._DEFAULT_DISTANCE)),
            duration=max(0.0, float(d.get(cls.FIELD_DURATION) or cls._DEFAULT_DURATION)),
            steps=RouteStepDataModel.from_dict_list(steps if isinstance(steps, list) else [])
        )

    def to_dict(self) -> Dict[str, Any]:
        """Serializes object to a dictionary in the format "attribute:value"."""
        return {
            self.FIELD_DISTANCE: self.distance,
            self.FIELD_DURATION: self.duration,
            self.FIELD_STEPS: self.to_dict_list(self.steps)
        }

    #endregion Serialization

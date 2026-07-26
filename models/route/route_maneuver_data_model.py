from __future__ import annotations
from dataclasses import dataclass
from typing import Any, ClassVar, Dict

from core.data.base_data_model import BaseDataModel


@dataclass
class RouteManeuverDataModel(BaseDataModel):
    """Stores the maneuver information used by route instructions."""

    # Default values
    _DEFAULT_TYPE: ClassVar[str] = ''
    _DEFAULT_MODIFIER: ClassVar[str] = ''
    _DEFAULT_EXIT: ClassVar[int | None] = None

    # Field name declarations
    FIELD_TYPE: ClassVar[str] = 'type'
    FIELD_MODIFIER: ClassVar[str] = 'modifier'
    FIELD_EXIT: ClassVar[str] = 'exit'

    # Fields
    type: str
    modifier: str
    exit: int | None

    #region Serialization

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> RouteManeuverDataModel:
        """Deserializes data from a dictionary in "attribute:value" format to an object."""
        try:
            exit_number = (
                int(d.get(cls.FIELD_EXIT))
                if d.get(cls.FIELD_EXIT) is not None
                else cls._DEFAULT_EXIT
            )
        except (TypeError, ValueError):
            exit_number = cls._DEFAULT_EXIT

        return cls(
            type=str(d.get(cls.FIELD_TYPE) or cls._DEFAULT_TYPE),
            modifier=str(d.get(cls.FIELD_MODIFIER) or cls._DEFAULT_MODIFIER),
            exit=exit_number
        )

    def to_dict(self) -> Dict[str, Any]:
        """Serializes object to a dictionary in the format "attribute:value"."""
        return {
            self.FIELD_TYPE: self.type,
            self.FIELD_MODIFIER: self.modifier,
            self.FIELD_EXIT: self.exit
        }

    #endregion Serialization

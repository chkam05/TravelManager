from __future__ import annotations
from dataclasses import dataclass
from typing import Any, ClassVar, Dict

from core.data.base_data_model import BaseDataModel


@dataclass
class FuelCostCache(BaseDataModel):
    """Stores cached fuel cost table data inside application settings."""

    # Default values

    # Field name declarations
    FIELD_DATA: ClassVar[str] = 'data'

    # Fields
    data: Dict[str, Any]

    #region Serialization

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> FuelCostCache:
        """Deserializes data from a dictionary in "attribute:value" format to an object."""
        data = d.get(cls.FIELD_DATA, d if isinstance(d, dict) else {})

        return cls(
            data=data if isinstance(data, dict) else {}
        )

    def to_dict(self) -> Dict[str, Any]:
        """Serializes object to a dictionary in the format "attribute:value"."""
        return {
            self.FIELD_DATA: self.data if isinstance(self.data, dict) else {}
        }

    #endregion Serialization

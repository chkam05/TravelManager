from __future__ import annotations
from dataclasses import dataclass
from typing import Any, ClassVar, Dict

from core.data.base_data_model import BaseDataModel


@dataclass
class PublicTransportCity(BaseDataModel):
    """Stores a city name and its provider-defined display color."""

    # Default values
    _DEFAULT_COLOR: ClassVar[str] = '#000000'

    # Field name declarations
    FIELD_NAME: ClassVar[str] = 'name'
    FIELD_COLOR: ClassVar[str] = 'color'

    # Fields
    name: str
    color: str

    #region Serialization

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> PublicTransportCity:
        """Deserializes data from a dictionary in "attribute:value" format to an object."""
        color = str(d.get(cls.FIELD_COLOR) or cls._DEFAULT_COLOR).strip()
        return cls(
            name=str(d.get(cls.FIELD_NAME) or ''),
            color=color if color.startswith('#') else f'#{color}'
        )

    def to_dict(self) -> Dict[str, Any]:
        """Serializes object to a dictionary in the format "attribute:value"."""
        return {
            self.FIELD_NAME: self.name,
            self.FIELD_COLOR: self.color
        }

    #endregion Serialization

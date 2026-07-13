from __future__ import annotations
from dataclasses import dataclass
from typing import Any, ClassVar, Dict

from core.data.base_data_model import BaseDataModel


@dataclass
class PlaceAttributesDataModel(BaseDataModel):
    """Stores OpenStreetMap tag values defined by OpenStreetMap PrimaryFeaturesAttr.PlaceAttr."""

    # Default values
    _DEFAULT_VALUE: ClassVar[Any] = None

    # Field name declarations
    FIELD_POPULATION: ClassVar[str] = 'population'
    FIELD_IS_IN: ClassVar[str] = 'is_in'

    # OpenStreetMap tag declarations
    TAG_POPULATION: ClassVar[str] = 'population'
    TAG_IS_IN: ClassVar[str] = 'is_in'

    # Fields
    population: Any | None
    is_in: Any | None

    #region Serialization

    @classmethod
    def _get_value(cls, d: Dict[str, Any], field_name: str, tag_name: str) -> Any:
        """Gets a value by local field name or by the real OpenStreetMap tag key."""
        return d.get(tag_name, d.get(field_name, cls._DEFAULT_VALUE))

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> PlaceAttributesDataModel:
        """Deserializes data from a dictionary in "attribute:value" format to an object."""
        return cls(
            population=cls._get_value(d, cls.FIELD_POPULATION, cls.TAG_POPULATION),
            is_in=cls._get_value(d, cls.FIELD_IS_IN, cls.TAG_IS_IN)
        )

    def to_dict(self) -> Dict[str, Any]:
        """Serializes object to a dictionary in the format "attribute:value"."""
        return {
            self.TAG_POPULATION: self.population,
            self.TAG_IS_IN: self.is_in
        }

    #endregion Serialization

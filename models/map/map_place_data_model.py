from __future__ import annotations
from dataclasses import dataclass
from typing import Any, ClassVar, Dict, List

from core.data.base_data_model import BaseDataModel
from models.map.map_element_data_model import MapElementDataModel


@dataclass
class MapPlaceDataModel(BaseDataModel):
    """Stores a structured map place query response."""

    # Default values
    _DEFAULT_QUERY: ClassVar[str | None] = None
    _DEFAULT_SOURCE: ClassVar[str | None] = None

    # Field name declarations
    FIELD_QUERY: ClassVar[str] = 'query'
    FIELD_SOURCE: ClassVar[str] = 'source'
    FIELD_SELECTED: ClassVar[str] = 'selected'
    FIELD_ELEMENTS: ClassVar[str] = 'elements'

    # Fields
    query: str | None
    source: str | None
    selected: MapElementDataModel | None
    elements: List[MapElementDataModel]

    #region Serialization

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> MapPlaceDataModel:
        """Deserializes data from a dictionary in "attribute:value" format to an object."""
        selected = d.get(cls.FIELD_SELECTED)

        return cls(
            query=d.get(cls.FIELD_QUERY, cls._DEFAULT_QUERY),
            source=d.get(cls.FIELD_SOURCE, cls._DEFAULT_SOURCE),
            selected=MapElementDataModel.from_dict(selected) if selected else None,
            elements=MapElementDataModel.from_dict_list(d.get(cls.FIELD_ELEMENTS, []))
        )

    def to_dict(self) -> Dict[str, Any]:
        """Serializes object to a dictionary in the format "attribute:value"."""
        return {
            self.FIELD_QUERY: self.query,
            self.FIELD_SOURCE: self.source,
            self.FIELD_SELECTED: self.selected.to_dict() if self.selected else None,
            self.FIELD_ELEMENTS: BaseDataModel.to_dict_list(self.elements)
        }

    #endregion Serialization

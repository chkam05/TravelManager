from __future__ import annotations
from dataclasses import dataclass
from typing import Any, ClassVar, Dict, List

from core.data.base_data_model import BaseDataModel


@dataclass
class RouteGeometryDataModel(BaseDataModel):
    """Stores GeoJSON route geometry."""

    # Default values
    _DEFAULT_TYPE: ClassVar[str] = 'LineString'

    # Field name declarations
    FIELD_TYPE: ClassVar[str] = 'type'
    FIELD_COORDINATES: ClassVar[str] = 'coordinates'

    # Fields
    type: str
    coordinates: List[List[float]]

    #region Serialization

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> RouteGeometryDataModel:
        """Deserializes data from a dictionary in "attribute:value" format to an object."""
        coordinates = d.get(cls.FIELD_COORDINATES, [])
        return cls(
            type=str(d.get(cls.FIELD_TYPE) or cls._DEFAULT_TYPE),
            coordinates=[
                [float(value) for value in point[:2]]
                for point in coordinates
                if isinstance(point, (list, tuple)) and len(point) >= 2
            ] if isinstance(coordinates, list) else []
        )

    def to_dict(self) -> Dict[str, Any]:
        """Serializes object to a dictionary in the format "attribute:value"."""
        return {
            self.FIELD_TYPE: self.type,
            self.FIELD_COORDINATES: [list(point) for point in self.coordinates]
        }

    #endregion Serialization

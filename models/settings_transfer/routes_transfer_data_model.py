from __future__ import annotations
from dataclasses import dataclass
from typing import Any, ClassVar, Dict, List

from core.data.base_data_model import BaseDataModel
from models.settings.saved_route import SavedRoute


@dataclass
class RoutesTransferDataModel(BaseDataModel):
    """Stores the explicit saved routes transfer payload."""

    # Default values

    # Field name declarations
    FIELD_ROUTES: ClassVar[str] = 'routes'

    # Fields
    routes: List[SavedRoute]

    #region Serialization

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> RoutesTransferDataModel:
        """Deserializes data from a dictionary in "attribute:value" format to an object."""
        routes = d.get(cls.FIELD_ROUTES, [])
        return cls(
            routes=SavedRoute.from_dict_list(routes if isinstance(routes, list) else [])
        )

    def to_dict(self) -> Dict[str, Any]:
        """Serializes object to a dictionary in the format "attribute:value"."""
        return {
            self.FIELD_ROUTES: self.to_dict_list(self.routes)
        }

    #endregion Serialization

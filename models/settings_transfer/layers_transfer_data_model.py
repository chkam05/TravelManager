from __future__ import annotations

from dataclasses import dataclass
from typing import Any, ClassVar, Dict, List

from core.data.base_data_model import BaseDataModel
from models.settings.custom_layer import CustomLayer


@dataclass
class LayersTransferDataModel(BaseDataModel):
    """Stores the explicit custom layers transfer payload."""

    FIELD_LAYERS: ClassVar[str] = 'layers'

    layers: List[CustomLayer]

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> LayersTransferDataModel:
        layers = d.get(cls.FIELD_LAYERS, [])
        return cls(
            layers=CustomLayer.from_dict_list(layers if isinstance(layers, list) else [])
        )

    def to_dict(self) -> Dict[str, Any]:
        return {self.FIELD_LAYERS: self.to_dict_list(self.layers)}

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, ClassVar, Dict, List

from core.data.base_data_model import BaseDataModel


@dataclass
class CustomLayerElement(BaseDataModel):
    FIELD_ID: ClassVar[str] = 'id'
    FIELD_NAME: ClassVar[str] = 'name'
    FIELD_TYPE: ClassVar[str] = 'type'
    FIELD_POINTS: ClassVar[str] = 'points'
    FIELD_COLOR: ClassVar[str] = 'color'
    FIELD_WIDTH: ClassVar[str] = 'width'
    id: str
    name: str
    type: str
    points: List[List[float]]
    color: str
    width: int

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "CustomLayerElement":
        points = []
        for point in d.get('points', []) if isinstance(d.get('points'), list) else []:
            if isinstance(point, (list, tuple)) and len(point) == 2:
                points.append([float(point[0]), float(point[1])])
        return cls(str(d.get('id', '')), str(d.get('name', '')), str(d.get('type', 'line')),
                   points, str(d.get('color', '#1F6FAE')), max(1, min(20, int(d.get('width', 4) or 4))))

    def to_dict(self) -> Dict[str, Any]:
        return {'id': self.id, 'name': self.name, 'type': self.type, 'points': self.points,
                'color': self.color, 'width': self.width}


@dataclass
class CustomLayer(BaseDataModel):
    FIELD_ID: ClassVar[str] = 'id'
    FIELD_NAME: ClassVar[str] = 'name'
    FIELD_ELEMENTS: ClassVar[str] = 'elements'
    id: str
    name: str
    elements: List[CustomLayerElement]

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "CustomLayer":
        elements = d.get('elements', [])
        return cls(str(d.get('id', '')), str(d.get('name', '')),
                   CustomLayerElement.from_dict_list(elements if isinstance(elements, list) else []))

    def to_dict(self) -> Dict[str, Any]:
        return {'id': self.id, 'name': self.name, 'elements': self.to_dict_list(self.elements)}

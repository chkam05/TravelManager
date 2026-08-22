from __future__ import annotations

from dataclasses import dataclass, field
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
    FIELD_SEGMENTS: ClassVar[str] = 'segments'
    FIELD_BACKGROUND_COLOR: ClassVar[str] = 'background_color'
    FIELD_LINE_STYLE: ClassVar[str] = 'line_style'
    id: str
    name: str
    type: str
    points: List[List[float]]
    color: str
    width: int
    segments: List[Dict[str, Any]] = field(default_factory=list)
    background_color: str = '#1F6FAE38'
    line_style: str = 'solid'

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "CustomLayerElement":
        points = []
        for point in d.get('points', []) if isinstance(d.get('points'), list) else []:
            if isinstance(point, (list, tuple)) and len(point) == 2:
                points.append([float(point[0]), float(point[1])])
        raw_segments = d.get('segments', [])
        segments = [dict(item) for item in raw_segments if isinstance(item, dict)] if isinstance(raw_segments, list) else []
        return cls(str(d.get('id', '')), str(d.get('name', '')), str(d.get('type', 'line')),
                   points, str(d.get('color', '#1F6FAE')), max(1, min(20, int(d.get('width', 4) or 4))), segments,
                   str(d.get('background_color', '#1F6FAE38')),
                   str(d.get('line_style', 'solid')))

    def to_dict(self) -> Dict[str, Any]:
        return {'id': self.id, 'name': self.name, 'type': self.type, 'points': self.points,
                'color': self.color, 'width': self.width, 'segments': self.segments,
                'background_color': self.background_color, 'line_style': self.line_style}


@dataclass
class CustomLayer(BaseDataModel):
    FIELD_ID: ClassVar[str] = 'id'
    FIELD_NAME: ClassVar[str] = 'name'
    FIELD_ELEMENTS: ClassVar[str] = 'elements'
    FIELD_ICON: ClassVar[str] = 'icon'
    FIELD_SHOW_TITLE: ClassVar[str] = 'show_title'
    id: str
    name: str
    elements: List[CustomLayerElement]
    icon: str = ''
    show_title: bool = False

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "CustomLayer":
        elements = d.get('elements', [])
        return cls(str(d.get('id', '')), str(d.get('name', '')),
                   CustomLayerElement.from_dict_list(elements if isinstance(elements, list) else []),
                   str(d.get('icon', '') or ''), bool(d.get('show_title', False)))

    def to_dict(self) -> Dict[str, Any]:
        return {'id': self.id, 'name': self.name, 'elements': self.to_dict_list(self.elements),
                'icon': self.icon, 'show_title': self.show_title}

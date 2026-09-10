from __future__ import annotations

from dataclasses import dataclass, field
from math import isfinite
import re
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
    FIELD_HIDDEN: ClassVar[str] = 'hidden'
    FIELD_LOCKED: ClassVar[str] = 'locked'
    FIELD_NOTE: ClassVar[str] = 'note'
    FIELD_ICON: ClassVar[str] = 'icon'
    id: str
    name: str
    type: str
    points: List[List[float]]
    color: str
    width: int
    segments: List[Dict[str, Any]] = field(default_factory=list)
    background_color: str = '#1F6FAE38'
    line_style: str = 'solid'
    hidden: bool = False
    locked: bool = False
    note: str = ''
    icon: str = ''

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
                   str(d.get('line_style', 'solid')), d.get('hidden') is True, d.get('locked') is True, str(d.get('note', '')), str(d.get('icon', '')))

    def to_dict(self) -> Dict[str, Any]:
        return {'id': self.id, 'name': self.name, 'type': self.type, 'points': self.points,
                'color': self.color, 'width': self.width, 'segments': self.segments,
                'background_color': self.background_color, 'line_style': self.line_style, 'hidden': self.hidden, 'locked': self.locked, 'note': self.note, 'icon': self.icon}


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

    @classmethod
    def from_payload(cls, data: Any) -> "CustomLayer":
        """Validate untrusted API/import data before permissive legacy decoding."""
        def invalid(path: str) -> None:
            raise ValueError(f'Invalid layer data: {path}')

        def identifier(value: Any, path: str) -> None:
            if not isinstance(value, str) or not re.fullmatch(r'[A-Za-z0-9_.-]{1,128}', value):
                invalid(path)

        def point(value: Any, path: str) -> None:
            if not isinstance(value, list) or len(value) != 2:
                invalid(path)
            for coordinate, limit in zip(value, (90, 180)):
                if (type(coordinate) not in (int, float)
                        or not -limit <= coordinate <= limit
                        or not isfinite(coordinate)):
                    invalid(path)

        if not isinstance(data, dict):
            invalid('layer')
        identifier(data.get('id'), 'id')
        if not isinstance(data.get('name'), str) or not data['name'].strip():
            invalid('name')
        if not isinstance(data.get('icon', ''), str):
            invalid('icon')
        if not isinstance(data.get('show_title', False), bool):
            invalid('show_title')
        if not isinstance(data.get('elements'), list):
            invalid('elements')
        ids = set()
        for index, element in enumerate(data['elements']):
            path = f'elements[{index}]'
            if not isinstance(element, dict):
                invalid(path)
            identifier(element.get('id'), f'{path}.id')
            if element['id'] in ids:
                invalid(f'{path}.id (duplicate)')
            ids.add(element['id'])
            if not isinstance(element.get('name', ''), str):
                invalid(f'{path}.name')
            if element.get('type') not in ('line', 'route', 'area', 'point'):
                invalid(f'{path}.type')
            for flag in ('hidden', 'locked'):
                if not isinstance(element.get(flag, False), bool):
                    invalid(f'{path}.{flag}')
            points = element.get('points')
            for key, limit in (('note', 4000), ('icon', 32)):
                if not isinstance(element.get(key, ''), str) or len(element.get(key, '')) > limit:
                    invalid(f'{path}.{key}')
            if element['type'] == 'point' and (not isinstance(points, list) or len(points) != 1):
                invalid(f'{path}.points')
            minimum = 1 if element['type'] == 'point' else 3 if element['type'] == 'area' else 2
            if not isinstance(points, list) or len(points) < minimum:
                invalid(f'{path}.points')
            for point_index, value in enumerate(points):
                point(value, f'{path}.points[{point_index}]')
            if len({tuple(value) for value in points}) < minimum:
                invalid(f'{path}.points (distinct points required)')
            for key, default in (('color', '#1F6FAE'), ('background_color', '#1F6FAE38')):
                value = element.get(key, default)
                if not isinstance(value, str) or not re.fullmatch(r'#[0-9a-fA-F]{6}(?:[0-9a-fA-F]{2})?', value):
                    invalid(f'{path}.{key}')
            width = element.get('width', 4)
            if type(width) is not int or not 1 <= width <= 20:
                invalid(f'{path}.width')
            if element.get('line_style', 'solid') not in ('solid', 'dashed', 'dotted', 'double', 'dash-dot'):
                invalid(f'{path}.line_style')
            segments = element.get('segments', [])
            count = len(points) if element['type'] == 'area' else len(points) - 1
            # Old layers without segment metadata consist entirely of straight lines.
            if not isinstance(segments, list) or (segments and len(segments) != count):
                invalid(f'{path}.segments')
            for segment_index, segment in enumerate(segments):
                segment_path = f'{path}.segments[{segment_index}]'
                if not isinstance(segment, dict) or segment.get('type') not in ('line', 'curve'):
                    invalid(segment_path)
                if segment['type'] == 'curve':
                    point(segment.get('control1'), f'{segment_path}.control1')
                    point(segment.get('control2'), f'{segment_path}.control2')
                elif 'control1' in segment or 'control2' in segment:
                    invalid(segment_path)
        layer = cls.from_dict(data)
        layer.name = layer.name.strip()
        for element in layer.elements:
            if not element.segments:
                count = len(element.points) if element.type == 'area' else len(element.points) - 1
                element.segments = [{'type': 'line'} for _ in range(count)]
        return layer

    def to_dict(self) -> Dict[str, Any]:
        return {'id': self.id, 'name': self.name, 'elements': self.to_dict_list(self.elements),
                'icon': self.icon, 'show_title': self.show_title}

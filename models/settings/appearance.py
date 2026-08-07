from __future__ import annotations

from dataclasses import dataclass
from typing import Any, ClassVar, Dict, List

from core.data.base_data_model import BaseDataModel
from models.settings.color_preset import ColorPreset


@dataclass
class Appearance(BaseDataModel):
    """Stores user-selected application appearance settings."""

    # Default values
    DEFAULT_THEME: ClassVar[str] = 'light'
    DEFAULT_PRIMARY_COLOR: ClassVar[str] = ColorPreset.DEFAULT_CODE
    DEFAULT_ROUTE_POINT_COLOR: ClassVar[str] = '#1F6FAE'
    DEFAULT_ROUTE_COLOR: ClassVar[str] = '#1F6FAE'
    DEFAULT_PUBLIC_TRANSPORT_ROUTE_COLOR: ClassVar[str] = '#1F6FAE'
    DEFAULT_VEHICLE_COLORS: ClassVar[Dict[str, str]] = {
        'bus': '#1F6FAE',
        'tram': '#D73535',
        'trolley': '#10893E',
        'metro': '#704BA4',
        'train': '#C24D0F'
    }
    MAX_RECENT_COLORS: ClassVar[int] = 5
    THEMES: ClassVar[tuple[str, ...]] = ('light', 'dark')

    # Field name declarations
    FIELD_THEME: ClassVar[str] = 'theme'
    FIELD_PRIMARY_COLOR: ClassVar[str] = 'primary_color'
    FIELD_RECENT_COLORS: ClassVar[str] = 'recent_colors'
    FIELD_ROUTE_POINT_COLOR: ClassVar[str] = 'route_point_color'
    FIELD_ROUTE_COLOR: ClassVar[str] = 'route_color'
    FIELD_PUBLIC_TRANSPORT_ROUTE_COLOR: ClassVar[str] = 'public_transport_route_color'
    FIELD_VEHICLE_COLORS: ClassVar[str] = 'vehicle_colors'

    # Fields
    theme: str
    primary_color: str
    recent_colors: List[str]
    route_point_color: str
    route_color: str
    public_transport_route_color: str
    vehicle_colors: Dict[str, str]

    #region Serialization

    @classmethod
    def _theme(cls, value: Any) -> str:
        """Returns a supported theme identifier."""
        theme = str(value or '').strip().lower()
        return theme if theme in cls.THEMES else cls.DEFAULT_THEME

    @classmethod
    def _recent_colors(cls, value: Any) -> List[str]:
        """Normalizes, deduplicates and limits recently used colors."""
        if not isinstance(value, list):
            return []
        colors: List[str] = []
        for item in value:
            if not ColorPreset.is_valid_code(item):
                continue
            code = ColorPreset.normalize_code(item)
            if code not in colors:
                colors.append(code)
        return colors[:cls.MAX_RECENT_COLORS]

    @classmethod
    def _color(cls, value: Any, default: str) -> str:
        """Returns a normalized color or the field-specific default."""
        return (
            ColorPreset.normalize_code(value)
            if ColorPreset.is_valid_code(value)
            else default
        )

    @classmethod
    def _vehicle_colors(cls, value: Any) -> Dict[str, str]:
        """Returns colors for every supported public transport vehicle type."""
        source = value if isinstance(value, dict) else {}
        return {
            vehicle_type: cls._color(source.get(vehicle_type), default)
            for vehicle_type, default in cls.DEFAULT_VEHICLE_COLORS.items()
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> Appearance:
        """Deserializes appearance settings from a dictionary."""
        return cls(
            theme=cls._theme(d.get(cls.FIELD_THEME)),
            primary_color=ColorPreset.normalize_code(
                d.get(cls.FIELD_PRIMARY_COLOR)
            ),
            recent_colors=cls._recent_colors(
                d.get(cls.FIELD_RECENT_COLORS, [])
            ),
            route_point_color=cls._color(
                d.get(cls.FIELD_ROUTE_POINT_COLOR), cls.DEFAULT_ROUTE_POINT_COLOR
            ),
            route_color=cls._color(
                d.get(cls.FIELD_ROUTE_COLOR), cls.DEFAULT_ROUTE_COLOR
            ),
            public_transport_route_color=cls._color(
                d.get(cls.FIELD_PUBLIC_TRANSPORT_ROUTE_COLOR),
                cls.DEFAULT_PUBLIC_TRANSPORT_ROUTE_COLOR
            ),
            vehicle_colors=cls._vehicle_colors(d.get(cls.FIELD_VEHICLE_COLORS))
        )

    def to_dict(self) -> Dict[str, Any]:
        """Serializes appearance settings to a dictionary."""
        return {
            self.FIELD_THEME: self.theme,
            self.FIELD_PRIMARY_COLOR: self.primary_color,
            self.FIELD_RECENT_COLORS: list(self.recent_colors),
            self.FIELD_ROUTE_POINT_COLOR: self.route_point_color,
            self.FIELD_ROUTE_COLOR: self.route_color,
            self.FIELD_PUBLIC_TRANSPORT_ROUTE_COLOR: self.public_transport_route_color,
            self.FIELD_VEHICLE_COLORS: dict(self.vehicle_colors)
        }

    #endregion Serialization

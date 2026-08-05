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
    MAX_RECENT_COLORS: ClassVar[int] = 5
    THEMES: ClassVar[tuple[str, ...]] = ('light', 'dark')

    # Field name declarations
    FIELD_THEME: ClassVar[str] = 'theme'
    FIELD_PRIMARY_COLOR: ClassVar[str] = 'primary_color'
    FIELD_RECENT_COLORS: ClassVar[str] = 'recent_colors'

    # Fields
    theme: str
    primary_color: str
    recent_colors: List[str]

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
    def from_dict(cls, d: Dict[str, Any]) -> Appearance:
        """Deserializes appearance settings from a dictionary."""
        return cls(
            theme=cls._theme(d.get(cls.FIELD_THEME)),
            primary_color=ColorPreset.normalize_code(
                d.get(cls.FIELD_PRIMARY_COLOR)
            ),
            recent_colors=cls._recent_colors(
                d.get(cls.FIELD_RECENT_COLORS, [])
            )
        )

    def to_dict(self) -> Dict[str, Any]:
        """Serializes appearance settings to a dictionary."""
        return {
            self.FIELD_THEME: self.theme,
            self.FIELD_PRIMARY_COLOR: self.primary_color,
            self.FIELD_RECENT_COLORS: list(self.recent_colors)
        }

    #endregion Serialization

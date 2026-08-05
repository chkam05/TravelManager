from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, ClassVar, Dict

from core.data.base_data_model import BaseDataModel


@dataclass
class ColorPreset(BaseDataModel):
    """Stores one named color available in the appearance picker."""

    # Default values
    DEFAULT_CODE: ClassVar[str] = '#1F6FAE'

    # Field name declarations
    FIELD_CODE: ClassVar[str] = 'code'
    FIELD_NAME_EN: ClassVar[str] = 'name_en'
    FIELD_NAME_PL: ClassVar[str] = 'name_pl'

    # Fields
    code: str
    name_en: str
    name_pl: str

    #region Serialization

    @staticmethod
    def is_valid_code(value: Any) -> bool:
        """Checks whether a value is a six-digit HEX color."""
        return bool(re.fullmatch(r'#[0-9A-Fa-f]{6}', str(value or '').strip()))

    @classmethod
    def normalize_code(cls, value: Any) -> str:
        """Returns an uppercase six-digit HEX color or the default color."""
        code = str(value or '').strip().upper()
        if cls.is_valid_code(code):
            return code
        return cls.DEFAULT_CODE

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> ColorPreset:
        """Deserializes a color preset from a dictionary."""
        return cls(
            code=cls.normalize_code(d.get(cls.FIELD_CODE)),
            name_en=str(d.get(cls.FIELD_NAME_EN) or ''),
            name_pl=str(d.get(cls.FIELD_NAME_PL) or '')
        )

    def to_dict(self) -> Dict[str, Any]:
        """Serializes the color preset to a dictionary."""
        return {
            self.FIELD_CODE: self.code,
            self.FIELD_NAME_EN: self.name_en,
            self.FIELD_NAME_PL: self.name_pl
        }

    #endregion Serialization

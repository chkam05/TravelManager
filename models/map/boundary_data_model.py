from __future__ import annotations
from dataclasses import dataclass
from typing import Any, ClassVar, Dict

from core.data.base_data_model import BaseDataModel


@dataclass
class BoundaryDataModel(BaseDataModel):
    """Stores OpenStreetMap tag values defined by OpenStreetMap PrimaryFeaturesAttr.BoundaryAttr."""

    # Default values
    _DEFAULT_VALUE: ClassVar[Any] = None

    # Field name declarations
    FIELD_ADMIN_LEVEL: ClassVar[str] = 'admin_level'
    FIELD_RELIGIOUS_LEVEL: ClassVar[str] = 'religious_level'
    FIELD_BORDER_TYPE: ClassVar[str] = 'border_type'
    FIELD_START_DATE: ClassVar[str] = 'start_date'

    # OpenStreetMap tag declarations
    TAG_ADMIN_LEVEL: ClassVar[str] = 'admin_level'
    TAG_RELIGIOUS_LEVEL: ClassVar[str] = 'religious_level'
    TAG_BORDER_TYPE: ClassVar[str] = 'border_type'
    TAG_START_DATE: ClassVar[str] = 'start_date'

    # Fields
    admin_level: Any | None
    religious_level: Any | None
    border_type: Any | None
    start_date: Any | None

    #region Serialization

    @classmethod
    def _get_value(cls, d: Dict[str, Any], field_name: str, tag_name: str) -> Any:
        """Gets a value by local field name or by the real OpenStreetMap tag key."""
        return d.get(tag_name, d.get(field_name, cls._DEFAULT_VALUE))

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> BoundaryDataModel:
        """Deserializes data from a dictionary in "attribute:value" format to an object."""
        return cls(
            admin_level=cls._get_value(d, cls.FIELD_ADMIN_LEVEL, cls.TAG_ADMIN_LEVEL),
            religious_level=cls._get_value(d, cls.FIELD_RELIGIOUS_LEVEL, cls.TAG_RELIGIOUS_LEVEL),
            border_type=cls._get_value(d, cls.FIELD_BORDER_TYPE, cls.TAG_BORDER_TYPE),
            start_date=cls._get_value(d, cls.FIELD_START_DATE, cls.TAG_START_DATE)
        )

    def to_dict(self) -> Dict[str, Any]:
        """Serializes object to a dictionary in the format "attribute:value"."""
        return {
            self.TAG_ADMIN_LEVEL: self.admin_level,
            self.TAG_RELIGIOUS_LEVEL: self.religious_level,
            self.TAG_BORDER_TYPE: self.border_type,
            self.TAG_START_DATE: self.start_date
        }

    #endregion Serialization

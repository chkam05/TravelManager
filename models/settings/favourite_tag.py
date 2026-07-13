from __future__ import annotations

from dataclasses import dataclass
from typing import Any, ClassVar, Dict

from core.data.base_data_model import BaseDataModel


@dataclass
class FavouriteTag(BaseDataModel):
    """Stores a favourite place tag used to describe and render map markers."""

    # Default values
    DEFAULT_TAG_ID: ClassVar[str] = 'default'
    DEFAULT_NAME: ClassVar[str] = 'Ulubione'
    DEFAULT_ICON: ClassVar[str] = '⭐'

    # Field name declarations
    FIELD_ID: ClassVar[str] = 'id'
    FIELD_NAME: ClassVar[str] = 'name'
    FIELD_ICON: ClassVar[str] = 'icon'

    # Fields
    id: str
    name: str
    icon: str

    #region Defaults

    @classmethod
    def default(cls) -> FavouriteTag:
        """Returns the default favourite tag."""
        return cls(
            id=cls.DEFAULT_TAG_ID,
            name=cls.DEFAULT_NAME,
            icon=cls.DEFAULT_ICON
        )

    #endregion Defaults

    #region Serialization

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> FavouriteTag:
        """Deserializes favourite tag data from a dictionary."""
        return cls(
            id=str(d.get(cls.FIELD_ID, '')),
            name=str(d.get(cls.FIELD_NAME, '')),
            icon=str(d.get(cls.FIELD_ICON, cls.DEFAULT_ICON) or cls.DEFAULT_ICON)
        )

    def to_dict(self) -> Dict[str, Any]:
        """Serializes favourite tag data to a dictionary."""
        return {
            self.FIELD_ID: self.id,
            self.FIELD_NAME: self.name,
            self.FIELD_ICON: self.icon
        }

    #endregion Serialization

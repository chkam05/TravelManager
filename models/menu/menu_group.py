from __future__ import annotations

from dataclasses import dataclass
from typing import Any, ClassVar, Dict

from core.data.base_data_model import BaseDataModel


@dataclass
class MenuGroup(BaseDataModel):
    """Describes a section used to group navigation items."""

    # Field name declarations
    FIELD_ID: ClassVar[str] = 'id'
    FIELD_NAME_KEY: ClassVar[str] = 'name_key'
    FIELD_DESCRIPTION_KEY: ClassVar[str] = 'description_key'
    FIELD_HOME_INDEX: ClassVar[str] = 'home_index'
    FIELD_MENU_INDEX: ClassVar[str] = 'menu_index'

    # Fields
    id: int
    name_key: str
    description_key: str
    home_index: int
    menu_index: int

    #region Serialization

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> MenuGroup:
        return cls(
            id=int(d.get(cls.FIELD_ID, 0)),
            name_key=str(d.get(cls.FIELD_NAME_KEY, '')),
            description_key=str(d.get(cls.FIELD_DESCRIPTION_KEY, '')),
            home_index=int(d.get(cls.FIELD_HOME_INDEX, 0)),
            menu_index=int(d.get(cls.FIELD_MENU_INDEX, 0))
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            self.FIELD_ID: self.id,
            self.FIELD_NAME_KEY: self.name_key,
            self.FIELD_DESCRIPTION_KEY: self.description_key,
            self.FIELD_HOME_INDEX: self.home_index,
            self.FIELD_MENU_INDEX: self.menu_index
        }

    #endregion Serialization

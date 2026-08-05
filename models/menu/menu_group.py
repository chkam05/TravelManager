from __future__ import annotations

from dataclasses import dataclass
from typing import Any, ClassVar, Dict

from core.data.base_data_model import BaseDataModel


@dataclass
class MenuGroup(BaseDataModel):
    """Describes a section used to group navigation items."""

    # Field name declarations
    FIELD_ID: ClassVar[str] = 'id'
    FIELD_NAME: ClassVar[str] = 'name'
    FIELD_DESCRIPTION: ClassVar[str] = 'description'
    FIELD_HOME_INDEX: ClassVar[str] = 'home_index'
    FIELD_MENU_INDEX: ClassVar[str] = 'menu_index'

    # Fields
    id: int
    name: str
    description: str
    home_index: int
    menu_index: int

    #region Serialization

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> MenuGroup:
        return cls(
            id=int(d.get(cls.FIELD_ID, 0)),
            name=str(d.get(cls.FIELD_NAME, '')),
            description=str(d.get(cls.FIELD_DESCRIPTION, '')),
            home_index=int(d.get(cls.FIELD_HOME_INDEX, 0)),
            menu_index=int(d.get(cls.FIELD_MENU_INDEX, 0))
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            self.FIELD_ID: self.id,
            self.FIELD_NAME: self.name,
            self.FIELD_DESCRIPTION: self.description,
            self.FIELD_HOME_INDEX: self.home_index,
            self.FIELD_MENU_INDEX: self.menu_index
        }

    #endregion Serialization

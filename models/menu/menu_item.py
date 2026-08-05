from __future__ import annotations

from dataclasses import dataclass
from typing import Any, ClassVar, Dict

from core.data.base_data_model import BaseDataModel


@dataclass
class MenuItem(BaseDataModel):
    """Describes one navigation item shared by the menu and home view."""

    # Field name declarations
    FIELD_ICON: ClassVar[str] = 'icon'
    FIELD_NAME: ClassVar[str] = 'name'
    FIELD_DESCRIPTION: ClassVar[str] = 'description'
    FIELD_URL: ClassVar[str] = 'url'
    FIELD_HOME_GROUP_ID: ClassVar[str] = 'home_group_id'
    FIELD_MENU_GROUP_ID: ClassVar[str] = 'menu_group_id'

    # Fields
    icon: str
    name: str
    description: str
    url: str
    home_group_id: int
    menu_group_id: int

    #region Serialization

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> MenuItem:
        return cls(
            icon=str(d.get(cls.FIELD_ICON, 'circle')),
            name=str(d.get(cls.FIELD_NAME, '')),
            description=str(d.get(cls.FIELD_DESCRIPTION, '')),
            url=str(d.get(cls.FIELD_URL, '')),
            home_group_id=int(d.get(cls.FIELD_HOME_GROUP_ID, 0)),
            menu_group_id=int(d.get(cls.FIELD_MENU_GROUP_ID, 0))
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            self.FIELD_ICON: self.icon,
            self.FIELD_NAME: self.name,
            self.FIELD_DESCRIPTION: self.description,
            self.FIELD_URL: self.url,
            self.FIELD_HOME_GROUP_ID: self.home_group_id,
            self.FIELD_MENU_GROUP_ID: self.menu_group_id
        }

    #endregion Serialization

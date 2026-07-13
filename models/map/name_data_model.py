from __future__ import annotations
from dataclasses import dataclass
from typing import Any, ClassVar, Dict

from core.data.base_data_model import BaseDataModel


@dataclass
class NameDataModel(BaseDataModel):
    """Stores OpenStreetMap tag values defined by OpenStreetMap NameAttr."""

    # Default values
    _DEFAULT_VALUE: ClassVar[Any] = None

    # Field name declarations
    FIELD_NAME: ClassVar[str] = 'name'
    FIELD_NAME_LEFT: ClassVar[str] = 'name_left'
    FIELD_NAME_RIGHT: ClassVar[str] = 'name_right'
    FIELD_INT_NAME: ClassVar[str] = 'int_name'
    FIELD_LOC_NAME: ClassVar[str] = 'loc_name'
    FIELD_NAT_NAME: ClassVar[str] = 'nat_name'
    FIELD_OFFICIAL_NAME: ClassVar[str] = 'official_name'
    FIELD_OLD_NAME: ClassVar[str] = 'old_name'
    FIELD_REF_NAME: ClassVar[str] = 'ref_name'
    FIELD_REG_NAME: ClassVar[str] = 'reg_name'
    FIELD_SHORT_NAME: ClassVar[str] = 'short_name'
    FIELD_FULL_NAME: ClassVar[str] = 'full_name'
    FIELD_SORTING_NAME: ClassVar[str] = 'sorting_name'
    FIELD_ALT_NAME: ClassVar[str] = 'alt_name'
    FIELD_NICKNAME: ClassVar[str] = 'nickname'
    FIELD_PROPOSED_NAME: ClassVar[str] = 'proposed_name'
    FIELD_NAME_1: ClassVar[str] = 'name_1'
    FIELD_NAME_2: ClassVar[str] = 'name_2'
    FIELD_BRIDGE_NAME: ClassVar[str] = 'bridge_name'
    FIELD_TUNNEL_NAME: ClassVar[str] = 'tunnel_name'

    # OpenStreetMap tag declarations
    TAG_NAME: ClassVar[str] = 'name'
    TAG_NAME_LEFT: ClassVar[str] = 'name:left'
    TAG_NAME_RIGHT: ClassVar[str] = 'name:right'
    TAG_INT_NAME: ClassVar[str] = 'int_name'
    TAG_LOC_NAME: ClassVar[str] = 'loc_name'
    TAG_NAT_NAME: ClassVar[str] = 'nat_name'
    TAG_OFFICIAL_NAME: ClassVar[str] = 'official_name'
    TAG_OLD_NAME: ClassVar[str] = 'old_name'
    TAG_REF_NAME: ClassVar[str] = 'ref_name'
    TAG_REG_NAME: ClassVar[str] = 'reg_name'
    TAG_SHORT_NAME: ClassVar[str] = 'short_name'
    TAG_FULL_NAME: ClassVar[str] = 'full_name'
    TAG_SORTING_NAME: ClassVar[str] = 'sorting_name'
    TAG_ALT_NAME: ClassVar[str] = 'alt_name'
    TAG_NICKNAME: ClassVar[str] = 'nickname'
    TAG_PROPOSED_NAME: ClassVar[str] = 'proposed:name'
    TAG_NAME_1: ClassVar[str] = 'name_1'
    TAG_NAME_2: ClassVar[str] = 'name_2'
    TAG_BRIDGE_NAME: ClassVar[str] = 'bridge:name'
    TAG_TUNNEL_NAME: ClassVar[str] = 'tunnel:name'

    # Fields
    name: Any | None
    name_left: Any | None
    name_right: Any | None
    int_name: Any | None
    loc_name: Any | None
    nat_name: Any | None
    official_name: Any | None
    old_name: Any | None
    ref_name: Any | None
    reg_name: Any | None
    short_name: Any | None
    full_name: Any | None
    sorting_name: Any | None
    alt_name: Any | None
    nickname: Any | None
    proposed_name: Any | None
    name_1: Any | None
    name_2: Any | None
    bridge_name: Any | None
    tunnel_name: Any | None

    #region Serialization

    @classmethod
    def _get_value(cls, d: Dict[str, Any], field_name: str, tag_name: str) -> Any:
        """Gets a value by local field name or by the real OpenStreetMap tag key."""
        return d.get(tag_name, d.get(field_name, cls._DEFAULT_VALUE))

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> NameDataModel:
        """Deserializes data from a dictionary in "attribute:value" format to an object."""
        return cls(
            name=cls._get_value(d, cls.FIELD_NAME, cls.TAG_NAME),
            name_left=cls._get_value(d, cls.FIELD_NAME_LEFT, cls.TAG_NAME_LEFT),
            name_right=cls._get_value(d, cls.FIELD_NAME_RIGHT, cls.TAG_NAME_RIGHT),
            int_name=cls._get_value(d, cls.FIELD_INT_NAME, cls.TAG_INT_NAME),
            loc_name=cls._get_value(d, cls.FIELD_LOC_NAME, cls.TAG_LOC_NAME),
            nat_name=cls._get_value(d, cls.FIELD_NAT_NAME, cls.TAG_NAT_NAME),
            official_name=cls._get_value(d, cls.FIELD_OFFICIAL_NAME, cls.TAG_OFFICIAL_NAME),
            old_name=cls._get_value(d, cls.FIELD_OLD_NAME, cls.TAG_OLD_NAME),
            ref_name=cls._get_value(d, cls.FIELD_REF_NAME, cls.TAG_REF_NAME),
            reg_name=cls._get_value(d, cls.FIELD_REG_NAME, cls.TAG_REG_NAME),
            short_name=cls._get_value(d, cls.FIELD_SHORT_NAME, cls.TAG_SHORT_NAME),
            full_name=cls._get_value(d, cls.FIELD_FULL_NAME, cls.TAG_FULL_NAME),
            sorting_name=cls._get_value(d, cls.FIELD_SORTING_NAME, cls.TAG_SORTING_NAME),
            alt_name=cls._get_value(d, cls.FIELD_ALT_NAME, cls.TAG_ALT_NAME),
            nickname=cls._get_value(d, cls.FIELD_NICKNAME, cls.TAG_NICKNAME),
            proposed_name=cls._get_value(d, cls.FIELD_PROPOSED_NAME, cls.TAG_PROPOSED_NAME),
            name_1=cls._get_value(d, cls.FIELD_NAME_1, cls.TAG_NAME_1),
            name_2=cls._get_value(d, cls.FIELD_NAME_2, cls.TAG_NAME_2),
            bridge_name=cls._get_value(d, cls.FIELD_BRIDGE_NAME, cls.TAG_BRIDGE_NAME),
            tunnel_name=cls._get_value(d, cls.FIELD_TUNNEL_NAME, cls.TAG_TUNNEL_NAME)
        )

    def to_dict(self) -> Dict[str, Any]:
        """Serializes object to a dictionary in the format "attribute:value"."""
        return {
            self.TAG_NAME: self.name,
            self.TAG_NAME_LEFT: self.name_left,
            self.TAG_NAME_RIGHT: self.name_right,
            self.TAG_INT_NAME: self.int_name,
            self.TAG_LOC_NAME: self.loc_name,
            self.TAG_NAT_NAME: self.nat_name,
            self.TAG_OFFICIAL_NAME: self.official_name,
            self.TAG_OLD_NAME: self.old_name,
            self.TAG_REF_NAME: self.ref_name,
            self.TAG_REG_NAME: self.reg_name,
            self.TAG_SHORT_NAME: self.short_name,
            self.TAG_FULL_NAME: self.full_name,
            self.TAG_SORTING_NAME: self.sorting_name,
            self.TAG_ALT_NAME: self.alt_name,
            self.TAG_NICKNAME: self.nickname,
            self.TAG_PROPOSED_NAME: self.proposed_name,
            self.TAG_NAME_1: self.name_1,
            self.TAG_NAME_2: self.name_2,
            self.TAG_BRIDGE_NAME: self.bridge_name,
            self.TAG_TUNNEL_NAME: self.tunnel_name
        }

    #endregion Serialization

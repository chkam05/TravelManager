from __future__ import annotations
from dataclasses import dataclass
from typing import Any, ClassVar, Dict

from core.data.base_data_model import BaseDataModel
from resources.public_transport.public_transport_type import PublicTransportType


@dataclass(unsafe_hash=True)
class PublicTransportBaseLine(BaseDataModel):
    """Stores a public transport line available from a provider."""

    # Default values
    _DEFAULT_TYPE: ClassVar[PublicTransportType] = PublicTransportType.BUS

    # Field name declarations
    FIELD_LINE: ClassVar[str] = 'line'
    FIELD_TYPE: ClassVar[str] = 'type'
    FIELD_URL: ClassVar[str] = 'url'
    FIELD_FREE_OF_CHARGE: ClassVar[str] = 'free_of_charge'
    FIELD_UPDATED: ClassVar[str] = 'updated'
    FIELD_DIRECTION: ClassVar[str] = 'direction'
    FIELD_SORT_NAME: ClassVar[str] = 'sort_name'

    # Fields
    line: str
    type: PublicTransportType
    url: str
    free_of_charge: bool
    updated: bool
    direction: str = ''
    sort_name: str = ''

    #region Serialization

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> PublicTransportBaseLine:
        """Deserializes data from a dictionary in "attribute:value" format to an object."""
        try:
            transport_type = PublicTransportType.from_str(
                str(d.get(cls.FIELD_TYPE) or cls._DEFAULT_TYPE)
            )
        except ValueError:
            transport_type = cls._DEFAULT_TYPE
        return cls(
            line=str(d.get(cls.FIELD_LINE) or ''),
            type=transport_type,
            url=str(d.get(cls.FIELD_URL) or ''),
            free_of_charge=bool(d.get(cls.FIELD_FREE_OF_CHARGE, False)),
            updated=bool(d.get(cls.FIELD_UPDATED, False)),
            direction=str(d.get(cls.FIELD_DIRECTION) or ''),
            sort_name=str(d.get(cls.FIELD_SORT_NAME) or '')
        )

    def to_dict(self) -> Dict[str, Any]:
        """Serializes object to a dictionary in the format "attribute:value"."""
        return {
            self.FIELD_LINE: self.line,
            self.FIELD_TYPE: str(self.type),
            self.FIELD_URL: self.url,
            self.FIELD_FREE_OF_CHARGE: self.free_of_charge,
            self.FIELD_UPDATED: self.updated,
            self.FIELD_DIRECTION: self.direction,
            self.FIELD_SORT_NAME: self.sort_name
        }

    #endregion Serialization

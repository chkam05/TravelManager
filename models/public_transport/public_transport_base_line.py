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

    # Fields
    line: str
    type: PublicTransportType
    url: str
    free_of_charge: bool
    updated: bool

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
            updated=bool(d.get(cls.FIELD_UPDATED, False))
        )

    def to_dict(self) -> Dict[str, Any]:
        """Serializes object to a dictionary in the format "attribute:value"."""
        return {
            self.FIELD_LINE: self.line,
            self.FIELD_TYPE: str(self.type),
            self.FIELD_URL: self.url,
            self.FIELD_FREE_OF_CHARGE: self.free_of_charge,
            self.FIELD_UPDATED: self.updated
        }

    #endregion Serialization

from __future__ import annotations
from dataclasses import dataclass
from typing import Any, ClassVar, Dict

from core.data.base_data_model import BaseDataModel
from models.public_transport.public_transport_city import PublicTransportCity
from resources.public_transport.public_transport_type import PublicTransportType


@dataclass
class PublicTransportDirectionStop(BaseDataModel):
    """Stores a stop on one direction of a public transport line."""

    # Default values
    _DEFAULT_TYPE: ClassVar[PublicTransportType] = PublicTransportType.BUS

    # Field name declarations
    FIELD_LINE: ClassVar[str] = 'line'
    FIELD_TYPE: ClassVar[str] = 'type'
    FIELD_CITY: ClassVar[str] = 'city'
    FIELD_IS_VARIANT: ClassVar[str] = 'is_variant'
    FIELD_NAME: ClassVar[str] = 'name'
    FIELD_PLATFORM: ClassVar[str] = 'platform'
    FIELD_URL: ClassVar[str] = 'url'

    # Fields
    line: str
    type: PublicTransportType
    city: PublicTransportCity
    is_variant: bool
    name: str
    platform: str
    url: str

    #region Serialization

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> PublicTransportDirectionStop:
        """Deserializes data from a dictionary in "attribute:value" format to an object."""
        city = d.get(cls.FIELD_CITY, {})
        try:
            transport_type = PublicTransportType.from_str(
                str(d.get(cls.FIELD_TYPE) or cls._DEFAULT_TYPE)
            )
        except ValueError:
            transport_type = cls._DEFAULT_TYPE
        return cls(
            line=str(d.get(cls.FIELD_LINE) or ''),
            type=transport_type,
            city=PublicTransportCity.from_dict(city if isinstance(city, dict) else {}),
            is_variant=bool(d.get(cls.FIELD_IS_VARIANT, False)),
            name=str(d.get(cls.FIELD_NAME) or ''),
            platform=str(d.get(cls.FIELD_PLATFORM) or ''),
            url=str(d.get(cls.FIELD_URL) or '')
        )

    def to_dict(self) -> Dict[str, Any]:
        """Serializes object to a dictionary in the format "attribute:value"."""
        return {
            self.FIELD_LINE: self.line,
            self.FIELD_TYPE: str(self.type),
            self.FIELD_CITY: self.city.to_dict(),
            self.FIELD_IS_VARIANT: self.is_variant,
            self.FIELD_NAME: self.name,
            self.FIELD_PLATFORM: self.platform,
            self.FIELD_URL: self.url
        }

    #endregion Serialization

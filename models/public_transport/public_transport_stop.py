from __future__ import annotations
from dataclasses import dataclass
from typing import Any, ClassVar, Dict, List

from core.data.base_data_model import BaseDataModel
from models.public_transport.public_transport_city import PublicTransportCity
from models.public_transport.public_transport_stop_platform import PublicTransportStopPlatform


@dataclass
class PublicTransportStop(BaseDataModel):
    """Stores a named stop and its typed platform list."""

    # Field name declarations
    FIELD_NAME: ClassVar[str] = 'name'
    FIELD_CITY: ClassVar[str] = 'city'
    FIELD_PLATFORMS: ClassVar[str] = 'platforms'

    # Fields
    name: str
    city: PublicTransportCity
    platforms: List[PublicTransportStopPlatform]

    #region Serialization

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> PublicTransportStop:
        """Deserializes data from a dictionary in "attribute:value" format to an object."""
        city = d.get(cls.FIELD_CITY, {})
        platforms = d.get(cls.FIELD_PLATFORMS, [])
        return cls(
            name=str(d.get(cls.FIELD_NAME) or ''),
            city=PublicTransportCity.from_dict(city if isinstance(city, dict) else {}),
            platforms=PublicTransportStopPlatform.from_dict_list(
                platforms if isinstance(platforms, list) else []
            )
        )

    def to_dict(self) -> Dict[str, Any]:
        """Serializes object to a dictionary in the format "attribute:value"."""
        return {
            self.FIELD_NAME: self.name,
            self.FIELD_CITY: self.city.to_dict(),
            self.FIELD_PLATFORMS: self.to_dict_list(self.platforms)
        }

    #endregion Serialization

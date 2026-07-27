from __future__ import annotations
from dataclasses import dataclass
from datetime import time
from typing import Any, ClassVar, Dict

from core.data.base_data_model import BaseDataModel
from models.public_transport.model_serialization import parse_time


@dataclass
class PublicTransportDepartureTime(BaseDataModel):
    """Stores one scheduled departure from a stop."""

    # Field name declarations
    FIELD_DEPARTURE_TIME: ClassVar[str] = 'departure_time'
    FIELD_IS_HIGH_FLOOR: ClassVar[str] = 'is_high_floor'
    FIELD_URL: ClassVar[str] = 'url'
    FIELD_VARIANT: ClassVar[str] = 'variant'

    # Fields
    departure_time: time | None
    is_high_floor: bool
    url: str
    variant: str

    #region Serialization

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> PublicTransportDepartureTime:
        """Deserializes data from a dictionary in "attribute:value" format to an object."""
        return cls(
            departure_time=parse_time(d.get(cls.FIELD_DEPARTURE_TIME)),
            is_high_floor=bool(d.get(cls.FIELD_IS_HIGH_FLOOR, False)),
            url=str(d.get(cls.FIELD_URL) or ''),
            variant=str(d.get(cls.FIELD_VARIANT) or '')
        )

    def to_dict(self) -> Dict[str, Any]:
        """Serializes object to a dictionary in the format "attribute:value"."""
        return {
            self.FIELD_DEPARTURE_TIME: (
                self.departure_time.isoformat(timespec='minutes')
                if self.departure_time else None
            ),
            self.FIELD_IS_HIGH_FLOOR: self.is_high_floor,
            self.FIELD_URL: self.url,
            self.FIELD_VARIANT: self.variant
        }

    #endregion Serialization

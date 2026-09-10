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
    FIELD_SCHEDULED_DEPARTURE_TIME: ClassVar[str] = 'scheduled_departure_time'
    FIELD_DELAY_MINUTES: ClassVar[str] = 'delay_minutes'
    FIELD_CANCELLED: ClassVar[str] = 'cancelled'
    FIELD_REALTIME_UPDATED_AT: ClassVar[str] = 'realtime_updated_at'
    FIELD_REALTIME_STALE: ClassVar[str] = 'realtime_stale'

    # Fields
    departure_time: time | None
    is_high_floor: bool
    url: str
    variant: str
    scheduled_departure_time: time | None = None
    delay_minutes: int | None = None
    cancelled: bool = False
    realtime_updated_at: str = ''
    realtime_stale: bool = False

    #region Serialization

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> PublicTransportDepartureTime:
        """Deserializes data from a dictionary in "attribute:value" format to an object."""
        return cls(
            departure_time=parse_time(d.get(cls.FIELD_DEPARTURE_TIME)),
            is_high_floor=bool(d.get(cls.FIELD_IS_HIGH_FLOOR, False)),
            url=str(d.get(cls.FIELD_URL) or ''),
            variant=str(d.get(cls.FIELD_VARIANT) or ''),
            scheduled_departure_time=parse_time(d.get(cls.FIELD_SCHEDULED_DEPARTURE_TIME)),
            delay_minutes=(int(d[cls.FIELD_DELAY_MINUTES])
                           if d.get(cls.FIELD_DELAY_MINUTES) is not None else None),
            cancelled=bool(d.get(cls.FIELD_CANCELLED, False)),
            realtime_updated_at=str(d.get(cls.FIELD_REALTIME_UPDATED_AT) or ''),
            realtime_stale=bool(d.get(cls.FIELD_REALTIME_STALE, False))
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
            self.FIELD_VARIANT: self.variant,
            self.FIELD_SCHEDULED_DEPARTURE_TIME: (
                self.scheduled_departure_time.isoformat(timespec='minutes')
                if self.scheduled_departure_time else None
            ),
            self.FIELD_DELAY_MINUTES: self.delay_minutes,
            self.FIELD_CANCELLED: self.cancelled,
            self.FIELD_REALTIME_UPDATED_AT: self.realtime_updated_at,
            self.FIELD_REALTIME_STALE: self.realtime_stale
        }

    #endregion Serialization

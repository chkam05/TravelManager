from __future__ import annotations
from dataclasses import dataclass
from datetime import time
from typing import Any, ClassVar, Dict, List

from core.data.base_data_model import BaseDataModel
from models.public_transport.model_serialization import parse_coordinate, parse_time
from models.public_transport.public_transport_city import PublicTransportCity
from models.public_transport.public_transport_ride_stop import PublicTransportRideStop
from resources.public_transport.public_transport_type import PublicTransportType


@dataclass
class PublicTransportRide(BaseDataModel):
    """Stores the complete stop sequence and metadata for one ride."""

    # Default values
    _DEFAULT_TYPE: ClassVar[PublicTransportType] = PublicTransportType.BUS

    # Field name declarations
    FIELD_LINE: ClassVar[str] = 'line'
    FIELD_TYPE: ClassVar[str] = 'type'
    FIELD_STOP_NAME: ClassVar[str] = 'stop_name'
    FIELD_PLATFORM: ClassVar[str] = 'platform'
    FIELD_DEPARTURE_TIME: ClassVar[str] = 'departure_time'
    FIELD_CITIES: ClassVar[str] = 'cities'
    FIELD_NEXT_STOPS: ClassVar[str] = 'next_stops'
    FIELD_CARRIER: ClassVar[str] = 'carrier'
    FIELD_VEHICLE_TYPE: ClassVar[str] = 'vehicle_type'
    FIELD_LATITUDE: ClassVar[str] = 'latitude'
    FIELD_LONGITUDE: ClassVar[str] = 'longitude'
    FIELD_SCHEDULED_DEPARTURE_TIME: ClassVar[str] = 'scheduled_departure_time'
    FIELD_DELAY_MINUTES: ClassVar[str] = 'delay_minutes'
    FIELD_CANCELLED: ClassVar[str] = 'cancelled'
    FIELD_REALTIME_UPDATED_AT: ClassVar[str] = 'realtime_updated_at'
    FIELD_REALTIME_STALE: ClassVar[str] = 'realtime_stale'

    # Fields
    line: str
    type: PublicTransportType
    stop_name: str
    platform: str
    departure_time: time | None
    cities: List[PublicTransportCity]
    next_stops: List[PublicTransportRideStop]
    carrier: str
    vehicle_type: str
    latitude: float | None
    longitude: float | None
    scheduled_departure_time: time | None = None
    delay_minutes: int | None = None
    cancelled: bool = False
    realtime_updated_at: str = ''
    realtime_stale: bool = False

    #region Serialization

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> PublicTransportRide:
        """Deserializes data from a dictionary in "attribute:value" format to an object."""
        cities = d.get(cls.FIELD_CITIES, [])
        next_stops = d.get(cls.FIELD_NEXT_STOPS, [])
        try:
            transport_type = PublicTransportType.from_str(
                str(d.get(cls.FIELD_TYPE) or cls._DEFAULT_TYPE)
            )
        except ValueError:
            transport_type = cls._DEFAULT_TYPE
        return cls(
            line=str(d.get(cls.FIELD_LINE) or ''),
            type=transport_type,
            stop_name=str(d.get(cls.FIELD_STOP_NAME) or ''),
            platform=str(d.get(cls.FIELD_PLATFORM) or ''),
            departure_time=parse_time(d.get(cls.FIELD_DEPARTURE_TIME)),
            cities=PublicTransportCity.from_dict_list(cities if isinstance(cities, list) else []),
            next_stops=PublicTransportRideStop.from_dict_list(
                next_stops if isinstance(next_stops, list) else []
            ),
            carrier=str(d.get(cls.FIELD_CARRIER) or ''),
            vehicle_type=str(d.get(cls.FIELD_VEHICLE_TYPE) or ''),
            latitude=parse_coordinate(d.get(cls.FIELD_LATITUDE), -90, 90),
            longitude=parse_coordinate(d.get(cls.FIELD_LONGITUDE), -180, 180),
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
            self.FIELD_LINE: self.line,
            self.FIELD_TYPE: str(self.type),
            self.FIELD_STOP_NAME: self.stop_name,
            self.FIELD_PLATFORM: self.platform,
            self.FIELD_DEPARTURE_TIME: (
                self.departure_time.isoformat(timespec='minutes')
                if self.departure_time else None
            ),
            self.FIELD_CITIES: self.to_dict_list(self.cities),
            self.FIELD_NEXT_STOPS: self.to_dict_list(self.next_stops),
            self.FIELD_CARRIER: self.carrier,
            self.FIELD_VEHICLE_TYPE: self.vehicle_type,
            self.FIELD_LATITUDE: self.latitude,
            self.FIELD_LONGITUDE: self.longitude,
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

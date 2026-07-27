from __future__ import annotations
from dataclasses import dataclass
from datetime import time
from typing import Any, ClassVar, Dict

from core.data.base_data_model import BaseDataModel
from models.public_transport.model_serialization import parse_coordinate, parse_time
from models.public_transport.public_transport_city import PublicTransportCity


@dataclass
class PublicTransportRideStop(BaseDataModel):
    """Stores one stop and cumulative metrics on a ride."""

    # Field name declarations
    FIELD_STOP: ClassVar[str] = 'stop'
    FIELD_DEPARTURE_TIME: ClassVar[str] = 'departure_time'
    FIELD_TRAVEL_TIME: ClassVar[str] = 'travel_time'
    FIELD_TRAVEL_TIME_SUM: ClassVar[str] = 'travel_time_sum'
    FIELD_DISTANCE: ClassVar[str] = 'distance'
    FIELD_DISTANCE_SUM: ClassVar[str] = 'distance_sum'
    FIELD_CITY: ClassVar[str] = 'city'
    FIELD_LATITUDE: ClassVar[str] = 'latitude'
    FIELD_LONGITUDE: ClassVar[str] = 'longitude'

    # Fields
    stop: str
    departure_time: time | None
    travel_time: int
    travel_time_sum: int
    distance: float
    distance_sum: float
    city: PublicTransportCity
    latitude: float | None
    longitude: float | None

    #region Serialization

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> PublicTransportRideStop:
        """Deserializes data from a dictionary in "attribute:value" format to an object."""
        city = d.get(cls.FIELD_CITY, {})
        return cls(
            stop=str(d.get(cls.FIELD_STOP) or ''),
            departure_time=parse_time(d.get(cls.FIELD_DEPARTURE_TIME)),
            travel_time=max(0, int(d.get(cls.FIELD_TRAVEL_TIME) or 0)),
            travel_time_sum=max(0, int(d.get(cls.FIELD_TRAVEL_TIME_SUM) or 0)),
            distance=max(0.0, float(d.get(cls.FIELD_DISTANCE) or 0.0)),
            distance_sum=max(0.0, float(d.get(cls.FIELD_DISTANCE_SUM) or 0.0)),
            city=PublicTransportCity.from_dict(city if isinstance(city, dict) else {}),
            latitude=parse_coordinate(d.get(cls.FIELD_LATITUDE), -90, 90),
            longitude=parse_coordinate(d.get(cls.FIELD_LONGITUDE), -180, 180)
        )

    def to_dict(self) -> Dict[str, Any]:
        """Serializes object to a dictionary in the format "attribute:value"."""
        return {
            self.FIELD_STOP: self.stop,
            self.FIELD_DEPARTURE_TIME: (
                self.departure_time.isoformat(timespec='minutes')
                if self.departure_time else None
            ),
            self.FIELD_TRAVEL_TIME: self.travel_time,
            self.FIELD_TRAVEL_TIME_SUM: self.travel_time_sum,
            self.FIELD_DISTANCE: self.distance,
            self.FIELD_DISTANCE_SUM: self.distance_sum,
            self.FIELD_CITY: self.city.to_dict(),
            self.FIELD_LATITUDE: self.latitude,
            self.FIELD_LONGITUDE: self.longitude
        }

    #endregion Serialization

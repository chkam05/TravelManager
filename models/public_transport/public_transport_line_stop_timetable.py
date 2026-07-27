from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from typing import Any, ClassVar, Dict, List

from core.data.base_data_model import BaseDataModel
from models.public_transport.model_serialization import (
    parse_date,
    parse_date_url_map,
    parse_coordinate,
    serialize_date_url_map
)
from models.public_transport.public_transport_announcement import PublicTransportAnnouncement
from models.public_transport.public_transport_date_timetable import PublicTransportDateTimetable
from resources.public_transport.public_transport_type import PublicTransportType


@dataclass
class PublicTransportLineStopTimetable(BaseDataModel):
    """Stores line departures from one stop and direction."""

    # Default values
    _DEFAULT_TYPE: ClassVar[PublicTransportType] = PublicTransportType.BUS

    # Field name declarations
    FIELD_LINE: ClassVar[str] = 'line'
    FIELD_TYPE: ClassVar[str] = 'type'
    FIELD_ANNOUNCEMENTS: ClassVar[str] = 'announcements'
    FIELD_STOP_NAME: ClassVar[str] = 'stop_name'
    FIELD_DIRECTION_NAME: ClassVar[str] = 'direction_name'
    FIELD_PLATFORM: ClassVar[str] = 'platform'
    FIELD_TIMETABLE: ClassVar[str] = 'timetable'
    FIELD_DATES: ClassVar[str] = 'dates'
    FIELD_LATITUDE: ClassVar[str] = 'latitude'
    FIELD_LONGITUDE: ClassVar[str] = 'longitude'

    # Fields
    line: str
    type: PublicTransportType
    announcements: List[PublicTransportAnnouncement]
    stop_name: str
    direction_name: str
    platform: str
    timetable: Dict[date, PublicTransportDateTimetable]
    dates: Dict[date, str]
    latitude: float | None
    longitude: float | None

    #region Serialization

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> PublicTransportLineStopTimetable:
        """Deserializes data from a dictionary in "attribute:value" format to an object."""
        announcements = d.get(cls.FIELD_ANNOUNCEMENTS, [])
        timetable = d.get(cls.FIELD_TIMETABLE, {})
        try:
            transport_type = PublicTransportType.from_str(
                str(d.get(cls.FIELD_TYPE) or cls._DEFAULT_TYPE)
            )
        except ValueError:
            transport_type = cls._DEFAULT_TYPE
        parsed_timetable: Dict[date, PublicTransportDateTimetable] = {}
        if isinstance(timetable, dict):
            for key, value in timetable.items():
                parsed_key = parse_date(key)
                if parsed_key and isinstance(value, dict):
                    parsed_timetable[parsed_key] = PublicTransportDateTimetable.from_dict(value)
        return cls(
            line=str(d.get(cls.FIELD_LINE) or ''),
            type=transport_type,
            announcements=PublicTransportAnnouncement.from_dict_list(
                announcements if isinstance(announcements, list) else []
            ),
            stop_name=str(d.get(cls.FIELD_STOP_NAME) or ''),
            direction_name=str(d.get(cls.FIELD_DIRECTION_NAME) or ''),
            platform=str(d.get(cls.FIELD_PLATFORM) or ''),
            timetable=parsed_timetable,
            dates=parse_date_url_map(d.get(cls.FIELD_DATES)),
            latitude=parse_coordinate(d.get(cls.FIELD_LATITUDE), -90, 90),
            longitude=parse_coordinate(d.get(cls.FIELD_LONGITUDE), -180, 180)
        )

    def to_dict(self) -> Dict[str, Any]:
        """Serializes object to a dictionary in the format "attribute:value"."""
        return {
            self.FIELD_LINE: self.line,
            self.FIELD_TYPE: str(self.type),
            self.FIELD_ANNOUNCEMENTS: self.to_dict_list(self.announcements),
            self.FIELD_STOP_NAME: self.stop_name,
            self.FIELD_DIRECTION_NAME: self.direction_name,
            self.FIELD_PLATFORM: self.platform,
            self.FIELD_TIMETABLE: {
                key.isoformat(): value.to_dict()
                for key, value in self.timetable.items()
            },
            self.FIELD_DATES: serialize_date_url_map(self.dates),
            self.FIELD_LATITUDE: self.latitude,
            self.FIELD_LONGITUDE: self.longitude
        }

    #endregion Serialization

from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from typing import Any, ClassVar, Dict

from core.data.base_data_model import BaseDataModel
from models.public_transport.model_serialization import (
    parse_coordinate,
    parse_date_url_map,
    serialize_date_url_map
)
from models.public_transport.public_transport_base_line import PublicTransportBaseLine
from models.public_transport.public_transport_date_timetable import PublicTransportDateTimetable


@dataclass
class PublicTransportStopAll(BaseDataModel):
    """Stores every line timetable available for one platform."""

    # Serialized item field declarations
    ITEM_FIELD_LINE: ClassVar[str] = 'line'
    ITEM_FIELD_TIMETABLE: ClassVar[str] = 'timetable'

    # Field name declarations
    FIELD_STOP_NAME: ClassVar[str] = 'stop_name'
    FIELD_PLATFORM: ClassVar[str] = 'platform'
    FIELD_DATES: ClassVar[str] = 'dates'
    FIELD_LINES: ClassVar[str] = 'lines'
    FIELD_LATITUDE: ClassVar[str] = 'latitude'
    FIELD_LONGITUDE: ClassVar[str] = 'longitude'

    # Fields
    stop_name: str
    platform: str
    dates: Dict[date, str]
    lines: Dict[PublicTransportBaseLine, PublicTransportDateTimetable]
    latitude: float | None
    longitude: float | None

    #region Serialization

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> PublicTransportStopAll:
        """Deserializes data from a dictionary in "attribute:value" format to an object."""
        lines = d.get(cls.FIELD_LINES, [])
        mapped_lines: Dict[
            PublicTransportBaseLine,
            PublicTransportDateTimetable
        ] = {}
        if isinstance(lines, list):
            for item in lines:
                if not isinstance(item, dict):
                    continue
                line = item.get(cls.ITEM_FIELD_LINE)
                timetable = item.get(cls.ITEM_FIELD_TIMETABLE)
                if isinstance(line, dict) and isinstance(timetable, dict):
                    mapped_lines[PublicTransportBaseLine.from_dict(line)] = (
                        PublicTransportDateTimetable.from_dict(timetable)
                    )
        return cls(
            stop_name=str(d.get(cls.FIELD_STOP_NAME) or ''),
            platform=str(d.get(cls.FIELD_PLATFORM) or ''),
            dates=parse_date_url_map(d.get(cls.FIELD_DATES)),
            lines=mapped_lines,
            latitude=parse_coordinate(d.get(cls.FIELD_LATITUDE), -90, 90),
            longitude=parse_coordinate(d.get(cls.FIELD_LONGITUDE), -180, 180)
        )

    def to_dict(self) -> Dict[str, Any]:
        """Serializes object to a dictionary in the format "attribute:value"."""
        return {
            self.FIELD_STOP_NAME: self.stop_name,
            self.FIELD_PLATFORM: self.platform,
            self.FIELD_DATES: serialize_date_url_map(self.dates),
            self.FIELD_LINES: [
                {
                    self.ITEM_FIELD_LINE: line.to_dict(),
                    self.ITEM_FIELD_TIMETABLE: timetable.to_dict()
                }
                for line, timetable in self.lines.items()
            ],
            self.FIELD_LATITUDE: self.latitude,
            self.FIELD_LONGITUDE: self.longitude
        }

    #endregion Serialization

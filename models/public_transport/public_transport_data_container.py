from __future__ import annotations
from dataclasses import dataclass
from typing import Any, ClassVar, Dict, List

from core.data.base_data_model import BaseDataModel
from models.public_transport.public_transport_base_line import PublicTransportBaseLine
from models.public_transport.public_transport_line import PublicTransportLine
from models.public_transport.public_transport_line_stop_timetable import PublicTransportLineStopTimetable
from models.public_transport.public_transport_ride import PublicTransportRide
from models.public_transport.public_transport_stop import PublicTransportStop
from models.public_transport.public_transport_stop_all import PublicTransportStopAll


@dataclass
class PublicTransportDataContainer(BaseDataModel):
    """Stores all downloaded view data for one public transport provider."""

    # Field name declarations
    FIELD_CARRIER: ClassVar[str] = 'carrier'
    FIELD_BASE_URL: ClassVar[str] = 'base_url'
    FIELD_BASE_LINES: ClassVar[str] = 'base_lines'
    FIELD_LINES: ClassVar[str] = 'lines'
    FIELD_LINE_STOP_TIMETABLES: ClassVar[str] = 'line_stop_timetables'
    FIELD_RIDES: ClassVar[str] = 'rides'
    FIELD_STOPS: ClassVar[str] = 'stops'
    FIELD_STOP_ALL: ClassVar[str] = 'stop_all'

    # Fields
    carrier: str
    base_url: str
    base_lines: List[PublicTransportBaseLine]
    lines: List[PublicTransportLine]
    line_stop_timetables: List[PublicTransportLineStopTimetable]
    rides: List[PublicTransportRide]
    stops: List[PublicTransportStop]
    stop_all: List[PublicTransportStopAll]

    #region Serialization

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> PublicTransportDataContainer:
        """Deserializes data from a dictionary in "attribute:value" format to an object."""
        return cls(
            carrier=str(d.get(cls.FIELD_CARRIER) or ''),
            base_url=str(d.get(cls.FIELD_BASE_URL) or ''),
            base_lines=PublicTransportBaseLine.from_dict_list(
                d.get(cls.FIELD_BASE_LINES, [])
                if isinstance(d.get(cls.FIELD_BASE_LINES), list) else []
            ),
            lines=PublicTransportLine.from_dict_list(
                d.get(cls.FIELD_LINES, [])
                if isinstance(d.get(cls.FIELD_LINES), list) else []
            ),
            line_stop_timetables=PublicTransportLineStopTimetable.from_dict_list(
                d.get(cls.FIELD_LINE_STOP_TIMETABLES, [])
                if isinstance(d.get(cls.FIELD_LINE_STOP_TIMETABLES), list) else []
            ),
            rides=PublicTransportRide.from_dict_list(
                d.get(cls.FIELD_RIDES, [])
                if isinstance(d.get(cls.FIELD_RIDES), list) else []
            ),
            stops=PublicTransportStop.from_dict_list(
                d.get(cls.FIELD_STOPS, [])
                if isinstance(d.get(cls.FIELD_STOPS), list) else []
            ),
            stop_all=PublicTransportStopAll.from_dict_list(
                d.get(cls.FIELD_STOP_ALL, [])
                if isinstance(d.get(cls.FIELD_STOP_ALL), list) else []
            )
        )

    def to_dict(self) -> Dict[str, Any]:
        """Serializes object to a dictionary in the format "attribute:value"."""
        return {
            self.FIELD_CARRIER: self.carrier,
            self.FIELD_BASE_URL: self.base_url,
            self.FIELD_BASE_LINES: self.to_dict_list(self.base_lines),
            self.FIELD_LINES: self.to_dict_list(self.lines),
            self.FIELD_LINE_STOP_TIMETABLES: self.to_dict_list(self.line_stop_timetables),
            self.FIELD_RIDES: self.to_dict_list(self.rides),
            self.FIELD_STOPS: self.to_dict_list(self.stops),
            self.FIELD_STOP_ALL: self.to_dict_list(self.stop_all)
        }

    #endregion Serialization

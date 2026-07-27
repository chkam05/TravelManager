from __future__ import annotations
from dataclasses import dataclass
from typing import Any, ClassVar, Dict, List

from core.data.base_data_model import BaseDataModel
from models.public_transport.public_transport_announcement import PublicTransportAnnouncement
from models.public_transport.public_transport_base_line import PublicTransportBaseLine
from models.public_transport.public_transport_stop import PublicTransportStop


@dataclass
class PublicTransportCache(BaseDataModel):
    """Stores persistent announcements, lines and stops for one carrier."""

    # Field name declarations
    FIELD_CARRIER: ClassVar[str] = 'carrier'
    FIELD_ANNOUNCEMENTS: ClassVar[str] = 'announcements'
    FIELD_LINES: ClassVar[str] = 'lines'
    FIELD_STOPS: ClassVar[str] = 'stops'
    FIELD_STOP_LOCATIONS_INITIALIZED: ClassVar[str] = (
        'stop_locations_initialized'
    )

    # Fields
    carrier: str
    announcements: List[PublicTransportAnnouncement]
    lines: List[PublicTransportBaseLine]
    stops: List[PublicTransportStop]
    stop_locations_initialized: bool

    #region Serialization

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> PublicTransportCache:
        """Deserializes persistent public transport cache data."""
        announcements = d.get(cls.FIELD_ANNOUNCEMENTS, [])
        lines = d.get(cls.FIELD_LINES, [])
        stops = d.get(cls.FIELD_STOPS, [])
        return cls(
            carrier=str(d.get(cls.FIELD_CARRIER) or ''),
            announcements=PublicTransportAnnouncement.from_dict_list(
                announcements if isinstance(announcements, list) else []
            ),
            lines=PublicTransportBaseLine.from_dict_list(
                lines if isinstance(lines, list) else []
            ),
            stops=PublicTransportStop.from_dict_list(
                stops if isinstance(stops, list) else []
            ),
            stop_locations_initialized=bool(
                d.get(cls.FIELD_STOP_LOCATIONS_INITIALIZED, False)
            )
        )

    def to_dict(self) -> Dict[str, Any]:
        """Serializes persistent public transport cache data."""
        return {
            self.FIELD_CARRIER: self.carrier,
            self.FIELD_ANNOUNCEMENTS: self.to_dict_list(self.announcements),
            self.FIELD_LINES: self.to_dict_list(self.lines),
            self.FIELD_STOPS: self.to_dict_list(self.stops),
            self.FIELD_STOP_LOCATIONS_INITIALIZED: (
                self.stop_locations_initialized
            )
        }

    #endregion Serialization

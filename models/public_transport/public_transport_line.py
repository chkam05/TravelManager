from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from typing import Any, ClassVar, Dict, List

from core.data.base_data_model import BaseDataModel
from models.public_transport.model_serialization import (
    parse_date_url_map,
    serialize_date_url_map
)
from models.public_transport.public_transport_announcement import PublicTransportAnnouncement
from models.public_transport.public_transport_direction import PublicTransportDirection
from resources.public_transport.public_transport_type import PublicTransportType


@dataclass
class PublicTransportLine(BaseDataModel):
    """Stores detailed data for a public transport line."""

    # Default values
    _DEFAULT_TYPE: ClassVar[PublicTransportType] = PublicTransportType.BUS

    # Field name declarations
    FIELD_LINE: ClassVar[str] = 'line'
    FIELD_TYPE: ClassVar[str] = 'type'
    FIELD_ANNOUNCEMENTS: ClassVar[str] = 'announcements'
    FIELD_DIRECTIONS: ClassVar[str] = 'directions'
    FIELD_DATES: ClassVar[str] = 'dates'

    # Fields
    line: str
    type: PublicTransportType
    announcements: List[PublicTransportAnnouncement]
    directions: List[PublicTransportDirection]
    dates: Dict[date, str]

    #region Serialization

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> PublicTransportLine:
        """Deserializes data from a dictionary in "attribute:value" format to an object."""
        announcements = d.get(cls.FIELD_ANNOUNCEMENTS, [])
        directions = d.get(cls.FIELD_DIRECTIONS, [])
        try:
            transport_type = PublicTransportType.from_str(
                str(d.get(cls.FIELD_TYPE) or cls._DEFAULT_TYPE)
            )
        except ValueError:
            transport_type = cls._DEFAULT_TYPE
        return cls(
            line=str(d.get(cls.FIELD_LINE) or ''),
            type=transport_type,
            announcements=PublicTransportAnnouncement.from_dict_list(
                announcements if isinstance(announcements, list) else []
            ),
            directions=PublicTransportDirection.from_dict_list(
                directions if isinstance(directions, list) else []
            ),
            dates=parse_date_url_map(d.get(cls.FIELD_DATES))
        )

    def to_dict(self) -> Dict[str, Any]:
        """Serializes object to a dictionary in the format "attribute:value"."""
        return {
            self.FIELD_LINE: self.line,
            self.FIELD_TYPE: str(self.type),
            self.FIELD_ANNOUNCEMENTS: self.to_dict_list(self.announcements),
            self.FIELD_DIRECTIONS: self.to_dict_list(self.directions),
            self.FIELD_DATES: serialize_date_url_map(self.dates)
        }

    #endregion Serialization

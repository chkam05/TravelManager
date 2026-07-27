from __future__ import annotations
from dataclasses import dataclass
from typing import Any, ClassVar, Dict, List

from core.data.base_data_model import BaseDataModel
from models.public_transport.public_transport_base_line import PublicTransportBaseLine
from models.public_transport.public_transport_stop import PublicTransportStop


@dataclass
class PublicTransportCache(BaseDataModel):
    """Stores persistent line and stop lists downloaded for one carrier."""

    # Field name declarations
    FIELD_CARRIER: ClassVar[str] = 'carrier'
    FIELD_LINES: ClassVar[str] = 'lines'
    FIELD_STOPS: ClassVar[str] = 'stops'

    # Fields
    carrier: str
    lines: List[PublicTransportBaseLine]
    stops: List[PublicTransportStop]

    #region Serialization

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> PublicTransportCache:
        """Deserializes persistent public transport cache data."""
        lines = d.get(cls.FIELD_LINES, [])
        stops = d.get(cls.FIELD_STOPS, [])
        return cls(
            carrier=str(d.get(cls.FIELD_CARRIER) or ''),
            lines=PublicTransportBaseLine.from_dict_list(
                lines if isinstance(lines, list) else []
            ),
            stops=PublicTransportStop.from_dict_list(
                stops if isinstance(stops, list) else []
            )
        )

    def to_dict(self) -> Dict[str, Any]:
        """Serializes persistent public transport cache data."""
        return {
            self.FIELD_CARRIER: self.carrier,
            self.FIELD_LINES: self.to_dict_list(self.lines),
            self.FIELD_STOPS: self.to_dict_list(self.stops)
        }

    #endregion Serialization

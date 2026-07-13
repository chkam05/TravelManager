from __future__ import annotations
from dataclasses import dataclass
from typing import Any, ClassVar, Dict

from core.data.base_data_model import BaseDataModel


@dataclass
class RailwayDataModel(BaseDataModel):
    """Stores OpenStreetMap tag values defined by OpenStreetMap PrimaryFeaturesAttr.RailwayAttr."""

    # Default values
    _DEFAULT_VALUE: ClassVar[Any] = None

    # Field name declarations
    FIELD_BRIDGE: ClassVar[str] = 'bridge'
    FIELD_CUTTING: ClassVar[str] = 'cutting'
    FIELD_ELECTRIFIED: ClassVar[str] = 'electrified'
    FIELD_EMBANKMENT: ClassVar[str] = 'embankment'
    FIELD_EMBEDDED_RAILS: ClassVar[str] = 'embedded_rails'
    FIELD_FREQUENCY: ClassVar[str] = 'frequency'
    FIELD_PASSENGER_LINES: ClassVar[str] = 'passenger_lines'
    FIELD_RAILWAY_TRACK_REF: ClassVar[str] = 'railway_track_ref'
    FIELD_SERVICE: ClassVar[str] = 'service'
    FIELD_TUNNEL: ClassVar[str] = 'tunnel'
    FIELD_TRACKS: ClassVar[str] = 'tracks'
    FIELD_USAGE: ClassVar[str] = 'usage'
    FIELD_VOLTAGE: ClassVar[str] = 'voltage'

    # OpenStreetMap tag declarations
    TAG_BRIDGE: ClassVar[str] = 'bridge'
    TAG_CUTTING: ClassVar[str] = 'cutting'
    TAG_ELECTRIFIED: ClassVar[str] = 'electrified'
    TAG_EMBANKMENT: ClassVar[str] = 'embankment'
    TAG_EMBEDDED_RAILS: ClassVar[str] = 'embedded_rails'
    TAG_FREQUENCY: ClassVar[str] = 'frequency'
    TAG_PASSENGER_LINES: ClassVar[str] = 'passenger_lines'
    TAG_RAILWAY_TRACK_REF: ClassVar[str] = 'railway:track_ref'
    TAG_SERVICE: ClassVar[str] = 'service'
    TAG_TUNNEL: ClassVar[str] = 'tunnel'
    TAG_TRACKS: ClassVar[str] = 'tracks'
    TAG_USAGE: ClassVar[str] = 'usage'
    TAG_VOLTAGE: ClassVar[str] = 'voltage'

    # Fields
    bridge: Any | None
    cutting: Any | None
    electrified: Any | None
    embankment: Any | None
    embedded_rails: Any | None
    frequency: Any | None
    passenger_lines: Any | None
    railway_track_ref: Any | None
    service: Any | None
    tunnel: Any | None
    tracks: Any | None
    usage: Any | None
    voltage: Any | None

    #region Serialization

    @classmethod
    def _get_value(cls, d: Dict[str, Any], field_name: str, tag_name: str) -> Any:
        """Gets a value by local field name or by the real OpenStreetMap tag key."""
        return d.get(tag_name, d.get(field_name, cls._DEFAULT_VALUE))

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> RailwayDataModel:
        """Deserializes data from a dictionary in "attribute:value" format to an object."""
        return cls(
            bridge=cls._get_value(d, cls.FIELD_BRIDGE, cls.TAG_BRIDGE),
            cutting=cls._get_value(d, cls.FIELD_CUTTING, cls.TAG_CUTTING),
            electrified=cls._get_value(d, cls.FIELD_ELECTRIFIED, cls.TAG_ELECTRIFIED),
            embankment=cls._get_value(d, cls.FIELD_EMBANKMENT, cls.TAG_EMBANKMENT),
            embedded_rails=cls._get_value(d, cls.FIELD_EMBEDDED_RAILS, cls.TAG_EMBEDDED_RAILS),
            frequency=cls._get_value(d, cls.FIELD_FREQUENCY, cls.TAG_FREQUENCY),
            passenger_lines=cls._get_value(d, cls.FIELD_PASSENGER_LINES, cls.TAG_PASSENGER_LINES),
            railway_track_ref=cls._get_value(d, cls.FIELD_RAILWAY_TRACK_REF, cls.TAG_RAILWAY_TRACK_REF),
            service=cls._get_value(d, cls.FIELD_SERVICE, cls.TAG_SERVICE),
            tunnel=cls._get_value(d, cls.FIELD_TUNNEL, cls.TAG_TUNNEL),
            tracks=cls._get_value(d, cls.FIELD_TRACKS, cls.TAG_TRACKS),
            usage=cls._get_value(d, cls.FIELD_USAGE, cls.TAG_USAGE),
            voltage=cls._get_value(d, cls.FIELD_VOLTAGE, cls.TAG_VOLTAGE)
        )

    def to_dict(self) -> Dict[str, Any]:
        """Serializes object to a dictionary in the format "attribute:value"."""
        return {
            self.TAG_BRIDGE: self.bridge,
            self.TAG_CUTTING: self.cutting,
            self.TAG_ELECTRIFIED: self.electrified,
            self.TAG_EMBANKMENT: self.embankment,
            self.TAG_EMBEDDED_RAILS: self.embedded_rails,
            self.TAG_FREQUENCY: self.frequency,
            self.TAG_PASSENGER_LINES: self.passenger_lines,
            self.TAG_RAILWAY_TRACK_REF: self.railway_track_ref,
            self.TAG_SERVICE: self.service,
            self.TAG_TUNNEL: self.tunnel,
            self.TAG_TRACKS: self.tracks,
            self.TAG_USAGE: self.usage,
            self.TAG_VOLTAGE: self.voltage
        }

    #endregion Serialization

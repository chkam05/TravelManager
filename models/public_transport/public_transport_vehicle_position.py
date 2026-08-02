from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from typing import Any, ClassVar, Dict

from core.data.base_data_model import BaseDataModel
from models.public_transport.model_serialization import (
    parse_coordinate,
    parse_datetime
)
from resources.public_transport.public_transport_type import PublicTransportType


@dataclass
class PublicTransportVehiclePosition(BaseDataModel):
    """Stores one vehicle position received from a GTFS-Realtime feed."""

    # Default values
    _DEFAULT_TYPE: ClassVar[PublicTransportType] = PublicTransportType.BUS

    # Field name declarations
    FIELD_VEHICLE_ID: ClassVar[str] = 'vehicle_id'
    FIELD_VEHICLE_LABEL: ClassVar[str] = 'vehicle_label'
    FIELD_LICENSE_PLATE: ClassVar[str] = 'license_plate'
    FIELD_SOURCE_CODE: ClassVar[str] = 'source_code'
    FIELD_LINE: ClassVar[str] = 'line'
    FIELD_TRIP_ID: ClassVar[str] = 'trip_id'
    FIELD_TYPE: ClassVar[str] = 'type'
    FIELD_LATITUDE: ClassVar[str] = 'latitude'
    FIELD_LONGITUDE: ClassVar[str] = 'longitude'
    FIELD_BEARING: ClassVar[str] = 'bearing'
    FIELD_SPEED: ClassVar[str] = 'speed'
    FIELD_RECORDED_AT: ClassVar[str] = 'recorded_at'

    # Fields
    vehicle_id: str
    vehicle_label: str
    license_plate: str
    source_code: str
    line: str
    trip_id: str
    type: PublicTransportType
    latitude: float
    longitude: float
    bearing: float | None
    speed: float | None
    recorded_at: datetime | None

    #region Serialization

    @classmethod
    def from_dict(
        cls,
        d: Dict[str, Any]
    ) -> PublicTransportVehiclePosition:
        """Deserializes one GTFS-Realtime vehicle position."""
        try:
            transport_type = PublicTransportType.from_str(
                str(d.get(cls.FIELD_TYPE) or cls._DEFAULT_TYPE)
            )
        except ValueError:
            transport_type = cls._DEFAULT_TYPE
        return cls(
            vehicle_id=str(d.get(cls.FIELD_VEHICLE_ID) or ''),
            vehicle_label=str(d.get(cls.FIELD_VEHICLE_LABEL) or ''),
            license_plate=str(d.get(cls.FIELD_LICENSE_PLATE) or ''),
            source_code=str(d.get(cls.FIELD_SOURCE_CODE) or ''),
            line=str(d.get(cls.FIELD_LINE) or ''),
            trip_id=str(d.get(cls.FIELD_TRIP_ID) or ''),
            type=transport_type,
            latitude=parse_coordinate(
                d.get(cls.FIELD_LATITUDE),
                -90,
                90
            ) or 0.0,
            longitude=parse_coordinate(
                d.get(cls.FIELD_LONGITUDE),
                -180,
                180
            ) or 0.0,
            bearing=cls._optional_float(d.get(cls.FIELD_BEARING)),
            speed=cls._optional_float(d.get(cls.FIELD_SPEED)),
            recorded_at=parse_datetime(d.get(cls.FIELD_RECORDED_AT))
        )

    def to_dict(self) -> Dict[str, Any]:
        """Serializes one GTFS-Realtime vehicle position."""
        return {
            self.FIELD_VEHICLE_ID: self.vehicle_id,
            self.FIELD_VEHICLE_LABEL: self.vehicle_label,
            self.FIELD_LICENSE_PLATE: self.license_plate,
            self.FIELD_SOURCE_CODE: self.source_code,
            self.FIELD_LINE: self.line,
            self.FIELD_TRIP_ID: self.trip_id,
            self.FIELD_TYPE: str(self.type),
            self.FIELD_LATITUDE: self.latitude,
            self.FIELD_LONGITUDE: self.longitude,
            self.FIELD_BEARING: self.bearing,
            self.FIELD_SPEED: self.speed,
            self.FIELD_RECORDED_AT: (
                self.recorded_at.isoformat() if self.recorded_at else None
            )
        }

    @staticmethod
    def _optional_float(value: Any) -> float | None:
        """Converts an optional numeric value to float."""
        try:
            return float(value) if value is not None else None
        except (TypeError, ValueError):
            return None

    #endregion Serialization

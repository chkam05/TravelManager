from __future__ import annotations
from dataclasses import dataclass
from typing import Any, ClassVar, Dict, List

from core.data.base_data_model import BaseDataModel
from models.public_transport.public_transport_base_line import PublicTransportBaseLine
from models.public_transport.model_serialization import parse_coordinate


@dataclass
class PublicTransportStopPlatform(BaseDataModel):
    """Stores one physical platform and the lines serving it."""

    # Field name declarations
    FIELD_NAME: ClassVar[str] = 'name'
    FIELD_LINES: ClassVar[str] = 'lines'
    FIELD_URL_ALL: ClassVar[str] = 'url_all'
    FIELD_URL_CHRONO: ClassVar[str] = 'url_chrono'
    FIELD_LATITUDE: ClassVar[str] = 'latitude'
    FIELD_LONGITUDE: ClassVar[str] = 'longitude'

    # Fields
    name: str
    lines: List[PublicTransportBaseLine]
    url_all: str
    url_chrono: str
    latitude: float | None
    longitude: float | None

    #region Serialization

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> PublicTransportStopPlatform:
        """Deserializes data from a dictionary in "attribute:value" format to an object."""
        lines = d.get(cls.FIELD_LINES, [])
        return cls(
            name=str(d.get(cls.FIELD_NAME) or ''),
            lines=PublicTransportBaseLine.from_dict_list(
                lines if isinstance(lines, list) else []
            ),
            url_all=str(d.get(cls.FIELD_URL_ALL) or ''),
            url_chrono=str(d.get(cls.FIELD_URL_CHRONO) or ''),
            latitude=parse_coordinate(d.get(cls.FIELD_LATITUDE), -90, 90),
            longitude=parse_coordinate(d.get(cls.FIELD_LONGITUDE), -180, 180)
        )

    def to_dict(self) -> Dict[str, Any]:
        """Serializes object to a dictionary in the format "attribute:value"."""
        return {
            self.FIELD_NAME: self.name,
            self.FIELD_LINES: self.to_dict_list(self.lines),
            self.FIELD_URL_ALL: self.url_all,
            self.FIELD_URL_CHRONO: self.url_chrono,
            self.FIELD_LATITUDE: self.latitude,
            self.FIELD_LONGITUDE: self.longitude
        }

    #endregion Serialization

from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from typing import Any, ClassVar, Dict, List

from core.data.base_data_model import BaseDataModel
from models.public_transport.model_serialization import parse_date
from models.public_transport.public_transport_departure_time import PublicTransportDepartureTime


@dataclass
class PublicTransportDateTimetable(BaseDataModel):
    """Stores departures and route variants valid on one date."""

    # Field name declarations
    FIELD_DATE: ClassVar[str] = 'date'
    FIELD_DIRECTION_NAME: ClassVar[str] = 'direction_name'
    FIELD_EFFECTIVE_DATE_FROM: ClassVar[str] = 'effective_date_from'
    FIELD_EFFECTIVE_DATE_TO: ClassVar[str] = 'effective_date_to'
    FIELD_DEPARTURES: ClassVar[str] = 'departures'
    FIELD_VARIANTS: ClassVar[str] = 'variants'

    # Fields
    date: date | None
    direction_name: str
    effective_date_from: date | None
    effective_date_to: date | None
    departures: List[PublicTransportDepartureTime]
    variants: List[str]

    #region Serialization

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> PublicTransportDateTimetable:
        """Deserializes data from a dictionary in "attribute:value" format to an object."""
        departures = d.get(cls.FIELD_DEPARTURES, [])
        variants = d.get(cls.FIELD_VARIANTS, [])
        return cls(
            date=parse_date(d.get(cls.FIELD_DATE)),
            direction_name=str(d.get(cls.FIELD_DIRECTION_NAME) or ''),
            effective_date_from=parse_date(d.get(cls.FIELD_EFFECTIVE_DATE_FROM)),
            effective_date_to=parse_date(d.get(cls.FIELD_EFFECTIVE_DATE_TO)),
            departures=PublicTransportDepartureTime.from_dict_list(
                departures if isinstance(departures, list) else []
            ),
            variants=[str(value) for value in variants] if isinstance(variants, list) else []
        )

    def to_dict(self) -> Dict[str, Any]:
        """Serializes object to a dictionary in the format "attribute:value"."""
        return {
            self.FIELD_DATE: self.date.isoformat() if self.date else None,
            self.FIELD_DIRECTION_NAME: self.direction_name,
            self.FIELD_EFFECTIVE_DATE_FROM: (
                self.effective_date_from.isoformat() if self.effective_date_from else None
            ),
            self.FIELD_EFFECTIVE_DATE_TO: (
                self.effective_date_to.isoformat() if self.effective_date_to else None
            ),
            self.FIELD_DEPARTURES: self.to_dict_list(self.departures),
            self.FIELD_VARIANTS: list(self.variants)
        }

    #endregion Serialization

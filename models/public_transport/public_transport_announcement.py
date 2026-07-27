from __future__ import annotations
from dataclasses import dataclass
from datetime import date, datetime
from typing import Any, ClassVar, Dict, List

from core.data.base_data_model import BaseDataModel
from models.public_transport.model_serialization import parse_date, parse_datetime


@dataclass
class PublicTransportAnnouncement(BaseDataModel):
    """Stores a public transport service announcement."""

    # Field name declarations
    FIELD_LINES: ClassVar[str] = 'lines'
    FIELD_CITY: ClassVar[str] = 'city'
    FIELD_CONTENT: ClassVar[str] = 'content'
    FIELD_DESCRIPTION: ClassVar[str] = 'description'
    FIELD_EFFECTIVE_DATE_FROM: ClassVar[str] = 'effective_date_from'
    FIELD_EFFECTIVE_DATE_TO: ClassVar[str] = 'effective_date_to'
    FIELD_LAST_UPDATED_DATETIME: ClassVar[str] = 'last_updated_datetime'
    FIELD_URL: ClassVar[str] = 'url'

    # Fields
    lines: List[str]
    city: str
    content: str
    description: str
    effective_date_from: date | None
    effective_date_to: date | None
    last_updated_datetime: datetime | None
    url: str

    #region Serialization

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> PublicTransportAnnouncement:
        """Deserializes data from a dictionary in "attribute:value" format to an object."""
        lines = d.get(cls.FIELD_LINES, [])
        return cls(
            lines=[str(line) for line in lines] if isinstance(lines, list) else [],
            city=str(d.get(cls.FIELD_CITY) or ''),
            content=str(d.get(cls.FIELD_CONTENT) or ''),
            description=str(d.get(cls.FIELD_DESCRIPTION) or ''),
            effective_date_from=parse_date(d.get(cls.FIELD_EFFECTIVE_DATE_FROM)),
            effective_date_to=parse_date(d.get(cls.FIELD_EFFECTIVE_DATE_TO)),
            last_updated_datetime=parse_datetime(d.get(cls.FIELD_LAST_UPDATED_DATETIME)),
            url=str(d.get(cls.FIELD_URL) or '')
        )

    def to_dict(self) -> Dict[str, Any]:
        """Serializes object to a dictionary in the format "attribute:value"."""
        return {
            self.FIELD_LINES: list(self.lines),
            self.FIELD_CITY: self.city,
            self.FIELD_CONTENT: self.content,
            self.FIELD_DESCRIPTION: self.description,
            self.FIELD_EFFECTIVE_DATE_FROM: (
                self.effective_date_from.isoformat() if self.effective_date_from else None
            ),
            self.FIELD_EFFECTIVE_DATE_TO: (
                self.effective_date_to.isoformat() if self.effective_date_to else None
            ),
            self.FIELD_LAST_UPDATED_DATETIME: (
                self.last_updated_datetime.isoformat()
                if self.last_updated_datetime else None
            ),
            self.FIELD_URL: self.url
        }

    #endregion Serialization

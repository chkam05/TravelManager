from __future__ import annotations
from dataclasses import dataclass
from typing import Any, ClassVar, Dict

from core.data.base_data_model import BaseDataModel


@dataclass
class ExchangeRateDataModel(BaseDataModel):
    """Stores an exchange rate quoted against a base currency."""

    # Default values
    _DEFAULT_BASE_CURRENCY: ClassVar[str] = 'EUR'

    # Field name declarations
    FIELD_BASE_CURRENCY: ClassVar[str] = 'base_currency'
    FIELD_CURRENCY: ClassVar[str] = 'currency'
    FIELD_RATE: ClassVar[str] = 'rate'
    FIELD_SOURCE: ClassVar[str] = 'source'
    FIELD_UPDATED: ClassVar[str] = 'updated'

    # Fields
    base_currency: str
    currency: str
    rate: float
    source: str | None
    updated: str | None

    #region Serialization

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> ExchangeRateDataModel:
        """Deserializes exchange rate data from a dictionary."""
        try:
            rate = float(d.get(cls.FIELD_RATE, 0))
        except (TypeError, ValueError):
            rate = 0.0

        return cls(
            base_currency=str(d.get(cls.FIELD_BASE_CURRENCY) or cls._DEFAULT_BASE_CURRENCY).upper(),
            currency=str(d.get(cls.FIELD_CURRENCY) or '').upper(),
            rate=rate,
            source=d.get(cls.FIELD_SOURCE),
            updated=d.get(cls.FIELD_UPDATED)
        )

    def to_dict(self) -> Dict[str, Any]:
        """Serializes exchange rate data to a dictionary."""
        return {
            self.FIELD_BASE_CURRENCY: self.base_currency,
            self.FIELD_CURRENCY: self.currency,
            self.FIELD_RATE: self.rate,
            self.FIELD_SOURCE: self.source,
            self.FIELD_UPDATED: self.updated
        }

    #endregion Serialization

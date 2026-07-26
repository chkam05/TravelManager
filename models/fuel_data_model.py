from __future__ import annotations
from dataclasses import dataclass
from typing import Any, ClassVar, Dict, List

from core.data.base_data_model import BaseDataModel


@dataclass
class FuelDataModel(BaseDataModel):
    """Stores fuel prices for a single country."""

    # Default values
    _DEFAULT_PRICE: ClassVar[float | None] = None
    _DEFAULT_SOURCE: ClassVar[str | None] = None
    _DEFAULT_UPDATED: ClassVar[str | None] = None

    # Field name declarations
    FIELD_COUNTRY_CODE: ClassVar[str] = 'country_code'
    FIELD_COUNTRY: ClassVar[str] = 'country'
    FIELD_CURRENCY: ClassVar[str] = 'currency'
    FIELD_SOURCE_CURRENCY: ClassVar[str] = 'source_currency'
    FIELD_PETROL_95: ClassVar[str] = 'petrol_95'
    FIELD_PETROL_98: ClassVar[str] = 'petrol_98'
    FIELD_DIESEL: ClassVar[str] = 'diesel'
    FIELD_LPG: ClassVar[str] = 'lpg'
    FIELD_SOURCE: ClassVar[str] = 'source'
    FIELD_UPDATED: ClassVar[str] = 'updated'
    FIELD_LOADED_AT: ClassVar[str] = 'loaded_at'
    FIELD_MANUAL: ClassVar[str] = 'manual'
    FIELD_MANUAL_UPDATED_AT: ClassVar[str] = 'manual_updated_at'
    FIELD_MANUAL_FIELDS: ClassVar[str] = 'manual_fields'

    # Fields
    country_code: str
    country: str
    currency: str
    source_currency: str
    petrol_95: float | None
    petrol_98: float | None
    diesel: float | None
    lpg: float | None
    source: str | None
    updated: str | None
    loaded_at: str | None
    manual: bool
    manual_updated_at: str | None
    manual_fields: List[str]

    #region Serialization

    @staticmethod
    def _to_optional_price(value: Any) -> float | None:
        """Converts a value to a positive fuel price or an empty value."""
        if value in (None, ''):
            return None

        try:
            price = float(value)
        except (TypeError, ValueError):
            return None

        return price if price > 0 else None

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> FuelDataModel:
        """Deserializes fuel data from a dictionary."""
        return cls(
            country_code=str(d.get(cls.FIELD_COUNTRY_CODE) or ''),
            country=str(d.get(cls.FIELD_COUNTRY) or ''),
            currency=str(d.get(cls.FIELD_CURRENCY) or ''),
            source_currency=str(d.get(cls.FIELD_SOURCE_CURRENCY) or ''),
            petrol_95=cls._to_optional_price(d.get(cls.FIELD_PETROL_95)),
            petrol_98=cls._to_optional_price(d.get(cls.FIELD_PETROL_98)),
            diesel=cls._to_optional_price(d.get(cls.FIELD_DIESEL)),
            lpg=cls._to_optional_price(d.get(cls.FIELD_LPG)),
            source=d.get(cls.FIELD_SOURCE, cls._DEFAULT_SOURCE),
            updated=d.get(cls.FIELD_UPDATED, cls._DEFAULT_UPDATED),
            loaded_at=d.get(cls.FIELD_LOADED_AT),
            manual=bool(d.get(cls.FIELD_MANUAL, False)),
            manual_updated_at=d.get(cls.FIELD_MANUAL_UPDATED_AT),
            manual_fields=[
                str(field)
                for field in d.get(cls.FIELD_MANUAL_FIELDS, [])
                if field is not None
            ] if isinstance(d.get(cls.FIELD_MANUAL_FIELDS), list) else []
        )

    def to_dict(self) -> Dict[str, Any]:
        """Serializes fuel data to a dictionary."""
        return {
            self.FIELD_COUNTRY_CODE: self.country_code,
            self.FIELD_COUNTRY: self.country,
            self.FIELD_CURRENCY: self.currency,
            self.FIELD_SOURCE_CURRENCY: self.source_currency,
            self.FIELD_PETROL_95: self.petrol_95,
            self.FIELD_PETROL_98: self.petrol_98,
            self.FIELD_DIESEL: self.diesel,
            self.FIELD_LPG: self.lpg,
            self.FIELD_SOURCE: self.source,
            self.FIELD_UPDATED: self.updated,
            self.FIELD_LOADED_AT: self.loaded_at,
            self.FIELD_MANUAL: self.manual,
            self.FIELD_MANUAL_UPDATED_AT: self.manual_updated_at,
            self.FIELD_MANUAL_FIELDS: list(self.manual_fields)
        }

    #endregion Serialization

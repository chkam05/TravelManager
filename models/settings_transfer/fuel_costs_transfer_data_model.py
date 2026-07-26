from __future__ import annotations
from dataclasses import dataclass
from typing import Any, ClassVar, Dict, List

from core.data.base_data_model import BaseDataModel
from models.exchange_rate_data_model import ExchangeRateDataModel
from models.fuel_data_model import FuelDataModel


@dataclass
class FuelCostsTransferDataModel(BaseDataModel):
    """Stores the explicit fuel cost transfer payload."""

    # Default values

    # Field name declarations
    FIELD_FUEL_DATA: ClassVar[str] = 'fuel_data'
    FIELD_EXCHANGE_RATES: ClassVar[str] = 'exchange_rates'

    # Fields
    fuel_data: List[FuelDataModel]
    exchange_rates: List[ExchangeRateDataModel]

    #region Serialization

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> FuelCostsTransferDataModel:
        """Deserializes data from a dictionary in "attribute:value" format to an object."""
        fuel_data = d.get(cls.FIELD_FUEL_DATA, [])
        exchange_rates = d.get(cls.FIELD_EXCHANGE_RATES, [])

        return cls(
            fuel_data=FuelDataModel.from_dict_list(fuel_data if isinstance(fuel_data, list) else []),
            exchange_rates=ExchangeRateDataModel.from_dict_list(
                exchange_rates if isinstance(exchange_rates, list) else []
            )
        )

    def to_dict(self) -> Dict[str, Any]:
        """Serializes object to a dictionary in the format "attribute:value"."""
        return {
            self.FIELD_FUEL_DATA: self.to_dict_list(self.fuel_data),
            self.FIELD_EXCHANGE_RATES: self.to_dict_list(self.exchange_rates)
        }

    #endregion Serialization

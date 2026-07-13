from __future__ import annotations
from dataclasses import dataclass
from typing import Any, ClassVar, Dict

from core.data.base_data_model import BaseDataModel


@dataclass
class DeliveryDataModel(BaseDataModel):
    """Stores OpenStreetMap tag values defined by OpenStreetMap AnnotationsAttr.DeliveryAttr."""

    # Default values
    _DEFAULT_VALUE: ClassVar[Any] = None

    # Field name declarations
    FIELD_PARTNER: ClassVar[str] = 'partner'
    FIELD_CONDITIONAL: ClassVar[str] = 'conditional'
    FIELD_FEE: ClassVar[str] = 'fee'

    # OpenStreetMap tag declarations
    TAG_PARTNER: ClassVar[str] = 'delivery:partner'
    TAG_CONDITIONAL: ClassVar[str] = 'delivery:conditional'
    TAG_FEE: ClassVar[str] = 'delivery:fee'

    # Fields
    partner: Any | None
    conditional: Any | None
    fee: Any | None

    #region Serialization

    @classmethod
    def _get_value(cls, d: Dict[str, Any], field_name: str, tag_name: str) -> Any:
        """Gets a value by local field name or by the real OpenStreetMap tag key."""
        return d.get(tag_name, d.get(field_name, cls._DEFAULT_VALUE))

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> DeliveryDataModel:
        """Deserializes data from a dictionary in "attribute:value" format to an object."""
        return cls(
            partner=cls._get_value(d, cls.FIELD_PARTNER, cls.TAG_PARTNER),
            conditional=cls._get_value(d, cls.FIELD_CONDITIONAL, cls.TAG_CONDITIONAL),
            fee=cls._get_value(d, cls.FIELD_FEE, cls.TAG_FEE)
        )

    def to_dict(self) -> Dict[str, Any]:
        """Serializes object to a dictionary in the format "attribute:value"."""
        return {
            self.TAG_PARTNER: self.partner,
            self.TAG_CONDITIONAL: self.conditional,
            self.TAG_FEE: self.fee
        }

    #endregion Serialization

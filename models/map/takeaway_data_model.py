from __future__ import annotations
from dataclasses import dataclass
from typing import Any, ClassVar, Dict

from core.data.base_data_model import BaseDataModel


@dataclass
class TakeawayDataModel(BaseDataModel):
    """Stores OpenStreetMap tag values defined by OpenStreetMap AnnotationsAttr.TakeAWayAttr."""

    # Default values
    _DEFAULT_VALUE: ClassVar[Any] = None

    # Field name declarations
    FIELD_EMAIL: ClassVar[str] = 'email'
    FIELD_FAX: ClassVar[str] = 'fax'
    FIELD_PHONE: ClassVar[str] = 'phone'
    FIELD_SMS: ClassVar[str] = 'sms'
    FIELD_WEBSITE: ClassVar[str] = 'website'

    # OpenStreetMap tag declarations
    TAG_EMAIL: ClassVar[str] = 'takeaway:email'
    TAG_FAX: ClassVar[str] = 'takeaway:fax'
    TAG_PHONE: ClassVar[str] = 'takeaway:phone'
    TAG_SMS: ClassVar[str] = 'takeaway:sms'
    TAG_WEBSITE: ClassVar[str] = 'takeaway:website'

    # Fields
    email: Any | None
    fax: Any | None
    phone: Any | None
    sms: Any | None
    website: Any | None

    #region Serialization

    @classmethod
    def _get_value(cls, d: Dict[str, Any], field_name: str, tag_name: str) -> Any:
        """Gets a value by local field name or by the real OpenStreetMap tag key."""
        return d.get(tag_name, d.get(field_name, cls._DEFAULT_VALUE))

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> TakeawayDataModel:
        """Deserializes data from a dictionary in "attribute:value" format to an object."""
        return cls(
            email=cls._get_value(d, cls.FIELD_EMAIL, cls.TAG_EMAIL),
            fax=cls._get_value(d, cls.FIELD_FAX, cls.TAG_FAX),
            phone=cls._get_value(d, cls.FIELD_PHONE, cls.TAG_PHONE),
            sms=cls._get_value(d, cls.FIELD_SMS, cls.TAG_SMS),
            website=cls._get_value(d, cls.FIELD_WEBSITE, cls.TAG_WEBSITE)
        )

    def to_dict(self) -> Dict[str, Any]:
        """Serializes object to a dictionary in the format "attribute:value"."""
        return {
            self.TAG_EMAIL: self.email,
            self.TAG_FAX: self.fax,
            self.TAG_PHONE: self.phone,
            self.TAG_SMS: self.sms,
            self.TAG_WEBSITE: self.website
        }

    #endregion Serialization

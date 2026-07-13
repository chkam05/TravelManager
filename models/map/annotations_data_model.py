from __future__ import annotations
from dataclasses import dataclass
from typing import Any, ClassVar, Dict

from core.data.base_data_model import BaseDataModel
from models.map.delivery_data_model import DeliveryDataModel
from models.map.drive_through_data_model import DriveThroughDataModel
from models.map.takeaway_data_model import TakeawayDataModel


@dataclass
class AnnotationsDataModel(BaseDataModel):
    """Stores OpenStreetMap tag values defined by OpenStreetMap AnnotationsAttr."""

    # Default values
    _DEFAULT_VALUE: ClassVar[Any] = None

    # Field name declarations
    FIELD_COMMENT: ClassVar[str] = 'comment'
    FIELD_CONTACT_EMAIL: ClassVar[str] = 'contact_email'
    FIELD_CONTACT_FAX: ClassVar[str] = 'contact_fax'
    FIELD_CONTACT_PHONE: ClassVar[str] = 'contact_phone'
    FIELD_CONTACT_SMS: ClassVar[str] = 'contact_sms'
    FIELD_CONTACT_WEBSITE: ClassVar[str] = 'contact_website'
    FIELD_DESCRIPTION: ClassVar[str] = 'description'
    FIELD_EMAIL: ClassVar[str] = 'email'
    FIELD_FAX: ClassVar[str] = 'fax'
    FIELD_FIXME: ClassVar[str] = 'fixme'
    FIELD_IMAGE: ClassVar[str] = 'image'
    FIELD_NOTE: ClassVar[str] = 'note'
    FIELD_PHONE: ClassVar[str] = 'phone'
    FIELD_SOURCE: ClassVar[str] = 'source'
    FIELD_SOURCE_GEOMETRY: ClassVar[str] = 'source_geometry'
    FIELD_SOURCE_NAME: ClassVar[str] = 'source_name'
    FIELD_SOURCE_REF: ClassVar[str] = 'source_ref'
    FIELD_SOURCE_REF_LEGACY: ClassVar[str] = 'source_ref_legacy'
    FIELD_WEBSITE: ClassVar[str] = 'website'
    FIELD_WIKIPEDIA: ClassVar[str] = 'wikipedia'
    FIELD_DELIVERY: ClassVar[str] = 'delivery'
    FIELD_DRIVE_THROUGH: ClassVar[str] = 'drive_through'
    FIELD_TAKEAWAY: ClassVar[str] = 'takeaway'

    # OpenStreetMap tag declarations
    TAG_COMMENT: ClassVar[str] = 'comment'
    TAG_CONTACT_EMAIL: ClassVar[str] = 'contact:email'
    TAG_CONTACT_FAX: ClassVar[str] = 'contact:fax'
    TAG_CONTACT_PHONE: ClassVar[str] = 'contact:phone'
    TAG_CONTACT_SMS: ClassVar[str] = 'contact:sms'
    TAG_CONTACT_WEBSITE: ClassVar[str] = 'contact:website'
    TAG_DESCRIPTION: ClassVar[str] = 'description'
    TAG_EMAIL: ClassVar[str] = 'email'
    TAG_FAX: ClassVar[str] = 'fax'
    TAG_FIXME: ClassVar[str] = 'fixme'
    TAG_IMAGE: ClassVar[str] = 'image'
    TAG_NOTE: ClassVar[str] = 'note'
    TAG_PHONE: ClassVar[str] = 'phone'
    TAG_SOURCE: ClassVar[str] = 'source'
    TAG_SOURCE_GEOMETRY: ClassVar[str] = 'source:geometry'
    TAG_SOURCE_NAME: ClassVar[str] = 'source:name'
    TAG_SOURCE_REF: ClassVar[str] = 'source:ref'
    TAG_SOURCE_REF_LEGACY: ClassVar[str] = 'source_ref'
    TAG_WEBSITE: ClassVar[str] = 'website'
    TAG_WIKIPEDIA: ClassVar[str] = 'wikipedia'

    # Fields
    comment: Any | None
    contact_email: Any | None
    contact_fax: Any | None
    contact_phone: Any | None
    contact_sms: Any | None
    contact_website: Any | None
    description: Any | None
    email: Any | None
    fax: Any | None
    fixme: Any | None
    image: Any | None
    note: Any | None
    phone: Any | None
    source: Any | None
    source_geometry: Any | None
    source_name: Any | None
    source_ref: Any | None
    source_ref_legacy: Any | None
    website: Any | None
    wikipedia: Any | None
    delivery: DeliveryDataModel | None
    drive_through: DriveThroughDataModel | None
    takeaway: TakeawayDataModel | None

    #region Serialization

    @classmethod
    def _get_value(cls, d: Dict[str, Any], field_name: str, tag_name: str) -> Any:
        """Gets a value by local field name or by the real OpenStreetMap tag key."""
        return d.get(tag_name, d.get(field_name, cls._DEFAULT_VALUE))

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> AnnotationsDataModel:
        """Deserializes data from a dictionary in "attribute:value" format to an object."""
        return cls(
            comment=cls._get_value(d, cls.FIELD_COMMENT, cls.TAG_COMMENT),
            contact_email=cls._get_value(d, cls.FIELD_CONTACT_EMAIL, cls.TAG_CONTACT_EMAIL),
            contact_fax=cls._get_value(d, cls.FIELD_CONTACT_FAX, cls.TAG_CONTACT_FAX),
            contact_phone=cls._get_value(d, cls.FIELD_CONTACT_PHONE, cls.TAG_CONTACT_PHONE),
            contact_sms=cls._get_value(d, cls.FIELD_CONTACT_SMS, cls.TAG_CONTACT_SMS),
            contact_website=cls._get_value(d, cls.FIELD_CONTACT_WEBSITE, cls.TAG_CONTACT_WEBSITE),
            description=cls._get_value(d, cls.FIELD_DESCRIPTION, cls.TAG_DESCRIPTION),
            email=cls._get_value(d, cls.FIELD_EMAIL, cls.TAG_EMAIL),
            fax=cls._get_value(d, cls.FIELD_FAX, cls.TAG_FAX),
            fixme=cls._get_value(d, cls.FIELD_FIXME, cls.TAG_FIXME),
            image=cls._get_value(d, cls.FIELD_IMAGE, cls.TAG_IMAGE),
            note=cls._get_value(d, cls.FIELD_NOTE, cls.TAG_NOTE),
            phone=cls._get_value(d, cls.FIELD_PHONE, cls.TAG_PHONE),
            source=cls._get_value(d, cls.FIELD_SOURCE, cls.TAG_SOURCE),
            source_geometry=cls._get_value(d, cls.FIELD_SOURCE_GEOMETRY, cls.TAG_SOURCE_GEOMETRY),
            source_name=cls._get_value(d, cls.FIELD_SOURCE_NAME, cls.TAG_SOURCE_NAME),
            source_ref=cls._get_value(d, cls.FIELD_SOURCE_REF, cls.TAG_SOURCE_REF),
            source_ref_legacy=cls._get_value(d, cls.FIELD_SOURCE_REF_LEGACY, cls.TAG_SOURCE_REF_LEGACY),
            website=cls._get_value(d, cls.FIELD_WEBSITE, cls.TAG_WEBSITE),
            wikipedia=cls._get_value(d, cls.FIELD_WIKIPEDIA, cls.TAG_WIKIPEDIA),
            delivery=DeliveryDataModel.from_dict(d.get(cls.FIELD_DELIVERY, d)),
            drive_through=DriveThroughDataModel.from_dict(d.get(cls.FIELD_DRIVE_THROUGH, d)),
            takeaway=TakeawayDataModel.from_dict(d.get(cls.FIELD_TAKEAWAY, d))
        )

    def to_dict(self) -> Dict[str, Any]:
        """Serializes object to a dictionary in the format "attribute:value"."""
        return {
            self.TAG_COMMENT: self.comment,
            self.TAG_CONTACT_EMAIL: self.contact_email,
            self.TAG_CONTACT_FAX: self.contact_fax,
            self.TAG_CONTACT_PHONE: self.contact_phone,
            self.TAG_CONTACT_SMS: self.contact_sms,
            self.TAG_CONTACT_WEBSITE: self.contact_website,
            self.TAG_DESCRIPTION: self.description,
            self.TAG_EMAIL: self.email,
            self.TAG_FAX: self.fax,
            self.TAG_FIXME: self.fixme,
            self.TAG_IMAGE: self.image,
            self.TAG_NOTE: self.note,
            self.TAG_PHONE: self.phone,
            self.TAG_SOURCE: self.source,
            self.TAG_SOURCE_GEOMETRY: self.source_geometry,
            self.TAG_SOURCE_NAME: self.source_name,
            self.TAG_SOURCE_REF: self.source_ref,
            self.TAG_SOURCE_REF_LEGACY: self.source_ref_legacy,
            self.TAG_WEBSITE: self.website,
            self.TAG_WIKIPEDIA: self.wikipedia,
            self.FIELD_DELIVERY: self.delivery.to_dict() if self.delivery else None,
            self.FIELD_DRIVE_THROUGH: self.drive_through.to_dict() if self.drive_through else None,
            self.FIELD_TAKEAWAY: self.takeaway.to_dict() if self.takeaway else None
        }

    #endregion Serialization

from __future__ import annotations
from dataclasses import dataclass
from typing import Any, ClassVar, Dict

from core.data.base_data_model import BaseDataModel


@dataclass
class AddressDataModel(BaseDataModel):
    """Stores OpenStreetMap tag values defined by OpenStreetMap AddressAttr."""

    # Default values
    _DEFAULT_VALUE: ClassVar[Any] = None

    # Field name declarations
    FIELD_HOUSENUMBER: ClassVar[str] = 'housenumber'
    FIELD_HOUSENAME: ClassVar[str] = 'housename'
    FIELD_FLATS: ClassVar[str] = 'flats'
    FIELD_CONSCRIPTIONNUMBER: ClassVar[str] = 'conscriptionnumber'
    FIELD_STREET: ClassVar[str] = 'street'
    FIELD_PLACE: ClassVar[str] = 'place'
    FIELD_POSTCODE: ClassVar[str] = 'postcode'
    FIELD_CITY: ClassVar[str] = 'city'
    FIELD_COUNTRY: ClassVar[str] = 'country'
    FIELD_COUNTRY_CODE: ClassVar[str] = 'country_code'
    FIELD_HOUSE_NUMBER: ClassVar[str] = 'house_number'
    FIELD_ISO3166_2_LVL4: ClassVar[str] = 'iso3166_2_lvl4'
    FIELD_NEIGHBOURHOOD: ClassVar[str] = 'neighbourhood'
    FIELD_POSTBOX: ClassVar[str] = 'postbox'
    FIELD_FULL: ClassVar[str] = 'full'
    FIELD_QUARTER: ClassVar[str] = 'quarter'
    FIELD_ROAD: ClassVar[str] = 'road'
    FIELD_HAMLET: ClassVar[str] = 'hamlet'
    FIELD_SUBURB: ClassVar[str] = 'suburb'
    FIELD_SUBDISTRICT: ClassVar[str] = 'subdistrict'
    FIELD_DISTRICT: ClassVar[str] = 'district'
    FIELD_PROVINCE: ClassVar[str] = 'province'
    FIELD_STATE: ClassVar[str] = 'state'
    FIELD_STATE_DISTRICT: ClassVar[str] = 'state_district'
    FIELD_COUNTY: ClassVar[str] = 'county'
    FIELD_INTERPOLATION: ClassVar[str] = 'interpolation'
    FIELD_INCLUSION: ClassVar[str] = 'inclusion'

    # OpenStreetMap tag declarations
    TAG_HOUSENUMBER: ClassVar[str] = 'addr:housenumber'
    TAG_HOUSENAME: ClassVar[str] = 'addr:housename'
    TAG_FLATS: ClassVar[str] = 'addr:flats'
    TAG_CONSCRIPTIONNUMBER: ClassVar[str] = 'addr:conscriptionnumber'
    TAG_STREET: ClassVar[str] = 'addr:street'
    TAG_PLACE: ClassVar[str] = 'addr:place'
    TAG_POSTCODE: ClassVar[str] = 'addr:postcode'
    TAG_CITY: ClassVar[str] = 'addr:city'
    TAG_COUNTRY: ClassVar[str] = 'addr:country'
    TAG_COUNTRY_CODE: ClassVar[str] = 'country_code'
    TAG_HOUSE_NUMBER: ClassVar[str] = 'house_number'
    TAG_ISO3166_2_LVL4: ClassVar[str] = 'ISO3166-2-lvl4'
    TAG_NEIGHBOURHOOD: ClassVar[str] = 'neighbourhood'
    TAG_POSTBOX: ClassVar[str] = 'addr:postbox'
    TAG_FULL: ClassVar[str] = 'addr:full'
    TAG_QUARTER: ClassVar[str] = 'quarter'
    TAG_ROAD: ClassVar[str] = 'road'
    TAG_HAMLET: ClassVar[str] = 'addr:hamlet'
    TAG_SUBURB: ClassVar[str] = 'addr:suburb'
    TAG_SUBDISTRICT: ClassVar[str] = 'addr:subdistrict'
    TAG_DISTRICT: ClassVar[str] = 'addr:district'
    TAG_PROVINCE: ClassVar[str] = 'addr:province'
    TAG_STATE: ClassVar[str] = 'addr:state'
    TAG_STATE_DISTRICT: ClassVar[str] = 'state_district'
    TAG_COUNTY: ClassVar[str] = 'addr:county'
    TAG_INTERPOLATION: ClassVar[str] = 'addr:interpolation'
    TAG_INCLUSION: ClassVar[str] = 'addr:inclusion'

    # Fields
    housenumber: Any | None
    housename: Any | None
    flats: Any | None
    conscriptionnumber: Any | None
    street: Any | None
    place: Any | None
    postcode: Any | None
    city: Any | None
    country: Any | None
    country_code: Any | None
    house_number: Any | None
    iso3166_2_lvl4: Any | None
    neighbourhood: Any | None
    postbox: Any | None
    full: Any | None
    quarter: Any | None
    road: Any | None
    hamlet: Any | None
    suburb: Any | None
    subdistrict: Any | None
    district: Any | None
    province: Any | None
    state: Any | None
    state_district: Any | None
    county: Any | None
    interpolation: Any | None
    inclusion: Any | None

    #region Serialization

    @classmethod
    def _get_value(cls, d: Dict[str, Any], field_name: str, tag_name: str) -> Any:
        """Gets a value by local field name or by the real OpenStreetMap tag key."""
        return d.get(tag_name, d.get(field_name, cls._DEFAULT_VALUE))

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> AddressDataModel:
        """Deserializes data from a dictionary in "attribute:value" format to an object."""
        return cls(
            housenumber=cls._get_value(d, cls.FIELD_HOUSENUMBER, cls.TAG_HOUSENUMBER),
            housename=cls._get_value(d, cls.FIELD_HOUSENAME, cls.TAG_HOUSENAME),
            flats=cls._get_value(d, cls.FIELD_FLATS, cls.TAG_FLATS),
            conscriptionnumber=cls._get_value(d, cls.FIELD_CONSCRIPTIONNUMBER, cls.TAG_CONSCRIPTIONNUMBER),
            street=cls._get_value(d, cls.FIELD_STREET, cls.TAG_STREET),
            place=cls._get_value(d, cls.FIELD_PLACE, cls.TAG_PLACE),
            postcode=cls._get_value(d, cls.FIELD_POSTCODE, cls.TAG_POSTCODE),
            city=cls._get_value(d, cls.FIELD_CITY, cls.TAG_CITY),
            country=cls._get_value(d, cls.FIELD_COUNTRY, cls.TAG_COUNTRY),
            country_code=cls._get_value(d, cls.FIELD_COUNTRY_CODE, cls.TAG_COUNTRY_CODE),
            house_number=cls._get_value(d, cls.FIELD_HOUSE_NUMBER, cls.TAG_HOUSE_NUMBER),
            iso3166_2_lvl4=cls._get_value(d, cls.FIELD_ISO3166_2_LVL4, cls.TAG_ISO3166_2_LVL4),
            neighbourhood=cls._get_value(d, cls.FIELD_NEIGHBOURHOOD, cls.TAG_NEIGHBOURHOOD),
            postbox=cls._get_value(d, cls.FIELD_POSTBOX, cls.TAG_POSTBOX),
            full=cls._get_value(d, cls.FIELD_FULL, cls.TAG_FULL),
            quarter=cls._get_value(d, cls.FIELD_QUARTER, cls.TAG_QUARTER),
            road=cls._get_value(d, cls.FIELD_ROAD, cls.TAG_ROAD),
            hamlet=cls._get_value(d, cls.FIELD_HAMLET, cls.TAG_HAMLET),
            suburb=cls._get_value(d, cls.FIELD_SUBURB, cls.TAG_SUBURB),
            subdistrict=cls._get_value(d, cls.FIELD_SUBDISTRICT, cls.TAG_SUBDISTRICT),
            district=cls._get_value(d, cls.FIELD_DISTRICT, cls.TAG_DISTRICT),
            province=cls._get_value(d, cls.FIELD_PROVINCE, cls.TAG_PROVINCE),
            state=cls._get_value(d, cls.FIELD_STATE, cls.TAG_STATE),
            state_district=cls._get_value(d, cls.FIELD_STATE_DISTRICT, cls.TAG_STATE_DISTRICT),
            county=cls._get_value(d, cls.FIELD_COUNTY, cls.TAG_COUNTY),
            interpolation=cls._get_value(d, cls.FIELD_INTERPOLATION, cls.TAG_INTERPOLATION),
            inclusion=cls._get_value(d, cls.FIELD_INCLUSION, cls.TAG_INCLUSION)
        )

    def to_dict(self) -> Dict[str, Any]:
        """Serializes object to a dictionary in the format "attribute:value"."""
        return {
            self.TAG_HOUSENUMBER: self.housenumber,
            self.TAG_HOUSENAME: self.housename,
            self.TAG_FLATS: self.flats,
            self.TAG_CONSCRIPTIONNUMBER: self.conscriptionnumber,
            self.TAG_STREET: self.street,
            self.TAG_PLACE: self.place,
            self.TAG_POSTCODE: self.postcode,
            self.TAG_CITY: self.city,
            self.TAG_COUNTRY: self.country,
            self.TAG_COUNTRY_CODE: self.country_code,
            self.TAG_HOUSE_NUMBER: self.house_number,
            self.TAG_ISO3166_2_LVL4: self.iso3166_2_lvl4,
            self.TAG_NEIGHBOURHOOD: self.neighbourhood,
            self.TAG_POSTBOX: self.postbox,
            self.TAG_FULL: self.full,
            self.TAG_QUARTER: self.quarter,
            self.TAG_ROAD: self.road,
            self.TAG_HAMLET: self.hamlet,
            self.TAG_SUBURB: self.suburb,
            self.TAG_SUBDISTRICT: self.subdistrict,
            self.TAG_DISTRICT: self.district,
            self.TAG_PROVINCE: self.province,
            self.TAG_STATE: self.state,
            self.TAG_STATE_DISTRICT: self.state_district,
            self.TAG_COUNTY: self.county,
            self.TAG_INTERPOLATION: self.interpolation,
            self.TAG_INCLUSION: self.inclusion
        }

    #endregion Serialization

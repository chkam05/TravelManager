from __future__ import annotations
from dataclasses import dataclass
from typing import Any, ClassVar, Dict

from core.data.base_data_model import BaseDataModel


@dataclass
class ReferencesDataModel(BaseDataModel):
    """Stores OpenStreetMap tag values defined by OpenStreetMap ReferencesAttr."""

    # Default values
    _DEFAULT_VALUE: ClassVar[Any] = None

    # Field name declarations
    FIELD_IATA: ClassVar[str] = 'iata'
    FIELD_ICAO: ClassVar[str] = 'icao'
    FIELD_INT_REF: ClassVar[str] = 'int_ref'
    FIELD_LCN_REF: ClassVar[str] = 'lcn_ref'
    FIELD_LOC_REF: ClassVar[str] = 'loc_ref'
    FIELD_LOCAL_REF: ClassVar[str] = 'local_ref'
    FIELD_NAT_REF: ClassVar[str] = 'nat_ref'
    FIELD_NCN_REF: ClassVar[str] = 'ncn_ref'
    FIELD_OLD_REF: ClassVar[str] = 'old_ref'
    FIELD_RCN_REF: ClassVar[str] = 'rcn_ref'
    FIELD_REF: ClassVar[str] = 'ref'
    FIELD_REG_REF: ClassVar[str] = 'reg_ref'
    FIELD_ROUTE_REF: ClassVar[str] = 'route_ref'
    FIELD_SOURCE_REF: ClassVar[str] = 'source_ref'
    FIELD_WIKIDATA: ClassVar[str] = 'wikidata'
    FIELD_WIKIMEDIA_COMMONS: ClassVar[str] = 'wikimedia_commons'

    # OpenStreetMap tag declarations
    TAG_IATA: ClassVar[str] = 'iata'
    TAG_ICAO: ClassVar[str] = 'icao'
    TAG_INT_REF: ClassVar[str] = 'int_ref'
    TAG_LCN_REF: ClassVar[str] = 'lcn_ref'
    TAG_LOC_REF: ClassVar[str] = 'loc_ref'
    TAG_LOCAL_REF: ClassVar[str] = 'local_ref'
    TAG_NAT_REF: ClassVar[str] = 'nat_ref'
    TAG_NCN_REF: ClassVar[str] = 'ncn_ref'
    TAG_OLD_REF: ClassVar[str] = 'old_ref'
    TAG_RCN_REF: ClassVar[str] = 'rcn_ref'
    TAG_REF: ClassVar[str] = 'ref'
    TAG_REG_REF: ClassVar[str] = 'reg_ref'
    TAG_ROUTE_REF: ClassVar[str] = 'route_ref'
    TAG_SOURCE_REF: ClassVar[str] = 'source_ref'
    TAG_WIKIDATA: ClassVar[str] = 'wikidata'
    TAG_WIKIMEDIA_COMMONS: ClassVar[str] = 'wikimedia_commons'

    # Fields
    iata: Any | None
    icao: Any | None
    int_ref: Any | None
    lcn_ref: Any | None
    loc_ref: Any | None
    local_ref: Any | None
    nat_ref: Any | None
    ncn_ref: Any | None
    old_ref: Any | None
    rcn_ref: Any | None
    ref: Any | None
    reg_ref: Any | None
    route_ref: Any | None
    source_ref: Any | None
    wikidata: Any | None
    wikimedia_commons: Any | None

    #region Serialization

    @classmethod
    def _get_value(cls, d: Dict[str, Any], field_name: str, tag_name: str) -> Any:
        """Gets a value by local field name or by the real OpenStreetMap tag key."""
        return d.get(tag_name, d.get(field_name, cls._DEFAULT_VALUE))

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> ReferencesDataModel:
        """Deserializes data from a dictionary in "attribute:value" format to an object."""
        return cls(
            iata=cls._get_value(d, cls.FIELD_IATA, cls.TAG_IATA),
            icao=cls._get_value(d, cls.FIELD_ICAO, cls.TAG_ICAO),
            int_ref=cls._get_value(d, cls.FIELD_INT_REF, cls.TAG_INT_REF),
            lcn_ref=cls._get_value(d, cls.FIELD_LCN_REF, cls.TAG_LCN_REF),
            loc_ref=cls._get_value(d, cls.FIELD_LOC_REF, cls.TAG_LOC_REF),
            local_ref=cls._get_value(d, cls.FIELD_LOCAL_REF, cls.TAG_LOCAL_REF),
            nat_ref=cls._get_value(d, cls.FIELD_NAT_REF, cls.TAG_NAT_REF),
            ncn_ref=cls._get_value(d, cls.FIELD_NCN_REF, cls.TAG_NCN_REF),
            old_ref=cls._get_value(d, cls.FIELD_OLD_REF, cls.TAG_OLD_REF),
            rcn_ref=cls._get_value(d, cls.FIELD_RCN_REF, cls.TAG_RCN_REF),
            ref=cls._get_value(d, cls.FIELD_REF, cls.TAG_REF),
            reg_ref=cls._get_value(d, cls.FIELD_REG_REF, cls.TAG_REG_REF),
            route_ref=cls._get_value(d, cls.FIELD_ROUTE_REF, cls.TAG_ROUTE_REF),
            source_ref=cls._get_value(d, cls.FIELD_SOURCE_REF, cls.TAG_SOURCE_REF),
            wikidata=cls._get_value(d, cls.FIELD_WIKIDATA, cls.TAG_WIKIDATA),
            wikimedia_commons=cls._get_value(d, cls.FIELD_WIKIMEDIA_COMMONS, cls.TAG_WIKIMEDIA_COMMONS)
        )

    def to_dict(self) -> Dict[str, Any]:
        """Serializes object to a dictionary in the format "attribute:value"."""
        return {
            self.TAG_IATA: self.iata,
            self.TAG_ICAO: self.icao,
            self.TAG_INT_REF: self.int_ref,
            self.TAG_LCN_REF: self.lcn_ref,
            self.TAG_LOC_REF: self.loc_ref,
            self.TAG_LOCAL_REF: self.local_ref,
            self.TAG_NAT_REF: self.nat_ref,
            self.TAG_NCN_REF: self.ncn_ref,
            self.TAG_OLD_REF: self.old_ref,
            self.TAG_RCN_REF: self.rcn_ref,
            self.TAG_REF: self.ref,
            self.TAG_REG_REF: self.reg_ref,
            self.TAG_ROUTE_REF: self.route_ref,
            self.TAG_SOURCE_REF: self.source_ref,
            self.TAG_WIKIDATA: self.wikidata,
            self.TAG_WIKIMEDIA_COMMONS: self.wikimedia_commons
        }

    #endregion Serialization

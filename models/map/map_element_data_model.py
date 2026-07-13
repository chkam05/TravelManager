from __future__ import annotations
from dataclasses import dataclass
from typing import Any, ClassVar, Dict

from core.data.base_data_model import BaseDataModel
from models.map.address_data_model import AddressDataModel
from models.map.annotations_data_model import AnnotationsDataModel
from models.map.bounds_data_model import BoundsDataModel
from models.map.coordinates_data_model import CoordinatesDataModel
from models.map.name_data_model import NameDataModel
from models.map.primary_features_data_model import PrimaryFeaturesDataModel
from models.map.properties_data_model import PropertiesDataModel
from models.map.references_data_model import ReferencesDataModel
from models.map.restrictions_data_model import RestrictionsDataModel


@dataclass
class MapElementDataModel(BaseDataModel):
    """Stores a complete structured OpenStreetMap element payload."""

    # Default values
    _DEFAULT_VALUE: ClassVar[Any] = None
    _DEFAULT_RAW_DATA: ClassVar[Dict[str, Any]] = {}

    # Field name declarations
    FIELD_PLACE_ID: ClassVar[str] = 'place_id'
    FIELD_OSM_TYPE: ClassVar[str] = 'osm_type'
    FIELD_OSM_ID: ClassVar[str] = 'osm_id'
    FIELD_TYPE: ClassVar[str] = 'type'
    FIELD_CATEGORY: ClassVar[str] = 'category'
    FIELD_IMPORTANCE: ClassVar[str] = 'importance'
    FIELD_PLACE_RANK: ClassVar[str] = 'place_rank'
    FIELD_LICENCE: ClassVar[str] = 'licence'
    FIELD_DISPLAY_NAME: ClassVar[str] = 'display_name'
    FIELD_COORDINATES: ClassVar[str] = 'coordinates'
    FIELD_BOUNDS: ClassVar[str] = 'bounds'
    FIELD_ADDRESS: ClassVar[str] = 'address'
    FIELD_ANNOTATIONS: ClassVar[str] = 'annotations'
    FIELD_NAME: ClassVar[str] = 'name'
    FIELD_PROPERTIES: ClassVar[str] = 'properties'
    FIELD_REFERENCES: ClassVar[str] = 'references'
    FIELD_RESTRICTIONS: ClassVar[str] = 'restrictions'
    FIELD_PRIMARY_FEATURES: ClassVar[str] = 'primary_features'
    FIELD_RAW_DATA: ClassVar[str] = 'raw_data'

    # Fields
    place_id: int | str | None
    osm_type: str | None
    osm_id: int | str | None
    type: str | None
    category: str | None
    importance: float | str | None
    place_rank: int | str | None
    licence: str | None
    display_name: str | None
    coordinates: CoordinatesDataModel | None
    bounds: BoundsDataModel | None
    address: AddressDataModel | None
    annotations: AnnotationsDataModel | None
    name: NameDataModel | None
    properties: PropertiesDataModel | None
    references: ReferencesDataModel | None
    restrictions: RestrictionsDataModel | None
    primary_features: PrimaryFeaturesDataModel | None
    raw_data: Dict[str, Any]

    #region Serialization

    @classmethod
    def _flat_payload(cls, d: Dict[str, Any]) -> Dict[str, Any]:
        """Builds a flat tag dictionary from common OSM API response shapes."""
        payload = dict(d or {})
        payload.update(dict(d.get('address', {}) or {}))
        payload.update(dict(d.get('extratags', {}) or {}))
        payload.update(dict(d.get('tags', {}) or {}))
        return payload

    @classmethod
    def _nested_dict(cls, d: Dict[str, Any], field_name: str, fallback: Dict[str, Any]) -> Dict[str, Any]:
        """Returns a nested model dictionary only when the source field is dictionary-shaped."""
        value = d.get(field_name)

        return value if isinstance(value, dict) else fallback

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> MapElementDataModel:
        """Deserializes data from a dictionary in "attribute:value" format to an object."""
        flat = cls._flat_payload(d)

        return cls(
            place_id=d.get(cls.FIELD_PLACE_ID, cls._DEFAULT_VALUE),
            osm_type=d.get(cls.FIELD_OSM_TYPE, cls._DEFAULT_VALUE),
            osm_id=d.get(cls.FIELD_OSM_ID, cls._DEFAULT_VALUE),
            type=d.get(cls.FIELD_TYPE, cls._DEFAULT_VALUE),
            category=d.get(cls.FIELD_CATEGORY, d.get('class', cls._DEFAULT_VALUE)),
            importance=d.get(cls.FIELD_IMPORTANCE, cls._DEFAULT_VALUE),
            place_rank=d.get(cls.FIELD_PLACE_RANK, cls._DEFAULT_VALUE),
            licence=d.get(cls.FIELD_LICENCE, cls._DEFAULT_VALUE),
            display_name=d.get(cls.FIELD_DISPLAY_NAME, cls._DEFAULT_VALUE),
            coordinates=CoordinatesDataModel.from_dict(d.get(cls.FIELD_COORDINATES, d)),
            bounds=BoundsDataModel.from_dict(d.get(cls.FIELD_BOUNDS, d)),
            address=AddressDataModel.from_dict(cls._nested_dict(d, cls.FIELD_ADDRESS, flat)),
            annotations=AnnotationsDataModel.from_dict(cls._nested_dict(d, cls.FIELD_ANNOTATIONS, flat)),
            name=NameDataModel.from_dict(cls._nested_dict(d, cls.FIELD_NAME, flat)),
            properties=PropertiesDataModel.from_dict(cls._nested_dict(d, cls.FIELD_PROPERTIES, flat)),
            references=ReferencesDataModel.from_dict(cls._nested_dict(d, cls.FIELD_REFERENCES, flat)),
            restrictions=RestrictionsDataModel.from_dict(cls._nested_dict(d, cls.FIELD_RESTRICTIONS, flat)),
            primary_features=PrimaryFeaturesDataModel.from_dict(cls._nested_dict(d, cls.FIELD_PRIMARY_FEATURES, flat)),
            raw_data=dict(d.get(cls.FIELD_RAW_DATA, d) or {})
        )

    def to_dict(self) -> Dict[str, Any]:
        """Serializes object to a dictionary in the format "attribute:value"."""
        return {
            self.FIELD_PLACE_ID: self.place_id,
            self.FIELD_OSM_TYPE: self.osm_type,
            self.FIELD_OSM_ID: self.osm_id,
            self.FIELD_TYPE: self.type,
            self.FIELD_CATEGORY: self.category,
            self.FIELD_IMPORTANCE: self.importance,
            self.FIELD_PLACE_RANK: self.place_rank,
            self.FIELD_LICENCE: self.licence,
            self.FIELD_DISPLAY_NAME: self.display_name,
            self.FIELD_COORDINATES: self.coordinates.to_dict() if self.coordinates else None,
            self.FIELD_BOUNDS: self.bounds.to_dict() if self.bounds else None,
            self.FIELD_ADDRESS: self.address.to_dict() if self.address else None,
            self.FIELD_ANNOTATIONS: self.annotations.to_dict() if self.annotations else None,
            self.FIELD_NAME: self.name.to_dict() if self.name else None,
            self.FIELD_PROPERTIES: self.properties.to_dict() if self.properties else None,
            self.FIELD_REFERENCES: self.references.to_dict() if self.references else None,
            self.FIELD_RESTRICTIONS: self.restrictions.to_dict() if self.restrictions else None,
            self.FIELD_PRIMARY_FEATURES: self.primary_features.to_dict() if self.primary_features else None,
            self.FIELD_RAW_DATA: dict(self.raw_data or {})
        }

    #endregion Serialization

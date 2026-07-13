from __future__ import annotations
from dataclasses import dataclass
from typing import Any, ClassVar, Dict

from core.data.base_data_model import BaseDataModel


@dataclass
class BuildingDataModel(BaseDataModel):
    """Stores OpenStreetMap tag values defined by OpenStreetMap PrimaryFeaturesAttr.BuildingAttr."""

    # Default values
    _DEFAULT_VALUE: ClassVar[Any] = None

    # Field name declarations
    FIELD_ARCHITECTURE: ClassVar[str] = 'architecture'
    FIELD_COLOUR: ClassVar[str] = 'colour'
    FIELD_FIREPROOF: ClassVar[str] = 'fireproof'
    FIELD_FLATS: ClassVar[str] = 'flats'
    FIELD_LEVELS: ClassVar[str] = 'levels'
    FIELD_MATERIAL: ClassVar[str] = 'material'
    FIELD_BUILDING_MIN_LEVEL: ClassVar[str] = 'building_min_level'
    FIELD_PART: ClassVar[str] = 'part'
    FIELD_SOFT_STOREY: ClassVar[str] = 'soft_storey'
    FIELD_CONSTRUCTION_DATE: ClassVar[str] = 'construction_date'
    FIELD_ENTRANCE: ClassVar[str] = 'entrance'
    FIELD_HEIGHT: ClassVar[str] = 'height'
    FIELD_MAX_LEVEL: ClassVar[str] = 'max_level'
    FIELD_MIN_LEVEL: ClassVar[str] = 'min_level'
    FIELD_NON_EXISTENT_LEVELS: ClassVar[str] = 'non_existent_levels'
    FIELD_START_DATE: ClassVar[str] = 'start_date'

    # OpenStreetMap tag declarations
    TAG_ARCHITECTURE: ClassVar[str] = 'building:architecture'
    TAG_COLOUR: ClassVar[str] = 'building:colour'
    TAG_FIREPROOF: ClassVar[str] = 'building:fireproof'
    TAG_FLATS: ClassVar[str] = 'building:flats'
    TAG_LEVELS: ClassVar[str] = 'building:levels'
    TAG_MATERIAL: ClassVar[str] = 'building:material'
    TAG_BUILDING_MIN_LEVEL: ClassVar[str] = 'building:min_level'
    TAG_PART: ClassVar[str] = 'building:part'
    TAG_SOFT_STOREY: ClassVar[str] = 'building:soft_storey'
    TAG_CONSTRUCTION_DATE: ClassVar[str] = 'construction_date'
    TAG_ENTRANCE: ClassVar[str] = 'entrance'
    TAG_HEIGHT: ClassVar[str] = 'height'
    TAG_MAX_LEVEL: ClassVar[str] = 'max_level'
    TAG_MIN_LEVEL: ClassVar[str] = 'min_level'
    TAG_NON_EXISTENT_LEVELS: ClassVar[str] = 'non_existent_levels'
    TAG_START_DATE: ClassVar[str] = 'start_date'

    # Fields
    architecture: Any | None
    colour: Any | None
    fireproof: Any | None
    flats: Any | None
    levels: Any | None
    material: Any | None
    building_min_level: Any | None
    part: Any | None
    soft_storey: Any | None
    construction_date: Any | None
    entrance: Any | None
    height: Any | None
    max_level: Any | None
    min_level: Any | None
    non_existent_levels: Any | None
    start_date: Any | None

    #region Serialization

    @classmethod
    def _get_value(cls, d: Dict[str, Any], field_name: str, tag_name: str) -> Any:
        """Gets a value by local field name or by the real OpenStreetMap tag key."""
        return d.get(tag_name, d.get(field_name, cls._DEFAULT_VALUE))

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> BuildingDataModel:
        """Deserializes data from a dictionary in "attribute:value" format to an object."""
        return cls(
            architecture=cls._get_value(d, cls.FIELD_ARCHITECTURE, cls.TAG_ARCHITECTURE),
            colour=cls._get_value(d, cls.FIELD_COLOUR, cls.TAG_COLOUR),
            fireproof=cls._get_value(d, cls.FIELD_FIREPROOF, cls.TAG_FIREPROOF),
            flats=cls._get_value(d, cls.FIELD_FLATS, cls.TAG_FLATS),
            levels=cls._get_value(d, cls.FIELD_LEVELS, cls.TAG_LEVELS),
            material=cls._get_value(d, cls.FIELD_MATERIAL, cls.TAG_MATERIAL),
            building_min_level=cls._get_value(d, cls.FIELD_BUILDING_MIN_LEVEL, cls.TAG_BUILDING_MIN_LEVEL),
            part=cls._get_value(d, cls.FIELD_PART, cls.TAG_PART),
            soft_storey=cls._get_value(d, cls.FIELD_SOFT_STOREY, cls.TAG_SOFT_STOREY),
            construction_date=cls._get_value(d, cls.FIELD_CONSTRUCTION_DATE, cls.TAG_CONSTRUCTION_DATE),
            entrance=cls._get_value(d, cls.FIELD_ENTRANCE, cls.TAG_ENTRANCE),
            height=cls._get_value(d, cls.FIELD_HEIGHT, cls.TAG_HEIGHT),
            max_level=cls._get_value(d, cls.FIELD_MAX_LEVEL, cls.TAG_MAX_LEVEL),
            min_level=cls._get_value(d, cls.FIELD_MIN_LEVEL, cls.TAG_MIN_LEVEL),
            non_existent_levels=cls._get_value(d, cls.FIELD_NON_EXISTENT_LEVELS, cls.TAG_NON_EXISTENT_LEVELS),
            start_date=cls._get_value(d, cls.FIELD_START_DATE, cls.TAG_START_DATE)
        )

    def to_dict(self) -> Dict[str, Any]:
        """Serializes object to a dictionary in the format "attribute:value"."""
        return {
            self.TAG_ARCHITECTURE: self.architecture,
            self.TAG_COLOUR: self.colour,
            self.TAG_FIREPROOF: self.fireproof,
            self.TAG_FLATS: self.flats,
            self.TAG_LEVELS: self.levels,
            self.TAG_MATERIAL: self.material,
            self.TAG_BUILDING_MIN_LEVEL: self.building_min_level,
            self.TAG_PART: self.part,
            self.TAG_SOFT_STOREY: self.soft_storey,
            self.TAG_CONSTRUCTION_DATE: self.construction_date,
            self.TAG_ENTRANCE: self.entrance,
            self.TAG_HEIGHT: self.height,
            self.TAG_MAX_LEVEL: self.max_level,
            self.TAG_MIN_LEVEL: self.min_level,
            self.TAG_NON_EXISTENT_LEVELS: self.non_existent_levels,
            self.TAG_START_DATE: self.start_date
        }

    #endregion Serialization

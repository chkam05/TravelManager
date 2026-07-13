from __future__ import annotations
from dataclasses import dataclass
from typing import Any, ClassVar, Dict

from core.data.base_data_model import BaseDataModel
from models.map.boundary_data_model import BoundaryDataModel
from models.map.building_data_model import BuildingDataModel
from models.map.highway_data_model import HighwayDataModel
from models.map.place_attributes_data_model import PlaceAttributesDataModel
from models.map.railway_data_model import RailwayDataModel


@dataclass
class PrimaryFeaturesDataModel(BaseDataModel):
    """Stores OpenStreetMap tag values defined by OpenStreetMap PrimaryFeaturesAttr."""

    # Default values
    _DEFAULT_VALUE: ClassVar[Any] = None

    # Field name declarations
    FIELD_AERIALWAY: ClassVar[str] = 'aerialway'
    FIELD_AEROWAY: ClassVar[str] = 'aeroway'
    FIELD_AMENITY: ClassVar[str] = 'amenity'
    FIELD_BARRIER: ClassVar[str] = 'barrier'
    FIELD_BOUNDARY: ClassVar[str] = 'boundary'
    FIELD_BUILDING: ClassVar[str] = 'building'
    FIELD_CRAFT: ClassVar[str] = 'craft'
    FIELD_EMERGENCY: ClassVar[str] = 'emergency'
    FIELD_LIFEGUARD: ClassVar[str] = 'lifeguard'
    FIELD_GEOLOGICAL: ClassVar[str] = 'geological'
    FIELD_HEALTHCARE: ClassVar[str] = 'healthcare'
    FIELD_HIGHWAY: ClassVar[str] = 'highway'
    FIELD_FOOTWAY: ClassVar[str] = 'footway'
    FIELD_SIDEWALK: ClassVar[str] = 'sidewalk'
    FIELD_CYCLEWAY: ClassVar[str] = 'cycleway'
    FIELD_BUSWAY: ClassVar[str] = 'busway'
    FIELD_PARKING: ClassVar[str] = 'parking'
    FIELD_PARKING_SIDE: ClassVar[str] = 'parking_side'
    FIELD_PARKING_SIDE_ORIENTATION: ClassVar[str] = 'parking_side_orientation'
    FIELD_HISTORIC: ClassVar[str] = 'historic'
    FIELD_LANDUSE: ClassVar[str] = 'landuse'
    FIELD_LEISURE: ClassVar[str] = 'leisure'
    FIELD_MAN_MADE: ClassVar[str] = 'man_made'
    FIELD_MILITARY: ClassVar[str] = 'military'
    FIELD_NATURAL: ClassVar[str] = 'natural'
    FIELD_OFFICE: ClassVar[str] = 'office'
    FIELD_PLACE: ClassVar[str] = 'place'
    FIELD_POWER: ClassVar[str] = 'power'
    FIELD_POWER_LINE: ClassVar[str] = 'power_line'
    FIELD_PUBLIC_TRANSPORT: ClassVar[str] = 'public_transport'
    FIELD_RAILWAY: ClassVar[str] = 'railway'
    FIELD_ROUTE: ClassVar[str] = 'route'
    FIELD_SHOP: ClassVar[str] = 'shop'
    FIELD_TELECOM: ClassVar[str] = 'telecom'
    FIELD_TOURISM: ClassVar[str] = 'tourism'
    FIELD_WATER: ClassVar[str] = 'water'
    FIELD_WATERWAY: ClassVar[str] = 'waterway'
    FIELD_WATERWAYS_USAGE: ClassVar[str] = 'waterways_usage'
    FIELD_BOUNDARY_ATTRIBUTES: ClassVar[str] = 'boundary_attributes'
    FIELD_BUILDING_ATTRIBUTES: ClassVar[str] = 'building_attributes'
    FIELD_HIGHWAY_ATTRIBUTES: ClassVar[str] = 'highway_attributes'
    FIELD_PLACE_ATTRIBUTES: ClassVar[str] = 'place_attributes'
    FIELD_RAILWAY_ATTRIBUTES: ClassVar[str] = 'railway_attributes'

    # OpenStreetMap tag declarations
    TAG_AERIALWAY: ClassVar[str] = 'aerialway'
    TAG_AEROWAY: ClassVar[str] = 'aeroway'
    TAG_AMENITY: ClassVar[str] = 'amenity'
    TAG_BARRIER: ClassVar[str] = 'barrier'
    TAG_BOUNDARY: ClassVar[str] = 'boundary'
    TAG_BUILDING: ClassVar[str] = 'building'
    TAG_CRAFT: ClassVar[str] = 'craft'
    TAG_EMERGENCY: ClassVar[str] = 'emergency'
    TAG_LIFEGUARD: ClassVar[str] = 'lifeguard'
    TAG_GEOLOGICAL: ClassVar[str] = 'geological'
    TAG_HEALTHCARE: ClassVar[str] = 'healthcare'
    TAG_HIGHWAY: ClassVar[str] = 'highway'
    TAG_FOOTWAY: ClassVar[str] = 'footway'
    TAG_SIDEWALK: ClassVar[str] = 'sidewalk'
    TAG_CYCLEWAY: ClassVar[str] = 'cycleway'
    TAG_BUSWAY: ClassVar[str] = 'busway'
    TAG_PARKING: ClassVar[str] = 'parking'
    TAG_PARKING_SIDE: ClassVar[str] = 'parking:side'
    TAG_PARKING_SIDE_ORIENTATION: ClassVar[str] = 'orientation'
    TAG_HISTORIC: ClassVar[str] = 'historic'
    TAG_LANDUSE: ClassVar[str] = 'landuse'
    TAG_LEISURE: ClassVar[str] = 'leisure'
    TAG_MAN_MADE: ClassVar[str] = 'man_made'
    TAG_MILITARY: ClassVar[str] = 'military'
    TAG_NATURAL: ClassVar[str] = 'natural'
    TAG_OFFICE: ClassVar[str] = 'office'
    TAG_PLACE: ClassVar[str] = 'place'
    TAG_POWER: ClassVar[str] = 'power'
    TAG_POWER_LINE: ClassVar[str] = 'line'
    TAG_PUBLIC_TRANSPORT: ClassVar[str] = 'public_transport'
    TAG_RAILWAY: ClassVar[str] = 'railway'
    TAG_ROUTE: ClassVar[str] = 'route'
    TAG_SHOP: ClassVar[str] = 'shop'
    TAG_TELECOM: ClassVar[str] = 'telecom'
    TAG_TOURISM: ClassVar[str] = 'tourism'
    TAG_WATER: ClassVar[str] = 'water'
    TAG_WATERWAY: ClassVar[str] = 'waterway'
    TAG_WATERWAYS_USAGE: ClassVar[str] = 'usage'

    # Fields
    aerialway: Any | None
    aeroway: Any | None
    amenity: Any | None
    barrier: Any | None
    boundary: Any | None
    building: Any | None
    craft: Any | None
    emergency: Any | None
    lifeguard: Any | None
    geological: Any | None
    healthcare: Any | None
    highway: Any | None
    footway: Any | None
    sidewalk: Any | None
    cycleway: Any | None
    busway: Any | None
    parking: Any | None
    parking_side: Any | None
    parking_side_orientation: Any | None
    historic: Any | None
    landuse: Any | None
    leisure: Any | None
    man_made: Any | None
    military: Any | None
    natural: Any | None
    office: Any | None
    place: Any | None
    power: Any | None
    power_line: Any | None
    public_transport: Any | None
    railway: Any | None
    route: Any | None
    shop: Any | None
    telecom: Any | None
    tourism: Any | None
    water: Any | None
    waterway: Any | None
    waterways_usage: Any | None
    boundary_attributes: BoundaryDataModel | None
    building_attributes: BuildingDataModel | None
    highway_attributes: HighwayDataModel | None
    place_attributes: PlaceAttributesDataModel | None
    railway_attributes: RailwayDataModel | None

    #region Serialization

    @classmethod
    def _get_value(cls, d: Dict[str, Any], field_name: str, tag_name: str) -> Any:
        """Gets a value by local field name or by the real OpenStreetMap tag key."""
        return d.get(tag_name, d.get(field_name, cls._DEFAULT_VALUE))

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> PrimaryFeaturesDataModel:
        """Deserializes data from a dictionary in "attribute:value" format to an object."""
        return cls(
            aerialway=cls._get_value(d, cls.FIELD_AERIALWAY, cls.TAG_AERIALWAY),
            aeroway=cls._get_value(d, cls.FIELD_AEROWAY, cls.TAG_AEROWAY),
            amenity=cls._get_value(d, cls.FIELD_AMENITY, cls.TAG_AMENITY),
            barrier=cls._get_value(d, cls.FIELD_BARRIER, cls.TAG_BARRIER),
            boundary=cls._get_value(d, cls.FIELD_BOUNDARY, cls.TAG_BOUNDARY),
            building=cls._get_value(d, cls.FIELD_BUILDING, cls.TAG_BUILDING),
            craft=cls._get_value(d, cls.FIELD_CRAFT, cls.TAG_CRAFT),
            emergency=cls._get_value(d, cls.FIELD_EMERGENCY, cls.TAG_EMERGENCY),
            lifeguard=cls._get_value(d, cls.FIELD_LIFEGUARD, cls.TAG_LIFEGUARD),
            geological=cls._get_value(d, cls.FIELD_GEOLOGICAL, cls.TAG_GEOLOGICAL),
            healthcare=cls._get_value(d, cls.FIELD_HEALTHCARE, cls.TAG_HEALTHCARE),
            highway=cls._get_value(d, cls.FIELD_HIGHWAY, cls.TAG_HIGHWAY),
            footway=cls._get_value(d, cls.FIELD_FOOTWAY, cls.TAG_FOOTWAY),
            sidewalk=cls._get_value(d, cls.FIELD_SIDEWALK, cls.TAG_SIDEWALK),
            cycleway=cls._get_value(d, cls.FIELD_CYCLEWAY, cls.TAG_CYCLEWAY),
            busway=cls._get_value(d, cls.FIELD_BUSWAY, cls.TAG_BUSWAY),
            parking=cls._get_value(d, cls.FIELD_PARKING, cls.TAG_PARKING),
            parking_side=cls._get_value(d, cls.FIELD_PARKING_SIDE, cls.TAG_PARKING_SIDE),
            parking_side_orientation=cls._get_value(d, cls.FIELD_PARKING_SIDE_ORIENTATION, cls.TAG_PARKING_SIDE_ORIENTATION),
            historic=cls._get_value(d, cls.FIELD_HISTORIC, cls.TAG_HISTORIC),
            landuse=cls._get_value(d, cls.FIELD_LANDUSE, cls.TAG_LANDUSE),
            leisure=cls._get_value(d, cls.FIELD_LEISURE, cls.TAG_LEISURE),
            man_made=cls._get_value(d, cls.FIELD_MAN_MADE, cls.TAG_MAN_MADE),
            military=cls._get_value(d, cls.FIELD_MILITARY, cls.TAG_MILITARY),
            natural=cls._get_value(d, cls.FIELD_NATURAL, cls.TAG_NATURAL),
            office=cls._get_value(d, cls.FIELD_OFFICE, cls.TAG_OFFICE),
            place=cls._get_value(d, cls.FIELD_PLACE, cls.TAG_PLACE),
            power=cls._get_value(d, cls.FIELD_POWER, cls.TAG_POWER),
            power_line=cls._get_value(d, cls.FIELD_POWER_LINE, cls.TAG_POWER_LINE),
            public_transport=cls._get_value(d, cls.FIELD_PUBLIC_TRANSPORT, cls.TAG_PUBLIC_TRANSPORT),
            railway=cls._get_value(d, cls.FIELD_RAILWAY, cls.TAG_RAILWAY),
            route=cls._get_value(d, cls.FIELD_ROUTE, cls.TAG_ROUTE),
            shop=cls._get_value(d, cls.FIELD_SHOP, cls.TAG_SHOP),
            telecom=cls._get_value(d, cls.FIELD_TELECOM, cls.TAG_TELECOM),
            tourism=cls._get_value(d, cls.FIELD_TOURISM, cls.TAG_TOURISM),
            water=cls._get_value(d, cls.FIELD_WATER, cls.TAG_WATER),
            waterway=cls._get_value(d, cls.FIELD_WATERWAY, cls.TAG_WATERWAY),
            waterways_usage=cls._get_value(d, cls.FIELD_WATERWAYS_USAGE, cls.TAG_WATERWAYS_USAGE),
            boundary_attributes=BoundaryDataModel.from_dict(d.get(cls.FIELD_BOUNDARY_ATTRIBUTES, d)),
            building_attributes=BuildingDataModel.from_dict(d.get(cls.FIELD_BUILDING_ATTRIBUTES, d)),
            highway_attributes=HighwayDataModel.from_dict(d.get(cls.FIELD_HIGHWAY_ATTRIBUTES, d)),
            place_attributes=PlaceAttributesDataModel.from_dict(d.get(cls.FIELD_PLACE_ATTRIBUTES, d)),
            railway_attributes=RailwayDataModel.from_dict(d.get(cls.FIELD_RAILWAY_ATTRIBUTES, d))
        )

    def to_dict(self) -> Dict[str, Any]:
        """Serializes object to a dictionary in the format "attribute:value"."""
        return {
            self.TAG_AERIALWAY: self.aerialway,
            self.TAG_AEROWAY: self.aeroway,
            self.TAG_AMENITY: self.amenity,
            self.TAG_BARRIER: self.barrier,
            self.TAG_BOUNDARY: self.boundary,
            self.TAG_BUILDING: self.building,
            self.TAG_CRAFT: self.craft,
            self.TAG_EMERGENCY: self.emergency,
            self.TAG_LIFEGUARD: self.lifeguard,
            self.TAG_GEOLOGICAL: self.geological,
            self.TAG_HEALTHCARE: self.healthcare,
            self.TAG_HIGHWAY: self.highway,
            self.TAG_FOOTWAY: self.footway,
            self.TAG_SIDEWALK: self.sidewalk,
            self.TAG_CYCLEWAY: self.cycleway,
            self.TAG_BUSWAY: self.busway,
            self.TAG_PARKING: self.parking,
            self.TAG_PARKING_SIDE: self.parking_side,
            self.TAG_PARKING_SIDE_ORIENTATION: self.parking_side_orientation,
            self.TAG_HISTORIC: self.historic,
            self.TAG_LANDUSE: self.landuse,
            self.TAG_LEISURE: self.leisure,
            self.TAG_MAN_MADE: self.man_made,
            self.TAG_MILITARY: self.military,
            self.TAG_NATURAL: self.natural,
            self.TAG_OFFICE: self.office,
            self.TAG_PLACE: self.place,
            self.TAG_POWER: self.power,
            self.TAG_POWER_LINE: self.power_line,
            self.TAG_PUBLIC_TRANSPORT: self.public_transport,
            self.TAG_RAILWAY: self.railway,
            self.TAG_ROUTE: self.route,
            self.TAG_SHOP: self.shop,
            self.TAG_TELECOM: self.telecom,
            self.TAG_TOURISM: self.tourism,
            self.TAG_WATER: self.water,
            self.TAG_WATERWAY: self.waterway,
            self.TAG_WATERWAYS_USAGE: self.waterways_usage,
            self.FIELD_BOUNDARY_ATTRIBUTES: self.boundary_attributes.to_dict() if self.boundary_attributes else None,
            self.FIELD_BUILDING_ATTRIBUTES: self.building_attributes.to_dict() if self.building_attributes else None,
            self.FIELD_HIGHWAY_ATTRIBUTES: self.highway_attributes.to_dict() if self.highway_attributes else None,
            self.FIELD_PLACE_ATTRIBUTES: self.place_attributes.to_dict() if self.place_attributes else None,
            self.FIELD_RAILWAY_ATTRIBUTES: self.railway_attributes.to_dict() if self.railway_attributes else None
        }

    #endregion Serialization

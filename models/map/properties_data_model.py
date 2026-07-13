from __future__ import annotations
from dataclasses import dataclass
from typing import Any, ClassVar, Dict

from core.data.base_data_model import BaseDataModel


@dataclass
class PropertiesDataModel(BaseDataModel):
    """Stores OpenStreetMap tag values defined by OpenStreetMap PropertiesAttr."""

    # Default values
    _DEFAULT_VALUE: ClassVar[Any] = None

    # Field name declarations
    FIELD_AREA: ClassVar[str] = 'area'
    FIELD_BRAND: ClassVar[str] = 'brand'
    FIELD_BRIDGE: ClassVar[str] = 'bridge'
    FIELD_CAPACITY: ClassVar[str] = 'capacity'
    FIELD_CHARGE: ClassVar[str] = 'charge'
    FIELD_CLOTHES: ClassVar[str] = 'clothes'
    FIELD_COVERED: ClassVar[str] = 'covered'
    FIELD_CROSSING: ClassVar[str] = 'crossing'
    FIELD_CROSSING_ISLAND: ClassVar[str] = 'crossing_island'
    FIELD_CUTTING: ClassVar[str] = 'cutting'
    FIELD_DISUSED: ClassVar[str] = 'disused'
    FIELD_DRINKING_WATER: ClassVar[str] = 'drinking_water'
    FIELD_DRIVE_THROUGH: ClassVar[str] = 'drive_through'
    FIELD_DRIVE_IN: ClassVar[str] = 'drive_in'
    FIELD_ELECTRIFIED: ClassVar[str] = 'electrified'
    FIELD_ELE: ClassVar[str] = 'ele'
    FIELD_EMBANKMENT: ClassVar[str] = 'embankment'
    FIELD_END_DATE: ClassVar[str] = 'end_date'
    FIELD_ENERGY_CLASS: ClassVar[str] = 'energy_class'
    FIELD_EST_WIDTH: ClassVar[str] = 'est_width'
    FIELD_FEE: ClassVar[str] = 'fee'
    FIELD_FIRE_OBJECT_TYPE: ClassVar[str] = 'fire_object_type'
    FIELD_FIRE_OPERATOR: ClassVar[str] = 'fire_operator'
    FIELD_FIRE_RANK: ClassVar[str] = 'fire_rank'
    FIELD_FREQUENCY: ClassVar[str] = 'frequency'
    FIELD_GUTTER: ClassVar[str] = 'gutter'
    FIELD_HAZARD: ClassVar[str] = 'hazard'
    FIELD_HOT_WATER: ClassVar[str] = 'hot_water'
    FIELD_INSCRIPTION: ClassVar[str] = 'inscription'
    FIELD_INTERNET_ACCESS: ClassVar[str] = 'internet_access'
    FIELD_LAYER: ClassVar[str] = 'layer'
    FIELD_LEAF_CYCLE: ClassVar[str] = 'leaf_cycle'
    FIELD_LEAF_TYPE: ClassVar[str] = 'leaf_type'
    FIELD_LOCATION: ClassVar[str] = 'location'
    FIELD_NARROW: ClassVar[str] = 'narrow'
    FIELD_NUDISM: ClassVar[str] = 'nudism'
    FIELD_OPENING_HOURS: ClassVar[str] = 'opening_hours'
    FIELD_OPENING_HOURS_DRIVE_THROUGH: ClassVar[str] = 'opening_hours_drive_through'
    FIELD_OPERATOR: ClassVar[str] = 'operator'
    FIELD_POWER_SUPPLY: ClassVar[str] = 'power_supply'
    FIELD_PRODUCE: ClassVar[str] = 'produce'
    FIELD_RENTAL: ClassVar[str] = 'rental'
    FIELD_SAUNA: ClassVar[str] = 'sauna'
    FIELD_SERVICE_TIMES: ClassVar[str] = 'service_times'
    FIELD_SHOWER: ClassVar[str] = 'shower'
    FIELD_SPORT: ClassVar[str] = 'sport'
    FIELD_START_DATE: ClassVar[str] = 'start_date'
    FIELD_TACTILE_PAVING: ClassVar[str] = 'tactile_paving'
    FIELD_TIDAL: ClassVar[str] = 'tidal'
    FIELD_TOILETS: ClassVar[str] = 'toilets'
    FIELD_TOILETS_WHEELCHAIR: ClassVar[str] = 'toilets_wheelchair'
    FIELD_TOPLESS: ClassVar[str] = 'topless'
    FIELD_TUNNEL: ClassVar[str] = 'tunnel'
    FIELD_WHEELCHAIR: ClassVar[str] = 'wheelchair'
    FIELD_WIDTH: ClassVar[str] = 'width'
    FIELD_WOOD: ClassVar[str] = 'wood'

    # OpenStreetMap tag declarations
    TAG_AREA: ClassVar[str] = 'area'
    TAG_BRAND: ClassVar[str] = 'brand'
    TAG_BRIDGE: ClassVar[str] = 'bridge'
    TAG_CAPACITY: ClassVar[str] = 'capacity'
    TAG_CHARGE: ClassVar[str] = 'charge'
    TAG_CLOTHES: ClassVar[str] = 'clothes'
    TAG_COVERED: ClassVar[str] = 'covered'
    TAG_CROSSING: ClassVar[str] = 'crossing'
    TAG_CROSSING_ISLAND: ClassVar[str] = 'crossing:island'
    TAG_CUTTING: ClassVar[str] = 'cutting'
    TAG_DISUSED: ClassVar[str] = 'disused'
    TAG_DRINKING_WATER: ClassVar[str] = 'drinking_water'
    TAG_DRIVE_THROUGH: ClassVar[str] = 'drive_through'
    TAG_DRIVE_IN: ClassVar[str] = 'drive_in'
    TAG_ELECTRIFIED: ClassVar[str] = 'electrified'
    TAG_ELE: ClassVar[str] = 'ele'
    TAG_EMBANKMENT: ClassVar[str] = 'embankment'
    TAG_END_DATE: ClassVar[str] = 'end_date'
    TAG_ENERGY_CLASS: ClassVar[str] = 'energy_class'
    TAG_EST_WIDTH: ClassVar[str] = 'est_width'
    TAG_FEE: ClassVar[str] = 'fee'
    TAG_FIRE_OBJECT_TYPE: ClassVar[str] = 'fire_object:type'
    TAG_FIRE_OPERATOR: ClassVar[str] = 'fire_operator'
    TAG_FIRE_RANK: ClassVar[str] = 'fire_rank'
    TAG_FREQUENCY: ClassVar[str] = 'frequency'
    TAG_GUTTER: ClassVar[str] = 'gutter'
    TAG_HAZARD: ClassVar[str] = 'hazard'
    TAG_HOT_WATER: ClassVar[str] = 'hot_water'
    TAG_INSCRIPTION: ClassVar[str] = 'inscription'
    TAG_INTERNET_ACCESS: ClassVar[str] = 'internet_access'
    TAG_LAYER: ClassVar[str] = 'layer'
    TAG_LEAF_CYCLE: ClassVar[str] = 'leaf_cycle'
    TAG_LEAF_TYPE: ClassVar[str] = 'leaf_type'
    TAG_LOCATION: ClassVar[str] = 'location'
    TAG_NARROW: ClassVar[str] = 'narrow'
    TAG_NUDISM: ClassVar[str] = 'nudism'
    TAG_OPENING_HOURS: ClassVar[str] = 'opening_hours'
    TAG_OPENING_HOURS_DRIVE_THROUGH: ClassVar[str] = 'opening_hours:drive_through'
    TAG_OPERATOR: ClassVar[str] = 'operator'
    TAG_POWER_SUPPLY: ClassVar[str] = 'power_supply'
    TAG_PRODUCE: ClassVar[str] = 'produce'
    TAG_RENTAL: ClassVar[str] = 'rental'
    TAG_SAUNA: ClassVar[str] = 'sauna'
    TAG_SERVICE_TIMES: ClassVar[str] = 'service_times'
    TAG_SHOWER: ClassVar[str] = 'shower'
    TAG_SPORT: ClassVar[str] = 'sport'
    TAG_START_DATE: ClassVar[str] = 'start_date'
    TAG_TACTILE_PAVING: ClassVar[str] = 'tactile_paving'
    TAG_TIDAL: ClassVar[str] = 'tidal'
    TAG_TOILETS: ClassVar[str] = 'toilets'
    TAG_TOILETS_WHEELCHAIR: ClassVar[str] = 'toilets:wheelchair'
    TAG_TOPLESS: ClassVar[str] = 'topless'
    TAG_TUNNEL: ClassVar[str] = 'tunnel'
    TAG_WHEELCHAIR: ClassVar[str] = 'wheelchair'
    TAG_WIDTH: ClassVar[str] = 'width'
    TAG_WOOD: ClassVar[str] = 'wood'

    # Fields
    area: Any | None
    brand: Any | None
    bridge: Any | None
    capacity: Any | None
    charge: Any | None
    clothes: Any | None
    covered: Any | None
    crossing: Any | None
    crossing_island: Any | None
    cutting: Any | None
    disused: Any | None
    drinking_water: Any | None
    drive_through: Any | None
    drive_in: Any | None
    electrified: Any | None
    ele: Any | None
    embankment: Any | None
    end_date: Any | None
    energy_class: Any | None
    est_width: Any | None
    fee: Any | None
    fire_object_type: Any | None
    fire_operator: Any | None
    fire_rank: Any | None
    frequency: Any | None
    gutter: Any | None
    hazard: Any | None
    hot_water: Any | None
    inscription: Any | None
    internet_access: Any | None
    layer: Any | None
    leaf_cycle: Any | None
    leaf_type: Any | None
    location: Any | None
    narrow: Any | None
    nudism: Any | None
    opening_hours: Any | None
    opening_hours_drive_through: Any | None
    operator: Any | None
    power_supply: Any | None
    produce: Any | None
    rental: Any | None
    sauna: Any | None
    service_times: Any | None
    shower: Any | None
    sport: Any | None
    start_date: Any | None
    tactile_paving: Any | None
    tidal: Any | None
    toilets: Any | None
    toilets_wheelchair: Any | None
    topless: Any | None
    tunnel: Any | None
    wheelchair: Any | None
    width: Any | None
    wood: Any | None

    #region Serialization

    @classmethod
    def _get_value(cls, d: Dict[str, Any], field_name: str, tag_name: str) -> Any:
        """Gets a value by local field name or by the real OpenStreetMap tag key."""
        return d.get(tag_name, d.get(field_name, cls._DEFAULT_VALUE))

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> PropertiesDataModel:
        """Deserializes data from a dictionary in "attribute:value" format to an object."""
        return cls(
            area=cls._get_value(d, cls.FIELD_AREA, cls.TAG_AREA),
            brand=cls._get_value(d, cls.FIELD_BRAND, cls.TAG_BRAND),
            bridge=cls._get_value(d, cls.FIELD_BRIDGE, cls.TAG_BRIDGE),
            capacity=cls._get_value(d, cls.FIELD_CAPACITY, cls.TAG_CAPACITY),
            charge=cls._get_value(d, cls.FIELD_CHARGE, cls.TAG_CHARGE),
            clothes=cls._get_value(d, cls.FIELD_CLOTHES, cls.TAG_CLOTHES),
            covered=cls._get_value(d, cls.FIELD_COVERED, cls.TAG_COVERED),
            crossing=cls._get_value(d, cls.FIELD_CROSSING, cls.TAG_CROSSING),
            crossing_island=cls._get_value(d, cls.FIELD_CROSSING_ISLAND, cls.TAG_CROSSING_ISLAND),
            cutting=cls._get_value(d, cls.FIELD_CUTTING, cls.TAG_CUTTING),
            disused=cls._get_value(d, cls.FIELD_DISUSED, cls.TAG_DISUSED),
            drinking_water=cls._get_value(d, cls.FIELD_DRINKING_WATER, cls.TAG_DRINKING_WATER),
            drive_through=cls._get_value(d, cls.FIELD_DRIVE_THROUGH, cls.TAG_DRIVE_THROUGH),
            drive_in=cls._get_value(d, cls.FIELD_DRIVE_IN, cls.TAG_DRIVE_IN),
            electrified=cls._get_value(d, cls.FIELD_ELECTRIFIED, cls.TAG_ELECTRIFIED),
            ele=cls._get_value(d, cls.FIELD_ELE, cls.TAG_ELE),
            embankment=cls._get_value(d, cls.FIELD_EMBANKMENT, cls.TAG_EMBANKMENT),
            end_date=cls._get_value(d, cls.FIELD_END_DATE, cls.TAG_END_DATE),
            energy_class=cls._get_value(d, cls.FIELD_ENERGY_CLASS, cls.TAG_ENERGY_CLASS),
            est_width=cls._get_value(d, cls.FIELD_EST_WIDTH, cls.TAG_EST_WIDTH),
            fee=cls._get_value(d, cls.FIELD_FEE, cls.TAG_FEE),
            fire_object_type=cls._get_value(d, cls.FIELD_FIRE_OBJECT_TYPE, cls.TAG_FIRE_OBJECT_TYPE),
            fire_operator=cls._get_value(d, cls.FIELD_FIRE_OPERATOR, cls.TAG_FIRE_OPERATOR),
            fire_rank=cls._get_value(d, cls.FIELD_FIRE_RANK, cls.TAG_FIRE_RANK),
            frequency=cls._get_value(d, cls.FIELD_FREQUENCY, cls.TAG_FREQUENCY),
            gutter=cls._get_value(d, cls.FIELD_GUTTER, cls.TAG_GUTTER),
            hazard=cls._get_value(d, cls.FIELD_HAZARD, cls.TAG_HAZARD),
            hot_water=cls._get_value(d, cls.FIELD_HOT_WATER, cls.TAG_HOT_WATER),
            inscription=cls._get_value(d, cls.FIELD_INSCRIPTION, cls.TAG_INSCRIPTION),
            internet_access=cls._get_value(d, cls.FIELD_INTERNET_ACCESS, cls.TAG_INTERNET_ACCESS),
            layer=cls._get_value(d, cls.FIELD_LAYER, cls.TAG_LAYER),
            leaf_cycle=cls._get_value(d, cls.FIELD_LEAF_CYCLE, cls.TAG_LEAF_CYCLE),
            leaf_type=cls._get_value(d, cls.FIELD_LEAF_TYPE, cls.TAG_LEAF_TYPE),
            location=cls._get_value(d, cls.FIELD_LOCATION, cls.TAG_LOCATION),
            narrow=cls._get_value(d, cls.FIELD_NARROW, cls.TAG_NARROW),
            nudism=cls._get_value(d, cls.FIELD_NUDISM, cls.TAG_NUDISM),
            opening_hours=cls._get_value(d, cls.FIELD_OPENING_HOURS, cls.TAG_OPENING_HOURS),
            opening_hours_drive_through=cls._get_value(d, cls.FIELD_OPENING_HOURS_DRIVE_THROUGH, cls.TAG_OPENING_HOURS_DRIVE_THROUGH),
            operator=cls._get_value(d, cls.FIELD_OPERATOR, cls.TAG_OPERATOR),
            power_supply=cls._get_value(d, cls.FIELD_POWER_SUPPLY, cls.TAG_POWER_SUPPLY),
            produce=cls._get_value(d, cls.FIELD_PRODUCE, cls.TAG_PRODUCE),
            rental=cls._get_value(d, cls.FIELD_RENTAL, cls.TAG_RENTAL),
            sauna=cls._get_value(d, cls.FIELD_SAUNA, cls.TAG_SAUNA),
            service_times=cls._get_value(d, cls.FIELD_SERVICE_TIMES, cls.TAG_SERVICE_TIMES),
            shower=cls._get_value(d, cls.FIELD_SHOWER, cls.TAG_SHOWER),
            sport=cls._get_value(d, cls.FIELD_SPORT, cls.TAG_SPORT),
            start_date=cls._get_value(d, cls.FIELD_START_DATE, cls.TAG_START_DATE),
            tactile_paving=cls._get_value(d, cls.FIELD_TACTILE_PAVING, cls.TAG_TACTILE_PAVING),
            tidal=cls._get_value(d, cls.FIELD_TIDAL, cls.TAG_TIDAL),
            toilets=cls._get_value(d, cls.FIELD_TOILETS, cls.TAG_TOILETS),
            toilets_wheelchair=cls._get_value(d, cls.FIELD_TOILETS_WHEELCHAIR, cls.TAG_TOILETS_WHEELCHAIR),
            topless=cls._get_value(d, cls.FIELD_TOPLESS, cls.TAG_TOPLESS),
            tunnel=cls._get_value(d, cls.FIELD_TUNNEL, cls.TAG_TUNNEL),
            wheelchair=cls._get_value(d, cls.FIELD_WHEELCHAIR, cls.TAG_WHEELCHAIR),
            width=cls._get_value(d, cls.FIELD_WIDTH, cls.TAG_WIDTH),
            wood=cls._get_value(d, cls.FIELD_WOOD, cls.TAG_WOOD)
        )

    def to_dict(self) -> Dict[str, Any]:
        """Serializes object to a dictionary in the format "attribute:value"."""
        return {
            self.TAG_AREA: self.area,
            self.TAG_BRAND: self.brand,
            self.TAG_BRIDGE: self.bridge,
            self.TAG_CAPACITY: self.capacity,
            self.TAG_CHARGE: self.charge,
            self.TAG_CLOTHES: self.clothes,
            self.TAG_COVERED: self.covered,
            self.TAG_CROSSING: self.crossing,
            self.TAG_CROSSING_ISLAND: self.crossing_island,
            self.TAG_CUTTING: self.cutting,
            self.TAG_DISUSED: self.disused,
            self.TAG_DRINKING_WATER: self.drinking_water,
            self.TAG_DRIVE_THROUGH: self.drive_through,
            self.TAG_DRIVE_IN: self.drive_in,
            self.TAG_ELECTRIFIED: self.electrified,
            self.TAG_ELE: self.ele,
            self.TAG_EMBANKMENT: self.embankment,
            self.TAG_END_DATE: self.end_date,
            self.TAG_ENERGY_CLASS: self.energy_class,
            self.TAG_EST_WIDTH: self.est_width,
            self.TAG_FEE: self.fee,
            self.TAG_FIRE_OBJECT_TYPE: self.fire_object_type,
            self.TAG_FIRE_OPERATOR: self.fire_operator,
            self.TAG_FIRE_RANK: self.fire_rank,
            self.TAG_FREQUENCY: self.frequency,
            self.TAG_GUTTER: self.gutter,
            self.TAG_HAZARD: self.hazard,
            self.TAG_HOT_WATER: self.hot_water,
            self.TAG_INSCRIPTION: self.inscription,
            self.TAG_INTERNET_ACCESS: self.internet_access,
            self.TAG_LAYER: self.layer,
            self.TAG_LEAF_CYCLE: self.leaf_cycle,
            self.TAG_LEAF_TYPE: self.leaf_type,
            self.TAG_LOCATION: self.location,
            self.TAG_NARROW: self.narrow,
            self.TAG_NUDISM: self.nudism,
            self.TAG_OPENING_HOURS: self.opening_hours,
            self.TAG_OPENING_HOURS_DRIVE_THROUGH: self.opening_hours_drive_through,
            self.TAG_OPERATOR: self.operator,
            self.TAG_POWER_SUPPLY: self.power_supply,
            self.TAG_PRODUCE: self.produce,
            self.TAG_RENTAL: self.rental,
            self.TAG_SAUNA: self.sauna,
            self.TAG_SERVICE_TIMES: self.service_times,
            self.TAG_SHOWER: self.shower,
            self.TAG_SPORT: self.sport,
            self.TAG_START_DATE: self.start_date,
            self.TAG_TACTILE_PAVING: self.tactile_paving,
            self.TAG_TIDAL: self.tidal,
            self.TAG_TOILETS: self.toilets,
            self.TAG_TOILETS_WHEELCHAIR: self.toilets_wheelchair,
            self.TAG_TOPLESS: self.topless,
            self.TAG_TUNNEL: self.tunnel,
            self.TAG_WHEELCHAIR: self.wheelchair,
            self.TAG_WIDTH: self.width,
            self.TAG_WOOD: self.wood
        }

    #endregion Serialization

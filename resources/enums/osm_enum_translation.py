from __future__ import annotations

import re
from typing import ClassVar

from core.enums.enum_str import EnumStr
from core.language_service import LanguageService
from resources.enums.abutters import Abutters
from resources.enums.access import Access
from resources.enums.advertising import Advertising
from resources.enums.aerialway import Aerialway
from resources.enums.aeroway import Aeroway
from resources.enums.alcohol import Alcohol
from resources.enums.amenity import Amenity
from resources.enums.area import Area
from resources.enums.artwork_type import ArtworkType
from resources.enums.attraction import Attraction
from resources.enums.barrier import Barrier
from resources.enums.basin import Basin
from resources.enums.bicycle import Bicycle
from resources.enums.bicycle_road import BicycleRoad
from resources.enums.boat import Boat
from resources.enums.boundary import Boundary
from resources.enums.bridge import Bridge
from resources.enums.building import Building
from resources.enums.building_material import BuildingMaterial
from resources.enums.building_part import BuildingPart
from resources.enums.bus_bay import BusBay
from resources.enums.busway import Busway
from resources.enums.castle_type import CastleType
from resources.enums.change import Change
from resources.enums.construction import Construction
from resources.enums.covered import Covered
from resources.enums.craft import Craft
from resources.enums.crossing import Crossing
from resources.enums.cycleway import Cycleway
from resources.enums.denomination import Denomination
from resources.enums.diplomatic import Diplomatic
from resources.enums.drinking_water_legal import DrinkingWaterLegal
from resources.enums.electrified import Electrified
from resources.enums.embankment import Embankment
from resources.enums.embedded_rails import EmbeddedRails
from resources.enums.emergency import Emergency
from resources.enums.entrance import Entrance
from resources.enums.fee import Fee
from resources.enums.footway import Footway
from resources.enums.ford import Ford
from resources.enums.generator_method import GeneratorMethod
from resources.enums.generator_source import GeneratorSource
from resources.enums.geological import Geological
from resources.enums.golf import Golf
from resources.enums.hazard import Hazard
from resources.enums.healthcare import Healthcare
from resources.enums.highway import Highway
from resources.enums.historic import Historic
from resources.enums.horse import Horse
from resources.enums.hov import Hov
from resources.enums.image_type import ImageType
from resources.enums.incline import Incline
from resources.enums.information import Information
from resources.enums.landuse import Landuse
from resources.enums.leaf_type import LeafType
from resources.enums.leisure import Leisure
from resources.enums.lifeguard import Lifeguard
from resources.enums.line import Line
from resources.enums.location import Location
from resources.enums.man_made import ManMade
from resources.enums.memorial import Memorial
from resources.enums.military import Military
from resources.enums.motor_vehicle import MotorVehicle
from resources.enums.mountain_pass import MountainPass
from resources.enums.natural import Natural
from resources.enums.noexit import Noexit
from resources.enums.office import Office
from resources.enums.oneway import Oneway
from resources.enums.openfire import Openfire
from resources.enums.orientation import Orientation
from resources.enums.overtaking import Overtaking
from resources.enums.parking import Parking
from resources.enums.parking_condition import ParkingCondition
from resources.enums.parking_lane import ParkingLane
from resources.enums.passing_places import PassingPlaces
from resources.enums.place import Place
from resources.enums.power import Power
from resources.enums.priority import Priority
from resources.enums.priority_road import PriorityRoad
from resources.enums.public_transport import PublicTransport
from resources.enums.railway import Railway
from resources.enums.religion import Religion
from resources.enums.roller_coaster import RollerCoaster
from resources.enums.route import Route
from resources.enums.sac_scale import SacScale
from resources.enums.sauna import Sauna
from resources.enums.seasonal import Seasonal
from resources.enums.service import Service
from resources.enums.shop import Shop
from resources.enums.shower import Shower
from resources.enums.side import Side
from resources.enums.sidewalk import Sidewalk
from resources.enums.smoking import Smoking
from resources.enums.smoothness import Smoothness
from resources.enums.source import Source
from resources.enums.sport import Sport
from resources.enums.substance import Substance
from resources.enums.surface import Surface
from resources.enums.telecom import Telecom
from resources.enums.telescope_type import TelescopeType
from resources.enums.tidal import Tidal
from resources.enums.tourism import Tourism
from resources.enums.tower_construction import TowerConstruction
from resources.enums.tower_type import TowerType
from resources.enums.tracktype import Tracktype
from resources.enums.traffic_calming import TrafficCalming
from resources.enums.trail_visibility import TrailVisibility
from resources.enums.trailblazed import Trailblazed
from resources.enums.tunnel import Tunnel
from resources.enums.turn import Turn
from resources.enums.usage import Usage
from resources.enums.vending import Vending
from resources.enums.visibility import Visibility
from resources.enums.water import Water
from resources.enums.waterway import Waterway
from resources.enums.wetland import Wetland
from resources.enums.areas.agriculture_industry import AgricultureIndustry
from resources.enums.areas.buildings import Buildings
from resources.enums.areas.city_planning import CityPlanning
from resources.enums.areas.electricity import Electricity as AreaElectricity
from resources.enums.areas.institutional_areas import InstitutionalAreas
from resources.enums.areas.leisure_recreation import LeisureRecreation
from resources.enums.areas.military import Military as AreaMilitary
from resources.enums.areas.miscellaneous_framed_areas import MiscellaneousFramedAreas
from resources.enums.areas.nature import Nature as AreaNature
from resources.enums.areas.sports import Sports
from resources.enums.areas.transportation import Transportation as AreaTransportation
from resources.enums.lines.aerial_lifts import AerialLifts
from resources.enums.lines.agricultural_forestry_roads import AgriculturalForestryRoads
from resources.enums.lines.barriers import Barriers
from resources.enums.lines.boundaries import Boundaries
from resources.enums.lines.city_roads import CityRoads
from resources.enums.lines.energy_supply import EnergySupply
from resources.enums.lines.major_roads import MajorRoads
from resources.enums.lines.miscellaneous_roads import MiscellaneousRoads
from resources.enums.lines.nature import Nature as LineNature
from resources.enums.lines.non_motorized_vehicles_roads_ways import NonMotorizedVehiclesRoadsWays
from resources.enums.lines.platforms import Platforms
from resources.enums.lines.railways import Railways
from resources.enums.lines.water_traffic import WaterTraffic
from resources.enums.lines.water_ways import WaterWays
from resources.enums.symbols.administrative_facilities import AdministrativeFacilities
from resources.enums.symbols.communication import Communication
from resources.enums.symbols.culture_entertainment_arts import CultureEntertainmentArts
from resources.enums.symbols.electricity import Electricity as SymbolElectricity
from resources.enums.symbols.finance import Finance
from resources.enums.symbols.gastronomy import Gastronomy
from resources.enums.symbols.health_care import HealthCare
from resources.enums.symbols.historical_objects import HistoricalObjects
from resources.enums.symbols.landmarks_man_made_infrastructure_masts_towers import LandmarksManMadeInfrastructureMastsTowers
from resources.enums.symbols.leisure_recreation_sports import LeisureRecreationSports
from resources.enums.symbols.nature import Nature as SymbolNature
from resources.enums.symbols.outdoor import Outdoor
from resources.enums.symbols.places import Places
from resources.enums.symbols.religious_place import ReligiousPlace
from resources.enums.symbols.road_features import RoadFeatures
from resources.enums.symbols.shops_services import ShopsServices
from resources.enums.symbols.tourism_accommodation import TourismAccommodation
from resources.enums.symbols.transportation import Transportation as SymbolTransportation
from resources.enums.symbols.waste_management import WasteManagement


class OsmEnumTranslation:
    """Maps displayed OSM fields to stable enum translation keys."""

    STAGE_11_ENUMS: ClassVar[tuple[type[EnumStr], ...]] = (
        Abutters, Access, Advertising, Aerialway, Aeroway, Alcohol, Amenity,
        Area, ArtworkType, Attraction, Barrier, Basin, Bicycle, BicycleRoad,
        Boat, Boundary, Bridge, Building, BuildingMaterial, BuildingPart,
        BusBay, Busway, CastleType, Change, Construction, Covered, Craft,
        Crossing, Cycleway, Denomination, Diplomatic, DrinkingWaterLegal,
        Electrified, Embankment, EmbeddedRails, Emergency, Entrance, Fee,
        Footway, Ford
    )
    STAGE_12_ENUMS: ClassVar[tuple[type[EnumStr], ...]] = (
        GeneratorMethod, GeneratorSource, Geological, Golf, Hazard, Healthcare,
        Highway, Historic, Horse, Hov, ImageType, Incline, Information,
        Landuse, LeafType, Leisure, Lifeguard, Line, Location, ManMade,
        Memorial, Military, MotorVehicle, MountainPass, Natural, Noexit,
        Office, Oneway, Openfire, Orientation, Overtaking, Parking,
        ParkingCondition, ParkingLane, PassingPlaces, Place, Power, Priority,
        PriorityRoad, PublicTransport
    )
    STAGE_13_ENUMS: ClassVar[tuple[type[EnumStr], ...]] = (
        Railway, Religion, RollerCoaster, Route, SacScale, Sauna, Seasonal,
        Service, Shop, Shower, Side, Sidewalk, Smoking, Smoothness, Source,
        Sport, Substance, Surface, Telecom, TelescopeType, Tidal, Tourism,
        TowerConstruction, TowerType, Tracktype, TrafficCalming,
        TrailVisibility, Trailblazed, Tunnel, Turn, Usage, Vending, Visibility,
        Water, Waterway, Wetland
    )
    STAGE_14_ENUMS: ClassVar[tuple[type[EnumStr], ...]] = (
        AgricultureIndustry, Buildings, CityPlanning, AreaElectricity,
        InstitutionalAreas, LeisureRecreation, AreaMilitary,
        MiscellaneousFramedAreas, AreaNature, Sports, AreaTransportation,
        AerialLifts, AgriculturalForestryRoads, Barriers, Boundaries, CityRoads,
        EnergySupply, MajorRoads, MiscellaneousRoads, LineNature,
        NonMotorizedVehiclesRoadsWays, Platforms, Railways, WaterTraffic,
        WaterWays, AdministrativeFacilities, Communication,
        CultureEntertainmentArts, SymbolElectricity, Finance, Gastronomy,
        HealthCare, HistoricalObjects,
        LandmarksManMadeInfrastructureMastsTowers, LeisureRecreationSports,
        SymbolNature, Outdoor, Places, ReligiousPlace, RoadFeatures,
        ShopsServices, TourismAccommodation, SymbolTransportation,
        WasteManagement
    )
    ENUMS: ClassVar[tuple[type[EnumStr], ...]] = (
        STAGE_11_ENUMS + STAGE_12_ENUMS + STAGE_13_ENUMS + STAGE_14_ENUMS
    )

    ENUM_BY_FIELD: ClassVar[dict[str, type[EnumStr]]] = {
        'abutters': Abutters,
        'access': Access,
        'advertising': Advertising,
        'aerialway': Aerialway,
        'aeroway': Aeroway,
        'alcohol': Alcohol,
        'amenity': Amenity,
        'area': Area,
        'artwork_type': ArtworkType,
        'artwork:type': ArtworkType,
        'attraction': Attraction,
        'barrier': Barrier,
        'basin': Basin,
        'bicycle': Bicycle,
        'bicycle_road': BicycleRoad,
        'boat': Boat,
        'boundary': Boundary,
        'bridge': Bridge,
        'building': Building,
        'building_material': BuildingMaterial,
        'building:material': BuildingMaterial,
        'building_part': BuildingPart,
        'building:part': BuildingPart,
        'bus_bay': BusBay,
        'busway': Busway,
        'castle_type': CastleType,
        'castle:type': CastleType,
        'change': Change,
        'construction': Construction,
        'covered': Covered,
        'craft': Craft,
        'crossing': Crossing,
        'crossing:island': Area,
        'cycleway': Cycleway,
        'cycleway:left': Cycleway,
        'cycleway:right': Cycleway,
        'cycleway:both': Cycleway,
        'denomination': Denomination,
        'diplomatic': Diplomatic,
        'drinking_water:legal': DrinkingWaterLegal,
        'drinking_water_legal': DrinkingWaterLegal,
        'electrified': Electrified,
        'embankment': Embankment,
        'embedded_rails': EmbeddedRails,
        'embedded_rails:yes': EmbeddedRails,
        'emergency': Emergency,
        'entrance': Entrance,
        'fee': Fee,
        'footway': Footway,
        'ford': Ford,
        'generator_method': GeneratorMethod,
        'generator:method': GeneratorMethod,
        'generator_source': GeneratorSource,
        'generator:source': GeneratorSource,
        'geological': Geological,
        'golf': Golf,
        'hazard': Hazard,
        'healthcare': Healthcare,
        'highway': Highway,
        'historic': Historic,
        'horse': Horse,
        'hov': Hov,
        'image_type': ImageType,
        'incline': Incline,
        'information': Information,
        'landuse': Landuse,
        'leaf_type': LeafType,
        'leaf:type': LeafType,
        'leisure': Leisure,
        'lifeguard': Lifeguard,
        'line': Line,
        'location': Location,
        'man_made': ManMade,
        'memorial': Memorial,
        'memorial:type': Memorial,
        'military': Military,
        'motor_vehicle': MotorVehicle,
        'mountain_pass': MountainPass,
        'natural': Natural,
        'noexit': Noexit,
        'office': Office,
        'oneway': Oneway,
        'oneway:bicycle': Oneway,
        'openfire': Openfire,
        'orientation': Orientation,
        'overtaking': Overtaking,
        'parking': Parking,
        'parking:side': Parking,
        'parking_condition': ParkingCondition,
        'parking:condition': ParkingCondition,
        'parking_lane': ParkingLane,
        'parking:lane': ParkingLane,
        'passing_places': PassingPlaces,
        'place': Place,
        'power': Power,
        'priority': Priority,
        'priority_road': PriorityRoad,
        'public_transport': PublicTransport,
        'railway': Railway,
        'religion': Religion,
        'roller_coaster': RollerCoaster,
        'route': Route,
        'sac_scale': SacScale,
        'sauna': Sauna,
        'seasonal': Seasonal,
        'service': Service,
        'shop': Shop,
        'shower': Shower,
        'side': Side,
        'sidewalk': Sidewalk,
        'smoking': Smoking,
        'smoothness': Smoothness,
        'source': Source,
        'sport': Sport,
        'substance': Substance,
        'surface': Surface,
        'telecom': Telecom,
        'telescope_type': TelescopeType,
        'telescope:type': TelescopeType,
        'tidal': Tidal,
        'tourism': Tourism,
        'tower_construction': TowerConstruction,
        'tower:construction': TowerConstruction,
        'tower_type': TowerType,
        'tower:type': TowerType,
        'tracktype': Tracktype,
        'traffic_calming': TrafficCalming,
        'trail_visibility': TrailVisibility,
        'trailblazed': Trailblazed,
        'tunnel': Tunnel,
        'turn': Turn,
        'usage': Usage,
        'vending': Vending,
        'visibility': Visibility,
        'water': Water,
        'waterway': Waterway,
        'wetland': Wetland,
    }

    def __new__(cls):
        raise TypeError(f'{cls.__name__} cannot be instantiated.')

    @staticmethod
    def group(enum_type: type[EnumStr]) -> str:
        """Returns the catalogue group assigned to an enum class."""
        snake_name = re.sub(r'(?<!^)(?=[A-Z])', '_', enum_type.__name__).upper()
        return f'RES_ENUM_{snake_name}'

    @classmethod
    def key(cls, enum_type: type[EnumStr], member: EnumStr) -> str:
        """Returns a stable English UPPER_CASE key for one enum member."""
        return f'{cls.group(enum_type)}.{cls.member_key(member)}'

    @staticmethod
    def member_key(member: EnumStr) -> str:
        """Returns a catalogue-safe key for an enum member."""
        name = member.name.lstrip('_')
        return f'NUMBER_{name}' if name[:1].isdigit() else name

    @classmethod
    def name_keys(cls, enum_type: type[EnumStr]) -> dict[EnumStr, str]:
        """Returns every member-to-key mapping for an enum class."""
        return {member: cls.key(enum_type, member) for member in enum_type}

    @classmethod
    def get(cls, field: str, value: object) -> str:
        """Localises a known displayed value and preserves unknown OSM data."""
        enum_type = cls.ENUM_BY_FIELD.get(str(field or '').strip().casefold())
        if enum_type is None or not isinstance(value, str):
            return str(value)

        labels: list[str] = []
        for raw_part in value.split(';'):
            part = raw_part.strip()
            try:
                member = enum_type(part)
            except ValueError:
                labels.append(part)
            else:
                labels.append(LanguageService.translate_current(cls.key(enum_type, member)))
        return '; '.join(labels)

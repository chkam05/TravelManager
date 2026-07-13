from typing import Any, ClassVar, TypeAlias

from resources.enums.access import Access
from resources.enums.advertising import Advertising
from resources.enums.aerialway import Aerialway
from resources.enums.aeroway import Aeroway
from resources.enums.amenity import Amenity
from resources.enums.area import Area
from resources.enums.areas.agriculture_industry import AgricultureIndustry
from resources.enums.areas.buildings import Buildings
from resources.enums.areas.city_planning import CityPlanning
from resources.enums.areas.electricity import Electricity as ElectricityArea
from resources.enums.areas.institutional_areas import InstitutionalAreas
from resources.enums.areas.leisure_recreation import LeisureRecreation
from resources.enums.areas.military import Military as MilitaryArea
from resources.enums.areas.miscellaneous_framed_areas import MiscellaneousFramedAreas
from resources.enums.areas.nature import Nature as NatureArea
from resources.enums.areas.sports import Sports
from resources.enums.areas.transportation import Transportation as TransportationArea
from resources.enums.artwork_type import ArtworkType
from resources.enums.attraction import Attraction
from resources.enums.barrier import Barrier
from resources.enums.basin import Basin
from resources.enums.bicycle import Bicycle
from resources.enums.boundary import Boundary
from resources.enums.building import Building
from resources.enums.castle_type import CastleType
from resources.enums.construction import Construction
from resources.enums.diplomatic import Diplomatic
from resources.enums.emergency import Emergency
from resources.enums.entrance import Entrance
from resources.enums.ford import Ford
from resources.enums.generator_method import GeneratorMethod
from resources.enums.generator_source import GeneratorSource
from resources.enums.golf import Golf
from resources.enums.highway import Highway
from resources.enums.historic import Historic
from resources.enums.horse import Horse
from resources.enums.image_type import ImageType
from resources.enums.information import Information
from resources.enums.landuse import Landuse
from resources.enums.leaf_type import LeafType
from resources.enums.leisure import Leisure
from resources.enums.lines.aerial_lifts import AerialLifts
from resources.enums.lines.agricultural_forestry_roads import AgriculturalForestryRoads
from resources.enums.lines.barriers import Barriers
from resources.enums.lines.boundaries import Boundaries
from resources.enums.lines.city_roads import CityRoads
from resources.enums.lines.energy_supply import EnergySupply
from resources.enums.lines.major_roads import MajorRoads
from resources.enums.lines.miscellaneous_roads import MiscellaneousRoads
from resources.enums.lines.nature import Nature as NatureLines
from resources.enums.lines.non_motorized_vehicles_roads_ways import NonMotorizedVehiclesRoadsWays
from resources.enums.lines.platforms import Platforms
from resources.enums.lines.railways import Railways
from resources.enums.lines.water_traffic import WaterTraffic
from resources.enums.lines.water_ways import WaterWays
from resources.enums.location import Location
from resources.enums.man_made import ManMade
from resources.enums.memorial import Memorial
from resources.enums.military import Military
from resources.enums.mountain_pass import MountainPass
from resources.enums.natural import Natural
from resources.enums.office import Office
from resources.enums.oneway import Oneway
from resources.enums.parking import Parking
from resources.enums.place import Place
from resources.enums.power import Power
from resources.enums.public_transport import PublicTransport
from resources.enums.railway import Railway
from resources.enums.religion import Religion
from resources.enums.roller_coaster import RollerCoaster
from resources.enums.route import Route
from resources.enums.service import Service
from resources.enums.shop import Shop
from resources.enums.sport import Sport
from resources.enums.substance import Substance
from resources.enums.surface import Surface
from resources.enums.symbols.administrative_facilities import AdministrativeFacilities
from resources.enums.symbols.communication import Communication
from resources.enums.symbols.culture_entertainment_arts import CultureEntertainmentArts
from resources.enums.symbols.electricity import Electricity
from resources.enums.symbols.finance import Finance
from resources.enums.symbols.gastronomy import Gastronomy
from resources.enums.symbols.health_care import HealthCare
from resources.enums.symbols.historical_objects import HistoricalObjects
from resources.enums.symbols.landmarks_man_made_infrastructure_masts_towers import LandmarksManMadeInfrastructureMastsTowers
from resources.enums.symbols.leisure_recreation_sports import LeisureRecreationSports
from resources.enums.symbols.nature import Nature
from resources.enums.symbols.outdoor import Outdoor
from resources.enums.symbols.places import Places
from resources.enums.symbols.religious_place import ReligiousPlace
from resources.enums.symbols.road_features import RoadFeatures
from resources.enums.symbols.shops_services import ShopsServices
from resources.enums.symbols.tourism_accommodation import TourismAccommodation
from resources.enums.symbols.transportation import Transportation
from resources.enums.symbols.waste_management import WasteManagement
from resources.enums.telescope_type import TelescopeType
from resources.enums.tourism import Tourism
from resources.enums.tower_construction import TowerConstruction
from resources.enums.tower_type import TowerType
from resources.enums.tracktype import Tracktype
from resources.enums.tunnel import Tunnel
from resources.enums.vending import Vending
from resources.enums.waterway import Waterway
from resources.enums.wetland import Wetland
from resources.map_areas import MapAreas
from resources.map_keys import MapKeys
from resources.map_lines import MapLines
from resources.map_symbols import MapSymbols


LegendDict: TypeAlias = dict[str, dict[str, Any]]


class MapLegend:

    def __new__(cls, *args, **kwargs):
        """Prevent instantiation of this static utility class."""
        raise TypeError(f'{cls.__name__} is a static utility class and cannot be instantiated.')
    
    FIELD_TITLE: ClassVar[str] = 'title'
    FIELD_ICON: ClassVar[str] = 'icon'
    FIELD_REQUIREMENTS: ClassVar[str] = 'requirements'

    SYMBOLS: ClassVar[LegendDict] = {
        MapSymbols.GASTRONOMY: {
            Gastronomy.BAR.value: {
                FIELD_TITLE: 'Bar',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.AMENITY: Amenity.BAR.value,
                    }
                ]
            },
            Gastronomy.BIERGARTEN.value: {
                FIELD_TITLE: 'Biergarten (traditional sense)',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.AMENITY: Amenity.BIERGARTEN.value,
                    }
                ]
            },
            Gastronomy.CAFE.value: {
                FIELD_TITLE: 'Cafe',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.AMENITY: Amenity.CAFE.value,
                    }
                ]
            },
            Gastronomy.FAST_FOOD.value: {
                FIELD_TITLE: 'Fast food restaurant or snack bar or sandwich bar or similar',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.AMENITY: Amenity.FAST_FOOD.value,
                    }
                ]
            },
            Gastronomy.ICE_CREAM.value: {
                FIELD_TITLE: 'Ice cream shop',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.AMENITY: Amenity.ICE_CREAM.value,
                    }
                ]
            },
            Gastronomy.OUTDOOR_SEATING.value: {
                FIELD_TITLE: 'An outdoor seating area, usually for the consumption of food and drink from neighbouring cafes and restaurants',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.LEISURE: Leisure.OUTDOOR_SEATING.value,
                    }
                ]
            },
            Gastronomy.PUB.value: {
                FIELD_TITLE: 'Pub',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.AMENITY: Amenity.PUB.value,
                    }
                ]
            },
            Gastronomy.RESTAURANT.value: {
                FIELD_TITLE: 'Restaurant (except fast food) / food court',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.AMENITY: Amenity.RESTAURANT.value,
                    },
                    {
                        MapKeys.AMENITY: Amenity.FOOD_COURT.value,
                    }
                ]
            },
        },
        MapSymbols.CULTURE_ENTERTAINMENT_ARTS: {
            CultureEntertainmentArts.AMUSEMENT_ARCADE.value: {
                FIELD_TITLE: 'A venue with pay-to-play games',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.LEISURE: Leisure.AMUSEMENT_ARCADE.value,
                    }
                ]
            },
            CultureEntertainmentArts.ARTS_CENTRE.value: {
                FIELD_TITLE: 'Arts centre',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.AMENITY: Amenity.ARTS_CENTRE.value,
                    }
                ]
            },
            CultureEntertainmentArts.ARTWORK.value: {
                FIELD_TITLE: 'Artwork',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.TOURISM: Tourism.ARTWORK.value,
                    }
                ]
            },
            CultureEntertainmentArts.CASINO.value: {
                FIELD_TITLE: 'Casino',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.AMENITY: Amenity.CASINO.value,
                    }
                ]
            },
            CultureEntertainmentArts.CINEMA.value: {
                FIELD_TITLE: 'Cinema',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.AMENITY: Amenity.CINEMA.value,
                    }
                ]
            },
            CultureEntertainmentArts.COMMUNITY_CENTRE.value: {
                FIELD_TITLE: 'Community centre',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.AMENITY: Amenity.COMMUNITY_CENTRE.value,
                    }
                ]
            },
            CultureEntertainmentArts.GALLERY.value: {
                FIELD_TITLE: 'Art gallery, art museum',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.TOURISM: Tourism.GALLERY.value,
                    }
                ]
            },
            CultureEntertainmentArts.INTERNET_CAFE.value: {
                FIELD_TITLE: 'Internet cafe',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.AMENITY: Amenity.INTERNET_CAFE.value,
                    }
                ]
            },
            CultureEntertainmentArts.LIBRARY.value: {
                FIELD_TITLE: 'Library',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.AMENITY: Amenity.LIBRARY.value,
                    }
                ]
            },
            CultureEntertainmentArts.MUSEUM.value: {
                FIELD_TITLE: 'Museum',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.TOURISM: Tourism.MUSEUM.value,
                    }
                ]
            },
            CultureEntertainmentArts.NIGHTCLUB.value: {
                FIELD_TITLE: 'Nightclub',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.AMENITY: Amenity.NIGHTCLUB.value,
                    }
                ]
            },
            CultureEntertainmentArts.PUBLIC_BOOKCASE.value: {
                FIELD_TITLE: 'Public bookcase',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.AMENITY: Amenity.PUBLIC_BOOKCASE.value,
                    }
                ]
            },
            CultureEntertainmentArts.THEATRE.value: {
                FIELD_TITLE: 'Theatre',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.AMENITY: Amenity.THEATRE.value,
                    }
                ]
            },
        },
        MapSymbols.HISTORICAL_OBJECTS: {
            HistoricalObjects.ARCHAEOLOGICAL_SITE.value: {
                FIELD_TITLE: 'Place in which objects of historic interest are preserved',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.HISTORIC: Historic.ARCHAEOLOGICAL_SITE.value,
                    }
                ]
            },
            HistoricalObjects.BUST.value: {
                FIELD_TITLE: 'Bust',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.HISTORIC: Historic.MEMORIAL.value,
                        MapKeys.MEMORIAL: Memorial.BUST.value,
                    },
                    {
                        MapKeys.TOURISM: Tourism.ARTWORK.value,
                        MapKeys.ARTWORK_TYPE: ArtworkType.BUST.value,
                    }
                ]
            },
            HistoricalObjects.CARTO_SHRINE.value: {
                FIELD_TITLE: 'Historical shrine',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.HISTORIC: Historic.WAYSIDE_SHRINE.value,
                    }
                ]
            },
            HistoricalObjects.CASTLE.value: {
                FIELD_TITLE: 'Castle',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.HISTORIC: Historic.CASTLE.value,
                    }
                ]
            },
            HistoricalObjects.CITY_GATE.value: {
                FIELD_TITLE: 'City gate',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.HISTORIC: Historic.CITY_GATE.value,
                    }
                ]
            },
            HistoricalObjects.FORTRESS.value: {
                FIELD_TITLE: 'Defensive castle / Fortress / Castra / Shiro / Kremlin',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.HISTORIC: Historic.CASTLE.value,
                        MapKeys.CASTLE_TYPE: [
                            CastleType.DEFENSIVE.value,
                            CastleType.FORTRESS.value,
                            CastleType.CASTRUM.value,
                            CastleType.SHIRO.value,
                            CastleType.KREMLIN.value,
                        ]
                    }
                ]
            },
            HistoricalObjects.HISTORIC_FORT: {
                FIELD_TITLE: 'Military historic fort',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.HISTORIC: Historic.FORT.value,
                    }
                ]
            },
            HistoricalObjects.MANOR.value: {
                FIELD_TITLE: 'Manor house',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.HISTORIC: Historic.MANOR.value,
                    },
                    {
                        MapKeys.HISTORIC: Historic.CASTLE.value,
                        MapKeys.CASTLE_TYPE: CastleType.MANOR.value,
                    }
                ]
            },
            HistoricalObjects.MEMORIAL.value: {
                FIELD_TITLE: 'Memorial (standard size)',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.HISTORIC: Historic.MEMORIAL.value,
                    }
                ]
            },
            HistoricalObjects.MONUMENT.value: {
                FIELD_TITLE: 'Monument',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.HISTORIC: Historic.MONUMENT.value,
                    }
                ]
            },
            HistoricalObjects.OBELISK.value: {
                FIELD_TITLE: 'Obelisk',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.MAN_MADE: ManMade.OBELISK.value,
                    }
                ]
            },
            HistoricalObjects.PALACE.value: {
                FIELD_TITLE: 'Palace / Stately home',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.HISTORIC: Historic.CASTLE.value,
                        MapKeys.CASTLE_TYPE: [
                            CastleType.PALACE.value,
                            CastleType.STATELY.value,
                        ],
                    }
                ]
            },
            HistoricalObjects.PLAQUE.value: {
                FIELD_TITLE: 'Memorial plaque / Blue plaque',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.HISTORIC: Historic.MEMORIAL.value,
                        MapKeys.MEMORIAL: [
                            Memorial.PLAQUE.value,
                            Memorial.BLUE_PLAQUE.value,
                        ]
                    }
                ]
            },
            HistoricalObjects.STATUE.value: {
                FIELD_TITLE: 'Statue',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.HISTORIC: Historic.MEMORIAL.value,
                        MapKeys.MEMORIAL: Memorial.STATUE.value,
                    },
                    {
                        MapKeys.TOURISM: Tourism.ARTWORK.value,
                        MapKeys.ARTWORK_TYPE: ArtworkType.STATUE.value,
                    }
                ]
            },
            HistoricalObjects.STONE.value: {
                FIELD_TITLE: 'Memorial as a stone',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.HISTORIC: Historic.MEMORIAL.value,
                        MapKeys.MEMORIAL: Memorial.STONE.value,
                    }
                ]
            },
        },
        MapSymbols.LEISURE_RECREATION_SPORTS: {
            LeisureRecreationSports.BEACH_RESORT.value: {
                FIELD_TITLE: 'A managed beach',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.LEISURE: Leisure.BEACH_RESORT.value,
                    }
                ]
            },
            LeisureRecreationSports.BOWLING_ALLEY.value: {
                FIELD_TITLE: 'Bowling centre',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.LEISURE: Leisure.BOWLING_ALLEY.value,
                    }
                ]
            },
            LeisureRecreationSports.DOG_PARK.value: {
                FIELD_TITLE: 'Dog park',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.LEISURE: Leisure.DOG_PARK.value,
                    }
                ]
            },
            LeisureRecreationSports.FISHING.value: {
                FIELD_TITLE: 'A public place for fishing',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.LEISURE: Leisure.FISHING.value,
                    }
                ]
            },
            LeisureRecreationSports.FITNESS.value: {
                FIELD_TITLE: 'Fitness centre / fitness station',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.LEISURE: Leisure.FITNESS_CENTRE.value,
                    },
                    {
                        MapKeys.LEISURE: Leisure.FITNESS_STATION.value,
                    }
                ]
            },
            LeisureRecreationSports.GOLF_COURSE.value: {
                FIELD_TITLE: 'Golf course',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.LEISURE: Leisure.GOLF_COURSE.value,
                    }
                ]
            },
            LeisureRecreationSports.LEISURE_DANCE.value: {
                FIELD_TITLE: 'Dance venue or dance hall',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.LEISURE: Leisure.DANCE.value,
                    }
                ]
            },
            LeisureRecreationSports.LEISURE_GOLF_PIN.value: {
                FIELD_TITLE: 'Hole of a golf course',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.GOLF: Golf.PIN.value,
                    }
                ]
            },
            LeisureRecreationSports.MASSAGE.value: {
                FIELD_TITLE: 'Massage shop',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.SHOP: Shop.MASSAGE.value,
                    }
                ]
            },
            LeisureRecreationSports.MINIATURE_GOLF.value: {
                FIELD_TITLE: 'Miniature golf course',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.LEISURE: Leisure.MINIATURE_GOLF.value,
                    }
                ]
            },
            LeisureRecreationSports.PLAYGROUND.value: {
                FIELD_TITLE: 'Playground',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.LEISURE: Leisure.PLAYGROUND.value,
                    }
                ]
            },
            LeisureRecreationSports.PUBLIC_BATH.value: {
                FIELD_TITLE: 'A location where the public may bathe in common',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.AMENITY: Amenity.PUBLIC_BATH.value,
                    }
                ]
            },
            LeisureRecreationSports.SAUNA.value: {
                FIELD_TITLE: 'Sauna',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.LEISURE: Leisure.SAUNA.value,
                    }
                ]
            },
            LeisureRecreationSports.SWIMMING.value: {
                FIELD_TITLE: 'Water park / swimming area / (indoor or outdoor) swimming pool',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.LEISURE: Leisure.WATER_PARK.value,
                    },
                    {
                        MapKeys.LEISURE: Leisure.SWIMMING_AREA.value,
                    },
                    {
                        MapKeys.LEISURE: Leisure.SPORTS_CENTRE.value,
                        MapKeys.SPORT: Sport.SWIMMING.value,
                    }
                ]
            },
        },
        MapSymbols.WASTE_MANAGEMENT: {
            WasteManagement.EXCREMENT_BAGS.value: {
                FIELD_TITLE: 'Excrement bag dispenser',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.AMENITY: Amenity.VENDING_MACHINE.value,
                        MapKeys.VENDING: Vending.EXCREMENT_BAGS.value,
                    }
                ]
            },
            WasteManagement.RECYCLING.value: {
                FIELD_TITLE: 'Recycling container or recycling centre',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.AMENITY: Amenity.RECYCLING.value,
                    }
                ]
            },
            WasteManagement.TOILETS.value: {
                FIELD_TITLE: 'Public toilets',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.AMENITY: Amenity.TOILETS.value,
                    }
                ]
            },
            WasteManagement.WASTE_BASKET.value: {
                FIELD_TITLE: '	Waste basket',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.AMENITY: Amenity.WASTE_BASKET.value,
                    }
                ]
            },
            WasteManagement.WASTE_DISPOSAL.value: {
                FIELD_TITLE: 'Disposal bin (medium size), for bagged up household or industrial waste',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.AMENITY: Amenity.WASTE_DISPOSAL.value,
                    }
                ]
            },
        },
        MapSymbols.OUTDOOR: {
            Outdoor.BBQ.value: {
                FIELD_TITLE: 'Barbeque',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.AMENITY: Amenity.BBQ.value,
                    }
                ]
            },
            Outdoor.BENCH.value: {
                FIELD_TITLE: 'Bench',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.AMENITY: Amenity.BENCH.value,
                    }
                ]
            },
            Outdoor.BIRD_HIDE.value: {
                FIELD_TITLE: 'Bird hide',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.LEISURE: Leisure.BIRD_HIDE.value,
                    }
                ]
            },
            Outdoor.CAMPING.value: {
                FIELD_TITLE: '	Campsite, campground',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.TOURISM: Tourism.CAMP_SITE.value,
                    }
                ]
            },
            Outdoor.CARAVAN.value: {
                FIELD_TITLE: 'Caravan site, caravan park, RV park',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.TOURISM: Tourism.CARAVAN_SITE.value,
                    }
                ]
            },
            Outdoor.DRINKING_WATER.value: {
                FIELD_TITLE: 'Drinking water, bubbler, drinking fountain',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.AMENITY: Amenity.DRINKING_WATER.value,
                    }
                ]
            },
            Outdoor.FIREPIT.value: {
                FIELD_TITLE: 'Fireplace',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.LEISURE: Leisure.FIREPIT.value,
                    }
                ]
            },
            Outdoor.FOUNTAIN.value: {
                FIELD_TITLE: 'Fountain (recreational/decorational)',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.AMENITY: Amenity.FOUNTAIN.value,
                    }
                ]
            },
            Outdoor.PICNIC_SITE.value: {
                FIELD_TITLE: 'Picnic site',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.TOURISM: Tourism.PICNIC_SITE.value,
                    }
                ]
            },
            Outdoor.SHELTER.value: {
                FIELD_TITLE: 'Shelter (e.g. weather shelter)',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.AMENITY: Amenity.SHELTER.value,
                    }
                ]
            },
            Outdoor.SHOWER.value: {
                FIELD_TITLE: 'Shower',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.AMENITY: Amenity.SHOWER.value,
                    }
                ]
            },
            Outdoor.TABLE.value: {
                FIELD_TITLE: '	Picnic table',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.LEISURE: Leisure.PICNIC_TABLE.value,
                    }
                ]
            },
        },
        MapSymbols.TOURISM_ACCOMMODATION: {
            TourismAccommodation.ALPINEHUT.value: {
                FIELD_TITLE: 'Alpine hut',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.TOURISM: Tourism.ALPINE_HUT.value,
                    }
                ]
            },
            TourismAccommodation.APARTMENT.value: {
                FIELD_TITLE: 'Apartment',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.TOURISM: Tourism.APARTMENT.value,
                    }
                ]
            },
            TourismAccommodation.AUDIOGUIDE.value: {
                FIELD_TITLE: 'Audioguide',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.TOURISM: Tourism.INFORMATION.value,
                        MapKeys.INFORMATION: Information.AUDIOGUIDE.value,
                    }
                ]
            },
            TourismAccommodation.BOARD.value: {
                FIELD_TITLE: 'Information board',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.TOURISM: Tourism.INFORMATION.value,
                        MapKeys.INFORMATION: Information.BOARD.value,
                    }
                ]
            },
            TourismAccommodation.CHALET.value: {
                FIELD_TITLE: 'Chalet (holiday cottage)',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.TOURISM: Tourism.CHALET.value,
                    }
                ]
            },
            TourismAccommodation.GUIDEPOST.value: {
                FIELD_TITLE: 'Guidepost',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.TOURISM: Tourism.INFORMATION.value,
                        MapKeys.INFORMATION: Information.GUIDEPOST.value,
                    }
                ]
            },
            TourismAccommodation.HOSTEL.value: {
                FIELD_TITLE: 'Hostel',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.TOURISM: Tourism.HOSTEL.value,
                    }
                ]
            },
            TourismAccommodation.HOTEL.value: {
                FIELD_TITLE: 'Hotel',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.TOURISM: Tourism.HOTEL.value,
                    }
                ]
            },
            TourismAccommodation.MAP.value: {
                FIELD_TITLE: 'Board with a map / Information map as 3D-model',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.TOURISM: Tourism.INFORMATION.value,
                        MapKeys.INFORMATION: Information.MAP.value,
                    },
                    {
                        MapKeys.TOURISM: Tourism.INFORMATION.value,
                        MapKeys.INFORMATION: Information.TACTILE_MAP.value,
                    }
                ]
            },
            TourismAccommodation.MOTEL.value: {
                FIELD_TITLE: 'Motel',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.TOURISM: Tourism.MOTEL.value,
                    }
                ]
            },
            TourismAccommodation.OFFICE.value: {
                FIELD_TITLE: 'Tourism-Information',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.TOURISM: Tourism.INFORMATION.value,
                        MapKeys.INFORMATION: Information.OFFICE.value,
                    }
                ]
            },
            TourismAccommodation.TERMINAL.value: {
                FIELD_TITLE: 'Information terminal',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.TOURISM: Tourism.INFORMATION.value,
                        MapKeys.INFORMATION: Information.TERMINAL.value,
                    }
                ]
            },
            TourismAccommodation.TOURISM_GUEST_HOUSE.value: {
                FIELD_TITLE: 'Guest house',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.TOURISM: Tourism.GUEST_HOUSE.value,
                    }
                ]
            },
            TourismAccommodation.VIEWPOINT.value: {
                FIELD_TITLE: 'Viewpoint',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.TOURISM: Tourism.VIEWPOINT.value,
                    }
                ]
            },
            TourismAccommodation.WILDERNESS_HUT.value: {
                FIELD_TITLE: 'Wilderness hut',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.TOURISM: Tourism.WILDERNESS_HUT.value,
                    }
                ]
            },
        },
        MapSymbols.FINANCE: {
            Finance.ATM.value: {
                FIELD_TITLE: 'ATM or cash point',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.AMENITY: Amenity.ATM.value,
                    }
                ]
            },
            Finance.BANK.value: {
                FIELD_TITLE: 'Bank',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.AMENITY: Amenity.BANK.value,
                    }
                ]
            },
            Finance.BUREAU_DE_CHANGE.value: {
                FIELD_TITLE: 'Bureau de change',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.AMENITY: Amenity.BUREAU_DE_CHANGE.value,
                    }
                ]
            },
        },
        MapSymbols.HEALTH_CARE: {
            HealthCare.DENTIST.value: {
                FIELD_TITLE: 'Dentist',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.AMENITY: Amenity.DENTIST.value,
                    }
                ]
            },
            HealthCare.DOCTORS.value: {
                FIELD_TITLE: 'Surgery or a small clinic (for ambulant treatment) / Doctor\'s practice',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.AMENITY: Amenity.CLINIC.value,
                    },
                    {
                        MapKeys.AMENITY: Amenity.DOCTORS.value,
                    }
                ]
            },
            HealthCare.HOSPITAL.value: {
                FIELD_TITLE: 'Hospital (for stationary treatment)',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.AMENITY: Amenity.HOSPITAL.value,
                    }
                ]
            },
            HealthCare.PHARMACY.value: {
                FIELD_TITLE: 'Pharmacy',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.AMENITY: Amenity.PHARMACY.value,
                    }
                ]
            },
            HealthCare.VETERINARY.value: {
                FIELD_TITLE: 'Veterinary',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.AMENITY: Amenity.VETERINARY.value,
                    }
                ]
            },
        },
        MapSymbols.COMMUNICATION: {
            Communication.EMERGENCY_PHONE.value: {
                FIELD_TITLE: 'Emergency phone',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.EMERGENCY: Emergency.PHONE.value,
                    }
                ]
            },
            Communication.PARCEL_LOCKER.value: {
                FIELD_TITLE: 'Machine for picking up and sending parcels',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.AMENITY: Amenity.PARCEL_LOCKER.value,
                    }
                ]
            },
            Communication.POST_BOX.value: {
                FIELD_TITLE: 'Post box',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.AMENITY: Amenity.POST_BOX.value,
                    }
                ]
            },
            Communication.POST_OFFICE.value: {
                FIELD_TITLE: 'Post office',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.AMENITY: Amenity.POST_OFFICE.value,
                    }
                ]
            },
            Communication.TELEPHONE.value: {
                FIELD_TITLE: 'Public telephone',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.AMENITY: Amenity.TELEPHONE.value,
                    }
                ]
            },
        },
        MapSymbols.TRANSPORTATION: {
            Transportation.AERODROME.value: {
                FIELD_TITLE: '	Airport',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.AEROWAY: Aeroway.AERODROME.value,
                    }
                ]
            },
            Transportation.AMENITY_BUS_STATION.value: {
                FIELD_TITLE: 'Bus station',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.AMENITY: Amenity.BUS_STATION.value,
                    }
                ]
            },
            Transportation.BICYCLE_REPAIR_STATION.value: {
                FIELD_TITLE: 'Bicycle repair station',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.AMENITY: Amenity.BICYCLE_REPAIR_STATION.value,
                    }
                ]
            },
            Transportation.BOAT_RENTAL.value: {
                FIELD_TITLE: 'Boat rental',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.AMENITY: Amenity.BOAT_RENTAL.value,
                    }
                ]
            },
            Transportation.BUS_STOP.value: {
                FIELD_TITLE: 'Bus stop',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.HIGHWAY: Highway.BUS_STOP.value,
                    }
                ]
            },
            Transportation.CHARGING_STATION.value: {
                FIELD_TITLE: 'Charging station',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.AMENITY: Amenity.CHARGING_STATION.value,
                    }
                ]
            },
            Transportation.ELEVATOR.value: {
                FIELD_TITLE: 'Elevator',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.HIGHWAY: Highway.ELEVATOR.value,
                    }
                ]
            },
            Transportation.FERRY.value: {
                FIELD_TITLE: 'Ferry terminal',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.AMENITY: Amenity.FERRY_TERMINAL.value,
                    }
                ]
            },
            Transportation.FUEL.value: {
                FIELD_TITLE: 'Gas station or petrol station or similar',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.AMENITY: Amenity.FUEL.value,
                    }
                ]
            },
            Transportation.HELIPAD.value: {
                FIELD_TITLE: 'Helipad',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.AEROWAY: Aeroway.HELIPAD.value,
                    }
                ]
            },
            Transportation.PARKING.value: {
                FIELD_TITLE: 'Car parking',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.AMENITY: Amenity.PARKING.value,
                    }
                ]
            },
            Transportation.PARKING_BICYCLE.value: {
                FIELD_TITLE: 'Bicycle parking',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.AMENITY: Amenity.BICYCLE_PARKING.value,
                    }
                ]
            },
            Transportation.PARKING_ENTRANCE.value: {
                FIELD_TITLE: 'Underground parking entrance',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.AMENITY: Amenity.PARKING_ENTRANCE.value,
                        MapKeys.PARKING: Parking.UNDERGROUND.value,
                    }
                ]
            },
            Transportation.PARKING_ENTRANCE_MULTI_STOREY.value: {
                FIELD_TITLE: 'Multi-storey parking entrance',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.AMENITY: Amenity.PARKING_ENTRANCE.value,
                        MapKeys.PARKING: Parking.MULTI_STOREY.value,
                    }
                ]
            },
            Transportation.PARKING_MOTORCYCLE.value: {
                FIELD_TITLE: 'Motorcycle parking',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.AMENITY: Amenity.MOTORCYCLE_PARKING.value,
                    }
                ]
            },
            Transportation.PARKING_SUBTLE.value: {
                FIELD_TITLE: 'Car parking on the carriageway / Car parking adjacent to the carriageway',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.AMENITY: Amenity.PARKING.value,
                        MapKeys.PARKING: [
                            Parking.LANE.value,
                            Parking.STREET_SIDE.value,
                        ],
                    }
                ]
            },
            Transportation.PARKING_TICKETS.value: {
                FIELD_TITLE: 'A machine selling tickets for parking',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.AMENITY: Amenity.VENDING_MACHINE.value,
                        MapKeys.VENDING: Vending.PARKING_TICKETS.value,
                    }
                ]
            },
            Transportation.PUBLIC_TRANSPORT_TICKETS.value: {
                FIELD_TITLE: 'A machine vending bus, tram, train... tickets',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.AMENITY: Amenity.VENDING_MACHINE.value,
                        MapKeys.VENDING: Vending.PUBLIC_TRANSPORT_TICKETS.value,
                    }
                ]
            },
            Transportation.RAILWAY_TRAM_STOP_MAPNIK.value: {
                FIELD_TITLE: 'Railway station / Railway stop point / Tram stop point / Aerialway station',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.RAILWAY: Railway.STATION.value,
                    },
                    {
                        MapKeys.RAILWAY: Railway.HALT.value,
                    },
                    {
                        MapKeys.RAILWAY: Railway.TRAM_STOP.value,
                    },
                    {
                        MapKeys.AERIALWAY: Aerialway.STATION.value,
                    }
                ]
            },
            Transportation.RENTAL_BICYCLE.value: {
                FIELD_TITLE: 'Bicycle-sharing/rental station',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.AMENITY: Amenity.BICYCLE_RENTAL.value,
                    }
                ]
            },
            Transportation.RENTAL_CAR.value: {
                FIELD_TITLE: 'Rent a car',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.AMENITY: Amenity.CAR_RENTAL.value,
                    }
                ]
            },
            Transportation.SUBWAY_ENTRANCE.value: {
                FIELD_TITLE: 'Subway entrance',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.RAILWAY: Railway.SUBWAY_ENTRANCE.value,
                    }
                ]
            },
            Transportation.TAXI.value: {
                FIELD_TITLE: 'Taxi rank',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.AMENITY: Amenity.TAXI.value,
                    }
                ]
            },
            Transportation.TRANSPORT_SLIPWAY.value: {
                FIELD_TITLE: 'Slipway for boats',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.LEISURE: Leisure.SLIPWAY.value,
                    }
                ]
            },
        },
        MapSymbols.ROAD_FEATURES: {
            RoadFeatures.BARRIER.value: {
                FIELD_TITLE: 'Barriers (bollard / large block / turnstile / log)',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.BARRIER: Barrier.BOLLARD.value,
                    },
                    {
                        MapKeys.BARRIER: Barrier.BLOCK.value,
                    },
                    {
                        MapKeys.BARRIER: Barrier.TURNSTILE.value,
                    },
                    {
                        MapKeys.BARRIER: Barrier.LOG.value,
                    }
                ]
            },
            RoadFeatures.BARRIER_CATTLE_GRID.value: {
                FIELD_TITLE: 'Cattle grid',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.BARRIER: Barrier.CATTLE_GRID.value,
                    }
                ]
            },
            RoadFeatures.BARRIER_GATE.value: {
                FIELD_TITLE: 'Gate',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.BARRIER: Barrier.GATE.value,
                    }
                ]
            },
            RoadFeatures.BARRIER_STILE.value: {
                FIELD_TITLE: 'Stile',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.BARRIER: Barrier.STILE.value,
                    }
                ]
            },
            RoadFeatures.CYCLE_BARRIER.value: {
                FIELD_TITLE: '	Barriers to bicycle traffic',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.BARRIER: Barrier.CYCLE_BARRIER.value,
                    }
                ]
            },
            RoadFeatures.DAM_NODE.value: {
                FIELD_TITLE: 'Dam',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.WATERWAY: Waterway.DAM.value,
                    }
                ]
            },
            RoadFeatures.FORD.value: {
                FIELD_TITLE: 'Ford / Ford with stepping stones',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.FORD: Ford.YES.value,
                    },
                    {
                        MapKeys.FORD: Ford.STEPPING_STONES.value,
                    }
                ]
            },
            RoadFeatures.FULL_HEIGHT_TURNSTILE.value: {
                FIELD_TITLE: 'A full-height turnstile',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.BARRIER: Barrier.FULL_HEIGHT_TURNSTILE.value,
                    }
                ]
            },
            RoadFeatures.HIGHWAY_MINI_ROUNDABOUT.value: {
                FIELD_TITLE: 'Mini roundabout',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.HIGHWAY: Highway.MINI_ROUNDABOUT.value,
                    }
                ]
            },
            RoadFeatures.KISSING_GATE.value: {
                FIELD_TITLE: '	A gate which allows people to cross, but not livestock.',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.BARRIER: Barrier.KISSING_GATE.value,
                    }
                ]
            },
            RoadFeatures.LEVEL_CROSSING.value: {
                FIELD_TITLE: 'Railroad crossing, zoom <=15',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.RAILWAY: Railway.LEVEL_CROSSING.value,
                    },
                    {
                        MapKeys.RAILWAY: Railway.CROSSING.value,
                    }
                ]
            },
            RoadFeatures.LEVEL_CROSSING2.value: {
                FIELD_TITLE: 'Railroad crossing, zoom >=16',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.RAILWAY: Railway.LEVEL_CROSSING.value,
                    },
                    {
                        MapKeys.RAILWAY: Railway.CROSSING.value,
                    }
                ]
            },
            RoadFeatures.LIFTGATE.value: {
                FIELD_TITLE: 'Boom barrier',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.BARRIER: Barrier.LIFT_GATE.value,
                    },
                    {
                        MapKeys.BARRIER: Barrier.SWING_GATE.value,
                    }
                ]
            },
            RoadFeatures.LOCK_GATE_NODE.value: {
                FIELD_TITLE: '	Gate of a lock',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.WATERWAY: Waterway.LOCK_GATE.value,
                    }
                ]
            },
            RoadFeatures.MOTORCYCLE_BARRIER.value: {
                FIELD_TITLE: 'Motorcycle barrier',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.BARRIER: Barrier.MOTORCYCLE_BARRIER.value,
                    }
                ]
            },
            RoadFeatures.MOUNTAIN_PASS.value: {
                FIELD_TITLE: '	Saddle on a course of a way',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.MOUNTAIN_PASS: MountainPass.YES.value,
                    }
                ]
            },
            RoadFeatures.ONEWAY.value: {
                FIELD_TITLE: 'One-way',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.ONEWAY: Oneway.YES.value,
                    }
                ]
            },
            RoadFeatures.TOLL_BOOTH.value: {
                FIELD_TITLE: 'Tollbooth',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.BARRIER: Barrier.TOLL_BOOTH.value,
                    }
                ]
            },
            RoadFeatures.TRAFFIC_LIGHT.value: {
                FIELD_TITLE: 'Traffic lights',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.HIGHWAY: Highway.TRAFFIC_SIGNALS.value,
                    }
                ]
            },
            RoadFeatures.TURNING_CIRCLE_ON_HIGHWAY_TRACK.value: {
                FIELD_TITLE: 'Turning circle at agricultural or forestry roads',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.HIGHWAY: [
                            Highway.TURNING_CIRCLE.value,
                            Highway.TRACK.value,
                        ]
                    }
                ]
            },
            RoadFeatures.WEIR_NODE.value: {
                FIELD_TITLE: 'Weir',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.WATERWAY: Waterway.WEIR.value,
                    }
                ]
            },
        },
        MapSymbols.NATURE: {
            Nature.CAVE.value: {
                FIELD_TITLE: 'Cave entrance',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.NATURAL: Natural.CAVE_ENTRANCE.value,
                    }
                ]
            },
            Nature.PEAK.value: {
                FIELD_TITLE: 'Peak, summit, etc.',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.NATURAL: Natural.PEAK.value,
                    }
                ]
            },
            Nature.SADDLE.value: {
                FIELD_TITLE: 'Topographic saddle',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.NATURAL: Natural.SADDLE.value,
                    }
                ]
            },
            Nature.SPRING.value: {
                FIELD_TITLE: 'Spring',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.NATURAL: Natural.SPRING.value,
                    }
                ]
            },
            Nature.TREE.value: {
                FIELD_TITLE: 'Tree',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.NATURAL: Natural.TREE.value,
                    }
                ]
            },
            Nature.VOLCANO.value: {
                FIELD_TITLE: 'Volcano',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.NATURAL: Natural.VOLCANO.value,
                    }
                ]
            },
            Nature.WATERFALL.value: {
                FIELD_TITLE: 'Waterfall',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.WATERWAY: Waterway.WATERFALL.value,
                    }
                ]
            },
        },
        MapSymbols.ADMINISTRATIVE_FACILITIES: {
            AdministrativeFacilities.COURTHOUSE.value: {
                FIELD_TITLE: 'Court house',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.AMENITY: Amenity.COURTHOUSE.value,
                    }
                ]
            },
            AdministrativeFacilities.DIPLOMATIC.value: {
                FIELD_TITLE: 'Embassy',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.OFFICE: Office.DIPLOMATIC.value,
                        MapKeys.DIPLOMATIC: Diplomatic.EMBASSY.value,
                    }
                ]
            },
            AdministrativeFacilities.FIRE_STATION.value: {
                FIELD_TITLE: '	Fire station',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.AMENITY: Amenity.FIRE_STATION.value,
                    }
                ]
            },
            AdministrativeFacilities.OFFICE_DIPLOMATIC_CONSULATE.value: {
                FIELD_TITLE: 'Consulate',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.OFFICE: Office.DIPLOMATIC.value,
                        MapKeys.DIPLOMATIC: Diplomatic.CONSULATE.value,
                    }
                ]
            },
            AdministrativeFacilities.POLICE.value: {
                FIELD_TITLE: 'Police station',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.AMENITY: Amenity.POLICE.value,
                    }
                ]
            },
            AdministrativeFacilities.PRISON.value: {
                FIELD_TITLE: 'Prison',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.AMENITY: Amenity.PRISON.value,
                    }
                ]
            },
            AdministrativeFacilities.SOCIAL_FACILITY.value: {
                FIELD_TITLE: 'Social facility',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.AMENITY: Amenity.SOCIAL_FACILITY.value,
                    }
                ]
            },
            AdministrativeFacilities.TOWN_HALL.value: {
                FIELD_TITLE: 'Townhall',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.AMENITY: Amenity.TOWNHALL.value,
                    }
                ]
            },
        },
        MapSymbols.RELIGIOUS_PLACE: {
            ReligiousPlace.BUDDHIST.value: {
                FIELD_TITLE: 'Buddhist',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.AMENITY: Amenity.PLACE_OF_WORSHIP.value,
                        MapKeys.RELIGION: Religion.BUDDHIST.value,
                    }
                ]
            },
            ReligiousPlace.CHRISTIAN.value: {
                FIELD_TITLE: '	Christian (except Jehovah\'s Witnesses, La Luz del Mundo, Iglesia ni Cristo and Mormons)',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.AMENITY: Amenity.PLACE_OF_WORSHIP.value,
                        MapKeys.RELIGION: Religion.CHRISTIAN.value,
                    }
                ]
            },
            ReligiousPlace.HINDUIST.value: {
                FIELD_TITLE: 'Hindu',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.AMENITY: Amenity.PLACE_OF_WORSHIP.value,
                        MapKeys.RELIGION: Religion.HINDU.value,
                    }
                ]
            },
            ReligiousPlace.JEWISH.value: {
                FIELD_TITLE: 'Jewish',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.AMENITY: Amenity.PLACE_OF_WORSHIP.value,
                        MapKeys.RELIGION: Religion.JEWISH.value,
                    }
                ]
            },
            ReligiousPlace.MUSLIM.value: {
                FIELD_TITLE: 'Muslim',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.AMENITY: Amenity.PLACE_OF_WORSHIP.value,
                        MapKeys.RELIGION: Religion.MUSLIM.value,
                    }
                ]
            },
            ReligiousPlace.PLACE_OF_WORSHIP.value: {
                FIELD_TITLE: 'Unspecified or other religion',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.AMENITY: Amenity.PLACE_OF_WORSHIP.value,
                        MapKeys.RELIGION: '*',
                    }
                ]
            },
            ReligiousPlace.SHINTOIST.value: {
                FIELD_TITLE: 'Shinto',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.AMENITY: Amenity.PLACE_OF_WORSHIP.value,
                        MapKeys.RELIGION: Religion.SHINTO.value,
                    }
                ]
            },
            ReligiousPlace.SIKHIST.value: {
                FIELD_TITLE: 'Sikh',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.AMENITY: Amenity.PLACE_OF_WORSHIP.value,
                        MapKeys.RELIGION: Religion.SIKH.value,
                    }
                ]
            },
            ReligiousPlace.TAOIST.value: {
                FIELD_TITLE: 'Taoist',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.AMENITY: Amenity.PLACE_OF_WORSHIP.value,
                        MapKeys.RELIGION: Religion.TAOIST.value,
                    }
                ]
            },
        },
        MapSymbols.SHOPS_SERVICES: {
            ShopsServices.ALCOHOL.value: {
                FIELD_TITLE: 'Shop selling alcohol / Wine shop',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.SHOP: Shop.ALCOHOL.value,
                    },
                    {
                        MapKeys.SHOP: Shop.WINE.value,
                    }
                ]
            },
            ShopsServices.ART.value: {
                FIELD_TITLE: 'Art shop',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.SHOP: Shop.ART.value,
                    }
                ]
            },
            ShopsServices.BAG.value: {
                FIELD_TITLE: 'Bag shop',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.SHOP: Shop.BAG.value,
                    }
                ]
            },
            ShopsServices.BAKERY.value: {
                FIELD_TITLE: 'Bakery',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.SHOP: Shop.BAKERY.value,
                    }
                ]
            },
            ShopsServices.BEAUTY.value: {
                FIELD_TITLE: 'Beauty services except hairdressing',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.SHOP: Shop.BEAUTY.value,
                    }
                ]
            },
            ShopsServices.BED.value: {
                FIELD_TITLE: 'Shop selling mattresses',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.SHOP: Shop.BED.value,
                    }
                ]
            },
            ShopsServices.BEVERAGES.value: {
                FIELD_TITLE: 'Shop selling beverages',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.SHOP: Shop.BEVERAGES.value,
                    }
                ]
            },
            ShopsServices.BICYCLE.value: {
                FIELD_TITLE: 'Bicycle shop, retail, repair and/or rental',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.SHOP: Shop.BICYCLE.value,
                    }
                ]
            },
            ShopsServices.BOOKMAKER.value: {
                FIELD_TITLE: 'Bookmaker',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.SHOP: Shop.BOOKMAKER.value,
                    }
                ]
            },
            ShopsServices.BOOKS.value: {
                FIELD_TITLE: 'Book store',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.SHOP: Shop.BOOKS.value,
                    }
                ]
            },
            ShopsServices.BUTCHER.value: {
                FIELD_TITLE: 'Butcher',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.SHOP: Shop.BUTCHER.value,
                    }
                ]
            },
            ShopsServices.CAR_PARTS.value: {
                FIELD_TITLE: 'Car parts shop',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.SHOP: Shop.CAR_PARTS.value,
                    }
                ]
            },
            ShopsServices.CAR_REPAIR.value: {
                FIELD_TITLE: 'Car repair service',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.SHOP: Shop.CAR_REPAIR.value,
                    }
                ]
            },
            ShopsServices.CAR_WASH.value: {
                FIELD_TITLE: 'Car wash',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.AMENITY: Amenity.CAR_WASH.value,
                    }
                ]
            },
            ShopsServices.CARPET.value: {
                FIELD_TITLE: 'Shop selling carpets',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.SHOP: Shop.CARPET.value,
                    }
                ]
            },
            ShopsServices.CHARITY.value: {
                FIELD_TITLE: 'Charity store',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.SHOP: Shop.CHARITY.value,
                    }
                ]
            },
            ShopsServices.CHEMIST.value: {
                FIELD_TITLE: 'Chemist',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.SHOP: Shop.CHEMIST.value,
                    }
                ]
            },
            ShopsServices.CLOTHES.value: {
                FIELD_TITLE: 'Clothes shop / Fashion shop',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.SHOP: Shop.CLOTHES.value,
                    },
                    {
                        MapKeys.SHOP: Shop.FASHION.value,
                    }
                ]
            },
            ShopsServices.COFFEE.value: {
                FIELD_TITLE: 'Coffee shop',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.SHOP: Shop.COFFEE.value,
                    }
                ]
            },
            ShopsServices.COMPUTER.value: {
                FIELD_TITLE: 'Computer store',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.SHOP: Shop.COMPUTER.value,
                    }
                ]
            },
            ShopsServices.CONFECTIONERY.value: {
                FIELD_TITLE: 'Confectionery / Chocolate shop / Patisserie',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.SHOP: Shop.CONFECTIONERY.value,
                    },
                    {
                        MapKeys.SHOP: Shop.CHOCOLATE.value,
                    },
                    {
                        MapKeys.SHOP: Shop.PASTRY.value,
                    }
                ]
            },
            ShopsServices.CONVENIENCE.value: {
                FIELD_TITLE: 'Convenience store',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.SHOP: Shop.CONVENIENCE.value,
                    }
                ]
            },
            ShopsServices.COPYSHOP.value: {
                FIELD_TITLE: 'Copy shop',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.SHOP: Shop.COPYSHOP.value,
                    }
                ]
            },
            ShopsServices.DAIRY.value: {
                FIELD_TITLE: 'Shop selling dairy products',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.SHOP: Shop.DAIRY.value,
                    }
                ]
            },
            ShopsServices.DELI.value: {
                FIELD_TITLE: 'Shop selling delicatessen (gourmet foods)',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.SHOP: Shop.DELI.value,
                    }
                ]
            },
            ShopsServices.DEPARTMENT_STORE.value: {
                FIELD_TITLE: 'Department store',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.SHOP: Shop.DEPARTMENT_STORE.value,
                    }
                ]
            },
            ShopsServices.DOITYOURSELF.value: {
                FIELD_TITLE: 'Do-It-Yourself store / Hardware store',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.SHOP: Shop.DOITYOURSELF.value,
                    },
                    {
                        MapKeys.SHOP: Shop.HARDWARE.value,
                    }
                ]
            },
            ShopsServices.ELECTRONICS.value: {
                FIELD_TITLE: 'Shop selling consumer electronics',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.SHOP: Shop.ELECTRONICS.value,
                    }
                ]
            },
            ShopsServices.FABRIC.value: {
                FIELD_TITLE: 'Shop that sells fabric',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.SHOP: Shop.FABRIC.value,
                    }
                ]
            },
            ShopsServices.FLORIST.value: {
                FIELD_TITLE: 'Florist',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.SHOP: Shop.FLORIST.value,
                    }
                ]
            },
            ShopsServices.FURNITURE.value: {
                FIELD_TITLE: 'Furniture store',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.SHOP: Shop.FURNITURE.value,
                    }
                ]
            },
            ShopsServices.GARDEN_CENTRE.value: {
                FIELD_TITLE: 'Garden centre',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.SHOP: Shop.GARDEN_CENTRE.value,
                    }
                ]
            },
            ShopsServices.GIFT.value: {
                FIELD_TITLE: 'Gift or souvenier shop',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.SHOP: Shop.GIFT.value,
                    }
                ]
            },
            ShopsServices.GREENGROCER.value: {
                FIELD_TITLE: 'Greengrocer / Farm shop',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.SHOP: Shop.GREENGROCER.value,
                    },
                    {
                        MapKeys.SHOP: Shop.FARM.value,
                    }
                ]
            },
            ShopsServices.HAIRDRESSER.value: {
                FIELD_TITLE: 'Hairdresser\'s and/or barber\'s',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.SHOP: Shop.HAIRDRESSER.value,
                    }
                ]
            },
            ShopsServices.HEARING_AIDS.value: {
                FIELD_TITLE: 'Shop selling hearing aids',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.SHOP: Shop.HEARING_AIDS.value,
                    }
                ]
            },
            ShopsServices.HIFI.value: {
                FIELD_TITLE: 'Hi-fi store',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.SHOP: Shop.HIFI.value,
                    }
                ]
            },
            ShopsServices.HOUSEWARE.value: {
                FIELD_TITLE: 'Shop selling houseware',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.SHOP: Shop.HOUSEWARE.value,
                    }
                ]
            },
            ShopsServices.INTERIOR_DECORATION.value: {
                FIELD_TITLE: 'Shop selling interior decorations',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.SHOP: Shop.INTERIOR_DECORATION.value,
                    }
                ]
            },
            ShopsServices.JEWELLERY.value: {
                FIELD_TITLE: 'Jewellery',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.SHOP: Shop.JEWELRY.value,
                    }
                ]
            },
            ShopsServices.LAUNDRY.value: {
                FIELD_TITLE: 'Laundry shop / Clothes dry cleaning service',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.SHOP: Shop.LAUNDRY.value,
                    },
                    {
                        MapKeys.SHOP: Shop.DRY_CLEANING.value,
                    }
                ]
            },
            ShopsServices.MARKETPLACE.value: {
                FIELD_TITLE: 'Marketplace',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.AMENITY: Amenity.MARKETPLACE.value,
                    }
                ]
            },
            ShopsServices.MEDICAL_SUPPLY.value: {
                FIELD_TITLE: 'A store where you can buy medical equipment',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.SHOP: Shop.MEDICAL_SUPPLY.value,
                    }
                ]
            },
            ShopsServices.MOBILE_PHONE.value: {
                FIELD_TITLE: 'Shop selling mobile phones and accessories',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.SHOP: Shop.MOBILE_PHONE.value,
                    }
                ]
            },
            ShopsServices.MUSICAL_INSTRUMENT.value: {
                FIELD_TITLE: 'Shop selling musical instruments',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.SHOP: Shop.MUSICAL_INSTRUMENT.value,
                    }
                ]
            },
            ShopsServices.NEWSAGENT.value: {
                FIELD_TITLE: 'Kiosk / Newsstand',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.SHOP: Shop.KIOSK.value,
                    },
                    {
                        MapKeys.SHOP: Shop.NEWSAGENT.value,
                    }
                ]
            },
            ShopsServices.OPTICIAN.value: {
                FIELD_TITLE: 'Optician',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.SHOP: Shop.OPTICIAN.value,
                    }
                ]
            },
            ShopsServices.OUTDOOR.value: {
                FIELD_TITLE: 'Shop selling outdoor equipment',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.SHOP: Shop.OUTDOOR.value,
                    }
                ]
            },
            ShopsServices.PAINT.value: {
                FIELD_TITLE: 'Shop selling paints',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.SHOP: Shop.PAINT.value,
                    }
                ]
            },
            ShopsServices.PERFUMERY.value: {
                FIELD_TITLE: 'Cosmetics shop / Perfumery',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.SHOP: Shop.COSMETICS.value,
                    },
                    {
                        MapKeys.SHOP: Shop.PERFUMERY.value,
                    }
                ]
            },
            ShopsServices.PET.value: {
                FIELD_TITLE: 'Pet shop',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.SHOP: Shop.PET.value,
                    }
                ]
            },
            ShopsServices.PHOTO.value: {
                FIELD_TITLE: 'Photo shop or photo studio',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.SHOP: Shop.PHOTO.value,
                    },
                    {
                        MapKeys.SHOP: Shop.PHOTO_STUDIO.value,
                    },
                    {
                        MapKeys.SHOP: Shop.PHOTOGRAPHY.value,
                    }
                ]
            },
            ShopsServices.PURPLE_CAR.value: {
                FIELD_TITLE: '	Car store',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.SHOP: Shop.CAR.value,
                    }
                ]
            },
            ShopsServices.SEAFOOD.value: {
                FIELD_TITLE: '	Shop selling fish and/or seafood',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.SHOP: Shop.SEAFOOD.value,
                    },
                    {
                        MapKeys.SHOP: Shop.FISHMONGER.value,
                    }
                ]
            },
            ShopsServices.SECOND_HAND.value: {
                FIELD_TITLE: 'A shop selling second hand goods',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.SHOP: Shop.SECOND_HAND.value,
                    }
                ]
            },
            ShopsServices.SHOES.value: {
                FIELD_TITLE: 'Shoe store',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.SHOP: Shop.SHOES.value,
                    }
                ]
            },
            ShopsServices.SHOP_MOTORCYCLE.value: {
                FIELD_TITLE: 'Motorcycle shop',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.SHOP: Shop.MOTORCYCLE.value,
                    }
                ]
            },
            ShopsServices.SHOP_MOTORCYCLE_REPAIR.value: {
                FIELD_TITLE: 'A place where you can get your motorcycles repaired',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.SHOP: Shop.MOTORCYCLE_REPAIR.value,
                    }
                ]
            },
            ShopsServices.SHOP_MUSIC.value: {
                FIELD_TITLE: 'Shop selling recorded music',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.SHOP: Shop.MUSIC.value,
                    }
                ]
            },
            ShopsServices.SHOP_OFFICE.value: {
                FIELD_TITLE: 'Office, department, bureau (all)',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.OFFICE: '*',
                    }
                ]
            },
            ShopsServices.SHOP_OTHER.value: {
                FIELD_TITLE: 'Shop (specified and other, not listed above) / Driving school',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.SHOP: '*',
                    },
                    {
                        MapKeys.AMENITY: Amenity.DRIVING_SCHOOL.value,
                    }
                ]
            },
            ShopsServices.SOCIAL_AMENITY_DARKEN.value: {
                FIELD_TITLE: 'Nursing home care / Childcare',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.AMENITY: Amenity.NURSING_HOME.value,
                    },
                    {
                        MapKeys.AMENITY: Amenity.CHILDCARE.value,
                    }
                ]
            },
            ShopsServices.SPORTS.value: {
                FIELD_TITLE: 'Sports equipment shop',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.SHOP: Shop.SPORTS.value,
                    }
                ]
            },
            ShopsServices.STATIONERY.value: {
                FIELD_TITLE: 'Stationery shop',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.SHOP: Shop.STATIONERY.value,
                    }
                ]
            },
            ShopsServices.SUPERMARKET.value: {
                FIELD_TITLE: 'Supermarket',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.SHOP: Shop.SUPERMARKET.value,
                    }
                ]
            },
            ShopsServices.TEA.value: {
                FIELD_TITLE: 'Tea shop',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.SHOP: Shop.TEA.value,
                    }
                ]
            },
            ShopsServices.TICKET.value: {
                FIELD_TITLE: 'A shop selling tickets for concerts, events, public transport',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.SHOP: Shop.TICKET.value,
                    }
                ]
            },
            ShopsServices.TOBACCO.value: {
                FIELD_TITLE: 'Tobacco shop',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.SHOP: Shop.TOBACCO.value,
                    }
                ]
            },
            ShopsServices.TOYS.value: {
                FIELD_TITLE: 'Toy shop',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.SHOP: Shop.TOYS.value,
                    }
                ]
            },
            ShopsServices.TRADE.value: {
                FIELD_TITLE: 'A place of business that sells to a particular trade or trades / Wholesale',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.SHOP: Shop.TRADE.value,
                    },
                    {
                        MapKeys.SHOP: Shop.WHOLESALE.value,
                    }
                ]
            },
            ShopsServices.TRAVEL_AGENCY.value: {
                FIELD_TITLE: 'Travel agency',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.SHOP: Shop.TRAVEL_AGENCY.value,
                    }
                ]
            },
            ShopsServices.TYRES.value: {
                FIELD_TITLE: 'Tyres shop',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.SHOP: Shop.TYRES.value,
                    }
                ]
            },
            ShopsServices.VARIETY_STORE.value: {
                FIELD_TITLE: 'Variety store',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.SHOP: Shop.VARIETY_STORE.value,
                    }
                ]
            },
            ShopsServices.VEHICLE_INSPECTION.value: {
                FIELD_TITLE: 'Government vehicle inspection',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.AMENITY: Amenity.VEHICLE_INSPECTION.value,
                    }
                ]
            },
            ShopsServices.VIDEO.value: {
                FIELD_TITLE: 'Shop selling or renting videos/DVDs',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.SHOP: Shop.VIDEO.value,
                    }
                ]
            },
            ShopsServices.VIDEO_GAMES.value: {
                FIELD_TITLE: 'Shop selling video games',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.SHOP: Shop.VIDEO_GAMES.value,
                    }
                ]
            },
        },
        MapSymbols.LANDMARKS_MAN_MADE_INFRASTRUCTURE_MASTS_TOWERS: {
            LandmarksManMadeInfrastructureMastsTowers.BUNKER_OSMCARTO.value: {
                FIELD_TITLE: 'Bunker',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.MILITARY: Military.BUNKER.value,
                    }
                ]
            },
            LandmarksManMadeInfrastructureMastsTowers.CHIMNEY.value: {
                FIELD_TITLE: 'Chimney',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.MAN_MADE: ManMade.CHIMNEY.value,
                    }
                ]
            },
            LandmarksManMadeInfrastructureMastsTowers.COLUMN.value: {
                FIELD_TITLE: 'Advertising column',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.ADVERTISING: Advertising.COLUMN.value,
                    }
                ]
            },
            LandmarksManMadeInfrastructureMastsTowers.COMMUNICATION_TOWER.value: {
                FIELD_TITLE: 'A huge tower for transmitting radio applications',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.MAN_MADE: ManMade.COMMUNICATIONS_TOWER.value,
                    }
                ]
            },
            LandmarksManMadeInfrastructureMastsTowers.CRANE.value: {
                FIELD_TITLE: 'Crane (stationary)',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.MAN_MADE: ManMade.CRANE.value,
                    }
                ]
            },
            LandmarksManMadeInfrastructureMastsTowers.CROSS.value: {
                FIELD_TITLE: 'Wayside cross / Summit cross or similar',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.HISTORIC: Historic.WAYSIDE_CROSS.value,
                    },
                    {
                        MapKeys.MAN_MADE: ManMade.CROSS.value,
                    }
                ]
            },
            LandmarksManMadeInfrastructureMastsTowers.GENERATOR_WIND.value: {
                FIELD_TITLE: 'Wind turbine',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.POWER: Power.GENERATOR.value,
                        MapKeys.GENERATOR_SOURCE: GeneratorSource.WIND.value,
                    },
                    {
                        MapKeys.POWER: Power.GENERATOR.value,
                        MapKeys.GENERATOR_SOURCE: GeneratorSource.WIND.value,
                        MapKeys.GENERATOR_METHOD: GeneratorMethod.WIND_TURBINE.value,
                    }
                ]
            },
            LandmarksManMadeInfrastructureMastsTowers.HUNTING_STAND.value: {
                FIELD_TITLE: 'Hunting stand',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.AMENITY: Amenity.HUNTING_STAND.value,
                    }
                ]
            },
            LandmarksManMadeInfrastructureMastsTowers.LIGHTHOUSE.value: {
                FIELD_TITLE: 'Lighthouse',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.MAN_MADE: ManMade.LIGHTHOUSE.value,
                    }
                ]
            },
            LandmarksManMadeInfrastructureMastsTowers.MAST_COMMUNICATIONS.value: {
                FIELD_TITLE: 'Mast with transmitters',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.MAN_MADE: ManMade.MAST.value,
                        MapKeys.TOWER_TYPE: TowerType.COMMUNICATION.value,
                    }
                ]
            },
            LandmarksManMadeInfrastructureMastsTowers.MAST_GENERAL.value: {
                FIELD_TITLE: 'Mast in general',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.MAN_MADE: ManMade.MAST.value,
                    }
                ]
            },
            LandmarksManMadeInfrastructureMastsTowers.MAST_LIGHTING.value: {
                FIELD_TITLE: 'Poles for lighting',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.MAN_MADE: ManMade.MAST.value,
                        MapKeys.TOWER_TYPE: TowerType.LIGHTING.value,
                    }
                ]
            },
            LandmarksManMadeInfrastructureMastsTowers.STORAGE_TANK.value: {
                FIELD_TITLE: 'Storage tanks / Silo',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.MAN_MADE: ManMade.STORAGE_TANK.value,
                    },
                    {
                        MapKeys.MAN_MADE: ManMade.SILO.value,
                    }
                ]
            },
            LandmarksManMadeInfrastructureMastsTowers.TELESCOPE_DISH.value: {
                FIELD_TITLE: '	Radio telescope',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.MAN_MADE: ManMade.TELESCOPE.value,
                        MapKeys.TELESCOPE_TYPE: TelescopeType.RADIO.value,
                    }
                ]
            },
            LandmarksManMadeInfrastructureMastsTowers.TELESCOPE_DOME.value: {
                FIELD_TITLE: 'Optical telescope',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.MAN_MADE: ManMade.TELESCOPE.value,
                        MapKeys.TELESCOPE_TYPE: TelescopeType.OPTICAL.value,
                    }
                ]
            },
            LandmarksManMadeInfrastructureMastsTowers.TOWER_BELL_TOWER.value: {
                FIELD_TITLE: 'Bell tower',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.MAN_MADE: ManMade.MAST.value,
                        MapKeys.TOWER_TYPE: TowerType.BELL_TOWER.value,
                    }
                ]
            },
            LandmarksManMadeInfrastructureMastsTowers.TOWER_CANTILEVER_COMMUNICATION.value: {
                FIELD_TITLE: 'Communication towers',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.MAN_MADE: ManMade.TOWER.value,
                        MapKeys.TOWER_TYPE: TowerType.COMMUNICATION.value,
                    }
                ]
            },
            LandmarksManMadeInfrastructureMastsTowers.TOWER_COOLING.value: {
                FIELD_TITLE: 'Cooling tower',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.MAN_MADE: ManMade.TOWER.value,
                        MapKeys.TOWER_TYPE: TowerType.COOLING.value,
                    }
                ]
            },
            LandmarksManMadeInfrastructureMastsTowers.TOWER_DEFENSIVE.value: {
                FIELD_TITLE: 'Fortified defensive tower',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.MAN_MADE: ManMade.TOWER.value,
                        MapKeys.TOWER_TYPE: TowerType.DEFENSIVE.value,
                    }
                ]
            },
            LandmarksManMadeInfrastructureMastsTowers.TOWER_DISH.value: {
                FIELD_TITLE: 'The \'communication tower\' is a dish',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.MAN_MADE: ManMade.TOWER.value,
                        MapKeys.TOWER_CONSTRUCTION: TowerConstruction.DISH.value,
                    }
                ]
            },
            LandmarksManMadeInfrastructureMastsTowers.TOWER_DOME.value: {
                FIELD_TITLE: 'The \'communication tower\' is a dome',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.MAN_MADE: ManMade.TOWER.value,
                        MapKeys.TOWER_CONSTRUCTION: TowerConstruction.DOME.value,
                    }
                ]
            },
            LandmarksManMadeInfrastructureMastsTowers.TOWER_FREESTANDING.value: {
                FIELD_TITLE: '	Tower in general',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.MAN_MADE: ManMade.TOWER.value,
                    }
                ]
            },
            LandmarksManMadeInfrastructureMastsTowers.TOWER_LATTICE.value: {
                FIELD_TITLE: 'The tower is constructed from steel lattice',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.MAN_MADE: ManMade.TOWER.value,
                        MapKeys.TOWER_CONSTRUCTION: TowerConstruction.LATTICE.value,
                    }
                ]
            },
            LandmarksManMadeInfrastructureMastsTowers.TOWER_LATTICE_COMMUNICATION.value: {
                FIELD_TITLE: 'Lattice communication towers',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.MAN_MADE: ManMade.TOWER.value,
                        MapKeys.TOWER_TYPE: TowerType.COMMUNICATION.value,
                        MapKeys.TOWER_CONSTRUCTION: TowerConstruction.LATTICE.value,
                    }
                ]
            },
            LandmarksManMadeInfrastructureMastsTowers.TOWER_LATTICE_LIGHTING.value: {
                FIELD_TITLE: 'Tower is constructed from steel lattice for lighting',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.MAN_MADE: ManMade.TOWER.value,
                        MapKeys.TOWER_TYPE: TowerType.LIGHTING.value,
                        MapKeys.TOWER_CONSTRUCTION: TowerConstruction.LATTICE.value,
                    }
                ]
            },
            LandmarksManMadeInfrastructureMastsTowers.TOWER_LIGHTING.value: {
                FIELD_TITLE: 'Towers for lighting',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.MAN_MADE: ManMade.TOWER.value,
                        MapKeys.TOWER_TYPE: TowerType.LIGHTING.value,
                    }
                ]
            },
            LandmarksManMadeInfrastructureMastsTowers.TOWER_OBSERVATION.value: {
                FIELD_TITLE: 'Observation tower / Watch tower',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.MAN_MADE: ManMade.TOWER.value,
                        MapKeys.TOWER_TYPE: [
                            TowerType.OBSERVATION.value,
                            TowerType.WATCHTOWER.value,
                        ],
                    }
                ]
            },
            LandmarksManMadeInfrastructureMastsTowers.WATER_TOWER.value: {
                FIELD_TITLE: 'Water tower',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.MAN_MADE: ManMade.WATER_TOWER.value,
                    }
                ]
            },
            LandmarksManMadeInfrastructureMastsTowers.WINDMILL.value: {
                FIELD_TITLE: 'Windmill',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.MAN_MADE: ManMade.WINDMILL.value,
                    }
                ]
            },
        },
        MapSymbols.ELECTRICITY: {
            Electricity.POWER_POLE.value: {
                FIELD_TITLE: 'Small electricity pole, carrying low voltage electricity cables',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.POWER: Power.POLE.value,
                    }
                ]
            },
            Electricity.POWER_TOWER.value: {
                FIELD_TITLE: 'Big electricity pylon, carrying high voltage electricity cables',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.POWER: Power.TOWER.value,
                    }
                ]
            },
        },
        MapSymbols.PLACES: {
            Places.ENTRANCE.value: {
                FIELD_TITLE: '	A backdoor of a building',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.ENTRANCE: Entrance.SERVICE.value,
                    }
                ]
            },
            Places.ENTRANCE_MAIN.value: {
                FIELD_TITLE: 'Main entrance (exit) of a building',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.ENTRANCE: Entrance.MAIN.value,
                    }
                ]
            },
            Places.PLACE.value: {
                FIELD_TITLE: 'City',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.PLACE: Place.CITY.value,
                    }
                ]
            },
            Places.PLACE_CAPITAL.value: {
                FIELD_TITLE: 'Capital',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.CAPITAL: '*',
                    }
                ]
            },
            Places.RECT.value: {
                FIELD_TITLE: 'Entrance (exit) of a building / A direct public entrance to a shop which is not a main building entrance',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.ENTRANCE: Entrance.YES.value,
                    },
                    {
                        MapKeys.ENTRANCE: Entrance.SHOP.value,
                    }
                ]
            },
            Places.RECTDIAG.value: {
                FIELD_TITLE: 'Any door of a building and access is not allowed',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.ENTRANCE: '*',
                    },
                    {
                        MapKeys.ACCESS: Access.YES.value,
                    }
                ]
            },
        },
    }

    LINES: ClassVar[LegendDict] = {
        MapLines.MAJOR_ROADS: {
            MajorRoads.HIGHWAY_CONSTRUCTION_MOTORWAY_CARTO.value: {
                FIELD_TITLE: 'Motorway under construction / Motorway link under construction',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.HIGHWAY: Highway.CONSTRUCTION.value,
                        MapKeys.CONSTRUCTION: [
                            Construction.MOTORWAY.value,
                            Construction.MOTORWAY_LINK.value,
                        ],
                    }
                ]
            },
            MajorRoads.HIGHWAY_CONSTRUCTION_PRIMARY_CARTO.value: {
                FIELD_TITLE: 'Primary road under construction / Primary road link under construction',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.HIGHWAY: Highway.CONSTRUCTION.value,
                        MapKeys.CONSTRUCTION: [
                            Construction.PRIMARY.value,
                            Construction.PRIMARY_LINK.value,
                        ],
                    }
                ]
            },
            MajorRoads.HIGHWAY_CONSTRUCTION_SECONDARY_CARTO.value: {
                FIELD_TITLE: 'Secondary road under construction / Secondary road link under construction',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.HIGHWAY: Highway.CONSTRUCTION.value,
                        MapKeys.CONSTRUCTION: [
                            Construction.SECONDARY.value,
                            Construction.SECONDARY_LINK.value,
                        ],
                    }
                ]
            },
            MajorRoads.HIGHWAY_CONSTRUCTION_TRUNK_CARTO.value: {
                FIELD_TITLE: 'Trunk under construction / Trunk link under construction',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.HIGHWAY: Highway.CONSTRUCTION.value,
                        MapKeys.CONSTRUCTION: [
                            Construction.TRUNK.value,
                            Construction.TRUNK_LINK.value,
                        ],
                    }
                ]
            },
            MajorRoads.HIGHWAY_MOTORWAY_CARTO.value: {
                FIELD_TITLE: 'Motorway, the most important roads in a road network. Equivalent to freeway, Autobahn (Germany), etc.',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.HIGHWAY: Highway.MOTORWAY.value,
                    }
                ]
            },
            MajorRoads.HIGHWAY_MOTORWAY_LINK.value: {
                FIELD_TITLE: 'The link roads (sliproads / ramps) leading to and from a motorway',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.HIGHWAY: Highway.MOTORWAY_LINK.value,
                    }
                ]
            },
            MajorRoads.HIGHWAY_PRIMARY_CARTO.value: {
                FIELD_TITLE: 'Primary road',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.HIGHWAY: Highway.PRIMARY.value,
                    }
                ]
            },
            MajorRoads.HIGHWAY_PRIMARY_LINK.value: {
                FIELD_TITLE: 'Connecting slip roads/ramps of primary highways',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.HIGHWAY: Highway.PRIMARY_LINK.value,
                    }
                ]
            },
            MajorRoads.HIGHWAY_SECONDARY_CARTO.value: {
                FIELD_TITLE: 'Secondary road',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.HIGHWAY: Highway.SECONDARY.value,
                    }
                ]
            },
            MajorRoads.HIGHWAY_SECONDARY_LINK.value: {
                FIELD_TITLE: 'Connecting slip roads/ramps of secondary highways',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.HIGHWAY: Highway.SECONDARY_LINK.value,
                    }
                ]
            },
            MajorRoads.HIGHWAY_TERTIARY_CARTO.value: {
                FIELD_TITLE: 'Tertiary road',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.HIGHWAY: Highway.TERTIARY.value,
                    }
                ]
            },
            MajorRoads.HIGHWAY_TERTIARY_LINK.value: {
                FIELD_TITLE: 'Connecting slip roads/ramps of tertiary highways',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.HIGHWAY: Highway.TERTIARY_LINK.value,
                    }
                ]
            },
            MajorRoads.HIGHWAY_TRUNK_CARTO.value: {
                FIELD_TITLE: 'Trunks, the most important roads in a road network that aren\'t motorways',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.HIGHWAY: Highway.TRUNK.value,
                    }
                ]
            },
            MajorRoads.HIGHWAY_TRUNK_LINK.value: {
                FIELD_TITLE: 'The link roads (sliproads / ramps) leading to and from a trunk highway',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.HIGHWAY: Highway.TRUNK_LINK.value,
                    }
                ]
            },
            MajorRoads.HIGHWAY_UNCLASSIFIED.value: {
                FIELD_TITLE: 'Quaternary road',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.HIGHWAY: Highway.UNCLASSIFIED.value,
                    }
                ]
            },
        },
        MapLines.CITY_ROADS: {
            CityRoads.HIGHWAY_CONSTRUCTION_LIVING_STREET_CARTO.value: {
                FIELD_TITLE: 'Living street under construction',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.HIGHWAY: Highway.CONSTRUCTION.value,
                        MapKeys.CONSTRUCTION: Construction.LIVING_STREET.value,
                    }
                ]
            },
            CityRoads.HIGHWAY_CONSTRUCTION_PEDESTRIAN_CARTO.value: {
                FIELD_TITLE: 'Pedestrian street under construction',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.HIGHWAY: Highway.CONSTRUCTION.value,
                        MapKeys.CONSTRUCTION: Construction.PEDESTRIAN.value,
                    }
                ]
            },
            CityRoads.HIGHWAY_CONSTRUCTION_SERVICE_CARTO.value: {
                FIELD_TITLE: 'Access road under construction',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.HIGHWAY: Highway.CONSTRUCTION.value,
                        MapKeys.CONSTRUCTION: Construction.SERVICE.value,
                    }
                ]
            },
            CityRoads.HIGHWAY_CONSTRUCTION_TERTIARY_CARTO.value: {
                FIELD_TITLE: 'Tertiary road under construction / Tertiary road link under construction / Quaternary road under construction / Residential road under construction',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.HIGHWAY: Highway.CONSTRUCTION.value,
                        MapKeys.CONSTRUCTION: [
                            Construction.TERTIARY.value,
                            Construction.TERTIARY_LINK.value,
                            Construction.UNCLASSIFIED.value,
                            Construction.RESIDENTIAL.value,
                        ]
                    },
                    {
                        MapKeys.HIGHWAY: Highway.CONSTRUCTION.value,
                    }
                ]
            },
            CityRoads.HIGHWAY_DESTINATION.value: {
                FIELD_TITLE: 'Residential road only local traffic',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.HIGHWAY: Highway.RESIDENTIAL.value,
                        MapKeys.ACCESS: Access.DESTINATION.value,
                    }
                ]
            },
            CityRoads.HIGHWAY_PRIVAT.value: {
                FIELD_TITLE: 'Residential road only private traffic / prohibited to be used by the general public',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.HIGHWAY: Highway.RESIDENTIAL.value,
                        MapKeys.ACCESS: [
                            Access.PRIVATE.value,
                            Access.NO.value
                        ],
                    }
                ]
            },
            CityRoads.HIGHWAY_RESIDENTIAL.value: {
                FIELD_TITLE: 'Residential road',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.HIGHWAY: Highway.RESIDENTIAL.value,
                    }
                ]
            },
            CityRoads.HIGHWAY_SERVICE.value: {
                FIELD_TITLE: 'Access road (may be also outside of a city)',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.HIGHWAY: Highway.SERVICE.value,
                    }
                ]
            },
            CityRoads.HIGHWAY_SERVICE_MINOR.value: {
                FIELD_TITLE: 'Subordinated way in a parking lot / drive-through highway / driveway / slipway',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.HIGHWAY: Highway.SERVICE.value,
                        MapKeys.SERVICE: [
                            Service.PARKING_AISLE.value,
                            Service.DRIVE_THROUGH.value,
                            Service.DRIVEWAY.value,
                        ]
                    },
                    {
                        MapKeys.HIGHWAY: Highway.SERVICE.value,
                        MapKeys.LEISURE: Leisure.SLIPWAY.value,
                    }
                ]
            },
            CityRoads.LIVING_STREET_OSM.value: {
                FIELD_TITLE: 'Living street',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.HIGHWAY: Highway.LIVING_STREET.value,
                    }
                ]
            },
            CityRoads.PEDESTRIAN_WITH_AREA_OSM.value: {
                FIELD_TITLE: 'Pedestrian street',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.HIGHWAY: Highway.PEDESTRIAN.value,
                    }
                ]
            },
        },
        MapLines.NON_MOTORIZED_VEHICLES_ROADS_WAYS: {
            NonMotorizedVehiclesRoadsWays.CYCLEWAY_OSM.value: {
                FIELD_TITLE: 'Cycleway',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.HIGHWAY: Highway.CYCLEWAY.value,
                    },
                    {
                        MapKeys.HIGHWAY: Highway.PATH.value,
                        MapKeys.BICYCLE: Bicycle.DESIGNATED.value,
                    }
                ]
            },
            NonMotorizedVehiclesRoadsWays.HIGHWAY_BRIDLEWAY.value: {
                FIELD_TITLE: 'Bridleway',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.HIGHWAY: Highway.BRIDLEWAY.value,
                    },
                    {
                        MapKeys.HIGHWAY: Highway.PATH.value,
                        MapKeys.HORSE: Horse.DESIGNATED.value,
                    }
                ]
            },
            NonMotorizedVehiclesRoadsWays.HIGHWAY_CONSTRUCTION_MISC_WAYS_CARTO.value: {
                FIELD_TITLE: 'Bridleway / Cycleway / Footway / Multi-use path / Steps / Track under construction',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.HIGHWAY: Highway.CONSTRUCTION.value,
                        MapKeys.CONSTRUCTION: [
                            Construction.BRIDLEWAY.value,
                            Construction.CYCLEWAY.value,
                            Construction.FOOTWAY.value,
                            Construction.PATH.value,
                            Construction.STEPS.value,
                            Construction.PATH.value,
                        ]
                    }
                ]
            },
            NonMotorizedVehiclesRoadsWays.HIGHWAY_FOOTWAY.value: {
                FIELD_TITLE: 'Footway / Multi-use path',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.HIGHWAY: Highway.FOOTWAY.value,
                    },
                    {
                        MapKeys.HIGHWAY: Highway.PATH.value,
                    }
                ]
            },
            NonMotorizedVehiclesRoadsWays.HIGHWAY_STEPS.value: {
                FIELD_TITLE: 'Steps',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.HIGHWAY: Highway.STEPS.value,
                    }
                ]
            },
        },
        MapLines.AGRICULTURAL_FORESTRY_ROADS: {
            AgriculturalForestryRoads.MAPNIK_TRACKTYPE_GRADE1.value: {
                FIELD_TITLE: 'Track. Solid surface.',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.HIGHWAY: Highway.TRACK.value,
                        MapKeys.TRACKTYPE: Tracktype.GRADE1.value,
                    }
                ]
            },
            AgriculturalForestryRoads.MAPNIK_TRACKTYPE_GRADE2.value: {
                FIELD_TITLE: 'Track. Mostly solid surface.',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.HIGHWAY: Highway.TRACK.value,
                        MapKeys.TRACKTYPE: Tracktype.GRADE2.value,
                    }
                ]
            },
            AgriculturalForestryRoads.MAPNIK_TRACKTYPE_GRADE3.value: {
                FIELD_TITLE: 'Track. Even amount of solid and soft materials.',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.HIGHWAY: Highway.TRACK.value,
                        MapKeys.TRACKTYPE: Tracktype.GRADE3.value,
                    }
                ]
            },
            AgriculturalForestryRoads.MAPNIK_TRACKTYPE_GRADE4.value: {
                FIELD_TITLE: 'Track. Mostly soft surface.',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.HIGHWAY: Highway.TRACK.value,
                        MapKeys.TRACKTYPE: Tracktype.GRADE4.value,
                    }
                ]
            },
            AgriculturalForestryRoads.MAPNIK_TRACKTYPE_GRADE5.value: {
                FIELD_TITLE: 'Track. Soft surface.',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.HIGHWAY: Highway.TRACK.value,
                        MapKeys.TRACKTYPE: Tracktype.GRADE5.value,
                    }
                ]
            },
            AgriculturalForestryRoads.MAPNIK_TRACKTYPE_NOT_SET.value: {
                FIELD_TITLE: 'Track with unknown surface type.',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.HIGHWAY: Highway.TRACK.value,
                    }
                ]
            },
        },
        MapLines.MISCELLANEOUS_ROADS: {
            MiscellaneousRoads.AEROWAY_RUNWAY_LINE.value: {
                FIELD_TITLE: 'Runway',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.AEROWAY: Aeroway.RUNWAY.value,
                    }
                ]
            },
            MiscellaneousRoads.AEROWAY_TAXIWAY_LINE.value: {
                FIELD_TITLE: 'Taxiway',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.AEROWAY: Aeroway.TAXIWAY.value,
                    }
                ]
            },
            MiscellaneousRoads.HIGHWAY_BUS_GUIDEWAY_MAPNIK.value: {
                FIELD_TITLE: 'Way for guided buses',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.HIGHWAY: Highway.BUS_GUIDEWAY.value,
                    }
                ]
            },
            MiscellaneousRoads.HIGHWAY_CONSTRUCTION_ROAD_RACEWAY_CARTO.value: {
                FIELD_TITLE: 'Raceway under construction / Road with unknown classification under construction',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.HIGHWAY: Highway.CONSTRUCTION.value,
                        MapKeys.CONSTRUCTION: [
                            Construction.RACEWAY.value,
                            Construction.ROAD.value,
                        ]
                    }
                ]
            },
            MiscellaneousRoads.HIGHWAY_RACEWAY_MAPNIK.value: {
                FIELD_TITLE: 'Racetrack (motorised)',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.HIGHWAY: Highway.RACEWAY.value,
                    }
                ]
            },
            MiscellaneousRoads.HIGHWAY_ROAD_MAPNIK.value: {
                FIELD_TITLE: 'Completely unknown road type. Anything from footpath to motorway is possible. This should be temporary, until the road type has been surveyed properly.',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.HIGHWAY: Highway.ROAD.value,
                    }
                ]
            },
            MiscellaneousRoads.LEISURE_TRACK_LINE.value: {
                FIELD_TITLE: 'Track (non-motorised)',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.LEISURE: Leisure.TRACK.value,
                    }
                ]
            },
            MiscellaneousRoads.MAN_MADE_PIER.value: {
                FIELD_TITLE: 'Pier, Landing stage',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.MAN_MADE: ManMade.PIER.value,
                    }
                ]
            },
        },
        MapLines.RAILWAYS: {
            Railways.AREA_RAILWAY_TURNTABLE_MAPNIK.value: {
                FIELD_TITLE: 'Railway turntable',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.RAILWAY: Railway.TURNTABLE.value,
                    }
                ]
            },
            Railways.RAILWAY_CONSTRUCTION.value: {
                FIELD_TITLE: 'Construction railway',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.RAILWAY: Railway.CONSTRUCTION.value,
                    }
                ]
            },
            Railways.RAILWAY_DISUSED.value: {
                FIELD_TITLE: 'Disused railway',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.RAILWAY: Railway.DISUSED.value,
                    }
                ]
            },
            Railways.RAILWAY_LIGHT_RAIL_FUNICULAR_NARROW_GAUGE.value: {
                FIELD_TITLE: 'Narrow gauge railway / Cable-driven inclined railway / Rails of a light rail',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.RAILWAY: Railway.NARROW_GAUGE.value,
                    },
                    {
                        MapKeys.RAILWAY: Railway.FUNICULAR.value,
                    },
                    {
                        MapKeys.RAILWAY: Railway.LIGHT_RAIL.value,
                    }
                ]
            },
            Railways.RAILWAY_MINIATURE.value: {
                FIELD_TITLE: 'Miniature railway',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.RAILWAY: Railway.MINIATURE.value,
                    }
                ]
            },
            Railways.RAILWAY_MONORAIL.value: {
                FIELD_TITLE: 'Monorail railway',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.RAILWAY: Railway.MONORAIL.value,
                    }
                ]
            },
            Railways.RAILWAY_RAIL.value: {
                FIELD_TITLE: 'Railway for full-sized passenger trains',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.RAILWAY: Railway.RAIL.value,
                    }
                ]
            },
            Railways.RAILWAY_RAIL_SERVICE.value: {
                FIELD_TITLE: 'Railway full-sized passenger trains service segments (Siding track / Yard / Spur track)',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.RAILWAY: Railway.RAIL.value,
                        MapKeys.SERVICE: [
                            Service.SIDING.value,
                            Service.YARD.value,
                            Service.SPUR.value,
                        ]
                    }
                ]
            },
            Railways.RAILWAY_SUBWAY.value: {
                FIELD_TITLE: 'Subway railway',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.RAILWAY: Railway.SUBWAY.value,
                    }
                ]
            },
            Railways.RAILWAY_TRAM.value: {
                FIELD_TITLE: 'Tram railway',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.RAILWAY: Railway.TRAM.value,
                    }
                ]
            },
            Railways.ROLLER_COASTER_TRACK.value: {
                FIELD_TITLE: 'Roller coaster track',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.ROLLER_COASTER: RollerCoaster.TRACK.value,
                    }
                ]
            },
        },
        MapLines.AERIAL_LIFTS: {
            AerialLifts.AERIALWAY_GONDOLA.value: {
                FIELD_TITLE: 'Gondola lift / Cable car run / Mixed lift',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.AERIALWAY: Aerialway.GONDOLA.value,
                    },
                    {
                        MapKeys.AERIALWAY: Aerialway.CABLE_CAR.value,
                    },
                    {
                        MapKeys.AERIALWAY: Aerialway.MIXED_LIFT.value,
                    }
                ]
            },
            AerialLifts.AERIALWAY_GOODS.value: {
                FIELD_TITLE: 'An aerial lift for goods',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.AERIALWAY: Aerialway.GOODS.value,
                    }
                ]
            },
            AerialLifts.CHAIR_LIFT.value: {
                FIELD_TITLE: 'Chairlift / Drag lift / T-bar lift / J-bar lift / Platter lift / Rope tow lift / Zip line',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.AERIALWAY: Aerialway.CHAIR_LIFT.value,
                    },
                    {
                        MapKeys.AERIALWAY: Aerialway.DRAG_LIFT.value,
                    },
                    {
                        MapKeys.AERIALWAY: Aerialway.T_BAR.value,
                    },
                    {
                        MapKeys.AERIALWAY: Aerialway.J_BAR.value,
                    },
                    {
                        MapKeys.AERIALWAY: Aerialway.PLATTER.value,
                    },
                    {
                        MapKeys.AERIALWAY: Aerialway.ROPE_TOW.value,
                    },
                    {
                        MapKeys.AERIALWAY: Aerialway.ZIP_LINE.value,
                    }
                ]
            },
        },
        MapLines.WATER_WAYS: {
            WaterWays.ATTRACTION_WATER_SLIDE.value: {
                FIELD_TITLE: 'Water slide',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.ATTRACTION: Attraction.WATER_SLIDE.value,
                    }
                ]
            },
            WaterWays.RIVER.value: {
                FIELD_TITLE: 'River / Canal',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.WATERWAY: Waterway.RIVER.value,
                    },
                    {
                        MapKeys.WATERWAY: Waterway.CANAL.value,
                    }
                ]
            },
            WaterWays.STREAM.value: {
                FIELD_TITLE: 'Stream / Ditch / Drain',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.WATERWAY: Waterway.STREAM.value,
                    },
                    {
                        MapKeys.WATERWAY: Waterway.DITCH.value,
                    },
                    {
                        MapKeys.WATERWAY: Waterway.DRAIN.value,
                    }
                ]
            },
            WaterWays.WATERWAY_CANAL_TUNNEL_FLOODED.value: {
                FIELD_TITLE: 'Canal in tunnel',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.WATERWAY: Waterway.CANAL.value,
                        MapKeys.TUNNEL: Tunnel.FLOODED.value,
                    }
                ]
            },
            WaterWays.WATERWAY_RIVER_INTERMITTENT.value: {
                FIELD_TITLE: 'River intermittent / Canal intermittent / River seasonal / Canal seasonal',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.WATERWAY: Waterway.RIVER.value,
                        MapKeys.INTERMITTENT: '*',
                    },
                    {
                        MapKeys.WATERWAY: Waterway.RIVER.value,
                        MapKeys.SEASONAL: '*',
                    },
                    {
                        MapKeys.WATERWAY: Waterway.CANAL.value,
                        MapKeys.INTERMITTENT: '*',
                    },
                    {
                        MapKeys.WATERWAY: Waterway.CANAL.value,
                        MapKeys.SEASONAL: '*',
                    }
                ]
            },
            WaterWays.WATERWAY_RIVER_TUNNEL.value: {
                FIELD_TITLE: 'River in tunnel / Canal in tunnel',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.WATERWAY: Waterway.RIVER.value,
                        MapKeys.TUNNEL: Tunnel.YES.value,
                    },
                    {
                        MapKeys.WATERWAY: Waterway.CANAL.value,
                        MapKeys.TUNNEL: Tunnel.YES.value,
                    }
                ]
            },
            WaterWays.WATERWAY_STREAM_INTERMITTENT.value: {
                FIELD_TITLE: 'Stream intermittent / Stream seasonal / Ditch intermittent / Ditch seasonal / Drain intermittent / Drain seasonal',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.WATERWAY: Waterway.STREAM.value,
                        MapKeys.INTERMITTENT: '*',
                    },
                    {
                        MapKeys.WATERWAY: Waterway.STREAM.value,
                        MapKeys.SEASONAL: '*',
                    },
                    {
                        MapKeys.WATERWAY: Waterway.DITCH.value,
                        MapKeys.INTERMITTENT: '*',
                    },
                    {
                        MapKeys.WATERWAY: Waterway.DITCH.value,
                        MapKeys.SEASONAL: '*',
                    },
                    {
                        MapKeys.WATERWAY: Waterway.DRAIN.value,
                        MapKeys.INTERMITTENT: '*',
                    },
                    {
                        MapKeys.WATERWAY: Waterway.DRAIN.value,
                        MapKeys.SEASONAL: '*',
                    }
                ]
            },
            WaterWays.WATERWAY_STREAM_TUNNEL.value: {
                FIELD_TITLE: 'Stream in pipe or tunnel / Ditch in pipe or tunnel / drain in pipe or tunnel',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.WATERWAY: Waterway.STREAM.value,
                        MapKeys.TUNNEL: Tunnel.YES.value,
                    },
                    {
                        MapKeys.WATERWAY: Waterway.DITCH.value,
                        MapKeys.TUNNEL: Tunnel.YES.value,
                    },
                    {
                        MapKeys.WATERWAY: Waterway.DRAIN.value,
                        MapKeys.TUNNEL: Tunnel.YES.value,
                    }
                ]
            },
        },
        MapLines.WATER_TRAFFIC: {
            WaterTraffic.ROUTE_FERRY.value: {
                FIELD_TITLE: 'Ferry route',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.ROUTE: Route.FERRY.value,
                    }
                ]
            },
        },
        MapLines.PLATFORMS : {
            Platforms.HIGHWAY_RAILWAY_PLATFORM_LINE.value: {
                FIELD_TITLE: 'Platform at a bus stop or station / Railway platform',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.HIGHWAY: Highway.PLATFORM.value,
                    },
                    {
                        MapKeys.RAILWAY: Railway.PLATFORM.value,
                    }
                ]
            },
        },
        MapLines.ENERGY_SUPPLY: {
            EnergySupply.MAN_MADE_GOODS_CONVEYOR.value: {
                FIELD_TITLE: 'Conveyor system for transporting materials',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.MAN_MADE: ManMade.GOODS_CONVEYOR.value,
                    }
                ]
            },
            EnergySupply.MAN_MADE_PIPELINE.value: {
                FIELD_TITLE: 'Overground pipeline',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.MAN_MADE: ManMade.PIPELINE.value,
                        MapKeys.LOCATION: [
                            Location.OVERGROUND.value,
                            Location.OVERHEAD.value,
                        ]
                    }
                ]
            },
            EnergySupply.MAN_MADE_PIPELINE_SUBSTANCE_GAS.value: {
                FIELD_TITLE: 'Overground gas pipeline',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.MAN_MADE: ManMade.PIPELINE.value,
                        MapKeys.LOCATION: [
                            Location.OVERGROUND.value,
                            Location.OVERHEAD.value,
                        ],
                        MapKeys.SUBSTANCE: Substance.GAS.value,
                    }
                ]
            },
            EnergySupply.MAN_MADE_PIPELINE_SUBSTANCE_OIL.value: {
                FIELD_TITLE: 'Overground oil pipeline',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.MAN_MADE: ManMade.PIPELINE.value,
                        MapKeys.LOCATION: [
                            Location.OVERGROUND.value,
                            Location.OVERHEAD.value,
                        ],
                        MapKeys.SUBSTANCE: Substance.OIL.value,
                    }
                ]
            },
            EnergySupply.MAN_MADE_PIPELINE_SUBSTANCE_WATER.value: {
                FIELD_TITLE: 'Overground water pipeline',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.MAN_MADE: ManMade.PIPELINE.value,
                        MapKeys.LOCATION: [
                            Location.OVERGROUND.value,
                            Location.OVERHEAD.value,
                        ],
                        MapKeys.SUBSTANCE: Substance.WATER.value,
                    }
                ]
            },
            EnergySupply.POWER_LINE.value: {
                FIELD_TITLE: 'Major power line',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.POWER: Power.LINE.value,
                    }
                ]
            },
            EnergySupply.POWER_MINOR_LINE.value: {
                FIELD_TITLE: 'Minor power line / Path from tee area to the green of a golf course',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.POWER: Power.MINOR_LINE.value,
                    },
                    {
                        MapKeys.GOLF: Golf.HOLE.value,
                    }
                ]
            },
        },
        MapLines.BARRIERS: {
            Barriers.BARRIER_FENCE_MAPNIK.value: {
                FIELD_TITLE: 'Wall / Fence / Chain / Guard rail / Hand rail / Ditch / Jersey barrier',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.BARRIER: Barrier.RETAINING_WALL.value,
                    },
                    {
                        MapKeys.BARRIER: Barrier.WALL.value,
                    },
                    {
                        MapKeys.BARRIER: Barrier.FENCE.value,
                    },
                    {
                        MapKeys.BARRIER: Barrier.CHAIN.value,
                    },
                    {
                        MapKeys.BARRIER: Barrier.GUARD_RAIL.value,
                    },
                    {
                        MapKeys.BARRIER: Barrier.HANDRAIL.value,
                    },
                    {
                        MapKeys.BARRIER: Barrier.DITCH.value,
                    },
                    {
                        MapKeys.BARRIER: Barrier.JERSEY_BARRIER.value,
                    }
                ]
            },
            Barriers.BARRIER_HEDGE.value: {
                FIELD_TITLE: 'Hedge',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.BARRIER: Barrier.HEDGE.value,
                    }
                ]
            },
            Barriers.CITY_WALL.value: {
                FIELD_TITLE: 'City wall',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.BARRIER: Barrier.CITY_WALL.value,
                    },
                    {
                        MapKeys.HISTORIC: Historic.CITYWALLS.value,
                    }
                ]
            },
            Barriers.MAN_MADE_BREAKWATER.value: {
                FIELD_TITLE: 'Breakwater / Groyne',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.MAN_MADE: ManMade.BREAKWATER.value,
                    },
                    {
                        MapKeys.MAN_MADE: ManMade.GROYNE.value,
                    }
                ]
            },
            Barriers.WATERWAY_DAM_WAY.value: {
                FIELD_TITLE: 'Dam',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.WATERWAY: Waterway.DAM.value,
                    }
                ]
            },
            Barriers.WATERWAY_WEIR_WAY.value: {
                FIELD_TITLE: 'Weir',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.WATERWAY: Waterway.WEIR.value,
                    }
                ]
            },
        },
        MapLines.NATURE: {
            NatureLines.MAN_MADE_CUTLINE.value: {
                FIELD_TITLE: 'A straight line cut in a forest',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.MAN_MADE: ManMade.CUTLINE.value,
                    }
                ]
            },
            NatureLines.MAN_MADE_EMBANKMENT.value: {
                FIELD_TITLE: 'Embankment',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.MAN_MADE: ManMade.EMBANKMENT.value,
                    }
                ]
            },
            NatureLines.NATURAL_ARETE.value: {
                FIELD_TITLE: 'Arete',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.NATURAL: Natural.ARETE.value,
                    }
                ]
            },
            NatureLines.NATURAL_CLIFF.value: {
                FIELD_TITLE: 'Cliff',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.NATURAL: Natural.CLIFF.value,
                    }
                ]
            },
            NatureLines.NATURAL_RIDGE.value: {
                FIELD_TITLE: 'Ridge',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.NATURAL: Natural.RIDGE.value,
                    }
                ]
            },
            NatureLines.NATURAL_TREE_ROW_MAPNIK.value: {
                FIELD_TITLE: 'Line of trees',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.NATURAL: Natural.TREE_ROW.value,
                    }
                ]
            },
        },
        MapLines.BOUNDARIES: {
            Boundaries.ADMINLEVEL_2_MAPNIK.value: {
                FIELD_TITLE: 'National boundary',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.BOUNDARY: Boundary.ADMINISTRATIVE.value,
                        MapKeys.ADMIN_LEVEL: '2'
                    }
                ]
            },
            Boundaries.ADMINLEVEL_3_MAPNIK.value: {
                FIELD_TITLE: 'Sub-national boundary (highest level)',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.BOUNDARY: Boundary.ADMINISTRATIVE.value,
                        MapKeys.ADMIN_LEVEL: '3'
                    }
                ]
            },
            Boundaries.ADMINLEVEL_4_MAPNIK.value: {
                FIELD_TITLE: 'Sub-national boundary (second-highest level)',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.BOUNDARY: Boundary.ADMINISTRATIVE.value,
                        MapKeys.ADMIN_LEVEL: '4'
                    }
                ]
            },
            Boundaries.ADMINLEVEL_5_MAPNIK.value: {
                FIELD_TITLE: 'Sub-national boundary (third-highest level)',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.BOUNDARY: Boundary.ADMINISTRATIVE.value,
                        MapKeys.ADMIN_LEVEL: '5'
                    }
                ]
            },
            Boundaries.ADMINLEVEL_6_MAPNIK.value: {
                FIELD_TITLE: 'Sub-national boundary (fourth-highest level)',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.BOUNDARY: Boundary.ADMINISTRATIVE.value,
                        MapKeys.ADMIN_LEVEL: '6'
                    }
                ]
            },
            Boundaries.ADMINLEVEL_7_MAPNIK.value: {
                FIELD_TITLE: 'Sub-national boundary (fifth-highest or sixth-highest level)',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.BOUNDARY: Boundary.ADMINISTRATIVE.value,
                        MapKeys.ADMIN_LEVEL: [
                            '7',
                            '8',
                        ]
                    }
                ]
            },
            Boundaries.ADMINLEVEL_9_MAPNIK.value: {
                FIELD_TITLE: 'Sub-national boundary (seventh-highest or eighth-highest level)',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.BOUNDARY: Boundary.ADMINISTRATIVE.value,
                        MapKeys.ADMIN_LEVEL: [
                            '9',
                            '10',
                        ]
                    }
                ]
            },
        },
    }

    AREAS: ClassVar[LegendDict] = {
        MapAreas.NATURE: {
            NatureArea.AREA_BEACH_GRAVEL.value: {
                FIELD_TITLE: 'Beach with coarse sand surface / shoal with coarse sand surface',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.NATURAL: Natural.BEACH.value,
                        MapKeys.SURFACE: Surface.GRAVEL.value,
                    },
                    {
                        MapKeys.NATURAL: Natural.SHOAL.value,
                        MapKeys.SURFACE: Surface.GRAVEL.value,
                    }
                ]
            },
            NatureArea.AREA_BEACH_SAND.value: {
                FIELD_TITLE: 'Beach with sand surface / shoal with sand surface',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.NATURAL: Natural.BEACH.value,
                        MapKeys.SURFACE: Surface.SAND.value,
                    },
                    {
                        MapKeys.NATURAL: Natural.SHOAL.value,
                        MapKeys.SURFACE: Surface.SAND.value,
                    }
                ]
            },
            NatureArea.AREA_NATURAL_BEACH.value: {
                FIELD_TITLE: 'Generic beach / Shoal',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.NATURAL: Natural.BEACH.value,
                    },
                    {
                        MapKeys.NATURAL: Natural.SHOAL.value,
                    }
                ]
            },
            NatureArea.AREA_NATURAL_HEATH_YELLOW.value: {
                FIELD_TITLE: 'Dwarf scrubs',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.NATURAL: Natural.HEATH.value,
                    }
                ]
            },
            NatureArea.AREA_NATURAL_MARSH.value: {
                FIELD_TITLE: 'Wetland (generic)',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.NATURAL: Natural.WETLAND.value,
                    }
                ]
            },
            NatureArea.AREA_NATURAL_SCRUB.value: {
                FIELD_TITLE: 'Bushes and small trees',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.NATURAL: Natural.SCRUB.value,
                    }
                ]
            },
            NatureArea.AREA_NATURAL_WOOD.value: {
                FIELD_TITLE: 'Natural woodland which is mostly or not at all not used for timber production',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.NATURAL: Natural.WOOD.value,
                    }
                ]
            },
            NatureArea.AREA_SAND.value: {
                FIELD_TITLE: 'Generic sand area / golf bunker',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.NATURAL: Natural.SAND.value,
                    },
                    {
                        MapKeys.GOLF: Golf.BUNKER.value,
                    }
                ]
            },
            NatureArea.BARE_ROCK.value: {
                FIELD_TITLE: 'Bare rock surface',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.NATURAL: Natural.BARE_ROCK.value,
                    }
                ]
            },
            NatureArea.BASE_LAYER_LAND.value: {
                FIELD_TITLE: 'Land (This is only shown when no more specific information is available)',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: []
            },
            NatureArea.BASE_LAYER_WATER.value: {
                FIELD_TITLE: 'Body of water (ocean, sea, pond, river) / swimming pool / artificial basin / artificial lake / water-covered area of a river / dock',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.NATURAL: Natural.WATER.value,
                    },
                    {
                        MapKeys.LEISURE: Leisure.SWIMMING_POOL.value,
                    },
                    {
                        MapKeys.LANDUSE: Landuse.BASIN.value,
                    },
                    {
                        MapKeys.LANDUSE: Landuse.RESERVOIR.value,
                    },
                    {
                        MapKeys.WATERWAY: Waterway.RIVERBANK.value,
                    },
                    {
                        MapKeys.WATERWAY: Waterway.DOCK.value,
                    }
                ]
            },
            NatureArea.GLACIER_AREA.value: {
                FIELD_TITLE: 'Glacier',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.NATURAL: Natural.GLACIER.value,
                    }
                ]
            },
            NatureArea.LANDUSE_SALT_POND.value: {
                FIELD_TITLE: 'Salt pond',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.LANDUSE: Landuse.SALT_POND.value,
                    }
                ]
            },
            NatureArea.LEAFTYPE_BROADLEAVED.value: {
                FIELD_TITLE: 'Broadleaved woodland',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.NATURAL: Natural.WOOD.value,
                        MapKeys.LEAF_TYPE: LeafType.BROADLEAVED.value,
                    }
                ]
            },
            NatureArea.LEAFTYPE_LEAFLESS.value: {
                FIELD_TITLE: 'Leafless vegetation',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.NATURAL: Natural.WOOD.value,
                        MapKeys.LEAF_TYPE: LeafType.LEAFLESS.value,
                    }
                ]
            },
            NatureArea.LEAFTYPE_MIXED.value: {
                FIELD_TITLE: 'Mixed woodland',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.NATURAL: Natural.WOOD.value,
                        MapKeys.LEAF_TYPE: LeafType.MIXED.value,
                    }
                ]
            },
            NatureArea.LEAFTYPE_NEEDLELEAVED.value: {
                FIELD_TITLE: 'Needleleaved woodland',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.NATURAL: Natural.WOOD.value,
                        MapKeys.LEAF_TYPE: LeafType.NEEDLELEAVED.value,
                    }
                ]
            },
            NatureArea.NATURAL_GRASSLAND.value: {
                FIELD_TITLE: 'Natural grassland',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.NATURAL: Natural.GRASSLAND.value,
                    }
                ]
            },
            NatureArea.NATURAL_MUD_MAPNIK.value: {
                FIELD_TITLE: 'Mud',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.NATURAL: Natural.MUD.value,
                    }
                ]
            },
            NatureArea.NATURAL_REEF.value: {
                FIELD_TITLE: 'Reef',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.NATURAL: Natural.REEF.value,
                    }
                ]
            },
            NatureArea.NATURAL_WETLAND_BOG.value: {
                FIELD_TITLE: 'Bog / String bog',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.NATURAL: Natural.WETLAND.value,
                        MapKeys.WETLAND: [
                            Wetland.BOG.value,
                            Wetland.STRING_BOG.value,
                        ]
                    }
                ]
            },
            NatureArea.NATURAL_WETLAND_MANGROVE.value: {
                FIELD_TITLE: 'Mangrove',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.NATURAL: Natural.WETLAND.value,
                        MapKeys.WETLAND: Wetland.MANGROVE.value,
                    }
                ]
            },
            NatureArea.NATURAL_WETLAND_MARSH.value: {
                FIELD_TITLE: 'Marsh / Semi-wetland meadow / Fen',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.NATURAL: Natural.WETLAND.value,
                        MapKeys.WETLAND: [
                            Wetland.MARSH.value,
                            Wetland.WET_MEADOW.value,
                            Wetland.FEN.value,
                        ]
                    }
                ]
            },
            NatureArea.NATURAL_WETLAND_REED.value: {
                FIELD_TITLE: 'Reedbed',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.NATURAL: Natural.WETLAND.value,
                        MapKeys.WETLAND: Wetland.REEDBED.value,
                    }
                ]
            },
            NatureArea.NATURAL_WETLAND_SWAMP.value: {
                FIELD_TITLE: 'Swamp',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.NATURAL: Natural.WETLAND.value,
                        MapKeys.WETLAND: Wetland.SWAMP.value,
                    }
                ]
            },
            NatureArea.NATURAL_WETLAND_WATER.value: {
                FIELD_TITLE: 'Tidalflat, Mudflat',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.NATURAL: Natural.WETLAND.value,
                        MapKeys.WETLAND: Wetland.TIDALFLAT.value,
                    }
                ]
            },
            NatureArea.SALTMARSH_WATER: {
                FIELD_TITLE: 'Salt marsh',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.NATURAL: Natural.WETLAND.value,
                        MapKeys.WETLAND: Wetland.SALTMARSH.value,
                    }
                ]
            },
            NatureArea.SCREE.value: {
                FIELD_TITLE: 'Scree / Shingle',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.NATURAL: Natural.SCREE.value,
                    },
                    {
                        MapKeys.NATURAL: Natural.SHINGLE.value,
                    }
                ]
            },
            NatureArea.WATER_INTERMITTENT.value: {
                FIELD_TITLE: 'Water body intermittent / Water body seasonal / Infiltration basin / Detention basin',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.NATURAL: Natural.WATER.value,
                        MapKeys.INTERMITTENT: '*',
                    },
                    {
                        MapKeys.NATURAL: Natural.WATER.value,
                        MapKeys.SEASONAL: '*',
                    },
                    {
                        MapKeys.LANDUSE: Landuse.BASIN.value,
                        MapKeys.BASIN: Basin.INFILTRATION.value,
                    },
                    {
                        MapKeys.LANDUSE: Landuse.BASIN.value,
                        MapKeys.BASIN: Basin.DETENTION.value,
                    }
                ]
            },
        },
        MapAreas.CITY_PLANNING: {
            CityPlanning.AREA_LANDUSE_RESIDENTIAL.value: {
                FIELD_TITLE: 'Residential area',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.LANDUSE: Landuse.RESIDENTIAL.value,
                    }
                ]
            },
            CityPlanning.GARAGES_AREA.value: {
                FIELD_TITLE: 'Garages area',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.LANDUSE: Landuse.GARAGES.value,
                    }
                ]
            },
            CityPlanning.LANDUSE_CEMETERY.value: {
                FIELD_TITLE: 'Cemetery with unknown, other or no specific religious background / Grave yard with unknown, other or no specific religious background',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.LANDUSE: Landuse.CEMETERY.value,
                    },
                    {
                        MapKeys.AMENITY: Amenity.GRAVE_YARD.value,
                    }
                ]
            },
            CityPlanning.LANDUSE_CEMETERY_CHRISTIAN.value: {
                FIELD_TITLE: 'Christian cemetery / Christian grave yard',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.LANDUSE: Landuse.CEMETERY.value,
                        MapKeys.RELIGION: Religion.CHRISTIAN.value,
                    },
                    {
                        MapKeys.AMENITY: Amenity.GRAVE_YARD.value,
                        MapKeys.RELIGION: Religion.CHRISTIAN.value,
                    }
                ]
            },
            CityPlanning.LANDUSE_CEMETERY_JEWISH.value: {
                FIELD_TITLE: 'Jewish cemetery / Jewish grave yard',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.LANDUSE: Landuse.CEMETERY.value,
                        MapKeys.RELIGION: Religion.JEWISH.value,
                    },
                    {
                        MapKeys.AMENITY: Amenity.GRAVE_YARD.value,
                        MapKeys.RELIGION: Religion.JEWISH.value,
                    }
                ]
            },
            CityPlanning.LANDUSE_CEMETERY_MUSLIM.value: {
                FIELD_TITLE: 'Muslim cemetery / Muslim grave yard',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.LANDUSE: Landuse.CEMETERY.value,
                        MapKeys.RELIGION: Religion.MUSLIM.value,
                    },
                    {
                        MapKeys.AMENITY: Amenity.GRAVE_YARD.value,
                        MapKeys.RELIGION: Religion.MUSLIM.value,
                    }
                ]
            },
            CityPlanning.LANDUSE_COMMERCIAL.value: {
                FIELD_TITLE: 'Commercial area or business park (predominantly offices)',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.LANDUSE: Landuse.COMMERCIAL.value,
                    }
                ]
            },
            CityPlanning.LANDUSE_CONSTRUCTION_MAPNIK.value: {
                FIELD_TITLE: 'Brownfield / Construction yard',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.LANDUSE: Landuse.BROWNFIELD.value,
                    },
                    {
                        MapKeys.LANDUSE: Landuse.CONSTRUCTION.value,
                    }
                ]
            },
            CityPlanning.LANDUSE_INDUSTRIAL.value: {
                FIELD_TITLE: 'Industrial area / Area for railway usage / Waterworks / Wastewater plant',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.LANDUSE: Landuse.INDUSTRIAL.value,
                    },
                    {
                        MapKeys.LANDUSE: Landuse.RAILWAY.value,
                    },
                    {
                        MapKeys.MAN_MADE: ManMade.WATER_WORKS.value,
                    },
                    {
                        MapKeys.MAN_MADE: ManMade.WASTEWATER_PLANT.value,
                    }
                ]
            },
            CityPlanning.LANDUSE_LANDFILL_MAPNIK.value: {
                FIELD_TITLE: 'Landfill',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.LANDUSE: Landuse.LANDFILL.value,
                    }
                ]
            },
            CityPlanning.LANDUSE_RETAIL.value: {
                FIELD_TITLE: 'Retail area (predominantly shops) / Shopping mall',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.LANDUSE: Landuse.RETAIL.value,
                    },
                    {
                        MapKeys.SHOP: Shop.MALL.value,
                    },
                    {
                        MapKeys.AMENITY: Amenity.MARKETPLACE.value,
                    }
                ]
            },
        },
        MapAreas.BUILDINGS: {
            Buildings.AEA_BUILDING_YES.value: {
                FIELD_TITLE: 'Non-specific building',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.BUILDING: '*',
                    }
                ]
            },
            Buildings.AREA_AMENITY_PLACE_OF_WORSHIP.value: {
                FIELD_TITLE: 'Airport terminal / Train station / Aerialway station / Bus station / Place of worship where religious practices are held, i.e. church, synagogue, mosque, temple.',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.AEROWAY: Aeroway.TERMINAL.value,
                        MapKeys.BUILDING: '*',
                    },
                    {
                        MapKeys.BUILDING: Building.TRAIN_STATION.value,
                    },
                    {
                        MapKeys.AERIALWAY: Aerialway.STATION.value,
                        MapKeys.BUILDING: '*',
                    },
                    {
                        MapKeys.PUBLIC_TRANSPORT: PublicTransport.STATION.value,
                        MapKeys.BUILDING: '*',
                    },
                    {
                        MapKeys.AMENITY: Amenity.PLACE_OF_WORSHIP.value,
                        MapKeys.BUILDING: '*',
                    }
                ]
            },
        },
        MapAreas.TRANSPORTATION: {
            TransportationArea.AEROWAY_AREA.value: {
                FIELD_TITLE: 'Runway / taxiway / helipad',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.AEROWAY: Aeroway.RUNWAY.value,
                    },
                    {
                        MapKeys.AEROWAY: Aeroway.TAXIWAY.value,
                    },
                    {
                        MapKeys.AEROWAY: Aeroway.HELIPAD.value,
                    }
                ]
            },
            TransportationArea.AREA_PARKING.value: {
                FIELD_TITLE: 'Car parking lot, Bicycle parking, Motorcycle parking, Taxi rank',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.AMENITY: Amenity.PARKING.value,
                    },
                    {
                        MapKeys.AMENITY: Amenity.BICYCLE_PARKING.value,
                    },
                    {
                        MapKeys.AMENITY: Amenity.MOTORCYCLE_PARKING.value,
                    },
                    {
                        MapKeys.AMENITY: Amenity.TAXI.value,
                    }
                ]
            },
            TransportationArea.AREA_TRANSPORTATION.value: {
                FIELD_TITLE: 'Airport, Ferry terminal, Bus station',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.AEROWAY: Aeroway.AERODROME.value,
                    },
                    {
                        MapKeys.AMENITY: Amenity.FERRY_TERMINAL.value,
                    },
                    {
                        MapKeys.AMENITY: Amenity.BUS_STATION.value,
                    }
                ]
            },
            TransportationArea.HIGHWAY_LIVING_STREET_AREA.value: {
                FIELD_TITLE: 'Living street as an freely routable area',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.HIGHWAY: Highway.LIVING_STREET.value,
                        MapKeys.AREA: Area.YES.value,
                    }
                ]
            },
            TransportationArea.HIGHWAY_PEDESTRIAN_FOOTWAY_PATH_AREA.value: {
                FIELD_TITLE: 'Pedestrian street or footway as a freely routable area',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.HIGHWAY: Highway.PEDESTRIAN.value,
                        MapKeys.AREA: Area.YES.value,
                    },
                    {
                        MapKeys.HIGHWAY: Highway.FOOTWAY.value,
                        MapKeys.AREA: Area.YES.value,
                    }
                ]
            },
            TransportationArea.HIGHWAY_RAILWAY_PLATFORM_AREA.value: {
                FIELD_TITLE: 'Platform at a bus stop or station / Railway platform',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.HIGHWAY: Highway.PLATFORM.value,
                    },
                    {
                        MapKeys.RAILWAY: Railway.PLATFORM.value,
                    }
                ]
            },
            TransportationArea.HIGHWAY_SERVICE_RESIDENTIAL_UNCLASSIFIED_AREA.value: {
                FIELD_TITLE: 'Service highway as a freely routable area',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.HIGHWAY: Highway.SERVICE.value,
                        MapKeys.AREA: Area.YES.value,
                    }
                ]
            },
            TransportationArea.HIGHWAY_SERVICES.value: {
                FIELD_TITLE: 'Place where drivers can leave a road to refuel, rest, or take refreshments / Place where drivers can leave the road to rest, but not refuel',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.HIGHWAY: Highway.SERVICES.value,
                    },
                    {
                        MapKeys.HIGHWAY: Highway.REST_AREA.value,
                    }
                ]
            },
            TransportationArea.MAN_MADE_BRIDGE.value: {
                FIELD_TITLE: 'Bridge',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.MAN_MADE: ManMade.BRIDGE.value,
                    }
                ]
            },
            TransportationArea.OSMARENDER_APRON.value: {
                FIELD_TITLE: 'Apron',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.AEROWAY: Aeroway.APRON.value,
                    }
                ]
            },
        },
        MapAreas.AGRICULTURE_INDUSTRY: {
            AgricultureIndustry.AREA_LANDUSE_FARMYARD_MAPNIK.value: {
                FIELD_TITLE: 'Farmyard',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.LANDUSE: Landuse.FARMLAND.value,
                    }
                ]
            },
            AgricultureIndustry.AREA_LEISURE_GARDEN.value: {
                FIELD_TITLE: 'Garden',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.LEISURE: Leisure.GARDEN.value,
                    }
                ]
            },
            AgricultureIndustry.DAM_AREA.value: {
                FIELD_TITLE: 'Dam',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.WATERWAY: Waterway.DAM.value,
                    }
                ]
            },
            AgricultureIndustry.LANDUSE_ALLOTMENTS.value: {
                FIELD_TITLE: 'Allotments',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.LANDUSE: Landuse.ALLOTMENTS.value,
                    }
                ]
            },
            AgricultureIndustry.LANDUSE_FARM_MAPNIK.value: {
                FIELD_TITLE: 'Farmland / Land area used for growing plants in greenhouses',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.LANDUSE: Landuse.FARMLAND.value,
                    },
                    {
                        MapKeys.LANDUSE: Landuse.GREENHOUSE_HORTICULTURE.value,
                    }
                ]
            },
            AgricultureIndustry.LANDUSE_FOREST.value: {
                FIELD_TITLE: 'Managed forest',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.LANDUSE: Landuse.FOREST.value,
                    }
                ]
            },
            AgricultureIndustry.LANDUSE_PLANT_NURSERY.value: {
                FIELD_TITLE: 'Plant nursery',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.LANDUSE: Landuse.PLANT_NURSERY.value,
                    }
                ]
            },
            AgricultureIndustry.LANDUSE_QUARRY_MAPNIK.value: {
                FIELD_TITLE: 'Quarry',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.LANDUSE: Landuse.QUARRY.value,
                    }
                ]
            },
            AgricultureIndustry.LANDUSE_VINEYARD.value: {
                FIELD_TITLE: 'Vineyard',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.LANDUSE: Landuse.VINEYARD.value,
                    }
                ]
            },
            AgricultureIndustry.MAN_MADE_BREAKWATER_AREA.value: {
                FIELD_TITLE: 'Breakwater / Groyne',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.MAN_MADE: ManMade.BREAKWATER.value,
                        MapKeys.AREA: Area.YES.value,
                    },
                    {
                        MapKeys.MAN_MADE: ManMade.GROYNE.value,
                        MapKeys.AREA: Area.YES.value,
                    }
                ]
            },
            AgricultureIndustry.ORCHARD.value: {
                FIELD_TITLE: 'Orchard',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.LANDUSE: Landuse.ORCHARD.value,
                    }
                ]
            },
        },
        MapAreas.ELECTRICITY: {
            ElectricityArea.AREA_POWER.value: {
                FIELD_TITLE: 'Generator / Substation / Plant',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.POWER: Power.GENERATOR.value,
                    },
                    {
                        MapKeys.POWER: Power.SUBSTATION.value,
                    },
                    {
                        MapKeys.POWER: Power.PLANT.value,
                    }
                ]
            },
        },
        MapAreas.LEISURE_RECREATION: {
            LeisureRecreation.AREA_LEISURE_PARK.value: {
                FIELD_TITLE: 'Park',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.LEISURE: Leisure.PARK.value,
                    }
                ]
            },
            LeisureRecreation.AREA_LEISURE_PLAYGROUND.value: {
                FIELD_TITLE: 'Playground / Fitness station',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.LEISURE: Leisure.PLAYGROUND.value,
                    },
                    {
                        MapKeys.LEISURE: Leisure.FITNESS_STATION.value,
                    },
                    {
                        MapKeys.LEISURE: Leisure.SPORTS_CENTRE.value,
                    },
                    {
                        MapKeys.LEISURE: Leisure.STADIUM.value,
                    }
                ]
            },
            LeisureRecreation.AREA_TOURISM_CAMPSITE.value: {
                FIELD_TITLE: 'Campsite / Caravansite',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.TOURISM: Tourism.CAMP_SITE.value,
                    },
                    {
                        MapKeys.TOURISM: Tourism.CARAVAN_SITE.value,
                    }
                ]
            },
            LeisureRecreation.LANDUSE_FLOWERBED.value: {
                FIELD_TITLE: 'Flowerbed',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.LANDUSE: Landuse.FLOWERBED.value,
                    }
                ]
            },
            LeisureRecreation.LANDUSE_GRASS.value: {
                FIELD_TITLE: '(managed) Grassland / (managed) Meadow / Village green / Teeing ground of a golf course / Fairway of a golf course / Driving range of a golf course',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.LANDUSE: Landuse.GRASS.value,
                    },
                    {
                        MapKeys.LANDUSE: Landuse.MEADOW.value,
                    },
                    {
                        MapKeys.LANDUSE: Landuse.VILLAGE_GREEN.value,
                    },
                    {
                        MapKeys.GOLF: Golf.TEE.value,
                    },
                    {
                        MapKeys.GOLF: Golf.FAIRWAY.value,
                    },
                    {
                        MapKeys.GOLF: Golf.DRIVING_RANGE.value,
                    }
                ]
            },
            LeisureRecreation.LANDUSE_RECREATION_GROUND.value: {
                FIELD_TITLE: 'Recreation ground',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.LANDUSE: Landuse.RECREATION_GROUND.value,
                    }
                ]
            },
            LeisureRecreation.LEISURE_DOG_PARK.value: {
                FIELD_TITLE: 'Dog park',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.LEISURE: Leisure.DOG_PARK.value,
                    }
                ]
            },
        },
        MapAreas.SPORTS: {
            Sports.AREA_GOLF_MINIGOLF.value: {
                FIELD_TITLE: 'Golf course / Miniature golf course',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.LEISURE: Leisure.GOLF_COURSE.value,
                    },
                    {
                        MapKeys.LEISURE: Leisure.MINIATURE_GOLF.value,
                    }
                ]
            },
            Sports.GOLF_GREEN.value: {
                FIELD_TITLE: 'Putting green of a golf course',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.GOLF: Golf.GREEN.value,
                    }
                ]
            },
            Sports.GOLF_ROUGH.value: {
                FIELD_TITLE: 'Golf rough',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.GOLF: Golf.ROUGH.value,
                    }
                ]
            },
            Sports.LEISURE_ICE_RINK.value: {
                FIELD_TITLE: 'A place where you can skate and play bandy or ice hockey',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.LEISURE: Leisure.ICE_RINK.value,
                    }
                ]
            },
            Sports.LEISURE_PITCH.value: {
                FIELD_TITLE: 'Sports pitch (i.e. soccer field, basketball field, etc.) / Running track',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.LEISURE: Leisure.PITCH.value,
                    },
                    {
                        MapKeys.LEISURE: Leisure.TRACK.value,
                    }
                ]
            },
        },
        MapAreas.INSTITUTIONAL_AREAS: {
            InstitutionalAreas.AREA_AMENITY_PRISON.value: {
                FIELD_TITLE: 'Prison ground',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.AMENITY: Amenity.PRISON.value,
                    }
                ]
            },
            InstitutionalAreas.AREA_AMENITY_SCHOOL.value: {
                FIELD_TITLE: 'Area which belongs to a kindergarten, school, college, university, community centre, social facility, arts centre, hospital, clinic',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.AMENITY: Amenity.KINDERGARTEN.value,
                    },
                    {
                        MapKeys.AMENITY: Amenity.SCHOOL.value,
                    },
                    {
                        MapKeys.AMENITY: Amenity.COLLEGE.value,
                    },
                    {
                        MapKeys.AMENITY: Amenity.UNIVERSITY.value,
                    },
                    {
                        MapKeys.AMENITY: Amenity.COMMUNITY_CENTRE.value,
                    },
                    {
                        MapKeys.AMENITY: Amenity.SOCIAL_FACILITY.value,
                    },
                    {
                        MapKeys.AMENITY: Amenity.ARTS_CENTRE.value,
                    },
                    {
                        MapKeys.AMENITY: Amenity.HOSPITAL.value,
                    },
                    {
                        MapKeys.AMENITY: Amenity.CLINIC.value,
                    }
                ]
            },
            InstitutionalAreas.AREA_POLICE_FIRE_STATION.value: {
                FIELD_TITLE: 'Police station / Fire station',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.AMENITY: Amenity.POLICE.value,
                    },
                    {
                        MapKeys.AMENITY: Amenity.FIRE_STATION.value,
                    }
                ]
            },
            InstitutionalAreas.PLACE_OF_WORSHIP_AREA.value: {
                FIELD_TITLE: 'Religious ground / Place of worship where religious practices are held (other than building).',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.AMENITY: Amenity.PLACE_OF_WORSHIP.value,
                    }
                ]
            },
        },
        MapAreas.MILITARY: {
            MilitaryArea.AREA_MILITARY_EQUALS_DANGER_AREA.value: {
                FIELD_TITLE: 'A military zone which has been be declared to be dangerous for some reason (i.e. a firing range, bombing range, etc.).',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.MILITARY: Military.DANGER_AREA.value,
                    }
                ]
            },
            MilitaryArea.LANDUSE_MILITARY_MAPNIK.value: {
                FIELD_TITLE: 'Land used by the military.',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.LANDUSE: Landuse.MILITARY.value,
                    }
                ]
            },
        },
        MapAreas.MISCELLANEOUS_FRAMED_AREAS: {
            MiscellaneousFramedAreas.AREA_TOURISM_ZOO.value: {
                FIELD_TITLE: 'Zoo',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.TOURISM: Tourism.ZOO.value,
                    }
                ]
            },
            MiscellaneousFramedAreas.BOUNDARY_ABORIGINAL_LANDS.value: {
                FIELD_TITLE: 'Aboriginal Lands',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.BOUNDARY: Boundary.ABORIGINAL_LANDS.value,
                    }
                ]
            },
            MiscellaneousFramedAreas.LEISURE_MARINA.value: {
                FIELD_TITLE: 'Marina',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.LEISURE: Leisure.MARINA.value,
                    }
                ]
            },
            MiscellaneousFramedAreas.MAN_MADE_WORKS.value: {
                FIELD_TITLE: 'A factory or industrial production plant',
                FIELD_ICON: ImageType.SVG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.MAN_MADE: ManMade.WORKS.value,
                    }
                ]
            },
            MiscellaneousFramedAreas.NATIONAL_PARK.value: {
                FIELD_TITLE: 'National park / Nature reserve',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.BOUNDARY: Boundary.NATIONAL_PARK.value,
                    },
                    {
                        MapKeys.LEISURE: Leisure.NATURE_RESERVE.value,
                    }
                ]
            },
            MiscellaneousFramedAreas.PARKING_SPACE.value: {
                FIELD_TITLE: 'single parking space on a parking lot',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.AMENITY: Amenity.PARKING_SPACE.value,
                    }
                ]
            },
            MiscellaneousFramedAreas.THEME_PARK.value: {
                FIELD_TITLE: 'Theme park, Amusement park, Discovery park, Open-air museum, Miniature park',
                FIELD_ICON: ImageType.PNG.value,
                FIELD_REQUIREMENTS: [
                    {
                        MapKeys.TOURISM: Tourism.THEME_PARK.value,
                    }
                ]
            },
        },
    }

from typing import ClassVar


class MapSymbols:

    def __new__(cls, *args, **kwargs):
        """Prevent instantiation of this static utility class."""
        raise TypeError(f'{cls.__name__} is a static utility class and cannot be instantiated.')

    ADMINISTRATIVE_FACILITIES: ClassVar[str] = 'administrative_facilities'
    COMMUNICATION: ClassVar[str] = 'communication'
    CULTURE_ENTERTAINMENT_ARTS: ClassVar[str] = 'culture_entertainment_arts'
    ELECTRICITY: ClassVar[str] = 'electricity'
    FINANCE: ClassVar[str] = 'finance'
    GASTRONOMY: ClassVar[str] = 'gastronomy'
    HEALTH_CARE: ClassVar[str] = 'health_care'
    HISTORICAL_OBJECTS: ClassVar[str] = 'historical_objects'
    LANDMARKS_MAN_MADE_INFRASTRUCTURE_MASTS_TOWERS: ClassVar[str] = 'landmarks_man_made_infrastructure_masts_towers'
    LEISURE_RECREATION_SPORTS: ClassVar[str] = 'leisure_recreation_sports'
    NATURE: ClassVar[str] = 'nature'
    OUTDOOR: ClassVar[str] = 'outdoor'
    PLACES: ClassVar[str] = 'places'
    RELIGIOUS_PLACE: ClassVar[str] = 'religious_place'
    ROAD_FEATURES: ClassVar[str] = 'road_features'
    SHOPS_SERVICES: ClassVar[str] = 'shops_services'
    TOURISM_ACCOMMODATION: ClassVar[str] = 'tourism_accommodation'
    TRANSPORTATION: ClassVar[str] = 'transportation'
    WASTE_MANAGEMENT: ClassVar[str] = 'waste_management'

    NAME_KEYS: ClassVar[dict[str, str]] = {
        ADMINISTRATIVE_FACILITIES: 'RES_MAP_SYMBOL.ADMINISTRATIVE_FACILITIES',
        COMMUNICATION: 'RES_MAP_SYMBOL.COMMUNICATION',
        CULTURE_ENTERTAINMENT_ARTS: 'RES_MAP_SYMBOL.CULTURE_ENTERTAINMENT_ARTS',
        ELECTRICITY: 'RES_MAP_SYMBOL.ELECTRICITY',
        FINANCE: 'RES_MAP_SYMBOL.FINANCE',
        GASTRONOMY: 'RES_MAP_SYMBOL.GASTRONOMY',
        HEALTH_CARE: 'RES_MAP_SYMBOL.HEALTH_CARE',
        HISTORICAL_OBJECTS: 'RES_MAP_SYMBOL.HISTORICAL_OBJECTS',
        LANDMARKS_MAN_MADE_INFRASTRUCTURE_MASTS_TOWERS: 'RES_MAP_SYMBOL.LANDMARKS_MAN_MADE_INFRASTRUCTURE_MASTS_TOWERS',
        LEISURE_RECREATION_SPORTS: 'RES_MAP_SYMBOL.LEISURE_RECREATION_SPORTS',
        NATURE: 'RES_MAP_SYMBOL.NATURE',
        OUTDOOR: 'RES_MAP_SYMBOL.OUTDOOR',
        PLACES: 'RES_MAP_SYMBOL.PLACES',
        RELIGIOUS_PLACE: 'RES_MAP_SYMBOL.RELIGIOUS_PLACE',
        ROAD_FEATURES: 'RES_MAP_SYMBOL.ROAD_FEATURES',
        SHOPS_SERVICES: 'RES_MAP_SYMBOL.SHOPS_SERVICES',
        TOURISM_ACCOMMODATION: 'RES_MAP_SYMBOL.TOURISM_ACCOMMODATION',
        TRANSPORTATION: 'RES_MAP_SYMBOL.TRANSPORTATION',
        WASTE_MANAGEMENT: 'RES_MAP_SYMBOL.WASTE_MANAGEMENT'
    }

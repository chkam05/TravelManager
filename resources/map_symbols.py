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

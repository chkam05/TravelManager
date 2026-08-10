from typing import ClassVar


class MapAreas:

    def __new__(cls, *args, **kwargs):
        """Prevent instantiation of this static utility class."""
        raise TypeError(f'{cls.__name__} is a static utility class and cannot be instantiated.')

    AGRICULTURE_INDUSTRY: ClassVar[str] = 'agriculture_industry'
    BUILDINGS: ClassVar[str] = 'buildings'
    CITY_PLANNING: ClassVar[str] = 'city_planning'
    ELECTRICITY: ClassVar[str] = 'electricity'
    INSTITUTIONAL_AREAS: ClassVar[str] = 'institutional_areas'
    LEISURE_RECREATION: ClassVar[str] = 'leisure_recreation'
    MILITARY: ClassVar[str] = 'military'
    MISCELLANEOUS_FRAMED_AREAS: ClassVar[str] = 'miscellaneous_framed_areas'
    NATURE: ClassVar[str] = 'nature'
    SPORTS: ClassVar[str] = 'sports'
    TRANSPORTATION: ClassVar[str] = 'transportation'

    NAME_KEYS: ClassVar[dict[str, str]] = {
        AGRICULTURE_INDUSTRY: 'RES_MAP_AREA.AGRICULTURE_INDUSTRY',
        BUILDINGS: 'RES_MAP_AREA.BUILDINGS',
        CITY_PLANNING: 'RES_MAP_AREA.CITY_PLANNING',
        ELECTRICITY: 'RES_MAP_AREA.ELECTRICITY',
        INSTITUTIONAL_AREAS: 'RES_MAP_AREA.INSTITUTIONAL_AREAS',
        LEISURE_RECREATION: 'RES_MAP_AREA.LEISURE_RECREATION',
        MILITARY: 'RES_MAP_AREA.MILITARY',
        MISCELLANEOUS_FRAMED_AREAS: 'RES_MAP_AREA.MISCELLANEOUS_FRAMED_AREAS',
        NATURE: 'RES_MAP_AREA.NATURE',
        SPORTS: 'RES_MAP_AREA.SPORTS',
        TRANSPORTATION: 'RES_MAP_AREA.TRANSPORTATION'
    }

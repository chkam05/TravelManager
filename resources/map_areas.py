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

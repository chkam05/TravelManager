from typing import ClassVar


class MapLines:

    def __new__(cls, *args, **kwargs):
        """Prevent instantiation of this static utility class."""
        raise TypeError(f'{cls.__name__} is a static utility class and cannot be instantiated.')

    AERIAL_LIFTS: ClassVar[str] = 'aerial_lifts'
    AGRICULTURAL_FORESTRY_ROADS: ClassVar[str] = 'agricultural_forestry_roads'
    BARRIERS: ClassVar[str] = 'barriers'
    BOUNDARIES: ClassVar[str] = 'boundaries'
    CITY_ROADS: ClassVar[str] = 'city_roads'
    ENERGY_SUPPLY: ClassVar[str] = 'energy_supply'
    MAJOR_ROADS: ClassVar[str] = 'major_roads'
    MISCELLANEOUS_ROADS: ClassVar[str] = 'miscellaneous_roads'
    NATURE: ClassVar[str] = 'nature'
    NON_MOTORIZED_VEHICLES_ROADS_WAYS: ClassVar[str] = 'non_motorized_vehicles_roads_ways'
    PLATFORMS: ClassVar[str] = 'platforms'
    RAILWAYS: ClassVar[str] = 'railways'
    WATER_TRAFFIC: ClassVar[str] = 'water_traffic'
    WATER_WAYS: ClassVar[str] = 'water_ways'

    NAME_KEYS: ClassVar[dict[str, str]] = {
        AERIAL_LIFTS: 'RES_MAP_LINE.AERIAL_LIFTS',
        AGRICULTURAL_FORESTRY_ROADS: 'RES_MAP_LINE.AGRICULTURAL_FORESTRY_ROADS',
        BARRIERS: 'RES_MAP_LINE.BARRIERS',
        BOUNDARIES: 'RES_MAP_LINE.BOUNDARIES',
        CITY_ROADS: 'RES_MAP_LINE.CITY_ROADS',
        ENERGY_SUPPLY: 'RES_MAP_LINE.ENERGY_SUPPLY',
        MAJOR_ROADS: 'RES_MAP_LINE.MAJOR_ROADS',
        MISCELLANEOUS_ROADS: 'RES_MAP_LINE.MISCELLANEOUS_ROADS',
        NATURE: 'RES_MAP_LINE.NATURE',
        NON_MOTORIZED_VEHICLES_ROADS_WAYS: 'RES_MAP_LINE.NON_MOTORIZED_VEHICLES_ROADS_WAYS',
        PLATFORMS: 'RES_MAP_LINE.PLATFORMS',
        RAILWAYS: 'RES_MAP_LINE.RAILWAYS',
        WATER_TRAFFIC: 'RES_MAP_LINE.WATER_TRAFFIC',
        WATER_WAYS: 'RES_MAP_LINE.WATER_WAYS'
    }

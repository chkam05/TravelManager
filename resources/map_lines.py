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

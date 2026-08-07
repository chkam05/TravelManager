from datetime import datetime
from typing import ClassVar


class SettingsTransferTypes:
    """Defines supported settings transfer types and their presentation metadata."""

    def __new__(cls, *args, **kwargs):
        """Prevent instantiation of this static utility class."""
        raise TypeError(f'{cls.__name__} is a static utility class and cannot be instantiated.')

    # Transfer type declarations
    FUEL_COSTS: ClassVar[str] = 'fuel_costs'
    ROUTES: ClassVar[str] = 'routes'
    FAVOURITES: ClassVar[str] = 'favourites'
    CARS: ClassVar[str] = 'cars'

    # File name declarations
    FUEL_COSTS_FILE_NAME: ClassVar[str] = 'travel_manager_fuel_prices_{timestamp}.json'
    ROUTES_FILE_NAME: ClassVar[str] = 'travel_manager_rotes_{timestamp}.json'
    FAVOURITES_FILE_NAME: ClassVar[str] = 'travel_manager_favourites_{timestamp}.json'
    CARS_FILE_NAME: ClassVar[str] = 'travel_manager_cars_{timestamp}.json'

    # Label declarations
    FUEL_COSTS_LABEL: ClassVar[str] = 'Ceny paliwa'
    ROUTES_LABEL: ClassVar[str] = 'Trasy'
    FAVOURITES_LABEL: ClassVar[str] = 'Ulubione i Tagi'
    CARS_LABEL: ClassVar[str] = 'Samochody'

    VALUES: ClassVar[tuple[str, ...]] = (FUEL_COSTS, ROUTES, FAVOURITES, CARS)

    @classmethod
    def is_supported(cls, data_type: str) -> bool:
        """Checks whether a settings transfer type is supported."""
        return data_type in cls.VALUES

    @classmethod
    def file_name(cls, data_type: str, now: datetime | None = None) -> str:
        """Returns the default export file name for a transfer type."""
        timestamp = (now or datetime.now()).strftime('%Y%m%d_%H%M%S')
        if data_type == cls.FUEL_COSTS:
            template = cls.FUEL_COSTS_FILE_NAME
        elif data_type == cls.ROUTES:
            template = cls.ROUTES_FILE_NAME
        elif data_type == cls.FAVOURITES:
            template = cls.FAVOURITES_FILE_NAME
        elif data_type == cls.CARS:
            template = cls.CARS_FILE_NAME
        else:
            raise ValueError('Unsupported settings transfer type.')
        return template.format(timestamp=timestamp)

    @classmethod
    def label(cls, data_type: str) -> str:
        """Returns the display label for a transfer type."""
        if data_type == cls.FUEL_COSTS:
            return cls.FUEL_COSTS_LABEL
        if data_type == cls.ROUTES:
            return cls.ROUTES_LABEL
        if data_type == cls.FAVOURITES:
            return cls.FAVOURITES_LABEL
        if data_type == cls.CARS:
            return cls.CARS_LABEL
        raise ValueError('Unsupported settings transfer type.')

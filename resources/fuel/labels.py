from typing import ClassVar


class FuelLabels:
    """Maps application fuel types to labels used by external sources."""

    def __new__(cls, *args, **kwargs):
        """Prevent instantiation of this static utility class."""
        raise TypeError(f'{cls.__name__} is a static utility class and cannot be instantiated.')

    VALUES: ClassVar[dict[str, str]] = {
        '95': '95',
        '98': '98',
        'diesel': 'ON',
        'gaz': 'LPG'
    }

    NAME_KEYS: ClassVar[dict[str, str]] = {
        '95': 'RES_FUEL_TYPE.PETROL_95',
        '98': 'RES_FUEL_TYPE.PETROL_98',
        'diesel': 'RES_FUEL_TYPE.DIESEL',
        'gaz': 'RES_FUEL_TYPE.LPG'
    }

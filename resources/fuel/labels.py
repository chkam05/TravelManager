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

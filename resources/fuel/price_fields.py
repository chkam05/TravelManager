from typing import ClassVar


class FuelPriceFields:
    """Fuel price fields used by fuel cost rows."""

    def __new__(cls, *args, **kwargs):
        """Prevent instantiation of this static utility class."""
        raise TypeError(f'{cls.__name__} is a static utility class and cannot be instantiated.')

    PETROL_95: ClassVar[str] = 'petrol_95'
    PETROL_98: ClassVar[str] = 'petrol_98'
    DIESEL: ClassVar[str] = 'diesel'
    LPG: ClassVar[str] = 'lpg'

    VALUES: ClassVar[tuple[str, ...]] = (PETROL_95, PETROL_98, DIESEL, LPG)

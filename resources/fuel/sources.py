from typing import ClassVar


class FuelSources:
    """External source URLs used for fuel prices and exchange rates."""

    def __new__(cls, *args, **kwargs):
        """Prevent instantiation of this static utility class."""
        raise TypeError(f'{cls.__name__} is a static utility class and cannot be instantiated.')

    AUTOCENTRUM_URL: ClassVar[str] = 'https://www.autocentrum.pl/paliwa/ceny-paliw/'
    OIL_BULLETIN_URL: ClassVar[str] = 'https://energy.ec.europa.eu/data-and-analysis/weekly-oil-bulletin_en'
    FRANKFURTER_URL: ClassVar[str] = 'https://api.frankfurter.dev/v2/rates?base=EUR'

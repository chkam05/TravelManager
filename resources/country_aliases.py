from typing import ClassVar

from resources.enums.countries.country_codes import CountryCodes
from resources.enums.countries.country_names import CountryNames


class CountryAliases:
    """Country name aliases used when parsing external tabular data."""

    def __new__(cls, *args, **kwargs):
        """Prevent instantiation of this static utility class."""
        raise TypeError(f'{cls.__name__} is a static utility class and cannot be instantiated.')

    VALUES: ClassVar[dict[str, str]] = {
        CountryNames.AUSTRIA.value: CountryCodes.AUSTRIA.value,
        CountryNames.BELGIUM.value: CountryCodes.BELGIUM.value,
        CountryNames.BULGARIA.value: CountryCodes.BULGARIA.value,
        CountryNames.CROATIA.value: CountryCodes.CROATIA.value,
        CountryNames.CYPRUS.value: CountryCodes.CYPRUS.value,
        CountryNames.CZECHIA.value: CountryCodes.CZECHIA.value,
        CountryNames.CZECH_REPUBLIC.value: CountryCodes.CZECH_REPUBLIC.value,
        CountryNames.DENMARK.value: CountryCodes.DENMARK.value,
        CountryNames.ESTONIA.value: CountryCodes.ESTONIA.value,
        CountryNames.FINLAND.value: CountryCodes.FINLAND.value,
        CountryNames.FRANCE.value: CountryCodes.FRANCE.value,
        CountryNames.GERMANY.value: CountryCodes.GERMANY.value,
        CountryNames.GREECE.value: CountryCodes.GREECE.value,
        CountryNames.HELLAS.value: CountryCodes.HELLAS.value,
        CountryNames.HUNGARY.value: CountryCodes.HUNGARY.value,
        CountryNames.IRELAND.value: CountryCodes.IRELAND.value,
        CountryNames.ITALY.value: CountryCodes.ITALY.value,
        CountryNames.LATVIA.value: CountryCodes.LATVIA.value,
        CountryNames.LITHUANIA.value: CountryCodes.LITHUANIA.value,
        CountryNames.LUXEMBOURG.value: CountryCodes.LUXEMBOURG.value,
        CountryNames.MALTA.value: CountryCodes.MALTA.value,
        CountryNames.MOLDOVA.value: CountryCodes.MOLDOVA.value,
        CountryNames.NETHERLANDS.value: CountryCodes.NETHERLANDS.value,
        CountryNames.POLAND.value: CountryCodes.POLAND.value,
        CountryNames.PORTUGAL.value: CountryCodes.PORTUGAL.value,
        CountryNames.ROMANIA.value: CountryCodes.ROMANIA.value,
        CountryNames.SLOVAKIA.value: CountryCodes.SLOVAKIA.value,
        CountryNames.SLOVENIA.value: CountryCodes.SLOVENIA.value,
        CountryNames.SPAIN.value: CountryCodes.SPAIN.value,
        CountryNames.SWITZERLAND.value: CountryCodes.SWITZERLAND.value,
        CountryNames.SWEDEN.value: CountryCodes.SWEDEN.value,
    }

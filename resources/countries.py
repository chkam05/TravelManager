from typing import ClassVar

from resources.enums.countries.country_codes import CountryCodes
from resources.enums.countries.country_translation_pl import CountryTranslationPl
from resources.enums.countries.currency_codes import CurrencyCodes


class Countries:
    """Static European country presets used by fuel cost settings."""

    def __new__(cls, *args, **kwargs):
        """Prevent instantiation of this static utility class."""
        raise TypeError(f'{cls.__name__} is a static utility class and cannot be instantiated.')

    FIELD_COUNTRY: ClassVar[str] = 'country'
    FIELD_CURRENCY: ClassVar[str] = 'currency'

    VALUES: ClassVar[dict[str, dict[str, str]]] = {
        CountryCodes.ANDORRA.value: {
            FIELD_COUNTRY: CountryTranslationPl.ANDORRA.value,
            FIELD_CURRENCY: CurrencyCodes.EURO.value,
        },
        CountryCodes.ALBANIA.value: {
            FIELD_COUNTRY: CountryTranslationPl.ALBANIA.value,
            FIELD_CURRENCY: CurrencyCodes.ALBANIAN_LEK.value,
        },
        CountryCodes.AUSTRIA.value: {
            FIELD_COUNTRY: CountryTranslationPl.AUSTRIA.value,
            FIELD_CURRENCY: CurrencyCodes.EURO.value,
        },
        CountryCodes.BOSNIA_AND_HERZEGOVINA.value: {
            FIELD_COUNTRY: CountryTranslationPl.BOSNIA_AND_HERZEGOVINA.value,
            FIELD_CURRENCY: CurrencyCodes.BOSNIA_AND_HERZEGOVINA_CONVERTIBLE_MARK.value,
        },
        CountryCodes.BELGIUM.value: {
            FIELD_COUNTRY: CountryTranslationPl.BELGIUM.value,
            FIELD_CURRENCY: CurrencyCodes.EURO.value,
        },
        CountryCodes.BULGARIA.value: {
            FIELD_COUNTRY: CountryTranslationPl.BULGARIA.value,
            FIELD_CURRENCY: CurrencyCodes.BULGARIAN_LEV.value,
        },
        CountryCodes.BELARUS.value: {
            FIELD_COUNTRY: CountryTranslationPl.BELARUS.value,
            FIELD_CURRENCY: CurrencyCodes.BELARUSIAN_RUBLE.value,
        },
        CountryCodes.SWITZERLAND.value: {
            FIELD_COUNTRY: CountryTranslationPl.SWITZERLAND.value,
            FIELD_CURRENCY: CurrencyCodes.SWISS_FRANC.value,
        },
        CountryCodes.CYPRUS.value: {
            FIELD_COUNTRY: CountryTranslationPl.CYPRUS.value,
            FIELD_CURRENCY: CurrencyCodes.EURO.value,
        },
        CountryCodes.CZECHIA.value: {
            FIELD_COUNTRY: CountryTranslationPl.CZECHIA.value,
            FIELD_CURRENCY: CurrencyCodes.CZECH_KORUNA.value,
        },
        CountryCodes.GERMANY.value: {
            FIELD_COUNTRY: CountryTranslationPl.GERMANY.value,
            FIELD_CURRENCY: CurrencyCodes.EURO.value,
        },
        CountryCodes.DENMARK.value: {
            FIELD_COUNTRY: CountryTranslationPl.DENMARK.value,
            FIELD_CURRENCY: CurrencyCodes.DANISH_KRONE.value,
        },
        CountryCodes.ESTONIA.value: {
            FIELD_COUNTRY: CountryTranslationPl.ESTONIA.value,
            FIELD_CURRENCY: CurrencyCodes.EURO.value,
        },
        CountryCodes.GREECE.value: {
            FIELD_COUNTRY: CountryTranslationPl.GREECE.value,
            FIELD_CURRENCY: CurrencyCodes.EURO.value,
        },
        CountryCodes.SPAIN.value: {
            FIELD_COUNTRY: CountryTranslationPl.SPAIN.value,
            FIELD_CURRENCY: CurrencyCodes.EURO.value,
        },
        CountryCodes.FINLAND.value: {
            FIELD_COUNTRY: CountryTranslationPl.FINLAND.value,
            FIELD_CURRENCY: CurrencyCodes.EURO.value,
        },
        CountryCodes.FRANCE.value: {
            FIELD_COUNTRY: CountryTranslationPl.FRANCE.value,
            FIELD_CURRENCY: CurrencyCodes.EURO.value,
        },
        CountryCodes.CROATIA.value: {
            FIELD_COUNTRY: CountryTranslationPl.CROATIA.value,
            FIELD_CURRENCY: CurrencyCodes.EURO.value,
        },
        CountryCodes.HUNGARY.value: {
            FIELD_COUNTRY: CountryTranslationPl.HUNGARY.value,
            FIELD_CURRENCY: CurrencyCodes.HUNGARIAN_FORINT.value,
        },
        CountryCodes.IRELAND.value: {
            FIELD_COUNTRY: CountryTranslationPl.IRELAND.value,
            FIELD_CURRENCY: CurrencyCodes.EURO.value,
        },
        CountryCodes.ICELAND.value: {
            FIELD_COUNTRY: CountryTranslationPl.ICELAND.value,
            FIELD_CURRENCY: CurrencyCodes.ICELANDIC_KRONA.value,
        },
        CountryCodes.ITALY.value: {
            FIELD_COUNTRY: CountryTranslationPl.ITALY.value,
            FIELD_CURRENCY: CurrencyCodes.EURO.value,
        },
        CountryCodes.LIECHTENSTEIN.value: {
            FIELD_COUNTRY: CountryTranslationPl.LIECHTENSTEIN.value,
            FIELD_CURRENCY: CurrencyCodes.SWISS_FRANC.value,
        },
        CountryCodes.LITHUANIA.value: {
            FIELD_COUNTRY: CountryTranslationPl.LITHUANIA.value,
            FIELD_CURRENCY: CurrencyCodes.EURO.value,
        },
        CountryCodes.LUXEMBOURG.value: {
            FIELD_COUNTRY: CountryTranslationPl.LUXEMBOURG.value,
            FIELD_CURRENCY: CurrencyCodes.EURO.value,
        },
        CountryCodes.LATVIA.value: {
            FIELD_COUNTRY: CountryTranslationPl.LATVIA.value,
            FIELD_CURRENCY: CurrencyCodes.EURO.value,
        },
        CountryCodes.MONACO.value: {
            FIELD_COUNTRY: CountryTranslationPl.MONACO.value,
            FIELD_CURRENCY: CurrencyCodes.EURO.value,
        },
        CountryCodes.MOLDOVA.value: {
            FIELD_COUNTRY: CountryTranslationPl.MOLDOVA.value,
            FIELD_CURRENCY: CurrencyCodes.MOLDOVAN_LEU.value,
        },
        CountryCodes.MONTENEGRO.value: {
            FIELD_COUNTRY: CountryTranslationPl.MONTENEGRO.value,
            FIELD_CURRENCY: CurrencyCodes.EURO.value,
        },
        CountryCodes.NORTH_MACEDONIA.value: {
            FIELD_COUNTRY: CountryTranslationPl.NORTH_MACEDONIA.value,
            FIELD_CURRENCY: CurrencyCodes.MACEDONIAN_DENAR.value,
        },
        CountryCodes.MALTA.value: {
            FIELD_COUNTRY: CountryTranslationPl.MALTA.value,
            FIELD_CURRENCY: CurrencyCodes.EURO.value,
        },
        CountryCodes.NETHERLANDS.value: {
            FIELD_COUNTRY: CountryTranslationPl.NETHERLANDS.value,
            FIELD_CURRENCY: CurrencyCodes.EURO.value,
        },
        CountryCodes.NORWAY.value: {
            FIELD_COUNTRY: CountryTranslationPl.NORWAY.value,
            FIELD_CURRENCY: CurrencyCodes.NORWEGIAN_KRONE.value,
        },
        CountryCodes.POLAND.value: {
            FIELD_COUNTRY: CountryTranslationPl.POLAND.value,
            FIELD_CURRENCY: CurrencyCodes.POLISH_ZLOTY.value,
        },
        CountryCodes.PORTUGAL.value: {
            FIELD_COUNTRY: CountryTranslationPl.PORTUGAL.value,
            FIELD_CURRENCY: CurrencyCodes.EURO.value,
        },
        CountryCodes.ROMANIA.value: {
            FIELD_COUNTRY: CountryTranslationPl.ROMANIA.value,
            FIELD_CURRENCY: CurrencyCodes.ROMANIAN_LEU.value,
        },
        CountryCodes.SERBIA.value: {
            FIELD_COUNTRY: CountryTranslationPl.SERBIA.value,
            FIELD_CURRENCY: CurrencyCodes.SERBIAN_DINAR.value,
        },
        CountryCodes.SWEDEN.value: {
            FIELD_COUNTRY: CountryTranslationPl.SWEDEN.value,
            FIELD_CURRENCY: CurrencyCodes.SWEDISH_KRONA.value,
        },
        CountryCodes.SLOVENIA.value: {
            FIELD_COUNTRY: CountryTranslationPl.SLOVENIA.value,
            FIELD_CURRENCY: CurrencyCodes.EURO.value,
        },
        CountryCodes.SLOVAKIA.value: {
            FIELD_COUNTRY: CountryTranslationPl.SLOVAKIA.value,
            FIELD_CURRENCY: CurrencyCodes.EURO.value,
        },
        CountryCodes.SAN_MARINO.value: {
            FIELD_COUNTRY: CountryTranslationPl.SAN_MARINO.value,
            FIELD_CURRENCY: CurrencyCodes.EURO.value,
        },
        CountryCodes.TURKIYE.value: {
            FIELD_COUNTRY: CountryTranslationPl.TURKIYE.value,
            FIELD_CURRENCY: CurrencyCodes.TURKISH_LIRA.value,
        },
        CountryCodes.UKRAINE.value: {
            FIELD_COUNTRY: CountryTranslationPl.UKRAINE.value,
            FIELD_CURRENCY: CurrencyCodes.UKRAINIAN_HRYVNIA.value,
        },
        CountryCodes.GREAT_BRITAIN.value: {
            FIELD_COUNTRY: CountryTranslationPl.GREAT_BRITAIN.value,
            FIELD_CURRENCY: CurrencyCodes.STERLING.value,
        },
        CountryCodes.VATICAN.value: {
            FIELD_COUNTRY: CountryTranslationPl.VATICAN.value,
            FIELD_CURRENCY: CurrencyCodes.EURO.value,
        },
        CountryCodes.KOSOVO.value: {
            FIELD_COUNTRY: CountryTranslationPl.KOSOVO.value,
            FIELD_CURRENCY: CurrencyCodes.EURO.value,
        }
    }

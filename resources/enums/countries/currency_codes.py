from core.enums.enum_str import EnumStr


class CurrencyCodes(EnumStr):
    ALBANIAN_LEK = 'ALL'
    BELARUSIAN_RUBLE = 'BYN'
    BOSNIA_AND_HERZEGOVINA_CONVERTIBLE_MARK = 'BAM'
    BULGARIAN_LEV = 'BGN'
    CZECH_KORUNA = 'CZK'
    DANISH_KRONE = 'DKK'
    EURO = 'EUR'
    HUNGARIAN_FORINT = 'HUF'
    ICELANDIC_KRONA = 'ISK'
    MACEDONIAN_DENAR = 'MKD'
    MOLDOVAN_LEU = 'MDL'
    NORWEGIAN_KRONE = 'NOK'
    POLISH_ZLOTY = 'PLN'
    ROMANIAN_LEU = 'RON'
    SERBIAN_DINAR = 'RSD'
    STERLING = 'GBP'
    SWEDISH_KRONA = 'SEK'
    SWISS_FRANC = 'CHF'
    TURKISH_LIRA = 'TRY'
    UKRAINIAN_HRYVNIA = 'UAH'

    @classmethod
    def name_keys(cls) -> dict[str, str]:
        """Returns stable translation keys indexed by ISO currency code."""
        return {
            cls.ALBANIAN_LEK.value: 'RES_CURRENCY.ALBANIAN_LEK',
            cls.BELARUSIAN_RUBLE.value: 'RES_CURRENCY.BELARUSIAN_RUBLE',
            cls.BOSNIA_AND_HERZEGOVINA_CONVERTIBLE_MARK.value: 'RES_CURRENCY.CONVERTIBLE_MARK',
            cls.BULGARIAN_LEV.value: 'RES_CURRENCY.BULGARIAN_LEV',
            cls.CZECH_KORUNA.value: 'RES_CURRENCY.CZECH_KORUNA',
            cls.DANISH_KRONE.value: 'RES_CURRENCY.DANISH_KRONE',
            cls.EURO.value: 'RES_CURRENCY.EURO',
            cls.HUNGARIAN_FORINT.value: 'RES_CURRENCY.HUNGARIAN_FORINT',
            cls.ICELANDIC_KRONA.value: 'RES_CURRENCY.ICELANDIC_KRONA',
            cls.MACEDONIAN_DENAR.value: 'RES_CURRENCY.MACEDONIAN_DENAR',
            cls.MOLDOVAN_LEU.value: 'RES_CURRENCY.MOLDOVAN_LEU',
            cls.NORWEGIAN_KRONE.value: 'RES_CURRENCY.NORWEGIAN_KRONE',
            cls.POLISH_ZLOTY.value: 'RES_CURRENCY.POLISH_ZLOTY',
            cls.ROMANIAN_LEU.value: 'RES_CURRENCY.ROMANIAN_LEU',
            cls.SERBIAN_DINAR.value: 'RES_CURRENCY.SERBIAN_DINAR',
            cls.STERLING.value: 'RES_CURRENCY.POUND_STERLING',
            cls.SWEDISH_KRONA.value: 'RES_CURRENCY.SWEDISH_KRONA',
            cls.SWISS_FRANC.value: 'RES_CURRENCY.SWISS_FRANC',
            cls.TURKISH_LIRA.value: 'RES_CURRENCY.TURKISH_LIRA',
            cls.UKRAINIAN_HRYVNIA.value: 'RES_CURRENCY.UKRAINIAN_HRYVNIA'
        }

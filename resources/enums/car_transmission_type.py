from core.enums.enum_str import EnumStr


class CarTransmissionType(EnumStr):
    # Based on common transmission types: https://en.wikipedia.org/wiki/Transmission_(mechanical_device)
    MANUAL = 'Manualna'
    AUTOMATIC = 'Automatyczna'
    SEMI_AUTOMATIC = 'Półautomatyczna'
    AUTOMATED_MANUAL = 'Zautomatyzowana manualna'
    CVT = 'CVT'
    DUAL_CLUTCH = 'Dwusprzęgłowa'

    @classmethod
    def options(cls) -> tuple[dict[str, str], ...]:
        """Returns stable values with explicit translation keys for presentation."""
        return (
            {'value': cls.MANUAL.value, 'name_key': 'RES_ENUM_CAR_TRANSMISSION_TYPE.MANUAL'},
            {'value': cls.AUTOMATIC.value, 'name_key': 'RES_ENUM_CAR_TRANSMISSION_TYPE.AUTOMATIC'},
            {'value': cls.SEMI_AUTOMATIC.value, 'name_key': 'RES_ENUM_CAR_TRANSMISSION_TYPE.SEMI_AUTOMATIC'},
            {'value': cls.AUTOMATED_MANUAL.value, 'name_key': 'RES_ENUM_CAR_TRANSMISSION_TYPE.AUTOMATED_MANUAL'},
            {'value': cls.CVT.value, 'name_key': 'RES_ENUM_CAR_TRANSMISSION_TYPE.CVT'},
            {'value': cls.DUAL_CLUTCH.value, 'name_key': 'RES_ENUM_CAR_TRANSMISSION_TYPE.DUAL_CLUTCH'}
        )

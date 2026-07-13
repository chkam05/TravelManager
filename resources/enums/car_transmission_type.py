from core.enums.enum_str import EnumStr


class CarTransmissionType(EnumStr):
    # Based on common transmission types: https://en.wikipedia.org/wiki/Transmission_(mechanical_device)
    MANUAL = 'Manualna'
    AUTOMATIC = 'Automatyczna'
    SEMI_AUTOMATIC = 'Półautomatyczna'
    AUTOMATED_MANUAL = 'Zautomatyzowana manualna'
    CVT = 'CVT'
    DUAL_CLUTCH = 'Dwusprzęgłowa'

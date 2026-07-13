from core.enums.enum_str import EnumStr


class TelescopeType(EnumStr):
    # https://wiki.openstreetmap.org/wiki/Key:telescope:type
    GAMMA = 'gamma'
    OPTICAL = 'optical'
    RADIO = 'radio'
    SOLAR = 'solar'

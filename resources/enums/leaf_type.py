from core.enums.enum_str import EnumStr


class LeafType(EnumStr):
    # https://wiki.openstreetmap.org/wiki/Key:leaf_type
    BROADLEAVED = 'broadleaved'
    LEAFLESS = 'leafless'
    MIXED = 'mixed'
    NEEDLELEAVED = 'needleleaved'

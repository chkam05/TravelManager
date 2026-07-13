from core.enums.enum_str import EnumStr


class Busway(EnumStr):
    # https://wiki.openstreetmap.org/wiki/Key:busway
    LANE = 'lane'
    OPPOSITE = 'opposite'
    OPPOSITE_LANE = 'opposite_lane'

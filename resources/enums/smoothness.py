from core.enums.enum_str import EnumStr


class Smoothness(EnumStr):
    # https://wiki.openstreetmap.org/wiki/Key:smoothness
    BAD = 'bad'
    EXCELLENT = 'excellent'
    GOOD = 'good'
    HORRIBLE = 'horrible'
    IMPASSABLE = 'impassable'
    INTERMEDIATE = 'intermediate'
    VERY_BAD = 'very_bad'
    VERY_HORRIBLE = 'very_horrible'

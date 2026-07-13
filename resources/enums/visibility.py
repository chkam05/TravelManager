from core.enums.enum_str import EnumStr


class Visibility(EnumStr):
    # https://wiki.openstreetmap.org/wiki/Key:visibility
    BAD = 'bad'
    EXCELLENT = 'excellent'
    GOOD = 'good'
    HORRIBLE = 'horrible'
    INTERMEDIATE = 'intermediate'
    NO = 'no'

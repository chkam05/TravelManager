from core.enums.enum_str import EnumStr


class TrailVisibility(EnumStr):
    # https://wiki.openstreetmap.org/wiki/Key:trail_visibility
    BAD = 'bad'
    EXCELLENT = 'excellent'
    GOOD = 'good'
    HORRIBLE = 'horrible'
    INTERMEDIATE = 'intermediate'
    NO = 'no'

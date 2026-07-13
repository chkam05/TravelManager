from core.enums.enum_str import EnumStr


class Overtaking(EnumStr):
    # https://wiki.openstreetmap.org/wiki/Key:overtaking
    BACKWARD = 'backward'
    BOTH = 'both'
    CAUTION = 'caution'
    FORWARD = 'forward'
    NO = 'no'
    YES = 'yes'

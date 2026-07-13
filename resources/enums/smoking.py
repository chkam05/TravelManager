from core.enums.enum_str import EnumStr


class Smoking(EnumStr):
    # https://wiki.openstreetmap.org/wiki/Key:smoking
    DEDICATED = 'dedicated'
    ISOLATED = 'isolated'
    NO = 'no'
    OUTSIDE = 'outside'
    SEPARATED = 'separated'
    YES = 'yes'

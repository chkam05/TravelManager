from core.enums.enum_str import EnumStr


class Change(EnumStr):
    # https://wiki.openstreetmap.org/wiki/Key:change
    NO = 'no'
    NOT_LEFT = 'not_left'
    NOT_RIGHT = 'not_right'
    ONLY_LEFT = 'only_left'
    ONLY_RIGHT = 'only_right'
    YES = 'yes'

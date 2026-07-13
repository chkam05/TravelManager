from core.enums.enum_str import EnumStr


class Boat(EnumStr):
    # https://wiki.openstreetmap.org/wiki/Key:boat
    DESIGNATED = 'designated'
    NO = 'no'
    PERMISSIVE = 'permissive'
    PRIVATE = 'private'
    YES = 'yes'

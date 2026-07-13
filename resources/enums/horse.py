from core.enums.enum_str import EnumStr


class Horse(EnumStr):
    # https://wiki.openstreetmap.org/wiki/Key:horse
    DESIGNATED = 'designated'
    DESTINATION = 'destination'
    DISMOUNT = 'dismount'
    NO = 'no'
    PERMISSIVE = 'permissive'
    PRIVATE = 'private'
    YES = 'yes'

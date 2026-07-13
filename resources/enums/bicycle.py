from core.enums.enum_str import EnumStr


class Bicycle(EnumStr):
    # https://wiki.openstreetmap.org/wiki/Key:bicycle
    CUSTOMERS = 'customers'
    DESIGNATED = 'designated'
    DESTINATION = 'destination'
    DISCOURAGED = 'discouraged'
    DISMOUNT = 'dismount'
    NO = 'no'
    OPTIONAL_SIDEPATH = 'optional_sidepath'
    PERMISSIVE = 'permissive'
    PRIVATE = 'private'
    USE_SIDEPATH = 'use_sidepath'
    YES = 'yes'

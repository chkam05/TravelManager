from core.enums.enum_str import EnumStr


class Access(EnumStr):
    # https://wiki.openstreetmap.org/wiki/Key:access
    AGRICULTURAL = 'agricultural'
    DELIVERY = 'delivery'
    DESIGNATED = 'designated'
    DESTINATION = 'destination'
    FORESTRY = 'forestry'
    NO = 'no'
    OFFICIAL = 'official'
    PERMISSIVE = 'permissive'
    PRIVATE = 'private'
    YES = 'yes'

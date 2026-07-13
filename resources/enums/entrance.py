from core.enums.enum_str import EnumStr


class Entrance(EnumStr):
    # https://wiki.openstreetmap.org/wiki/Key:entrance
    EMERGENCY = 'emergency'
    ENTRANCE = 'entrance'
    EXIT = 'exit'
    GARAGE = 'garage'
    HOME = 'home'
    MAIN = 'main'
    NO = 'no'
    SECONDARY = 'secondary'
    SERVICE = 'service'
    SHOP = 'shop'
    STAIRCASE = 'staircase'
    YES = 'yes'

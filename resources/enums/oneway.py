from core.enums.enum_str import EnumStr


class Oneway(EnumStr):
    # https://wiki.openstreetmap.org/wiki/Key:oneway
    NO = 'no'
    REVERSE = '-1'
    REVERSIBLE = 'reversible'
    YES = 'yes'

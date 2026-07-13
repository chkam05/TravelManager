from core.enums.enum_str import EnumStr


class Fee(EnumStr):
    # https://wiki.openstreetmap.org/wiki/Key:fee
    DONATION = 'donation'
    NO = 'no'
    UNKNOWN = 'unknown'
    YES = 'yes'

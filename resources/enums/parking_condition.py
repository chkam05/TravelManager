from core.enums.enum_str import EnumStr


class ParkingCondition(EnumStr):
    # https://wiki.openstreetmap.org/wiki/Key:parking:condition
    CUSTOMERS = 'customers'
    DISC = 'disc'
    FREE = 'free'
    PRIVATE = 'private'
    RESIDENTS = 'residents'
    TICKET = 'ticket'

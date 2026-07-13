from core.enums.enum_str import EnumStr


class Basin(EnumStr):
    # https://wiki.openstreetmap.org/wiki/Key:basin
    AERATION = 'aeration'
    COOLING = 'cooling'
    DETENTION = 'detention'
    EVAPORATION = 'evaporation'
    FOOTBATH = 'footbath'
    INFILTRATION = 'infiltration'
    RETENTION = 'retention'
    SETTLING = 'settling'
    WATER_REGENERATION = 'water_regeneration'

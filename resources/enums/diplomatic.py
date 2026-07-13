from core.enums.enum_str import EnumStr


class Diplomatic(EnumStr):
    # https://wiki.openstreetmap.org/wiki/Key:diplomatic
    AMBASSADORS_RESIDENCE = 'ambassadors_residence'
    CONSULATE = 'consulate'
    DELEGATION = 'delegation'
    EMBASSY = 'embassy'
    HIGH_COMMISSION = 'high_commission'
    LIAISON = 'liaison'
    NON_DIPLOMATIC = 'non_diplomatic'
    PERMANENT_MISSION = 'permanent_mission'

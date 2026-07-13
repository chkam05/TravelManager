from core.enums.enum_str import EnumStr


class CastleType(EnumStr):
    # https://wiki.openstreetmap.org/wiki/Key:castle_type
    CASTRUM = 'castrum'
    CITADEL = 'citadel'
    DEFENSIVE = 'defensive'
    FORTIFIED_CHURCH = 'fortified_church'
    FORTRESS = 'fortress'
    HILLFORT = 'hillfort'
    KREMLIN = 'kremlin'
    MANOR = 'manor'
    PALACE = 'palace'
    SHIRO = 'shiro'
    STATELY = 'stately'

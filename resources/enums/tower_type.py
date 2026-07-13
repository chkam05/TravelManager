from core.enums.enum_str import EnumStr


class TowerType(EnumStr):
    # https://wiki.openstreetmap.org/wiki/Key:tower:type
    BELL_TOWER = 'bell_tower'
    CLIMBING = 'climbing'
    CLOCK = 'clock'
    COMMUNICATION = 'communication'
    COOLING = 'cooling'
    DEFENSIVE = 'defensive'
    DIVING = 'diving'
    HOSE = 'hose'
    LIGHTING = 'lighting'
    MINARET = 'minaret'
    MONITORING = 'monitoring'
    OBSERVATION = 'observation'
    PAGODA = 'pagoda'
    RADAR = 'radar'
    SIREN = 'siren'
    WATCHTOWER = 'watchtower'

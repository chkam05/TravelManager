from core.enums.enum_str import EnumStr


class PriorityRoad(EnumStr):
    # https://wiki.openstreetmap.org/wiki/Key:priority_road
    DESIGNATED = 'designated'
    END = 'end'
    YES_UNPOSTED = 'yes_unposted'

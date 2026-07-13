from core.enums.enum_str import EnumStr


class ParkingLane(EnumStr):
    # https://wiki.openstreetmap.org/wiki/Key:parking:lane
    DIAGONAL = 'diagonal'
    FIRE_LANE = 'fire_lane'
    MARKED = 'marked'
    NO_PARKING = 'no_parking'
    NO_STOPPING = 'no_stopping'
    PARALLEL = 'parallel'
    PERPENDICULAR = 'perpendicular'

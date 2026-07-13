from core.enums.enum_str import EnumStr


class Cycleway(EnumStr):
    # https://wiki.openstreetmap.org/wiki/Key:cycleway
    LANE = 'lane'
    OPPOSITE = 'opposite'
    OPPOSITE_LANE = 'opposite_lane'
    OPPOSITE_SHARE_BUSWAY = 'opposite_share_busway'
    OPPOSITE_TRACK = 'opposite_track'
    SHARE_BUSWAY = 'share_busway'
    SHARED_LANE = 'shared_lane'
    TRACK = 'track'

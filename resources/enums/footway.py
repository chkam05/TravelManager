from core.enums.enum_str import EnumStr


class Footway(EnumStr):
    # https://wiki.openstreetmap.org/wiki/Key:footway
    ACCESS_AISLE = 'access_aisle'
    ALLEY = 'alley'
    BOTH = 'both'
    CHEMIN_DE_RONDE = 'chemin_de_ronde'
    CROSSING = 'crossing'
    LANE = 'lane'
    LEFT = 'left'
    LINK = 'link'
    NO = 'no'
    NONE = 'none'
    PATH = 'path'
    RESIDENTIAL = 'residential'
    RIGHT = 'right'
    SEPARATE = 'separate'
    SIDEWALK = 'sidewalk'
    TRAFFIC_ISLAND = 'traffic_island'

from core.enums.enum_str import EnumStr


class Crossing(EnumStr):
    # https://wiki.openstreetmap.org/wiki/Key:crossing
    INFORMAL = 'informal'
    ISLAND = 'island'
    MARKED = 'marked'
    NO = 'no'
    SEPARATE = 'separate'
    TRAFFIC_SIGNALS = 'traffic_signals'
    UNCONTROLLED = 'uncontrolled'
    UNMARKED = 'unmarked'
    ZEBRA = 'zebra'

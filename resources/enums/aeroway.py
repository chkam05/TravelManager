from core.enums.enum_str import EnumStr


class Aeroway(EnumStr):
    # https://wiki.openstreetmap.org/wiki/Key:aeroway
    AERODROME = 'aerodrome'
    AIRCRAFT_CROSSING = 'aircraft_crossing'
    APRON = 'apron'
    GATE = 'gate'
    HANGAR = 'hangar'
    HELIPAD = 'helipad'
    HELIPORT = 'heliport'
    NAVIGATIONAID = 'navigationaid'
    RUNWAY = 'runway'
    SPACEPORT = 'spaceport'
    TAXIWAY = 'taxiway'
    TERMINAL = 'terminal'
    WINDSOCK = 'windsock'

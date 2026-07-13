from core.enums.enum_str import EnumStr


class Location(EnumStr):
    # https://wiki.openstreetmap.org/wiki/Key:location
    BRIDGE = 'bridge'
    CAVE = 'cave'
    INDOOR = 'indoor'
    OUTDOOR = 'outdoor'
    OVERGROUND = 'overground'
    OVERHEAD = 'overhead'
    PLATFORM = 'platform'
    ROOF = 'roof'
    ROOFTOP = 'rooftop'
    SURFACE = 'surface'
    UNDERGROUND = 'underground'
    UNDERWATER = 'underwater'

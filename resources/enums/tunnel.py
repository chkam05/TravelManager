from core.enums.enum_str import EnumStr


class Tunnel(EnumStr):
    # https://wiki.openstreetmap.org/wiki/Key:tunnel
    AVALANCHE_PROTECTOR = 'avalanche_protector'
    BUILDING_PASSAGE = 'building_passage'
    CANAL = 'canal'
    CULVERT = 'culvert'
    FLOODED = 'flooded'
    YES = 'yes'

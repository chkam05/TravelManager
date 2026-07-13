from core.enums.enum_str import EnumStr


class BuildingPart(EnumStr):
    # https://wiki.openstreetmap.org/wiki/Key:building:part
    BALCONY = 'balcony'
    COLUMN = 'column'
    CORRIDOR = 'corridor'
    PORCH = 'porch'
    ROOF = 'roof'
    STAIRCASE = 'staircase'
    STEPS = 'steps'
    YES = 'yes'

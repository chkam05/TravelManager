from core.enums.enum_str import EnumStr


class Orientation(EnumStr):
    # https://wiki.openstreetmap.org/wiki/Key:orientation
    DIAGONAL = 'diagonal'
    PARALLEL = 'parallel'
    PERPENDICULAR = 'perpendicular'

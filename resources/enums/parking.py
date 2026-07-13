from core.enums.enum_str import EnumStr


class Parking(EnumStr):
    # https://wiki.openstreetmap.org/wiki/Key:parking
    CARPORTS = 'carports'
    GARAGE_BOXES = 'garage_boxes'
    HALF_ON_KERB = 'half_on_kerb'
    LANE = 'lane'
    MULTI_STOREY = 'multi-storey'
    NO = 'no'
    ON_KERB = 'on_kerb'
    ROOFTOP = 'rooftop'
    SEPARATE = 'separate'
    SHEDS = 'sheds'
    SHOULDER = 'shoulder'
    STREET_SIDE = 'street_side'
    SURFACE = 'surface'
    UNDERGROUND = 'underground'
    YES = 'yes'

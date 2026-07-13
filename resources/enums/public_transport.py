from core.enums.enum_str import EnumStr


class PublicTransport(EnumStr):
    # https://wiki.openstreetmap.org/wiki/Key:public_transport
    PLATFORM = 'platform'
    STATION = 'station'
    STOP_AREA = 'stop_area'
    STOP_AREA_GROUP = 'stop_area_group'
    STOP_POSITION = 'stop_position'

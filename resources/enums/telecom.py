from core.enums.enum_str import EnumStr


class Telecom(EnumStr):
    # https://wiki.openstreetmap.org/wiki/Key:telecom
    CABLE_LANDING_STATION = 'cable_landing_station'
    CONNECTION_POINT = 'connection_point'
    DATA_CENTER = 'data_center'
    DISTRIBUTION_POINT = 'distribution_point'
    EXCHANGE = 'exchange'
    LINE = 'line'
    SERVICE_DEVICE = 'service_device'

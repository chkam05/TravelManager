from core.enums.enum_str import EnumStr


class PublicTransportType(EnumStr):
    """Declares public transport vehicle types used by timetable providers."""

    BUS = 'bus'
    TRAM = 'tram'
    TROLLEY = 'trolley'

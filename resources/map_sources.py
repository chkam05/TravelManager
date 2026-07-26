from typing import ClassVar


class MapSources:
    """External map service URLs and routing profiles."""

    def __new__(cls, *args, **kwargs):
        raise TypeError(f'{cls.__name__} is a static utility class and cannot be instantiated.')

    NOMINATIM_URL: ClassVar[str] = 'https://nominatim.openstreetmap.org'
    OVERPASS_URL: ClassVar[str] = 'https://overpass-api.de/api/interpreter'
    OVERPASS_FALLBACK_URLS: ClassVar[tuple[str, ...]] = (
        'https://overpass.kumi.systems/api/interpreter',
        'https://overpass.osm.ch/api/interpreter'
    )
    OSRM_URL: ClassVar[str] = 'https://router.project-osrm.org'
    OSM_ROUTING_URL: ClassVar[str] = 'https://routing.openstreetmap.de'
    VALHALLA_URL: ClassVar[str] = 'https://valhalla1.openstreetmap.de'
    ROUTE_PROFILES: ClassVar[dict[str, tuple[str, str]]] = {
        'car': (OSRM_URL, 'driving'),
        'bicycle': (f'{OSM_ROUTING_URL}/routed-bike', 'bike'),
        'foot': (f'{OSM_ROUTING_URL}/routed-foot', 'foot')
    }

from typing import ClassVar


class OfflineMapSources:
    """Audited remote sources used by the offline-map subsystem."""

    GEOFABRIK_HOST: ClassVar[str] = 'download.geofabrik.de'
    GEOFABRIK_INDEX_URL: ClassVar[str] = (
        'https://download.geofabrik.de/index-v1-nogeom.json'
    )
    USER_AGENT: ClassVar[str] = (
        'TravelManager/1.0 (offline maps; Geofabrik catalog)'
    )

    def __new__(cls, *args, **kwargs):
        raise TypeError(f'{cls.__name__} is a static utility class.')

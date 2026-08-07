from pathlib import Path
from threading import Lock
from typing import ClassVar

from config import SETTINGS_DIR
from utils.public_transport.warsaw_downloader import WarsawDownloader


class GorzowDownloader(WarsawDownloader):
    """Downloads the current CC0 MZK Gorzów GTFS conversion."""

    BASE_URL: ClassVar[str] = 'https://mkuran.pl/gtfs/'
    CARRIER: ClassVar[str] = 'MZK Gorzów Wielkopolski'
    CITY_NAME: ClassVar[str] = 'Gorzów Wielkopolski i okolice'
    CITY_COLOR: ClassVar[str] = '#009A44'
    URL_PREFIXES: ClassVar[tuple[str, ...]] = (BASE_URL,)
    _DATABASE_PATH: ClassVar[Path] = Path(SETTINGS_DIR) / 'gorzow_gtfs.sqlite3'
    _LEGACY_DATABASE_PATH: ClassVar[Path] = (
        Path(SETTINGS_DIR) / 'public_transport' / 'gorzow' / 'gtfs.sqlite3'
    )
    _DATABASE_LOCK: ClassVar[Lock] = Lock()
    _FEEDS: ClassVar[dict[str, dict[str, str]]] = {
        'G': {
            'name': 'MZK Gorzów Wielkopolski',
            'static': 'https://mkuran.pl/gtfs/gorzow_wlkp.zip',
            'vehicles': ''
        }
    }
    _CARRIERS: ClassVar[dict[str, str]] = {
        'G': 'MZK Gorzów Wielkopolski'
    }

from pathlib import Path
from threading import Lock
from typing import ClassVar

from config import SETTINGS_DIR
from utils.public_transport.warsaw_downloader import WarsawDownloader


class RadomDownloader(WarsawDownloader):
    """Downloads the CC0 MZDiK Radom GTFS conversion published by mkuran.pl."""

    BASE_URL: ClassVar[str] = 'https://mkuran.pl/gtfs/'
    CARRIER: ClassVar[str] = 'Miejski Zarząd Dróg i Komunikacji w Radomiu'
    CITY_NAME: ClassVar[str] = 'Radom'
    CITY_COLOR: ClassVar[str] = '#E31E24'
    URL_PREFIXES: ClassVar[tuple[str, ...]] = (BASE_URL,)
    _DATABASE_PATH: ClassVar[Path] = Path(SETTINGS_DIR) / 'radom_gtfs.sqlite3'
    _LEGACY_DATABASE_PATH: ClassVar[Path] = (
        Path(SETTINGS_DIR) / 'public_transport' / 'radom' / 'gtfs.sqlite3'
    )
    _DATABASE_LOCK: ClassVar[Lock] = Lock()
    _FEEDS: ClassVar[dict[str, dict[str, str]]] = {
        'R': {
            'name': 'MZDiK Radom',
            'static': 'https://mkuran.pl/gtfs/radom.zip',
            'vehicles': 'https://cdn.zbiorkom.live/gtfs-rt/radom.pb'
        }
    }
    _CARRIERS: ClassVar[dict[str, str]] = {'R': 'Miejski Zarząd Dróg i Komunikacji w Radomiu'}

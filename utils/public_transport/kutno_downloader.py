from pathlib import Path
from threading import Lock
from typing import ClassVar

from config import SETTINGS_DIR
from utils.public_transport.warsaw_downloader import WarsawDownloader


class KutnoDownloader(WarsawDownloader):
    """Downloads the Kutno GTFS feed published by zbiorkom.live."""

    BASE_URL: ClassVar[str] = 'https://cdn.zbiorkom.live/gtfs/'
    CARRIER: ClassVar[str] = 'Komunikacja Miejska w Kutnie'
    CITY_NAME: ClassVar[str] = 'Kutno'
    CITY_COLOR: ClassVar[str] = '#6C3453'
    URL_PREFIXES: ClassVar[tuple[str, ...]] = (BASE_URL,)
    _DATABASE_PATH: ClassVar[Path] = Path(SETTINGS_DIR) / 'kutno_gtfs.sqlite3'
    _LEGACY_DATABASE_PATH: ClassVar[Path] = (
        Path(SETTINGS_DIR) / 'public_transport' / 'kutno' / 'gtfs.sqlite3'
    )
    _DATABASE_LOCK: ClassVar[Lock] = Lock()
    _FEEDS: ClassVar[dict[str, dict[str, str]]] = {
        'K': {
            'name': 'Komunikacja Miejska Kutno',
            'static': 'https://cdn.zbiorkom.live/gtfs/kutno.zip',
            'vehicles': 'https://cdn.zbiorkom.live/gtfs-rt/kutno.pb'
        }
    }
    _CARRIERS: ClassVar[dict[str, str]] = {'K': 'Komunikacja Miejska w Kutnie'}

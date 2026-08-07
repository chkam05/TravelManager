from pathlib import Path
from threading import Lock
from typing import ClassVar

from config import SETTINGS_DIR
from utils.public_transport.warsaw_downloader import WarsawDownloader


class RybnikDownloader(WarsawDownloader):
    """Downloads the Rybnik GTFS feed published by zbiorkom.live."""

    BASE_URL: ClassVar[str] = 'https://cdn.zbiorkom.live/gtfs/'
    CARRIER: ClassVar[str] = 'Komunikacja Miejska w Rybniku'
    CITY_NAME: ClassVar[str] = 'Rybnik'
    CITY_COLOR: ClassVar[str] = '#137AA5'
    URL_PREFIXES: ClassVar[tuple[str, ...]] = (BASE_URL,)
    _DATABASE_PATH: ClassVar[Path] = Path(SETTINGS_DIR) / 'rybnik_gtfs.sqlite3'
    _LEGACY_DATABASE_PATH: ClassVar[Path] = (
        Path(SETTINGS_DIR) / 'public_transport' / 'rybnik' / 'gtfs.sqlite3'
    )
    _DATABASE_LOCK: ClassVar[Lock] = Lock()
    _FEEDS: ClassVar[dict[str, dict[str, str]]] = {
        'R': {
            'name': 'KM Rybnik',
            'static': 'https://cdn.zbiorkom.live/gtfs/rybnik.zip',
            'vehicles': 'https://cdn.zbiorkom.live/gtfs-rt/rybnik.pb'
        }
    }
    _CARRIERS: ClassVar[dict[str, str]] = {'R': 'Komunikacja Miejska w Rybniku'}

from pathlib import Path
from threading import Lock
from typing import ClassVar

from config import SETTINGS_DIR
from utils.public_transport.warsaw_downloader import WarsawDownloader


class ElblagDownloader(WarsawDownloader):
    """Downloads the CC0 ZKM Elbląg GTFS conversion."""

    BASE_URL: ClassVar[str] = 'https://mkuran.pl/gtfs/'
    CARRIER: ClassVar[str] = 'Zarząd Komunikacji Miejskiej w Elblągu'
    CITY_NAME: ClassVar[str] = 'Elbląg i okolice'
    CITY_COLOR: ClassVar[str] = '#006BB6'
    URL_PREFIXES: ClassVar[tuple[str, ...]] = (BASE_URL,)
    _DATABASE_PATH: ClassVar[Path] = Path(SETTINGS_DIR) / 'elblag_gtfs.sqlite3'
    _LEGACY_DATABASE_PATH: ClassVar[Path] = (
        Path(SETTINGS_DIR) / 'public_transport' / 'elblag' / 'gtfs.sqlite3'
    )
    _DATABASE_LOCK: ClassVar[Lock] = Lock()
    _FEEDS: ClassVar[dict[str, dict[str, str]]] = {
        'E': {
            'name': 'ZKM Elbląg',
            'static': 'https://mkuran.pl/gtfs/elblag.zip',
            'vehicles': ''
        }
    }
    _CARRIERS: ClassVar[dict[str, str]] = {'E': 'ZKM Elbląg'}

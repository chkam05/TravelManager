from pathlib import Path
from threading import Lock
from typing import ClassVar

from config import SETTINGS_DIR
from utils.public_transport.warsaw_downloader import WarsawDownloader


class LublinDownloader(WarsawDownloader):
    """Downloads the CC0 ZDiTM Lublin GTFS conversion."""

    BASE_URL: ClassVar[str] = 'https://mkuran.pl/gtfs/'
    CARRIER: ClassVar[str] = 'Zarząd Dróg i Transportu Miejskiego w Lublinie'
    CITY_NAME: ClassVar[str] = 'Lublin i okolice'
    CITY_COLOR: ClassVar[str] = '#006A44'
    URL_PREFIXES: ClassVar[tuple[str, ...]] = (BASE_URL,)
    _DATABASE_PATH: ClassVar[Path] = Path(SETTINGS_DIR) / 'lublin_gtfs.sqlite3'
    _LEGACY_DATABASE_PATH: ClassVar[Path] = (
        Path(SETTINGS_DIR) / 'public_transport' / 'lublin' / 'gtfs.sqlite3'
    )
    _DATABASE_LOCK: ClassVar[Lock] = Lock()
    _FEEDS: ClassVar[dict[str, dict[str, str]]] = {
        'L': {
            'name': 'ZDiTM Lublin',
            'static': 'https://mkuran.pl/gtfs/lublin.zip',
            'vehicles': ''
        }
    }
    _CARRIERS: ClassVar[dict[str, str]] = {'L': 'ZDiTM Lublin'}

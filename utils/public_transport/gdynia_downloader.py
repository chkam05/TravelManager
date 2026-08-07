from pathlib import Path
from threading import Lock
from typing import ClassVar

from config import SETTINGS_DIR
from utils.public_transport.tricity_gtfs_downloader import TricityGtfsDownloader


class GdyniaDownloader(TricityGtfsDownloader):
    """Downloads the official ZKM Gdynia static GTFS feed."""

    BASE_URL: ClassVar[str] = 'https://api.zdiz.gdynia.pl/pt/'
    CARRIER: ClassVar[str] = 'Zarząd Komunikacji Miejskiej w Gdyni'
    CITY_NAME: ClassVar[str] = 'Gdynia i okolice'
    CITY_COLOR: ClassVar[str] = '#00A6D6'
    URL_PREFIXES: ClassVar[tuple[str, ...]] = (BASE_URL,)
    _DATABASE_PATH: ClassVar[Path] = Path(SETTINGS_DIR) / 'gdynia_gtfs.sqlite3'
    _LEGACY_DATABASE_PATH: ClassVar[Path] = (
        Path(SETTINGS_DIR) / 'public_transport' / 'gdynia' / 'gtfs.sqlite3'
    )
    _DATABASE_LOCK: ClassVar[Lock] = Lock()
    _FEEDS: ClassVar[dict[str, dict[str, str]]] = {
        'Y': {
            'name': 'ZKM Gdynia',
            'static': 'https://api.zdiz.gdynia.pl/pt/gtfs.zip',
            'vehicles': ''
        }
    }
    _CARRIERS: ClassVar[dict[str, str]] = {
        'Y': 'Zarząd Komunikacji Miejskiej w Gdyni'
    }

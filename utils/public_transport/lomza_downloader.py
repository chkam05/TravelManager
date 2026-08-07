from pathlib import Path
from threading import Lock
from typing import ClassVar

from config import SETTINGS_DIR
from utils.public_transport.warsaw_downloader import WarsawDownloader


class LomzaDownloader(WarsawDownloader):
    """Downloads the CC0 MPK Łomża GTFS conversion published by mkuran.pl."""

    BASE_URL: ClassVar[str] = 'https://mkuran.pl/gtfs/'
    CARRIER: ClassVar[str] = 'MPK ZB w Łomży'
    CITY_NAME: ClassVar[str] = 'Łomża'
    CITY_COLOR: ClassVar[str] = '#DDAA00'
    URL_PREFIXES: ClassVar[tuple[str, ...]] = (BASE_URL,)
    _DATABASE_PATH: ClassVar[Path] = Path(SETTINGS_DIR) / 'lomza_gtfs.sqlite3'
    _LEGACY_DATABASE_PATH: ClassVar[Path] = (
        Path(SETTINGS_DIR) / 'public_transport' / 'lomza' / 'gtfs.sqlite3'
    )
    _DATABASE_LOCK: ClassVar[Lock] = Lock()
    _FEEDS: ClassVar[dict[str, dict[str, str]]] = {
        'L': {
            'name': 'MPK Łomża',
            'static': 'https://mkuran.pl/gtfs/lomza.zip',
            'vehicles': ''
        }
    }
    _CARRIERS: ClassVar[dict[str, str]] = {'L': 'MPK ZB w Łomży'}

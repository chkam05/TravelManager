from pathlib import Path
from threading import Lock
from typing import ClassVar

from config import SETTINGS_DIR
from utils.public_transport.warsaw_downloader import WarsawDownloader


class WejherowoDownloader(WarsawDownloader):
    """Downloads the CC0 MZK Wejherowo GTFS conversion published by mkuran.pl."""

    BASE_URL: ClassVar[str] = 'https://mkuran.pl/gtfs/'
    CARRIER: ClassVar[str] = 'Miejski Zakład Komunikacji w Wejherowie'
    CITY_NAME: ClassVar[str] = 'Wejherowo'
    CITY_COLOR: ClassVar[str] = '#478AC9'
    URL_PREFIXES: ClassVar[tuple[str, ...]] = (BASE_URL,)
    _DATABASE_PATH: ClassVar[Path] = Path(SETTINGS_DIR) / 'wejherowo_gtfs.sqlite3'
    _LEGACY_DATABASE_PATH: ClassVar[Path] = (
        Path(SETTINGS_DIR) / 'public_transport' / 'wejherowo' / 'gtfs.sqlite3'
    )
    _DATABASE_LOCK: ClassVar[Lock] = Lock()
    _FEEDS: ClassVar[dict[str, dict[str, str]]] = {
        'W': {
            'name': 'MZK Wejherowo',
            'static': 'https://mkuran.pl/gtfs/wejherowo.zip',
            'vehicles': ''
        }
    }
    _CARRIERS: ClassVar[dict[str, str]] = {'W': 'Miejski Zakład Komunikacji w Wejherowie'}

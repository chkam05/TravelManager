from pathlib import Path
from threading import Lock
from typing import ClassVar

from config import SETTINGS_DIR
from utils.public_transport.warsaw_downloader import WarsawDownloader


class ElkDownloader(WarsawDownloader):
    """Downloads the CC0 MZK Ełk GTFS conversion published by mkuran.pl."""

    BASE_URL: ClassVar[str] = 'https://mkuran.pl/gtfs/'
    CARRIER: ClassVar[str] = 'Miejski Zakład Komunikacji w Ełku'
    CITY_NAME: ClassVar[str] = 'Ełk'
    CITY_COLOR: ClassVar[str] = '#0755AA'
    URL_PREFIXES: ClassVar[tuple[str, ...]] = (BASE_URL,)
    _DATABASE_PATH: ClassVar[Path] = Path(SETTINGS_DIR) / 'elk_gtfs.sqlite3'
    _LEGACY_DATABASE_PATH: ClassVar[Path] = (
        Path(SETTINGS_DIR) / 'public_transport' / 'elk' / 'gtfs.sqlite3'
    )
    _DATABASE_LOCK: ClassVar[Lock] = Lock()
    _FEEDS: ClassVar[dict[str, dict[str, str]]] = {
        'E': {
            'name': 'MZK Ełk',
            'static': 'https://mkuran.pl/gtfs/elk.zip',
            'vehicles': 'https://mkuran.pl/gtfs/elk.pb'
        }
    }
    _CARRIERS: ClassVar[dict[str, str]] = {'E': 'Miejski Zakład Komunikacji w Ełku'}

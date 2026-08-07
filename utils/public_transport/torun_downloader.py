from pathlib import Path
from threading import Lock
from typing import ClassVar

from config import SETTINGS_DIR
from utils.public_transport.warsaw_downloader import WarsawDownloader


class TorunDownloader(WarsawDownloader):
    """Downloads the CC0 Toruń GTFS conversion published by mkuran.pl."""

    BASE_URL: ClassVar[str] = 'https://mkuran.pl/gtfs/'
    CARRIER: ClassVar[str] = 'Miejski Zakład Komunikacji w Toruniu'
    CITY_NAME: ClassVar[str] = 'Toruń i okolice'
    CITY_COLOR: ClassVar[str] = '#005CA9'
    URL_PREFIXES: ClassVar[tuple[str, ...]] = (BASE_URL,)
    _DATABASE_PATH: ClassVar[Path] = Path(SETTINGS_DIR) / 'torun_gtfs.sqlite3'
    _LEGACY_DATABASE_PATH: ClassVar[Path] = (
        Path(SETTINGS_DIR) / 'public_transport' / 'torun' / 'gtfs.sqlite3'
    )
    _DATABASE_LOCK: ClassVar[Lock] = Lock()
    _FEEDS: ClassVar[dict[str, dict[str, str]]] = {
        'R': {
            'name': 'MZK Toruń',
            'static': 'https://mkuran.pl/gtfs/torun.zip',
            'vehicles': ''
        }
    }
    _CARRIERS: ClassVar[dict[str, str]] = {'R': 'MZK Toruń'}

    @staticmethod
    def _platform_name(row) -> str:
        """Uses Toruń's two-digit stop-post code as the platform."""
        return str(row['platform_code'] or row['stop_code'] or '').strip()

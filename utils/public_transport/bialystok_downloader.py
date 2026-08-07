from pathlib import Path
import sqlite3
from threading import Lock
from typing import ClassVar

from config import SETTINGS_DIR
from utils.public_transport.warsaw_downloader import WarsawDownloader


class BialystokDownloader(WarsawDownloader):
    """Downloads the official BKM Białystok GTFS feed."""

    BASE_URL: ClassVar[str] = 'https://komunikacja.bialystok.pl/'
    CARRIER: ClassVar[str] = 'Białostocka Komunikacja Miejska'
    CITY_NAME: ClassVar[str] = 'Białystok'
    CITY_COLOR: ClassVar[str] = '#003A7D'
    URL_PREFIXES: ClassVar[tuple[str, ...]] = (BASE_URL,)
    _DATABASE_PATH: ClassVar[Path] = Path(SETTINGS_DIR) / 'bialystok_gtfs.sqlite3'
    _LEGACY_DATABASE_PATH: ClassVar[Path] = (
        Path(SETTINGS_DIR) / 'public_transport' / 'bialystok' / 'gtfs.sqlite3'
    )
    _DATABASE_LOCK: ClassVar[Lock] = Lock()
    _FEEDS: ClassVar[dict[str, dict[str, str]]] = {
        'B': {
            'name': 'BKM Białystok',
            'static': (
                'https://komunikacja.bialystok.pl/cms/File/download/gtfs/'
                'google_transit.zip'
            ),
            'vehicles': ''
        }
    }
    _CARRIERS: ClassVar[dict[str, str]] = {'B': 'Białostocka Komunikacja Miejska'}

    @classmethod
    def _ensure_database(cls, refresh: bool = False) -> Path:
        # BKM stores the line number in route_long_name, leaving short_name empty
        path = super()._ensure_database(refresh)
        connection = sqlite3.connect(path)
        try:
            connection.execute(
                """
                    UPDATE routes SET short_name = long_name
                    WHERE short_name = '' AND long_name <> ''
                """
            )
            connection.commit()
        finally:
            connection.close()
        return path

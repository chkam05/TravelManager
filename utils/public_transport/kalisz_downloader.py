from pathlib import Path
from threading import Lock
from typing import ClassVar

from config import SETTINGS_DIR
from utils.public_transport.warsaw_downloader import WarsawDownloader


class KaliszDownloader(WarsawDownloader):
    """Downloads the KLA Kalisz GTFS feed from kasznia.net (CC-BY-4.0)."""

    BASE_URL: ClassVar[str] = 'https://gtfs.kasznia.net/static/'
    CARRIER: ClassVar[str] = 'Komunikacja Lokalna Aglomeracji w Kaliszu'
    CITY_NAME: ClassVar[str] = 'Kalisz'
    CITY_COLOR: ClassVar[str] = '#051CED'
    URL_PREFIXES: ClassVar[tuple[str, ...]] = (BASE_URL,)
    _DATABASE_PATH: ClassVar[Path] = Path(SETTINGS_DIR) / 'kalisz_gtfs.sqlite3'
    _LEGACY_DATABASE_PATH: ClassVar[Path] = (
        Path(SETTINGS_DIR) / 'public_transport' / 'kalisz' / 'gtfs.sqlite3'
    )
    _DATABASE_LOCK: ClassVar[Lock] = Lock()
    _FEEDS: ClassVar[dict[str, dict[str, str]]] = {
        'K': {
            'name': 'KLA Kalisz',
            'static': 'https://gtfs.kasznia.net/static/kalisz.zip',
            'vehicles': ''
        }
    }
    _CARRIERS: ClassVar[dict[str, str]] = {'K': 'Komunikacja Lokalna Aglomeracji w Kaliszu'}

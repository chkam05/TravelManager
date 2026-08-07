from pathlib import Path
from threading import Lock
from typing import ClassVar

from config import SETTINGS_DIR
from utils.public_transport.warsaw_downloader import WarsawDownloader


class PrzemyslDownloader(WarsawDownloader):
    """Downloads the Przemyśl GTFS feed published by zbiorkom.live."""

    BASE_URL: ClassVar[str] = 'https://cdn.zbiorkom.live/gtfs/'
    CARRIER: ClassVar[str] = 'Komunikacja Miejska w Przemyślu'
    CITY_NAME: ClassVar[str] = 'Przemyśl'
    CITY_COLOR: ClassVar[str] = '#EE1C25'
    URL_PREFIXES: ClassVar[tuple[str, ...]] = (BASE_URL,)
    _DATABASE_PATH: ClassVar[Path] = Path(SETTINGS_DIR) / 'przemysl_gtfs.sqlite3'
    _LEGACY_DATABASE_PATH: ClassVar[Path] = (
        Path(SETTINGS_DIR) / 'public_transport' / 'przemysl' / 'gtfs.sqlite3'
    )
    _DATABASE_LOCK: ClassVar[Lock] = Lock()
    _FEEDS: ClassVar[dict[str, dict[str, str]]] = {
        'P': {
            'name': 'KM Przemyśl',
            'static': 'https://cdn.zbiorkom.live/gtfs/przemysl.zip',
            'vehicles': 'https://cdn.zbiorkom.live/gtfs-rt/przemysl.pb'
        }
    }
    _CARRIERS: ClassVar[dict[str, str]] = {'P': 'Komunikacja Miejska w Przemyślu'}

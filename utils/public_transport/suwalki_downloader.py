from pathlib import Path
from threading import Lock
from typing import ClassVar

from config import SETTINGS_DIR
from utils.public_transport.warsaw_downloader import WarsawDownloader


class SuwalikiDownloader(WarsawDownloader):
    """Downloads the Suwałki GTFS feed published by zbiorkom.live."""

    BASE_URL: ClassVar[str] = 'https://cdn.zbiorkom.live/gtfs/'
    CARRIER: ClassVar[str] = 'Komunikacja Miejska w Suwałkach'
    CITY_NAME: ClassVar[str] = 'Suwałki'
    CITY_COLOR: ClassVar[str] = '#006A21'
    URL_PREFIXES: ClassVar[tuple[str, ...]] = (BASE_URL,)
    _DATABASE_PATH: ClassVar[Path] = Path(SETTINGS_DIR) / 'suwalki_gtfs.sqlite3'
    _LEGACY_DATABASE_PATH: ClassVar[Path] = (
        Path(SETTINGS_DIR) / 'public_transport' / 'suwalki' / 'gtfs.sqlite3'
    )
    _DATABASE_LOCK: ClassVar[Lock] = Lock()
    _FEEDS: ClassVar[dict[str, dict[str, str]]] = {
        'S': {
            'name': 'KM Suwałki',
            'static': 'https://cdn.zbiorkom.live/gtfs/suwalki.zip',
            'vehicles': 'https://cdn.zbiorkom.live/gtfs-rt/suwalki.pb'
        }
    }
    _CARRIERS: ClassVar[dict[str, str]] = {'S': 'Komunikacja Miejska w Suwałkach'}

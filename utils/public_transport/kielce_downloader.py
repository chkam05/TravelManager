from pathlib import Path
from threading import Lock
from typing import ClassVar

from config import SETTINGS_DIR
from utils.public_transport.warsaw_downloader import WarsawDownloader


class KielceDownloader(WarsawDownloader):
    """Downloads the ZTM Kielce GTFS feed published by mkuran.pl."""

    BASE_URL: ClassVar[str] = 'https://mkuran.pl/gtfs/'
    CARRIER: ClassVar[str] = 'Zarząd Transportu Miejskiego w Kielcach'
    CITY_NAME: ClassVar[str] = 'Kielce'
    CITY_COLOR: ClassVar[str] = '#F5BB37'
    URL_PREFIXES: ClassVar[tuple[str, ...]] = (BASE_URL,)
    _DATABASE_PATH: ClassVar[Path] = Path(SETTINGS_DIR) / 'kielce_gtfs.sqlite3'
    _LEGACY_DATABASE_PATH: ClassVar[Path] = (
        Path(SETTINGS_DIR) / 'public_transport' / 'kielce' / 'gtfs.sqlite3'
    )
    _DATABASE_LOCK: ClassVar[Lock] = Lock()
    _FEEDS: ClassVar[dict[str, dict[str, str]]] = {
        'K': {
            'name': 'ZTM Kielce',
            'static': 'https://mkuran.pl/gtfs/kielce.zip',
            'vehicles': 'https://cdn.zbiorkom.live/gtfs-rt/kielce.pb'
        }
    }
    _CARRIERS: ClassVar[dict[str, str]] = {'K': 'Zarząd Transportu Miejskiego w Kielcach'}

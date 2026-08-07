from pathlib import Path
from threading import Lock
from typing import ClassVar

from config import SETTINGS_DIR
from utils.public_transport.krakow_downloader import KrakowDownloader


class SzczecinDownloader(KrakowDownloader):
    """Downloads ZDiTM Szczecin static and realtime GTFS feeds."""

    BASE_URL: ClassVar[str] = 'https://www.zditm.szczecin.pl/'
    CARRIER: ClassVar[str] = 'Zarząd Dróg i Transportu Miejskiego w Szczecinie'
    CITY_NAME: ClassVar[str] = 'Szczecin i okolice'
    CITY_COLOR: ClassVar[str] = '#005CA9'
    URL_PREFIXES: ClassVar[tuple[str, ...]] = (BASE_URL,)
    _DATABASE_PATH: ClassVar[Path] = Path(SETTINGS_DIR) / 'szczecin_gtfs.sqlite3'
    _LEGACY_DATABASE_PATH: ClassVar[Path] = (
        Path(SETTINGS_DIR) / 'public_transport' / 'szczecin' / 'gtfs.sqlite3'
    )
    _DATABASE_LOCK: ClassVar[Lock] = Lock()
    _FEEDS: ClassVar[dict[str, dict[str, str]]] = {
        'S': {
            'name': 'ZDiTM Szczecin',
            'static': 'https://www.zditm.szczecin.pl/storage/gtfs/gtfs.zip',
            'vehicles': (
                'https://www.zditm.szczecin.pl/storage/gtfs/'
                'gtfs-rt-vehicles.pb'
            )
        }
    }
    _CARRIERS: ClassVar[dict[str, str]] = {'S': 'ZDiTM Szczecin'}

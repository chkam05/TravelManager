from pathlib import Path
from threading import Lock
from typing import ClassVar

from config import SETTINGS_DIR
from utils.public_transport.warsaw_downloader import WarsawDownloader


class LegnicaDownloader(WarsawDownloader):
    """Downloads the MPK Legnica GTFS feed published by zbiorkom.live."""

    BASE_URL: ClassVar[str] = 'https://cdn.zbiorkom.live/gtfs/'
    CARRIER: ClassVar[str] = 'Miejskie Przedsiębiorstwo Komunikacyjne w Legnicy'
    CITY_NAME: ClassVar[str] = 'Legnica'
    CITY_COLOR: ClassVar[str] = '#003FA6'
    URL_PREFIXES: ClassVar[tuple[str, ...]] = (BASE_URL,)
    _DATABASE_PATH: ClassVar[Path] = Path(SETTINGS_DIR) / 'legnica_gtfs.sqlite3'
    _LEGACY_DATABASE_PATH: ClassVar[Path] = (
        Path(SETTINGS_DIR) / 'public_transport' / 'legnica' / 'gtfs.sqlite3'
    )
    _DATABASE_LOCK: ClassVar[Lock] = Lock()
    _FEEDS: ClassVar[dict[str, dict[str, str]]] = {
        'L': {
            'name': 'MPK Legnica',
            'static': 'https://cdn.zbiorkom.live/gtfs/legnica.zip',
            'vehicles': 'https://cdn.zbiorkom.live/gtfs-rt/legnica.pb'
        }
    }
    _CARRIERS: ClassVar[dict[str, str]] = {'L': 'Miejskie Przedsiębiorstwo Komunikacyjne w Legnicy'}

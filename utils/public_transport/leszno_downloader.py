from pathlib import Path
from threading import Lock
from typing import ClassVar

from config import SETTINGS_DIR
from utils.public_transport.warsaw_downloader import WarsawDownloader


class LesznoDownloader(WarsawDownloader):
    """Downloads the MZK Leszno GTFS feed published by zbiorkom.live."""

    BASE_URL: ClassVar[str] = 'https://cdn.zbiorkom.live/gtfs/'
    CARRIER: ClassVar[str] = 'Miejski Zakład Komunikacji w Lesznie'
    CITY_NAME: ClassVar[str] = 'Leszno'
    CITY_COLOR: ClassVar[str] = '#007DBD'
    URL_PREFIXES: ClassVar[tuple[str, ...]] = (BASE_URL,)
    _DATABASE_PATH: ClassVar[Path] = Path(SETTINGS_DIR) / 'leszno_gtfs.sqlite3'
    _LEGACY_DATABASE_PATH: ClassVar[Path] = (
        Path(SETTINGS_DIR) / 'public_transport' / 'leszno' / 'gtfs.sqlite3'
    )
    _DATABASE_LOCK: ClassVar[Lock] = Lock()
    _FEEDS: ClassVar[dict[str, dict[str, str]]] = {
        'L': {
            'name': 'MZK Leszno',
            'static': 'https://cdn.zbiorkom.live/gtfs/leszno.zip',
            'vehicles': ''
        }
    }
    _CARRIERS: ClassVar[dict[str, str]] = {'L': 'Miejski Zakład Komunikacji w Lesznie'}

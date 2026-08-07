from pathlib import Path
from threading import Lock
from typing import ClassVar

from config import SETTINGS_DIR
from utils.public_transport.warsaw_downloader import WarsawDownloader


class SwinoujscieDownloader(WarsawDownloader):
    """Downloads the CC0 KA Świnoujście GTFS conversion published by mkuran.pl."""

    BASE_URL: ClassVar[str] = 'https://mkuran.pl/gtfs/'
    CARRIER: ClassVar[str] = 'Komunikacja Autobusowa w Świnoujściu'
    CITY_NAME: ClassVar[str] = 'Świnoujście'
    CITY_COLOR: ClassVar[str] = '#005F9E'
    URL_PREFIXES: ClassVar[tuple[str, ...]] = (BASE_URL,)
    _DATABASE_PATH: ClassVar[Path] = Path(SETTINGS_DIR) / 'swinoujscie_gtfs.sqlite3'
    _LEGACY_DATABASE_PATH: ClassVar[Path] = (
        Path(SETTINGS_DIR) / 'public_transport' / 'swinoujscie' / 'gtfs.sqlite3'
    )
    _DATABASE_LOCK: ClassVar[Lock] = Lock()
    _FEEDS: ClassVar[dict[str, dict[str, str]]] = {
        'W': {
            'name': 'KA Świnoujście',
            'static': 'https://mkuran.pl/gtfs/swinoujscie.zip',
            'vehicles': ''
        }
    }
    _CARRIERS: ClassVar[dict[str, str]] = {'W': 'Komunikacja Autobusowa w Świnoujściu'}

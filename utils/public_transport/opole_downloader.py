from pathlib import Path
from threading import Lock
from typing import ClassVar

from config import SETTINGS_DIR
from utils.public_transport.warsaw_downloader import WarsawDownloader


class OpoleDownloader(WarsawDownloader):
    """Downloads the MZK Opole GTFS feed published by zbiorkom.live."""

    BASE_URL: ClassVar[str] = 'https://cdn.zbiorkom.live/gtfs/'
    CARRIER: ClassVar[str] = 'MZK Sp. z o.o. Opole'
    CITY_NAME: ClassVar[str] = 'Opole'
    CITY_COLOR: ClassVar[str] = '#661118'
    URL_PREFIXES: ClassVar[tuple[str, ...]] = ('https://rozklady.mzkopole.pl/', BASE_URL)
    _DATABASE_PATH: ClassVar[Path] = Path(SETTINGS_DIR) / 'opole_gtfs.sqlite3'
    _LEGACY_DATABASE_PATH: ClassVar[Path] = (
        Path(SETTINGS_DIR) / 'public_transport' / 'opole' / 'gtfs.sqlite3'
    )
    _DATABASE_LOCK: ClassVar[Lock] = Lock()
    _FEEDS: ClassVar[dict[str, dict[str, str]]] = {
        'O': {
            'name': 'MZK Opole',
            'static': 'https://cdn.zbiorkom.live/gtfs/opole.zip',
            'vehicles': ''
        }
    }
    _CARRIERS: ClassVar[dict[str, str]] = {'O': 'MZK Sp. z o.o. Opole'}

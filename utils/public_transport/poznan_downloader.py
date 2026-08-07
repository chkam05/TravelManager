from datetime import date
from pathlib import Path
import re
from threading import Lock
from typing import ClassVar
from urllib.parse import urlencode

from config import SETTINGS_DIR
from utils.public_transport.krakow_downloader import KrakowDownloader


class PoznanDownloader(KrakowDownloader):
    """Downloads ZTM Poznań static and realtime GTFS feeds."""

    BASE_URL: ClassVar[str] = 'https://www.ztm.poznan.pl/'
    CARRIER: ClassVar[str] = 'Zarząd Transportu Miejskiego w Poznaniu'
    CITY_NAME: ClassVar[str] = 'Poznań i okolice'
    CITY_COLOR: ClassVar[str] = '#005A9C'
    URL_PREFIXES: ClassVar[tuple[str, ...]] = (BASE_URL,)
    _STATIC_ENDPOINT: ClassVar[str] = (
        'https://www.ztm.poznan.pl/pl/dla-deweloperow/getGTFSFile'
    )
    _STATIC_INDEX: ClassVar[str] = (
        'https://www.ztm.poznan.pl/otwarte-dane/gtfsfiles/'
    )
    _DATABASE_PATH: ClassVar[Path] = Path(SETTINGS_DIR) / 'poznan_gtfs.sqlite3'
    _LEGACY_DATABASE_PATH: ClassVar[Path] = (
        Path(SETTINGS_DIR) / 'public_transport' / 'poznan' / 'gtfs.sqlite3'
    )
    _DATABASE_LOCK: ClassVar[Lock] = Lock()
    _FEEDS: ClassVar[dict[str, dict[str, str]]] = {
        'P': {
            'name': 'ZTM Poznań',
            'static': _STATIC_ENDPOINT,
            'vehicles': (
                'https://www.ztm.poznan.pl/pl/dla-deweloperow/'
                'getGtfsRtFile?file=vehicle_positions.pb'
            )
        }
    }
    _CARRIERS: ClassVar[dict[str, str]] = {'P': 'ZTM Poznań'}

    @classmethod
    def _vehicle_identifiers(cls, descriptor, entity_id: str) -> tuple[str, str, str]:
        """Maps Poznań's vehicle.id to fleet number and label to brigade."""
        fleet_number = str(descriptor.id or entity_id or '').strip()
        brigade = str(descriptor.label or '').strip()
        return fleet_number or brigade, fleet_number, brigade

    @classmethod
    def _current_static_url(cls) -> str:
        """Selects the published archive whose filename covers today."""
        try:
            html = super()._download_html(
                cls._STATIC_INDEX,
                'Lista archiwów GTFS: ZTM Poznań'
            )
            today = date.today().strftime('%Y%m%d')
            names = set(re.findall(r'\b(\d{8}_\d{8}\.zip)\b', html))
            matching = [name for name in names if name[:8] <= today <= name[9:17]]
            if matching:
                filename = max(matching, key=lambda name: name[:8])
                return f'{cls._STATIC_ENDPOINT}?{urlencode({"file": filename})}'
        except Exception:
            pass
        return cls._STATIC_ENDPOINT

    @classmethod
    def _download_bytes(
        cls, url: str, item: str, current: int = 1, total: int = 1
    ) -> bytes:
        """Resolves Poznań's date-ranged archive before downloading it."""
        if url == cls._STATIC_ENDPOINT:
            url = cls._current_static_url()
        return super()._download_bytes(url, item, current, total)

from datetime import date
from pathlib import Path
import re
from threading import Lock
from typing import ClassVar
from urllib.parse import urljoin

from config import SETTINGS_DIR
from utils.public_transport.warsaw_downloader import WarsawDownloader


class OlsztynDownloader(WarsawDownloader):
    """Downloads the currently effective official ZDZiT Olsztyn GTFS."""

    BASE_URL: ClassVar[str] = 'https://zdzit.olsztyn.eu/'
    CARRIER: ClassVar[str] = 'Zarząd Dróg, Zieleni i Transportu w Olsztynie'
    CITY_NAME: ClassVar[str] = 'Olsztyn i okolice'
    CITY_COLOR: ClassVar[str] = '#00A651'
    URL_PREFIXES: ClassVar[tuple[str, ...]] = (BASE_URL,)
    _STATIC_INDEX: ClassVar[str] = urljoin(BASE_URL, 'gtfs/')
    _DATABASE_PATH: ClassVar[Path] = Path(SETTINGS_DIR) / 'olsztyn_gtfs.sqlite3'
    _LEGACY_DATABASE_PATH: ClassVar[Path] = (
        Path(SETTINGS_DIR) / 'public_transport' / 'olsztyn' / 'gtfs.sqlite3'
    )
    _DATABASE_LOCK: ClassVar[Lock] = Lock()
    _FEEDS: ClassVar[dict[str, dict[str, str]]] = {
        'O': {
            'name': 'ZDZiT Olsztyn',
            'static': _STATIC_INDEX,
            'vehicles': ''
        }
    }
    _CARRIERS: ClassVar[dict[str, str]] = {'O': 'ZDZiT Olsztyn'}

    @classmethod
    def _current_static_url(cls) -> str:
        """Selects the newest archive whose start date is not in the future."""
        payload = super()._download_bytes(
            cls._STATIC_INDEX,
            'Lista archiwów GTFS: Olsztyn'
        )
        html = payload.decode('utf-8', errors='replace')
        candidates: list[tuple[date, str]] = []
        for href in re.findall(
            r'href=["\']([^"\']*GTFS_(\d{4})_(\d{2})_(\d{2})[^"\']*\.zip)["\']',
            html,
            re.IGNORECASE
        ):
            url, year, month, day = href
            try:
                start_date = date(int(year), int(month), int(day))
            except ValueError:
                continue
            candidates.append((start_date, urljoin(cls.BASE_URL, url)))
        active = [candidate for candidate in candidates if candidate[0] <= date.today()]
        if not active:
            raise RuntimeError('Nie udało się ustalić aktualnego pliku GTFS Olsztyna.')
        return max(active, key=lambda candidate: candidate[0])[1]

    @classmethod
    def _download_bytes(
        cls, url: str, item: str, current: int = 1, total: int = 1
    ) -> bytes:
        """Resolves Olsztyn's date-versioned archive before downloading it."""
        if url == cls._STATIC_INDEX:
            url = cls._current_static_url()
        return super()._download_bytes(url, item, current, total)

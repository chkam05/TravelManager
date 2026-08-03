from __future__ import annotations

from pathlib import Path
from threading import Lock
from typing import ClassVar
from urllib.parse import urljoin

from config import SETTINGS_DIR
from core.gtfs_database import GtfsDatabase
from models.public_transport.public_transport_announcement import PublicTransportAnnouncement
from resources.public_transport.public_transport_type import PublicTransportType
from utils.public_transport.download_progress import PublicTransportDownloadProgress
from utils.public_transport.krakow_downloader import KrakowDownloader


class WarsawDownloader(KrakowDownloader):
    """Downloads Warsaw timetables from the Warsaw GTFS feeds."""

    BASE_URL: ClassVar[str] = 'https://mkuran.pl/gtfs/'
    CARRIER: ClassVar[str] = 'Warszawski Transport Publiczny'
    CITY_NAME: ClassVar[str] = 'Warszawa i aglomeracja'
    CITY_COLOR: ClassVar[str] = '#E52329'
    URL_PREFIXES: ClassVar[tuple[str, ...]] = (BASE_URL,)
    _DATABASE_PATH: ClassVar[Path] = Path(SETTINGS_DIR) / 'warsaw_gtfs.sqlite3'
    _LEGACY_DATABASE_PATH: ClassVar[Path] = (
        Path(SETTINGS_DIR)
        / 'public_transport'
        / 'warsaw'
        / 'gtfs.sqlite3'
    )
    _DATABASE_LOCK: ClassVar[Lock] = Lock()
    _FEEDS: ClassVar[dict[str, dict[str, str]]] = {
        'W': {
            'name': 'Warszawski Transport Publiczny',
            'static': urljoin(BASE_URL, 'warsaw.zip'),
            'vehicles': urljoin(BASE_URL, 'warsaw/vehicles.pb')
        }
    }
    _CARRIERS: ClassVar[dict[str, str]] = {
        'W': 'Warszawski Transport Publiczny'
    }

    @staticmethod
    def _type_from_route(
        route_type: int,
        feed_id: str
    ) -> PublicTransportType:
        """Maps the transport modes present in the Warsaw GTFS feed."""
        del feed_id
        if route_type in {0, 900, 901, 902, 903, 904}:
            return PublicTransportType.TRAM
        if route_type in {1, 400, 401, 402, 403, 404, 405}:
            return PublicTransportType.METRO
        if route_type in {
            2, 100, 101, 102, 103, 104, 105, 106, 107,
            108, 109, 110, 111, 112, 113, 114, 115, 116,
            117
        }:
            return PublicTransportType.TRAIN
        if route_type in {11, 800}:
            return PublicTransportType.TROLLEY
        return PublicTransportType.BUS

    @staticmethod
    def _platform_name(row) -> str:
        """Returns Warsaw's two-digit stop-post number."""
        return str(
            row['platform_code']
            or row['description']
            or row['stop_code']
            or ''
        ).strip()

    @classmethod
    def _ensure_database(cls, refresh: bool = False) -> Path:
        """Builds a compact cache suited to the large Warsaw GTFS archive."""
        with cls._DATABASE_LOCK:
            GtfsDatabase.migrate_cache(
                cls._LEGACY_DATABASE_PATH,
                cls._DATABASE_PATH
            )
            if not refresh and GtfsDatabase.is_valid_cache(cls._DATABASE_PATH):
                return cls._DATABASE_PATH

            feed_id, feed = next(iter(cls._FEEDS.items()))
            archive = cls._download_bytes(
                feed['static'],
                f"GTFS: {feed['name']}",
                1,
                2
            )
            GtfsDatabase.build(
                cls._DATABASE_PATH,
                {feed_id: archive},
                lambda _feed_id, current, count: (
                    PublicTransportDownloadProgress.report(
                        f"Przetwarzanie GTFS: {feed['name']}",
                        1 + current,
                        1 + count
                    )
                ),
                coverage_days=cls._DATE_RANGE_DAYS,
                compact_shapes=True
            )
            return cls._DATABASE_PATH

    @classmethod
    def download_announcements(
        cls,
        include_content: bool = False,
        line: str = ''
    ) -> list[PublicTransportAnnouncement]:
        """Returns no notices; Warsaw notices are not part of this view yet."""
        del include_content, line
        return []

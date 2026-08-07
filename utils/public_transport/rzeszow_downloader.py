from pathlib import Path
import json
import sqlite3
from threading import Lock
from typing import ClassVar

from config import SETTINGS_DIR
from utils.public_transport.warsaw_downloader import WarsawDownloader

# Stable API endpoint by numeric dataset ID — slug-based endpoint returns 500.
_RESOURCES_API: str = (
    'https://otwartedane.erzeszow.pl/v1/datasets/180/resources/'
)


class RzeszowDownloader(WarsawDownloader):
    """Downloads the official RTM Rzeszów GTFS from the city open-data portal."""

    BASE_URL: ClassVar[str] = 'https://otwartedane.erzeszow.pl/'
    CARRIER: ClassVar[str] = 'Rzeszowski Transport Miejski'
    CITY_NAME: ClassVar[str] = 'Rzeszów'
    CITY_COLOR: ClassVar[str] = '#D32A00'
    URL_PREFIXES: ClassVar[tuple[str, ...]] = (BASE_URL,)
    _DATABASE_PATH: ClassVar[Path] = Path(SETTINGS_DIR) / 'rzeszow_gtfs.sqlite3'
    _LEGACY_DATABASE_PATH: ClassVar[Path] = (
        Path(SETTINGS_DIR) / 'public_transport' / 'rzeszow' / 'gtfs.sqlite3'
    )
    _DATABASE_LOCK: ClassVar[Lock] = Lock()
    _FEEDS: ClassVar[dict[str, dict[str, str]]] = {
        'R': {
            'name': 'RTM Rzeszów',
            'static': _RESOURCES_API,   # resolved at download time
            'vehicles': ''
        }
    }
    _CARRIERS: ClassVar[dict[str, str]] = {'R': 'Rzeszowski Transport Miejski'}

    @classmethod
    def _ensure_database(cls, refresh: bool = False) -> Path:
        # RTM Rzeszów publishes one route record per direction variant — deduplicate.
        path = super()._ensure_database(refresh)
        connection = sqlite3.connect(path)
        try:
            groups = connection.execute(
                """
                    SELECT feed_id, short_name, MIN(route_id) canonical_route
                    FROM routes GROUP BY feed_id, short_name HAVING COUNT(*) > 1
                """
            ).fetchall()
            for feed_id, short_name, canonical_route in groups:
                route_ids = [
                    row[0] for row in connection.execute(
                        'SELECT route_id FROM routes WHERE feed_id = ? AND short_name = ?',
                        (feed_id, short_name)
                    )
                ]
                placeholders = ','.join('?' for _ in route_ids)
                connection.execute(
                    f'UPDATE trips SET route_id = ? WHERE feed_id = ? '
                    f'AND route_id IN ({placeholders})',
                    (canonical_route, feed_id, *route_ids)
                )
                connection.execute(
                    f'DELETE FROM routes WHERE feed_id = ? '
                    f'AND route_id IN ({placeholders}) AND route_id <> ?',
                    (feed_id, *route_ids, canonical_route)
                )
            connection.commit()
        finally:
            connection.close()
        return path

    @classmethod
    def _current_static_url(cls) -> str:
        """Queries the open-data portal API and returns the newest GTFS ZIP URL."""
        payload = super()._download_bytes(
            _RESOURCES_API,
            'Lista archiwów GTFS: Rzeszów'
        )
        resources = json.loads(payload.decode('utf-8'))
        for resource in resources:
            file_url = resource.get('file') or ''
            if file_url.endswith('.zip'):
                return file_url
        raise RuntimeError('Nie udało się ustalić aktualnego pliku GTFS Rzeszowa.')

    @classmethod
    def _download_bytes(
        cls, url: str, item: str, current: int = 1, total: int = 1
    ) -> bytes:
        """Resolves the versioned GTFS archive URL before downloading it."""
        if url == _RESOURCES_API:
            url = cls._current_static_url()
        return super()._download_bytes(url, item, current, total)


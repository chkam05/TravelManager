from pathlib import Path
import sqlite3
from threading import Lock
from typing import ClassVar

from config import SETTINGS_DIR
from utils.public_transport.warsaw_downloader import WarsawDownloader


class BydgoszczDownloader(WarsawDownloader):
    """Downloads the official ZDMiKP Bydgoszcz static GTFS feed."""

    BASE_URL: ClassVar[str] = 'https://zdmikp.bydgoszcz.pl/'
    CARRIER: ClassVar[str] = 'ZDMiKP Bydgoszcz'
    CITY_NAME: ClassVar[str] = 'Bydgoszcz i okolice'
    CITY_COLOR: ClassVar[str] = '#D71920'
    URL_PREFIXES: ClassVar[tuple[str, ...]] = (BASE_URL,)
    _DATABASE_PATH: ClassVar[Path] = Path(SETTINGS_DIR) / 'bydgoszcz_gtfs.sqlite3'
    _LEGACY_DATABASE_PATH: ClassVar[Path] = (
        Path(SETTINGS_DIR) / 'public_transport' / 'bydgoszcz' / 'gtfs.sqlite3'
    )
    _DATABASE_LOCK: ClassVar[Lock] = Lock()
    _FEEDS: ClassVar[dict[str, dict[str, str]]] = {
        'B': {
            'name': 'ZDMiKP Bydgoszcz',
            'static': 'https://zdmikp.bydgoszcz.pl/rozklady/paczka/gtfs/gtfs.zip',
            'vehicles': ''
        }
    }
    _CARRIERS: ClassVar[dict[str, str]] = {'B': 'ZDMiKP Bydgoszcz'}

    @classmethod
    def _ensure_database(cls, refresh: bool = False) -> Path:
        """Normalizes Bydgoszcz's one-route-record-per-pattern convention."""
        path = super()._ensure_database(refresh)
        connection = sqlite3.connect(path)
        try:
            connection.execute(
                """
                    UPDATE routes SET route_type = 0
                    WHERE short_name IN ('1','2','3','4','5','6','7','8','9','10','11')
                """
            )
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
            connection.execute(
                """
                    UPDATE trips SET direction_id = CASE
                        WHEN LOWER(COALESCE((
                            SELECT s.name FROM stop_times st
                            JOIN stops s ON s.feed_id=st.feed_id AND s.stop_id=st.stop_id
                            WHERE st.feed_id=trips.feed_id AND st.trip_id=trips.trip_id
                            ORDER BY st.stop_sequence ASC LIMIT 1
                        ), '')) <= LOWER(COALESCE((
                            SELECT s.name FROM stop_times st
                            JOIN stops s ON s.feed_id=st.feed_id AND s.stop_id=st.stop_id
                            WHERE st.feed_id=trips.feed_id AND st.trip_id=trips.trip_id
                            ORDER BY st.stop_sequence DESC LIMIT 1
                        ), '')) THEN 0 ELSE 1 END
                    WHERE direction_id IS NULL
                """
            )
            connection.commit()
        finally:
            connection.close()
        return path

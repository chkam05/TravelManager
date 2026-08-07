from pathlib import Path
import re
from threading import Lock
from typing import ClassVar

from config import SETTINGS_DIR
from utils.public_transport.warsaw_downloader import WarsawDownloader


class LodzDownloader(WarsawDownloader):
    """Downloads Łódź's official static and realtime GTFS feeds."""

    BASE_URL: ClassVar[str] = 'https://otwarte.miasto.lodz.pl/'
    CARRIER: ClassVar[str] = 'Urząd Miasta Łodzi / MPK-Łódź'
    CITY_NAME: ClassVar[str] = 'Łódź i okolice'
    CITY_COLOR: ClassVar[str] = '#C8102E'
    URL_PREFIXES: ClassVar[tuple[str, ...]] = (BASE_URL,)
    _DATABASE_PATH: ClassVar[Path] = Path(SETTINGS_DIR) / 'lodz_gtfs.sqlite3'
    _LEGACY_DATABASE_PATH: ClassVar[Path] = (
        Path(SETTINGS_DIR) / 'public_transport' / 'lodz' / 'gtfs.sqlite3'
    )
    _DATABASE_LOCK: ClassVar[Lock] = Lock()
    _FEEDS: ClassVar[dict[str, dict[str, str]]] = {
        'L': {
            'name': 'Komunikacja miejska w Łodzi',
            'static': (
                'https://otwarte.miasto.lodz.pl/wp-content/uploads/'
                '2025/06/GTFS.zip'
            ),
            'vehicles': (
                'https://otwarte.miasto.lodz.pl/wp-content/uploads/'
                '2025/06/vehicle_positions.bin'
            )
        }
    }
    _CARRIERS: ClassVar[dict[str, str]] = {
        'L': 'Urząd Miasta Łodzi / MPK-Łódź'
    }

    @classmethod
    def download_vehicle_positions(
        cls,
        line: str = '',
        transport_type: str = '',
        feed_id: str = ''
    ):
        """Adds the scheduled Łódź brigade to realtime vehicles."""
        positions = super().download_vehicle_positions(
            line=line,
            transport_type=transport_type,
            feed_id=feed_id
        )
        with cls._connection() as connection:
            brigades = {
                str(row['trip_id']): re.sub(
                    r'\s+',
                    '',
                    str(row['block_id'] or '')
                )
                for row in connection.execute(
                    "SELECT trip_id, block_id FROM trips WHERE feed_id = 'L'"
                )
            }
        for position in positions:
            position.brigade = brigades.get(position.trip_id, '')
        return positions

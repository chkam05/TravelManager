from pathlib import Path
from threading import Lock
from typing import ClassVar

from config import SETTINGS_DIR
from utils.public_transport.tricity_gtfs_downloader import TricityGtfsDownloader


class GdanskDownloader(TricityGtfsDownloader):
    """Downloads ZTM Gdańsk static and realtime GTFS feeds."""

    BASE_URL: ClassVar[str] = 'https://ckan.multimediagdansk.pl/'
    CARRIER: ClassVar[str] = 'Zarząd Transportu Miejskiego w Gdańsku'
    CITY_NAME: ClassVar[str] = 'Gdańsk i okolice'
    CITY_COLOR: ClassVar[str] = '#D71920'
    URL_PREFIXES: ClassVar[tuple[str, ...]] = (BASE_URL,)
    _DATABASE_PATH: ClassVar[Path] = Path(SETTINGS_DIR) / 'gdansk_gtfs.sqlite3'
    _LEGACY_DATABASE_PATH: ClassVar[Path] = (
        Path(SETTINGS_DIR) / 'public_transport' / 'gdansk' / 'gtfs.sqlite3'
    )
    _DATABASE_LOCK: ClassVar[Lock] = Lock()
    _FEEDS: ClassVar[dict[str, dict[str, str]]] = {
        'G': {
            'name': 'ZTM Gdańsk',
            'static': (
                'https://ckan.multimediagdansk.pl/dataset/'
                'c24aa637-3619-4dc2-a171-a23eec8f2172/resource/'
                '30e783e4-2bec-4a7d-bb22-ee3e3b26ca96/download/'
                'gtfsgoogle.zip'
            ),
            'vehicles': (
                'https://ckan2.multimediagdansk.pl/'
                'gtfs-rt?feed=vehiclePositions'
            )
        }
    }
    _CARRIERS: ClassVar[dict[str, str]] = {
        'G': 'Zarząd Transportu Miejskiego w Gdańsku'
    }

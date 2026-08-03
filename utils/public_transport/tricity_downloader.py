from __future__ import annotations

from pathlib import Path
import re
from threading import Lock
from typing import ClassVar

from config import SETTINGS_DIR
from utils.public_transport.warsaw_downloader import WarsawDownloader


class TricityGtfsDownloader(WarsawDownloader):
    """Shares GTFS conventions used by the Gdańsk and Gdynia feeds."""

    _STOP_POST_PATTERN: ClassVar[re.Pattern[str]] = re.compile(
        r'\s+(T[12]|\d{2})$'
    )

    @classmethod
    def _stop_name(cls, row) -> str:
        """Removes the stop-post number embedded in a stop name."""
        return cls._STOP_POST_PATTERN.sub('', str(row['name']).strip())

    @classmethod
    def _platform_name(cls, row) -> str:
        """Extracts the stop-post number embedded in a stop name."""
        match = cls._STOP_POST_PATTERN.search(str(row['name']).strip())
        if match:
            return match.group(1)
        return super()._platform_name(row)


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


class GdyniaDownloader(TricityGtfsDownloader):
    """Downloads the official ZKM Gdynia static GTFS feed."""

    BASE_URL: ClassVar[str] = 'https://api.zdiz.gdynia.pl/pt/'
    CARRIER: ClassVar[str] = 'Zarząd Komunikacji Miejskiej w Gdyni'
    CITY_NAME: ClassVar[str] = 'Gdynia i okolice'
    CITY_COLOR: ClassVar[str] = '#00A6D6'
    URL_PREFIXES: ClassVar[tuple[str, ...]] = (BASE_URL,)
    _DATABASE_PATH: ClassVar[Path] = Path(SETTINGS_DIR) / 'gdynia_gtfs.sqlite3'
    _LEGACY_DATABASE_PATH: ClassVar[Path] = (
        Path(SETTINGS_DIR) / 'public_transport' / 'gdynia' / 'gtfs.sqlite3'
    )
    _DATABASE_LOCK: ClassVar[Lock] = Lock()
    _FEEDS: ClassVar[dict[str, dict[str, str]]] = {
        'Y': {
            'name': 'ZKM Gdynia',
            'static': 'https://api.zdiz.gdynia.pl/pt/gtfs.zip',
            'vehicles': ''
        }
    }
    _CARRIERS: ClassVar[dict[str, str]] = {
        'Y': 'Zarząd Komunikacji Miejskiej w Gdyni'
    }

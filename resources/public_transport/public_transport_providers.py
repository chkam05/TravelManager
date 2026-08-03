from __future__ import annotations
from typing import Any, ClassVar, Dict, Type
from urllib.parse import urlparse

from utils.public_transport.czestochowa_downloader import CzestochowaDownloader
from utils.public_transport.gzm_downloader import GzmDownloader
from utils.public_transport.krakow_downloader import KrakowDownloader
from utils.public_transport.warsaw_downloader import WarsawDownloader
from utils.public_transport.tricity_downloader import (
    GdanskDownloader,
    GdyniaDownloader
)


class PublicTransportProviders:
    """Registers public transport regions and their downloader implementations."""

    GZM: ClassVar[str] = 'gzm'
    CZESTOCHOWA: ClassVar[str] = 'czestochowa'
    KRAKOW: ClassVar[str] = 'krakow'
    WARSAW: ClassVar[str] = 'warsaw'
    GDANSK: ClassVar[str] = 'gdansk'
    GDYNIA: ClassVar[str] = 'gdynia'

    FIELD_NAME: ClassVar[str] = 'name'
    FIELD_DESCRIPTION: ClassVar[str] = 'description'
    FIELD_ICON: ClassVar[str] = 'icon'
    FIELD_DOWNLOADER: ClassVar[str] = 'downloader'
    FIELD_CAPABILITIES: ClassVar[str] = 'capabilities'
    FIELD_SETTINGS_CACHE: ClassVar[str] = 'settings_cache'
    FIELD_ATTRIBUTIONS: ClassVar[str] = 'attributions'

    CAPABILITY_SHOW_PLATFORMS: ClassVar[str] = 'show_platforms'
    CAPABILITY_SHOW_STOP_MAP: ClassVar[str] = 'show_stop_map'
    CAPABILITY_SHOW_RIDE_MAP: ClassVar[str] = 'show_ride_map'
    CAPABILITY_SHOW_RIDE_DISTANCES: ClassVar[str] = 'show_ride_distances'
    CAPABILITY_SHOW_VEHICLE_DETAILS: ClassVar[str] = 'show_vehicle_details'
    CAPABILITY_SHOW_HIGH_FLOOR: ClassVar[str] = 'show_high_floor'
    CAPABILITY_SHOW_STOP_DEPARTURES: ClassVar[str] = 'show_stop_departures'
    CAPABILITY_SHOW_RIDE: ClassVar[str] = 'show_ride'
    CAPABILITY_SHOW_ROUTE_MAP: ClassVar[str] = 'show_route_map'
    CAPABILITY_SHOW_VEHICLE_POSITIONS: ClassVar[str] = (
        'show_vehicle_positions'
    )
    CAPABILITY_CACHE_ANNOUNCEMENTS: ClassVar[str] = 'cache_announcements'
    CAPABILITY_DIRECTION_SELECTOR_LABEL: ClassVar[str] = (
        'direction_selector_label'
    )

    GZM_CAPABILITIES: ClassVar[Dict[str, object]] = {
        CAPABILITY_SHOW_PLATFORMS: True,
        CAPABILITY_SHOW_STOP_MAP: True,
        CAPABILITY_SHOW_RIDE_MAP: True,
        CAPABILITY_SHOW_RIDE_DISTANCES: True,
        CAPABILITY_SHOW_VEHICLE_DETAILS: True,
        CAPABILITY_SHOW_HIGH_FLOOR: True,
        CAPABILITY_SHOW_STOP_DEPARTURES: True,
        CAPABILITY_SHOW_RIDE: True,
        CAPABILITY_SHOW_ROUTE_MAP: True,
        CAPABILITY_SHOW_VEHICLE_POSITIONS: True,
        CAPABILITY_CACHE_ANNOUNCEMENTS: False,
        CAPABILITY_DIRECTION_SELECTOR_LABEL: 'Kierunek'
    }
    CZESTOCHOWA_CAPABILITIES: ClassVar[Dict[str, object]] = {
        CAPABILITY_SHOW_PLATFORMS: False,
        CAPABILITY_SHOW_STOP_MAP: True,
        CAPABILITY_SHOW_RIDE_MAP: True,
        CAPABILITY_SHOW_RIDE_DISTANCES: False,
        CAPABILITY_SHOW_VEHICLE_DETAILS: False,
        CAPABILITY_SHOW_HIGH_FLOOR: False,
        CAPABILITY_SHOW_STOP_DEPARTURES: False,
        CAPABILITY_SHOW_RIDE: True,
        CAPABILITY_SHOW_ROUTE_MAP: True,
        CAPABILITY_SHOW_VEHICLE_POSITIONS: False,
        CAPABILITY_CACHE_ANNOUNCEMENTS: True,
        CAPABILITY_DIRECTION_SELECTOR_LABEL: 'Wariant trasy'
    }
    KRAKOW_CAPABILITIES: ClassVar[Dict[str, object]] = {
        CAPABILITY_SHOW_PLATFORMS: True,
        CAPABILITY_SHOW_STOP_MAP: True,
        CAPABILITY_SHOW_RIDE_MAP: True,
        CAPABILITY_SHOW_RIDE_DISTANCES: False,
        CAPABILITY_SHOW_VEHICLE_DETAILS: False,
        CAPABILITY_SHOW_HIGH_FLOOR: False,
        CAPABILITY_SHOW_STOP_DEPARTURES: True,
        CAPABILITY_SHOW_RIDE: True,
        CAPABILITY_SHOW_ROUTE_MAP: True,
        CAPABILITY_SHOW_VEHICLE_POSITIONS: True,
        CAPABILITY_CACHE_ANNOUNCEMENTS: True,
        CAPABILITY_DIRECTION_SELECTOR_LABEL: 'Wariant trasy'
    }
    WARSAW_CAPABILITIES: ClassVar[Dict[str, object]] = {
        CAPABILITY_SHOW_PLATFORMS: True,
        CAPABILITY_SHOW_STOP_MAP: True,
        CAPABILITY_SHOW_RIDE_MAP: True,
        CAPABILITY_SHOW_RIDE_DISTANCES: False,
        CAPABILITY_SHOW_VEHICLE_DETAILS: False,
        CAPABILITY_SHOW_HIGH_FLOOR: False,
        CAPABILITY_SHOW_STOP_DEPARTURES: True,
        CAPABILITY_SHOW_RIDE: True,
        CAPABILITY_SHOW_ROUTE_MAP: True,
        CAPABILITY_SHOW_VEHICLE_POSITIONS: True,
        CAPABILITY_CACHE_ANNOUNCEMENTS: False,
        CAPABILITY_DIRECTION_SELECTOR_LABEL: 'Wariant trasy'
    }
    GDANSK_CAPABILITIES: ClassVar[Dict[str, object]] = {
        **WARSAW_CAPABILITIES,
        CAPABILITY_SHOW_VEHICLE_POSITIONS: True
    }
    GDYNIA_CAPABILITIES: ClassVar[Dict[str, object]] = {
        **WARSAW_CAPABILITIES,
        CAPABILITY_SHOW_VEHICLE_POSITIONS: False
    }

    VALUES: ClassVar[Dict[str, Dict[str, object]]] = {
        GZM: {
            FIELD_NAME: 'Górnośląsko-Zagłębiowska Metropolia',
            FIELD_DESCRIPTION: 'Transport GZM',
            FIELD_ICON: 'bus-front',
            FIELD_DOWNLOADER: GzmDownloader,
            FIELD_CAPABILITIES: GZM_CAPABILITIES,
            FIELD_SETTINGS_CACHE: False,
            FIELD_ATTRIBUTIONS: [{
                'name': 'Zarząd Transportu Metropolitalnego / Otwarte Dane GZM',
                'url': (
                    'https://otwartedane.metropoliagzm.pl/dataset/'
                    'rozklady-jazdy-i-lokalizacja-przystankow-gtfs-'
                    'wersja-rozszerzona'
                )
            }]
        },
        CZESTOCHOWA: {
            FIELD_NAME: 'Częstochowa',
            FIELD_DESCRIPTION: 'MPK w Częstochowie',
            FIELD_ICON: 'tram-front',
            FIELD_DOWNLOADER: CzestochowaDownloader,
            FIELD_CAPABILITIES: CZESTOCHOWA_CAPABILITIES,
            FIELD_SETTINGS_CACHE: True,
            FIELD_ATTRIBUTIONS: [{
                'name': 'Miasto Częstochowa / MPK w Częstochowie',
                'url': 'https://www.czestochowa.pl/rozklady-jazdy'
            }]
        },
        KRAKOW: {
            FIELD_NAME: 'Kraków',
            FIELD_DESCRIPTION: 'Komunikacja Miejska w Krakowie (GTFS)',
            FIELD_ICON: 'tram-front',
            FIELD_DOWNLOADER: KrakowDownloader,
            FIELD_CAPABILITIES: KRAKOW_CAPABILITIES,
            FIELD_SETTINGS_CACHE: False,
            FIELD_ATTRIBUTIONS: [{
                'name': 'Zarząd Transportu Publicznego w Krakowie',
                'url': 'https://gtfs.ztp.krakow.pl/'
            }]
        },
        WARSAW: {
            FIELD_NAME: 'Warszawa',
            FIELD_DESCRIPTION: 'Warszawski Transport Publiczny (GTFS)',
            FIELD_ICON: 'train-front',
            FIELD_DOWNLOADER: WarsawDownloader,
            FIELD_CAPABILITIES: WARSAW_CAPABILITIES,
            FIELD_SETTINGS_CACHE: False,
            FIELD_ATTRIBUTIONS: [
                {
                    'name': 'Zarząd Transportu Miejskiego w Warszawie',
                    'url': 'https://ztm.waw.pl/'
                },
                {
                    'name': 'GTFS: Mikołaj Kuranowski',
                    'url': 'https://mkuran.pl/gtfs/'
                },
                {
                    'name': 'Geometrie autobusów: © OpenStreetMap',
                    'url': 'https://www.openstreetmap.org/copyright'
                }
            ]
        },
        GDANSK: {
            FIELD_NAME: 'Gdańsk',
            FIELD_DESCRIPTION: 'ZTM Gdańsk (GTFS)',
            FIELD_ICON: 'tram-front',
            FIELD_DOWNLOADER: GdanskDownloader,
            FIELD_CAPABILITIES: GDANSK_CAPABILITIES,
            FIELD_SETTINGS_CACHE: False,
            FIELD_ATTRIBUTIONS: [{
                'name': 'Zarząd Transportu Miejskiego w Gdańsku',
                'url': 'https://ckan.multimediagdansk.pl/tl/dataset/tristar'
            }]
        },
        GDYNIA: {
            FIELD_NAME: 'Gdynia',
            FIELD_DESCRIPTION: 'ZKM Gdynia (GTFS)',
            FIELD_ICON: 'bus-front',
            FIELD_DOWNLOADER: GdyniaDownloader,
            FIELD_CAPABILITIES: GDYNIA_CAPABILITIES,
            FIELD_SETTINGS_CACHE: False,
            FIELD_ATTRIBUTIONS: [{
                'name': 'ZKM Gdynia / Otwarte Dane Gdynia',
                'url': (
                    'https://otwartedane.gdynia.pl/dataset/'
                    'informacje-o-rozkladach-jazdy-i-lokalizacji-przystankow'
                )
            }]
        }
    }

    def __new__(cls):
        """Prevents creating instances of this static resource class."""
        raise TypeError(f'{cls.__name__} cannot be instantiated.')

    @classmethod
    def downloader(cls, provider_id: str) -> Type[Any]:
        """Returns the downloader registered for a provider identifier."""
        provider = cls.VALUES.get(provider_id)
        if not provider:
            raise ValueError('Unsupported public transport provider.')
        return provider[cls.FIELD_DOWNLOADER]

    @classmethod
    def capabilities(cls, provider_id: str) -> Dict[str, object]:
        """Returns an immutable copy of provider-specific view capabilities."""
        provider = cls.VALUES.get(provider_id)
        if not provider:
            raise ValueError('Unsupported public transport provider.')
        capabilities = provider.get(cls.FIELD_CAPABILITIES, {})
        return dict(capabilities) if isinstance(capabilities, dict) else {}

    @classmethod
    def uses_settings_cache(cls, provider_id: str) -> bool:
        """Returns whether view data is persisted in settings JSON."""
        provider = cls.VALUES.get(provider_id)
        if not provider:
            raise ValueError('Unsupported public transport provider.')
        return bool(provider.get(cls.FIELD_SETTINGS_CACHE, False))

    @classmethod
    def providers_without_settings_cache(cls) -> list[str]:
        """Returns providers whose persistent cache has a separate backend."""
        return [
            provider_id
            for provider_id in cls.VALUES
            if not cls.uses_settings_cache(provider_id)
        ]

    @classmethod
    def options(cls) -> list[dict[str, Any]]:
        """Returns provider identifiers and labels for selection controls."""
        return [
            {
                'id': provider_id,
                'name': str(provider[cls.FIELD_NAME]),
                'description': str(provider[cls.FIELD_DESCRIPTION]),
                'icon': str(provider[cls.FIELD_ICON]),
                'attributions': list(provider.get(cls.FIELD_ATTRIBUTIONS, []))
            }
            for provider_id, provider in cls.VALUES.items()
        ]

    @classmethod
    def validate_url(cls, provider_id: str, url: str) -> str:
        """Validates that a detail URL belongs to the selected provider."""
        downloader = cls.downloader(provider_id)
        parsed = urlparse(url)
        prefixes = getattr(
            downloader,
            'URL_PREFIXES',
            (downloader.BASE_URL,)
        )
        is_allowed = any(
            parsed.scheme == expected.scheme
            and parsed.netloc == expected.netloc
            and parsed.path.startswith(expected.path)
            for expected in map(urlparse, prefixes)
        )
        if not is_allowed:
            raise ValueError('Invalid public transport URL.')
        return url

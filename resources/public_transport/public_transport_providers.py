from __future__ import annotations
from typing import Any, ClassVar, Dict, Type
from urllib.parse import urlparse

from utils.public_transport.czestochowa_downloader import CzestochowaDownloader
from utils.public_transport.gzm_downloader import GzmDownloader


class PublicTransportProviders:
    """Registers public transport regions and their downloader implementations."""

    GZM: ClassVar[str] = 'gzm'
    CZESTOCHOWA: ClassVar[str] = 'czestochowa'

    FIELD_NAME: ClassVar[str] = 'name'
    FIELD_DESCRIPTION: ClassVar[str] = 'description'
    FIELD_ICON: ClassVar[str] = 'icon'
    FIELD_DOWNLOADER: ClassVar[str] = 'downloader'
    FIELD_CAPABILITIES: ClassVar[str] = 'capabilities'

    CAPABILITY_SHOW_PLATFORMS: ClassVar[str] = 'show_platforms'
    CAPABILITY_SHOW_STOP_MAP: ClassVar[str] = 'show_stop_map'
    CAPABILITY_SHOW_RIDE_MAP: ClassVar[str] = 'show_ride_map'
    CAPABILITY_SHOW_RIDE_DISTANCES: ClassVar[str] = 'show_ride_distances'
    CAPABILITY_SHOW_VEHICLE_DETAILS: ClassVar[str] = 'show_vehicle_details'
    CAPABILITY_SHOW_HIGH_FLOOR: ClassVar[str] = 'show_high_floor'
    CAPABILITY_SHOW_STOP_DEPARTURES: ClassVar[str] = 'show_stop_departures'
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
        CAPABILITY_CACHE_ANNOUNCEMENTS: True,
        CAPABILITY_DIRECTION_SELECTOR_LABEL: 'Wariant trasy'
    }

    VALUES: ClassVar[Dict[str, Dict[str, object]]] = {
        GZM: {
            FIELD_NAME: 'Górnośląsko-Zagłębiowska Metropolia',
            FIELD_DESCRIPTION: 'Transport GZM',
            FIELD_ICON: 'bus-front',
            FIELD_DOWNLOADER: GzmDownloader,
            FIELD_CAPABILITIES: GZM_CAPABILITIES
        },
        CZESTOCHOWA: {
            FIELD_NAME: 'Częstochowa',
            FIELD_DESCRIPTION: 'MPK w Częstochowie',
            FIELD_ICON: 'tram-front',
            FIELD_DOWNLOADER: CzestochowaDownloader,
            FIELD_CAPABILITIES: CZESTOCHOWA_CAPABILITIES
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
    def options(cls) -> list[dict[str, str]]:
        """Returns provider identifiers and labels for selection controls."""
        return [
            {
                'id': provider_id,
                'name': str(provider[cls.FIELD_NAME]),
                'description': str(provider[cls.FIELD_DESCRIPTION]),
                'icon': str(provider[cls.FIELD_ICON])
            }
            for provider_id, provider in cls.VALUES.items()
        ]

    @classmethod
    def validate_url(cls, provider_id: str, url: str) -> str:
        """Validates that a detail URL belongs to the selected provider."""
        downloader = cls.downloader(provider_id)
        expected = urlparse(downloader.BASE_URL)
        parsed = urlparse(url)
        if (
            parsed.scheme != expected.scheme
            or parsed.netloc != expected.netloc
            or not parsed.path.startswith(expected.path)
        ):
            raise ValueError('Invalid public transport URL.')
        return url

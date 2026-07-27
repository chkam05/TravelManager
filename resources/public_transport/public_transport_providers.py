from __future__ import annotations
from typing import ClassVar, Dict, Type
from urllib.parse import urlparse

from utils.public_transport.gzm_downloader import GzmDownloader


class PublicTransportProviders:
    """Registers public transport regions and their downloader implementations."""

    GZM: ClassVar[str] = 'gzm'
    FIELD_NAME: ClassVar[str] = 'name'
    FIELD_DESCRIPTION: ClassVar[str] = 'description'
    FIELD_ICON: ClassVar[str] = 'icon'
    FIELD_DOWNLOADER: ClassVar[str] = 'downloader'

    VALUES: ClassVar[Dict[str, Dict[str, object]]] = {
        GZM: {
            FIELD_NAME: 'Górnośląsko-Zagłębiowska Metropolia',
            FIELD_DESCRIPTION: 'Transport GZM',
            FIELD_ICON: 'bus-front',
            FIELD_DOWNLOADER: GzmDownloader
        }
    }

    def __new__(cls):
        """Prevents creating instances of this static resource class."""
        raise TypeError(f'{cls.__name__} cannot be instantiated.')

    @classmethod
    def downloader(cls, provider_id: str) -> Type[GzmDownloader]:
        """Returns the downloader registered for a provider identifier."""
        provider = cls.VALUES.get(provider_id)
        if not provider:
            raise ValueError('Unsupported public transport provider.')
        return provider[cls.FIELD_DOWNLOADER]

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

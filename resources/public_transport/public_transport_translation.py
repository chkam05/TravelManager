from typing import ClassVar, Dict

from core.language_service import LanguageService
from resources.public_transport.public_transport_type import PublicTransportType


class PublicTransportTranslation:
    """Stores stable translation keys for public transport types."""

    NAME_KEYS: ClassVar[Dict[PublicTransportType, str]] = {
        PublicTransportType.BUS: 'RES_PUBLIC_TRANSPORT_TYPE.BUS',
        PublicTransportType.TRAM: 'RES_PUBLIC_TRANSPORT_TYPE.TRAM',
        PublicTransportType.TROLLEY: 'RES_PUBLIC_TRANSPORT_TYPE.TROLLEYBUS',
        PublicTransportType.METRO: 'RES_PUBLIC_TRANSPORT_TYPE.METRO',
        PublicTransportType.TRAIN: 'RES_PUBLIC_TRANSPORT_TYPE.TRAIN'
    }

    def __new__(cls):
        """Prevents creating instances of this static resource class."""
        raise TypeError(f'{cls.__name__} cannot be instantiated.')

    @classmethod
    def get(cls, transport_type: PublicTransportType) -> str:
        """Returns the localised label for a public transport type."""
        return LanguageService.translate_current(cls.NAME_KEYS[transport_type])

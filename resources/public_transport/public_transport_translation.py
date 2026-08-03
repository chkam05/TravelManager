from typing import ClassVar, Dict

from resources.public_transport.public_transport_type import PublicTransportType


class PublicTransportTranslation:
    """Stores Polish translations of public transport types."""

    VALUES: ClassVar[Dict[PublicTransportType, str]] = {
        PublicTransportType.BUS: 'Autobus',
        PublicTransportType.TRAM: 'Tramwaj',
        PublicTransportType.TROLLEY: 'Trolejbus',
        PublicTransportType.METRO: 'Metro',
        PublicTransportType.TRAIN: 'Pociąg'
    }

    def __new__(cls):
        """Prevents creating instances of this static resource class."""
        raise TypeError(f'{cls.__name__} cannot be instantiated.')

    @classmethod
    def get(cls, transport_type: PublicTransportType) -> str:
        """Returns the Polish label for a public transport type."""
        return cls.VALUES[transport_type]

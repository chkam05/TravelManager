from __future__ import annotations

import ipaddress
import socket
from typing import ClassVar


class NetworkUtils:
    """Helpers for validating application network addresses."""

    _ROUTE_PROBES: ClassVar[tuple[tuple[str, int], ...]] = (
        ('1.1.1.1', 80),
        ('8.8.8.8', 80),
    )

    def __new__(cls, *args, **kwargs):
        raise TypeError(
            f'{cls.__name__} is a static utility class and cannot be instantiated.'
        )

    @staticmethod
    def normalize_ipv4(value: str) -> str:
        """Validates and returns a normalized IPv4 address."""
        if not isinstance(value, str) or not value.strip():
            raise TypeError('Adres IP musi być niepustym tekstem.')

        try:
            address = ipaddress.ip_address(value.strip())
        except ValueError as error:
            raise ValueError(f'Nieprawidłowy adres IPv4: {value!r}.') from error

        if not isinstance(address, ipaddress.IPv4Address):
            raise ValueError('Obsługiwane są wyłącznie adresy IPv4.')

        return str(address)

    @staticmethod
    def _is_usable_local_ipv4(value: str | None) -> bool:
        """Checks whether an address can expose the service on the local network."""
        if not value:
            return False

        try:
            address = ipaddress.ip_address(value)
        except ValueError:
            return False

        return (
            isinstance(address, ipaddress.IPv4Address)
            and not address.is_loopback
            and not address.is_unspecified
            and not address.is_multicast
        )

    @classmethod
    def get_local_ip(cls) -> str | None:
        """Returns the IPv4 address of the currently active network interface."""
        for remote_address in cls._ROUTE_PROBES:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as connection:
                    connection.connect(remote_address)
                    address = connection.getsockname()[0]
            except OSError:
                continue

            if cls._is_usable_local_ipv4(address):
                return address

        try:
            addresses = socket.gethostbyname_ex(socket.gethostname())[2]
        except OSError:
            return None

        return next(
            (address for address in addresses if cls._is_usable_local_ipv4(address)),
            None
        )

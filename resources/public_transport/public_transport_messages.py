from __future__ import annotations

from dataclasses import dataclass, field
from typing import Mapping

from core.language_service import LanguageService


@dataclass(frozen=True)
class PublicTransportMessage:
    """Carries a translation key through downloader code without Flask coupling."""

    key: str
    parameters: Mapping[str, object] = field(default_factory=dict)


class _PublicTransportLocalizedError:
    """Adds structured translation data to a standard exception type."""

    def __init__(self, key: str, **parameters: object) -> None:
        self.translation = PublicTransportMessage(key, parameters)
        super().__init__(key)


class PublicTransportValueError(_PublicTransportLocalizedError, ValueError):
    """Represents a localisable invalid-input or missing-data error."""


class PublicTransportRuntimeError(_PublicTransportLocalizedError, RuntimeError):
    """Represents a localisable provider or dependency failure."""


def public_transport_message(
    key: str,
    **parameters: object
) -> PublicTransportMessage:
    """Builds a deferred public-transport translation message."""
    return PublicTransportMessage(key, parameters)


def resolve_public_transport_message(value: object) -> str:
    """Resolves deferred messages and errors in the active request locale."""
    if isinstance(value, _PublicTransportLocalizedError):
        value = value.translation
    if not isinstance(value, PublicTransportMessage):
        return str(value)

    parameters = {
        key: resolve_public_transport_message(parameter)
        if isinstance(parameter, (PublicTransportMessage, _PublicTransportLocalizedError))
        else parameter
        for key, parameter in value.parameters.items()
    }
    return LanguageService.translate_current(value.key, **parameters)

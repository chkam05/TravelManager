from __future__ import annotations

import json
import re
from threading import RLock
from typing import Any, ClassVar, Mapping

from flask import current_app, g, has_app_context

from resources.language_definitions import (
    DEFAULT_LANGUAGE,
    LANGUAGE_DEFINITIONS,
    normalize_language,
)
from resources.language_enum import Language


class LanguageService:
    """Loads grouped translations and resolves the current request language."""

    EXTENSION_KEY: ClassVar[str] = 'travel_manager_language_service'
    DEFAULT_LOCALE: ClassVar[str] = DEFAULT_LANGUAGE.value
    SUPPORTED_LOCALES: ClassVar[tuple[str, ...]] = tuple(
        language.value for language in LANGUAGE_DEFINITIONS
    )
    KEY_PATTERN: ClassVar[re.Pattern[str]] = re.compile(
        r'^[A-Z][A-Z0-9_]*(?:\.[A-Z][A-Z0-9_]*)+$'
    )

    def __init__(self):
        self._catalogs: dict[str, dict[str, Any]] = {}
        self._lock = RLock()

    @classmethod
    def normalize_locale(cls, locale: object) -> str:
        """Returns a supported locale or the application fallback locale."""
        return normalize_language(locale).value

    @classmethod
    def is_valid_key(cls, key: object) -> bool:
        """Checks whether a dotted translation key uses the required format."""
        return isinstance(key, str) and bool(cls.KEY_PATTERN.fullmatch(key))

    @classmethod
    def registered(cls) -> LanguageService:
        """Returns the language service registered on the current Flask app."""
        if not has_app_context():
            raise RuntimeError(
                'Translation requires an active Flask application context.'
            )
        service = current_app.extensions.get(cls.EXTENSION_KEY)
        if not isinstance(service, cls):
            raise RuntimeError('Language service is not configured.')
        return service

    @classmethod
    def current_locale(cls) -> str:
        """Returns the locale configured for the current Flask request."""
        return cls.normalize_locale(getattr(g, 'language', None))

    @classmethod
    def translate_current(cls, key: str, **parameters: object) -> str:
        """Translates a key for the current Flask request."""
        return cls.registered().translate(
            key,
            locale=cls.current_locale(),
            parameters=parameters
        )

    def load(self, locale: object) -> dict[str, Any]:
        """Loads one validated catalog, cached for the application lifetime."""
        normalized = self.normalize_locale(locale)

        with self._lock:
            cached = self._catalogs.get(normalized)
            if cached is not None:
                return cached

            language = Language(normalized)
            path = LANGUAGE_DEFINITIONS[language]
            with path.open('r', encoding='utf-8') as language_file:
                catalog = json.load(language_file)

            self._validate_catalog(catalog, normalized)
            self._catalogs[normalized] = catalog
            return catalog

    def translate(
        self,
        key: str,
        locale: object = None,
        parameters: Mapping[str, object] | None = None,
        **kwargs: object
    ) -> str:
        """Resolves a key, falls back to English, and interpolates named values."""
        if not self.is_valid_key(key):
            raise ValueError(f'Invalid translation key: {key!r}')

        normalized = self.normalize_locale(locale)
        value = self._find(self.load(normalized), key)

        if value is None and normalized != self.DEFAULT_LOCALE:
            value = self._find(self.load(self.DEFAULT_LOCALE), key)

        if value is None:
            return key

        replacements = dict(parameters or {})
        replacements.update(kwargs)
        return self._interpolate(value, replacements)

    def clear_cache(self) -> None:
        """Clears loaded catalogs, primarily for development and tests."""
        with self._lock:
            self._catalogs.clear()

    @classmethod
    def _validate_catalog(cls, catalog: object, locale: str) -> None:
        if not isinstance(catalog, dict):
            raise ValueError(f'Language catalog {locale!r} must be a JSON object.')
        cls._validate_value(catalog, locale)

    @classmethod
    def _validate_value(
        cls,
        value: object,
        locale: str,
        parts: tuple[str, ...] = ()
    ) -> None:
        if isinstance(value, dict):
            if not value:
                raise ValueError(
                    f'Language catalog {locale!r} contains an empty group: '
                    + '.'.join(parts)
                )
            for part, child in value.items():
                if not isinstance(part, str) or not re.fullmatch(
                    r'[A-Z][A-Z0-9_]*', part
                ):
                    raise ValueError(
                        f'Language catalog {locale!r} contains an invalid '
                        f'key segment: {part!r}'
                    )
                cls._validate_value(child, locale, (*parts, part))
            return

        if not isinstance(value, str):
            raise ValueError(
                f'Language catalog {locale!r} value must be a string: '
                + '.'.join(parts)
            )

    @staticmethod
    def _find(catalog: Mapping[str, Any], key: str) -> str | None:
        value: object = catalog
        for part in key.split('.'):
            if not isinstance(value, Mapping) or part not in value:
                return None
            value = value[part]
        return value if isinstance(value, str) else None

    @staticmethod
    def _interpolate(value: str, parameters: Mapping[str, object]) -> str:
        return re.sub(
            r'\{([A-Za-z_][A-Za-z0-9_]*)\}',
            lambda match: str(parameters.get(match.group(1), match.group(0))),
            value
        )

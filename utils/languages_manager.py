from __future__ import annotations

import fnmatch
import json
import re
import sys
from pathlib import Path
from typing import Any, ClassVar

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from core.language_service import LanguageService


class DuplicateLanguageKeyError(ValueError):
    """Raised when a language catalog contains a duplicate JSON key."""


class LanguagesManager:
    """Validates language catalogs and their references in application sources."""

    LANGUAGE_DIRECTORY: ClassVar[Path] = PROJECT_ROOT / 'assets' / 'languages'
    RESERVED_KEYS_PATH: ClassVar[Path] = PROJECT_ROOT / 'doc' / 'i18n_reserved_keys.txt'
    REFERENCE_PATTERN: ClassVar[re.Pattern[str]] = re.compile(
        r'''['"]([A-Z][A-Z0-9_]*(?:\.[A-Z][A-Z0-9_]*)+)['"]'''
    )
    PLACEHOLDER_PATTERN: ClassVar[re.Pattern[str]] = re.compile(
        r'\{([A-Za-z_][A-Za-z0-9_]*)\}'
    )
    SOURCE_SUFFIXES: ClassVar[set[str]] = {'.py', '.js', '.html'}
    SKIPPED_PARTS: ClassVar[set[str]] = {
        '.git', '.venv', '__pycache__', 'vendor', 'tests'
    }

    @staticmethod
    def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise DuplicateLanguageKeyError(f'Duplicate JSON key: {key}')
            result[key] = value
        return result

    @classmethod
    def load_catalog(cls, path: Path) -> dict[str, Any]:
        """Loads a catalog and rejects duplicate JSON keys."""
        with path.open('r', encoding='utf-8') as language_file:
            value = json.load(language_file, object_pairs_hook=cls._unique_object)
        if not isinstance(value, dict):
            raise ValueError('Catalog root must be a JSON object.')
        return value

    @classmethod
    def flatten(
        cls,
        value: dict[str, Any],
        prefix: str = ''
    ) -> dict[str, str]:
        """Flattens a grouped language catalog into dotted keys."""
        result: dict[str, str] = {}
        for key, child in value.items():
            path = f'{prefix}.{key}' if prefix else key
            if isinstance(child, dict):
                result.update(cls.flatten(child, path))
            else:
                result[path] = child
        return result

    @classmethod
    def referenced_keys(cls) -> set[str]:
        """Returns explicit translation keys referenced by application sources."""
        result: set[str] = set()
        for path in PROJECT_ROOT.rglob('*'):
            if not path.is_file() or path.suffix not in cls.SOURCE_SUFFIXES:
                continue
            if any(part in cls.SKIPPED_PARTS for part in path.parts):
                continue
            text = path.read_text(encoding='utf-8', errors='ignore')
            result.update(cls.REFERENCE_PATTERN.findall(text))
        return result

    @classmethod
    def reserved_key_patterns(cls) -> list[str]:
        """Loads documented keys whose references are constructed dynamically."""
        patterns: list[str] = []
        for line in cls.RESERVED_KEYS_PATH.read_text(encoding='utf-8').splitlines():
            value = line.split('#', 1)[0].strip()
            if value:
                patterns.append(value)
        return patterns

    @classmethod
    def audit(cls) -> list[str]:
        """Returns all catalog consistency and source-reference errors."""
        errors: list[str] = []
        catalogs: dict[str, dict[str, str]] = {}

        for locale in LanguageService.SUPPORTED_LOCALES:
            path = cls.LANGUAGE_DIRECTORY / f'{locale}.json'
            try:
                catalog = cls.load_catalog(path)
                LanguageService._validate_catalog(catalog, locale)
            except (OSError, json.JSONDecodeError, ValueError) as error:
                errors.append(f'{path.relative_to(PROJECT_ROOT)}: {error}')
                continue

            if 'SOURCE_TEXT' in catalog:
                errors.append(
                    f'{path.relative_to(PROJECT_ROOT)}: SOURCE_TEXT is forbidden.'
                )

            flat = cls.flatten(catalog)
            catalogs[locale] = flat
            if flat.get('META.CODE') != locale:
                errors.append(
                    f'{path.relative_to(PROJECT_ROOT)}: '
                    f'META.CODE must equal {locale!r}.'
                )

            for key, value in flat.items():
                if not LanguageService.is_valid_key(key):
                    errors.append(
                        f'{path.relative_to(PROJECT_ROOT)}: invalid key {key!r}.'
                    )
                if not isinstance(value, str):
                    errors.append(
                        f'{path.relative_to(PROJECT_ROOT)}: {key} is not a string.'
                    )

        fallback = catalogs.get(LanguageService.DEFAULT_LOCALE)
        if fallback is None:
            return errors

        fallback_keys = set(fallback)
        for locale, catalog in catalogs.items():
            keys = set(catalog)
            for key in sorted(fallback_keys - keys):
                errors.append(f'{locale}: missing key present in fallback: {key}')
            for key in sorted(keys - fallback_keys):
                errors.append(f'{locale}: extra key absent from fallback: {key}')
            for key in sorted(fallback_keys & keys):
                expected = set(cls.PLACEHOLDER_PATTERN.findall(fallback[key]))
                actual = set(cls.PLACEHOLDER_PATTERN.findall(catalog[key]))
                if expected != actual:
                    errors.append(
                        f'{locale}: placeholder mismatch for {key}: '
                        f'{sorted(actual)} != {sorted(expected)}'
                    )

        references = cls.referenced_keys()
        for key in sorted(references - fallback_keys):
            errors.append(f'Referenced translation key does not exist: {key}')

        try:
            reserved_patterns = cls.reserved_key_patterns()
        except OSError as error:
            errors.append(
                f'{cls.RESERVED_KEYS_PATH.relative_to(PROJECT_ROOT)}: {error}'
            )
            reserved_patterns = []

        reserved_keys = {
            key
            for key in fallback_keys
            if any(
                fnmatch.fnmatchcase(key, pattern)
                for pattern in reserved_patterns
            )
        }
        for pattern in reserved_patterns:
            if not any(
                fnmatch.fnmatchcase(key, pattern)
                for key in fallback_keys
            ):
                errors.append(
                    f'Reserved translation pattern does not match a key: {pattern}'
                )
        for key in sorted(fallback_keys - references - reserved_keys):
            errors.append(
                f'Unreferenced translation key is not documented as reserved: {key}'
            )

        return errors

    @classmethod
    def main(cls) -> int:
        """Runs the language audit and prints a command-line summary."""
        errors = cls.audit()
        if errors:
            print('Translation audit failed:')
            for error in errors:
                print(f'- {error}')
            return 1

        catalogs = {
            locale: cls.flatten(
                cls.load_catalog(cls.LANGUAGE_DIRECTORY / f'{locale}.json')
            )
            for locale in LanguageService.SUPPORTED_LOCALES
        }
        references = cls.referenced_keys()
        reserved = {
            key
            for key in catalogs[LanguageService.DEFAULT_LOCALE]
            if any(
                fnmatch.fnmatchcase(key, pattern)
                for pattern in cls.reserved_key_patterns()
            )
        }
        print(
            'Translation audit passed: '
            f'{len(catalogs[LanguageService.DEFAULT_LOCALE])} keys, '
            f'{len(references)} explicit references, '
            f'{len(reserved)} documented dynamic references, '
            f'{len(catalogs)} locales.'
        )
        return 0


if __name__ == '__main__':
    sys.exit(LanguagesManager.main())

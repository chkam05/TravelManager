from pathlib import Path

from config import PROJECT_ROOT
from resources.language_enum import Language


LANGUAGE_DEFINITIONS: dict[Language, Path] = {
    Language.ENGLISH: PROJECT_ROOT / 'assets' / 'languages' / 'en_US.json',
    Language.POLISH: PROJECT_ROOT / 'assets' / 'languages' / 'pl_PL.json',
}

DEFAULT_LANGUAGE = Language.ENGLISH


def normalize_language(value: object) -> Language:
    """Returns a registered language or the application fallback language."""
    try:
        language = Language(str(value or '').strip())
    except ValueError:
        return DEFAULT_LANGUAGE
    return language if language in LANGUAGE_DEFINITIONS else DEFAULT_LANGUAGE

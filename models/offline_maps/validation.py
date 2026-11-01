"""Shared validation helpers for persisted offline map metadata."""

from __future__ import annotations

from datetime import datetime
from math import isfinite
import re
from typing import Any
from urllib.parse import urlparse


REGION_ID_PATTERN = re.compile(r'^[A-Za-z0-9][A-Za-z0-9_/-]{0,199}$')
LOCAL_ID_PATTERN = re.compile(r'^[A-Za-z0-9][A-Za-z0-9_-]{0,127}$')


def required_text(value: Any, field: str, maximum: int = 300) -> str:
    text = str(value or '').strip()
    if not text or len(text) > maximum:
        raise ValueError(f'Invalid {field}.')
    return text


def optional_text(value: Any, field: str, maximum: int = 300) -> str:
    if value in (None, ''):
        return ''
    return required_text(value, field, maximum)


def region_id(value: Any, field: str = 'region id') -> str:
    text = required_text(value, field, 200)
    if not REGION_ID_PATTERN.fullmatch(text) or '..' in text.split('/'):
        raise ValueError(f'Invalid {field}.')
    return text


def local_id(value: Any, field: str = 'id') -> str:
    text = required_text(value, field, 128)
    if not LOCAL_ID_PATTERN.fullmatch(text):
        raise ValueError(f'Invalid {field}.')
    return text


def non_negative_integer(value: Any, field: str, allow_none: bool = False) -> int | None:
    if allow_none and value is None:
        return None
    if type(value) is not int or value < 0:
        raise ValueError(f'Invalid {field}.')
    return value


def iso_datetime(value: Any, field: str, optional: bool = True) -> str:
    text = optional_text(value, field, 64) if optional else required_text(value, field, 64)
    if not text:
        return ''
    try:
        datetime.fromisoformat(text.replace('Z', '+00:00'))
    except ValueError as error:
        raise ValueError(f'Invalid {field}.') from error
    return text


def string_list(value: Any, field: str, pattern: re.Pattern[str] | None = None) -> list[str]:
    if value is None:
        return []
    if not isinstance(value, list):
        raise ValueError(f'Invalid {field}.')
    result: list[str] = []
    for item in value:
        text = required_text(item, field, 200)
        if pattern and not pattern.fullmatch(text):
            raise ValueError(f'Invalid {field}.')
        if text not in result:
            result.append(text)
    return result


def bounds(value: Any, optional: bool = True) -> list[float] | None:
    if value is None and optional:
        return None
    if not isinstance(value, (list, tuple)) or len(value) != 4:
        raise ValueError('Invalid bounds.')
    if any(type(item) not in (int, float) or not isfinite(item) for item in value):
        raise ValueError('Invalid bounds.')
    west, south, east, north = [float(item) for item in value]
    if not (-180 <= west <= east <= 180 and -90 <= south <= north <= 90):
        raise ValueError('Invalid bounds.')
    return [west, south, east, north]


def https_url(value: Any, field: str = 'URL') -> str:
    text = required_text(value, field, 2048)
    parsed = urlparse(text)
    if parsed.scheme != 'https' or not parsed.netloc or parsed.username or parsed.password:
        raise ValueError(f'Invalid {field}.')
    return text

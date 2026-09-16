from __future__ import annotations

from html import unescape
import re


def display_name(value: str) -> str:
    """Turn Geofabrik display markup into plain text for selectors and cache."""
    plain = re.sub(r'<[^>]*>', ' ', unescape(value))
    return ' '.join(plain.split())

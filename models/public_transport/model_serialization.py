from __future__ import annotations
from datetime import date, datetime, time
from typing import Any, Dict


def parse_coordinate(
    value: Any,
    minimum: float,
    maximum: float
) -> float | None:
    """Converts a value to a coordinate inside its valid range."""
    try:
        coordinate = float(value)
    except (TypeError, ValueError):
        return None
    return coordinate if minimum <= coordinate <= maximum else None


def parse_date(value: Any) -> date | None:
    """Converts an ISO date value to a date."""
    if isinstance(value, date) and not isinstance(value, datetime):
        return value
    if not value:
        return None
    try:
        return date.fromisoformat(str(value))
    except ValueError:
        return None


def parse_datetime(value: Any) -> datetime | None:
    """Converts an ISO datetime value to a datetime."""
    if isinstance(value, datetime):
        return value
    if not value:
        return None
    try:
        return datetime.fromisoformat(str(value))
    except ValueError:
        return None


def parse_time(value: Any) -> time | None:
    """Converts an ISO time value to a time."""
    if isinstance(value, time):
        return value
    if not value:
        return None
    try:
        return time.fromisoformat(str(value))
    except ValueError:
        return None


def parse_date_url_map(value: Any) -> Dict[date, str]:
    """Converts ISO date keys to date objects."""
    if not isinstance(value, dict):
        return {}
    return {
        parsed: str(url)
        for key, url in value.items()
        if (parsed := parse_date(key)) is not None
    }


def serialize_date_url_map(value: Dict[date, str]) -> Dict[str, str]:
    """Converts date keys to JSON-compatible ISO strings."""
    return {key.isoformat(): url for key, url in value.items()}

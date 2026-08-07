from __future__ import annotations

import re
from typing import ClassVar

from utils.public_transport.warsaw_downloader import WarsawDownloader


class TricityGtfsDownloader(WarsawDownloader):
    """Shares GTFS conventions used by the Gdańsk and Gdynia feeds."""

    _STOP_POST_PATTERN: ClassVar[re.Pattern[str]] = re.compile(
        r'\s+(T[12]|\d{2})$'
    )

    @classmethod
    def _stop_name(cls, row) -> str:
        """Removes the stop-post number embedded in a stop name."""
        return cls._STOP_POST_PATTERN.sub('', str(row['name']).strip())

    @classmethod
    def _platform_name(cls, row) -> str:
        """Extracts the stop-post number embedded in a stop name."""
        match = cls._STOP_POST_PATTERN.search(str(row['name']).strip())
        if match:
            return match.group(1)
        return super()._platform_name(row)

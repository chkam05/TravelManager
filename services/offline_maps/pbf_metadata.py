from __future__ import annotations

from datetime import timezone
from email.utils import parsedate_to_datetime
import ssl
from typing import Any, Callable
from urllib.request import Request, urlopen

from resources.offline_maps.source_definitions import OfflineMapSources
from services.offline_maps.catalog_service import OfflineMapCatalogService


def pbf_metadata(
    url: str, opener: Callable[..., Any] = urlopen
) -> dict[str, int | str | None]:
    """Best-effort HEAD lookup for fields absent from Geofabrik's JSON index."""
    result: dict[str, int | str | None] = {
        'source_size': None, 'source_modified_at': '',
    }
    if not OfflineMapCatalogService._trusted_pbf_url(url):
        return result
    request = Request(url, method='HEAD', headers={
        'User-Agent': OfflineMapSources.USER_AGENT,
    })
    options: dict[str, Any] = {'timeout': 5}
    if opener is urlopen:
        try:
            import certifi
            options['context'] = ssl.create_default_context(cafile=certifi.where())
        except ImportError:
            pass
    try:
        with opener(request, **options) as response:
            if not OfflineMapCatalogService._trusted_pbf_url(response.geturl()):
                return result
            length = response.headers.get('Content-Length')
            if length and length.isdecimal():
                result['source_size'] = int(length)
            modified = response.headers.get('Last-Modified')
            if modified:
                date = parsedate_to_datetime(modified)
                result['source_modified_at'] = date.astimezone(timezone.utc).isoformat()
    except (OSError, ValueError, TypeError, OverflowError):
        # Missing HTTP metadata must not prevent an otherwise valid download.
        pass
    return result

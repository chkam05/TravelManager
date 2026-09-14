"""Controller-facing downloader classes backed by one railway repository."""
from __future__ import annotations

from resources.public_transport.rail_gtfs_sources import RailGtfsSources
from utils.public_transport.rail_gtfs_cache import RailGtfsCache
from utils.public_transport.rail_gtfs_repository import RailGtfsRepository
from utils.public_transport.rail_realtime import RailRealtime


class RailDownloader:
    BASE_URL = 'https://mkuran.pl/gtfs/'
    URL_PREFIXES = (BASE_URL,)
    PROVIDER_ID = ''

    @classmethod
    def _repository(cls) -> RailGtfsRepository:
        return RailGtfsRepository(cls.PROVIDER_ID)

    @classmethod
    def download_lines(cls, url=None, refresh=False):
        lines = cls._repository().download_lines(url, refresh)
        if refresh:
            mapping = RailGtfsSources.provider(cls.PROVIDER_ID)
            RailRealtime.refresh(mapping.source_id)
        return lines

    @classmethod
    def download_stops(cls, url=None, progress_callback=None, refresh=False):
        stops = cls._repository().download_stops(
            url, progress_callback, refresh
        )
        if refresh:
            mapping = RailGtfsSources.provider(cls.PROVIDER_ID)
            RailRealtime.refresh(mapping.source_id)
        return stops

    @classmethod
    def download_line(cls, url, include_announcement_content=False):
        del include_announcement_content
        return cls._repository().download_line(url)

    @classmethod
    def download_ride(cls, url):
        return cls._repository().download_ride(url)

    @classmethod
    def download_line_stop_timetable(
        cls, url, include_announcement_content=False
    ):
        return cls._repository().download_line_stop_timetable(
            url, include_announcement_content
        )

    @classmethod
    def download_stop_all(cls, url):
        return cls._repository().download_stop_all(url)

    @classmethod
    def download_announcements(cls, include_content=False, line=''):
        del include_content, line
        return []

    @classmethod
    def has_local_data(cls):
        mapping = RailGtfsSources.provider(cls.PROVIDER_ID)
        return RailGtfsCache.has_local_data(mapping.source_id)

    @staticmethod
    def enrich_stop_locations(stops):
        return stops


RAIL_DOWNLOADERS = {
    mapping.provider_id: type(
        ''.join(part.title() for part in mapping.provider_id.split('_')) + 'Downloader',
        (RailDownloader,),
        {'PROVIDER_ID': mapping.provider_id}
    )
    for mapping in RailGtfsSources.PROVIDERS
}

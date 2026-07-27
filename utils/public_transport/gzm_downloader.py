from __future__ import annotations
import csv
from datetime import date, datetime, time, timedelta, timezone
from io import BytesIO, TextIOWrapper
from pathlib import Path
import re
import ssl
from threading import Lock
from typing import Any, Callable, ClassVar
from urllib.error import URLError
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen
from zipfile import ZipFile

from config import SETTINGS_DIR
from core.gtfs_database import GtfsDatabase
from models.public_transport.public_transport_announcement import PublicTransportAnnouncement
from models.public_transport.public_transport_base_line import PublicTransportBaseLine
from models.public_transport.public_transport_city import PublicTransportCity
from models.public_transport.public_transport_data_container import PublicTransportDataContainer
from models.public_transport.public_transport_date_timetable import PublicTransportDateTimetable
from models.public_transport.public_transport_departure_time import PublicTransportDepartureTime
from models.public_transport.public_transport_direction import PublicTransportDirection
from models.public_transport.public_transport_direction_stop import PublicTransportDirectionStop
from models.public_transport.public_transport_line import PublicTransportLine
from models.public_transport.public_transport_line_stop_timetable import PublicTransportLineStopTimetable
from models.public_transport.public_transport_ride import PublicTransportRide
from models.public_transport.public_transport_ride_stop import PublicTransportRideStop
from models.public_transport.public_transport_stop import PublicTransportStop
from models.public_transport.public_transport_stop_all import PublicTransportStopAll
from models.public_transport.public_transport_stop_platform import PublicTransportStopPlatform
from models.public_transport.public_transport_vehicle_position import PublicTransportVehiclePosition
from resources.public_transport.public_transport_type import PublicTransportType
from utils.data.map_data_downloader import MapDataDownloader
from utils.public_transport.download_progress import PublicTransportDownloadProgress
from utils.public_transport.gzm_gtfs_repository import GzmGtfsRepository
from utils.public_transport.html_document import (
    HtmlNode as _HtmlNode,
    normalize_text as _normalize_text,
    parse_html
)


class GzmDownloader:
    """Downloads and parses public transport timetable data published by GZM."""

    BASE_URL = 'https://rj.transportgzm.pl/v2/'
    STOPS_URL = urljoin(BASE_URL, 'przystanki/')
    STOP_LOCATIONS_URL = 'https://rj.transportgzm.pl/api/v2/stops/data/'
    GTFS_DATASET_API = (
        'https://otwartedane.metropoliagzm.pl/api/3/action/package_show'
        '?id=rozklady-jazdy-i-lokalizacja-przystankow-gtfs-wersja-rozszerzona'
    )
    GTFS_RT_VEHICLES_URL = (
        'https://gtfsrt.transportgzm.pl:5443/'
        'gtfsrt/gzm/vehiclePositions'
    )
    CARRIER = 'Zarząd Transportu Metropolitalnego'
    _USER_AGENT = 'TravelManager/1.0'
    _REQUEST_TIMEOUT = 15
    _DATE_IN_URL_PATTERN = re.compile(r'/(20\d{6})(?:/|$)')
    _POLISH_DATE_PATTERN = re.compile(r'(\d{1,2})\.(\d{1,2})\.(\d{4})')
    _COLOR_PATTERN = re.compile(r'#[0-9a-fA-F]{6}')
    _LINE_PATH_PATTERN = re.compile(r'/rozklady/([^/]+)/')
    _STOP_PATH_PATTERN = re.compile(r'/stop/(\d+)/')
    _STOP_LOCATIONS_LOCK: ClassVar[Lock] = Lock()
    _STOP_LOCATIONS_CACHE: ClassVar[
        dict[str, tuple[float, float]] | None
    ] = None
    _DATABASE_PATH: ClassVar[Path] = (
        Path(SETTINGS_DIR)
        / 'gzm_gtfs.sqlite3'
    )
    _LEGACY_DATABASE_PATH: ClassVar[Path] = (
        Path(SETTINGS_DIR)
        / 'public_transport'
        / 'gzm'
        / 'gtfs.sqlite3'
    )
    _DATABASE_LOCK: ClassVar[Lock] = Lock()
    _GTFS_RESOURCE_PATTERN: ClassVar[re.Pattern[str]] = re.compile(
        r'schedule_ZTM_(\d{4}\.\d{2}\.\d{2})_(\d+)_(\d+)\.zip$',
        re.IGNORECASE
    )

    #region HTTP

    @classmethod
    def _download_html(
        cls,
        url: str,
        item: str = 'Dane przewoźnika',
        current: int = 1,
        total: int = 1
    ) -> str:
        """Downloads and decodes one GZM HTML page."""
        request = Request(url, headers={
            'Accept': 'text/html,application/xhtml+xml',
            'User-Agent': cls._USER_AGENT
        })

        ssl_context: list[ssl.SSLContext | None] = [None]

        def download() -> str:
            try:
                return cls._read_html(request, ssl_context[0])
            except URLError as error:
                if (
                    ssl_context[0] is None
                    and isinstance(
                        error.reason,
                        ssl.SSLCertVerificationError
                    )
                ):
                    ssl_context[0] = ssl._create_unverified_context()
                raise

        return PublicTransportDownloadProgress.retry(
            download,
            item,
            current,
            total
        )

    @classmethod
    def _read_html(
        cls,
        request: Request,
        context: ssl.SSLContext | None = None
    ) -> str:
        """Executes an HTTP request and decodes its response body."""
        with urlopen(
            request,
            timeout=cls._REQUEST_TIMEOUT,
            context=context
        ) as response:
            charset = response.headers.get_content_charset() or 'utf-8'
            return response.read().decode(charset, errors='replace')

    @classmethod
    def _download_bytes(
        cls,
        url: str,
        item: str,
        current: int = 1,
        total: int = 1
    ) -> bytes:
        """Downloads one binary GTFS resource with retries."""
        request = Request(url, headers={
            'Accept': '*/*',
            'User-Agent': cls._USER_AGENT
        })
        ssl_context: list[ssl.SSLContext | None] = [None]

        def download() -> bytes:
            try:
                with urlopen(
                    request,
                    timeout=max(cls._REQUEST_TIMEOUT, 45),
                    context=ssl_context[0]
                ) as response:
                    return response.read()
            except URLError as error:
                if (
                    ssl_context[0] is None
                    and isinstance(error.reason, ssl.SSLCertVerificationError)
                ):
                    ssl_context[0] = ssl._create_unverified_context()
                raise

        return PublicTransportDownloadProgress.retry(
            download,
            item,
            current,
            total
        )

    @classmethod
    def _gtfs_resources(cls, metadata: Any) -> list[tuple[str, str, str]]:
        """Returns all dated GZM GTFS packages published as one CKAN set."""
        result = metadata.get('result') if isinstance(metadata, dict) else None
        resources = (
            result.get('resources')
            if isinstance(result, dict) else None
        )
        candidates: list[tuple[tuple[str, int, int], str, str, str]] = []
        for resource in resources if isinstance(resources, list) else []:
            if not isinstance(resource, dict):
                continue
            name = str(resource.get('name') or '')
            url = str(resource.get('url') or '')
            match = cls._GTFS_RESOURCE_PATTERN.fullmatch(name)
            if not match or not url:
                continue
            candidates.append((
                (
                    match.group(1),
                    int(match.group(2)),
                    int(match.group(3))
                ),
                match.group(2),
                name,
                url
            ))
        if not candidates:
            raise ValueError('Portal GZM nie udostępnił paczki GTFS.')
        return [
            (serial, name, url)
            for _, serial, name, url in sorted(
                candidates,
                key=lambda item: item[0]
            )
        ]

    @staticmethod
    def _archive_coverage(payload: bytes) -> tuple[date, date] | None:
        """Reads the service range from feed_info.txt inside a GTFS ZIP."""
        try:
            with ZipFile(BytesIO(payload)) as archive:
                with archive.open('feed_info.txt') as source:
                    reader = csv.DictReader(TextIOWrapper(
                        source,
                        encoding='utf-8-sig',
                        newline=''
                    ))
                    row = next(reader, None)
            if not row:
                return None
            start = datetime.strptime(
                str(row.get('feed_start_date') or ''),
                '%Y%m%d'
            ).date()
            end = datetime.strptime(
                str(row.get('feed_end_date') or ''),
                '%Y%m%d'
            ).date()
            return start, end
        except (KeyError, StopIteration, ValueError):
            return None

    @classmethod
    def _ensure_database(cls, refresh: bool = False) -> Path:
        """Returns a current relational GZM GTFS cache."""
        with cls._DATABASE_LOCK:
            GtfsDatabase.migrate_cache(
                cls._LEGACY_DATABASE_PATH,
                cls._DATABASE_PATH
            )
            required_date = date.today() + timedelta(
                days=GzmGtfsRepository.DATE_RANGE_DAYS - 1
            )
            if (
                not refresh
                and GtfsDatabase.covers(cls._DATABASE_PATH, required_date)
            ):
                return cls._DATABASE_PATH
            metadata = PublicTransportDownloadProgress.retry(
                lambda: MapDataDownloader.get_json(
                    cls.GTFS_DATASET_API,
                    timeout=cls._REQUEST_TIMEOUT
                ),
                'Lista paczek GTFS GZM',
                1,
                3
            )
            resources = cls._gtfs_resources(metadata)
            total = 1 + len(resources) * 2
            archives: dict[str, bytes] = {}
            coverage_from = date.today()
            for index, (serial, archive_name, archive_url) in enumerate(
                resources,
                start=1
            ):
                archive = cls._download_bytes(
                    archive_url,
                    archive_name,
                    1 + index,
                    total
                )
                coverage = cls._archive_coverage(archive)
                if (
                    coverage is None
                    or (
                        coverage[1] >= coverage_from
                        and coverage[0] <= required_date
                    )
                ):
                    archives[f'{GzmGtfsRepository.FEED_ID}:{serial}'] = archive
            if not archives:
                raise ValueError(
                    'Paczki GTFS GZM nie obejmują wymaganego okresu.'
                )
            build_total = 1 + len(resources) + len(archives)
            GtfsDatabase.build(
                cls._DATABASE_PATH,
                archives,
                lambda feed_id, current, _count: (
                    PublicTransportDownloadProgress.report(
                        f'Przetwarzanie GTFS GZM: {feed_id}',
                        1 + len(resources) + current,
                        build_total
                    )
                ),
                coverage_days=GzmGtfsRepository.DATE_RANGE_DAYS,
                compact_shapes=True
            )
            return cls._DATABASE_PATH

    @classmethod
    def _repository(
        cls,
        refresh: bool = False
    ) -> GzmGtfsRepository:
        """Builds a repository backed by the current GZM cache."""
        return GzmGtfsRepository(
            cls._ensure_database(refresh),
            cls.BASE_URL
        )

    @staticmethod
    def _document(html: str) -> _HtmlNode:
        """Parses HTML into the internal dependency-free DOM."""
        return parse_html(html)

    @classmethod
    def download_stop_locations(
        cls,
        refresh: bool = False,
        item: str = 'Lokalizacje przystanków',
        current: int = 1,
        total: int = 1
    ) -> dict[str, tuple[float, float]]:
        """Downloads platform coordinates indexed by the GZM stop identifier."""
        with cls._STOP_LOCATIONS_LOCK:
            if cls._STOP_LOCATIONS_CACHE is not None and not refresh:
                return dict(cls._STOP_LOCATIONS_CACHE)
            data = PublicTransportDownloadProgress.retry(
                lambda: MapDataDownloader.get_json(cls.STOP_LOCATIONS_URL),
                item,
                current,
                total
            )
            cls._STOP_LOCATIONS_CACHE = cls.parse_stop_locations(data)
            return dict(cls._STOP_LOCATIONS_CACHE)

    @staticmethod
    def parse_stop_locations(data: Any) -> dict[str, tuple[float, float]]:
        """Parses the compact GZM stop-coordinate response."""
        result: dict[str, tuple[float, float]] = {}
        if not isinstance(data, list):
            return result
        for row in data:
            if not isinstance(row, list) or len(row) < 4:
                continue
            try:
                latitude = float(row[0])
                longitude = float(row[1])
            except (TypeError, ValueError):
                continue
            if -90 <= latitude <= 90 and -180 <= longitude <= 180:
                result[str(row[3])] = (latitude, longitude)
        return result

    @classmethod
    def _safe_stop_locations(
        cls,
        refresh: bool = False
    ) -> dict[str, tuple[float, float]]:
        """Returns available coordinates without blocking timetable downloads on errors."""
        try:
            return cls.download_stop_locations(refresh)
        except Exception:
            return {}

    @classmethod
    def _location_from_url(
        cls,
        url: str,
        locations: dict[str, tuple[float, float]]
    ) -> tuple[float | None, float | None]:
        """Resolves coordinates using a stop identifier embedded in a URL."""
        match = cls._STOP_PATH_PATTERN.search(url)
        if not match:
            return None, None
        return locations.get(match.group(1), (None, None))

    @classmethod
    def enrich_stop_locations(
        cls,
        stops: list[PublicTransportStop]
    ) -> list[PublicTransportStop]:
        """Returns GTFS stops, which already contain platform coordinates."""
        if any(
            platform.latitude is not None
            and platform.longitude is not None
            for stop in stops
            for platform in stop.platforms
        ):
            return stops
        locations = cls._safe_stop_locations()
        for stop in stops:
            for platform in stop.platforms:
                platform.latitude, platform.longitude = cls._location_from_url(
                    platform.url_all,
                    locations
                )
        return stops

    #endregion HTTP

    #region Shared parsing

    @classmethod
    def _absolute_url(cls, url: str, source_url: str | None = None) -> str:
        """Converts a provider-relative URL to an absolute URL."""
        return urljoin(source_url or cls.BASE_URL, url)

    @classmethod
    def _type_from_text(cls, value: str) -> PublicTransportType:
        """Maps a Polish transport label or GZM line URL to a transport type."""
        lowered = value.casefold()
        if 'tram' in lowered or '/0-t' in lowered:
            return PublicTransportType.TRAM
        if 'trolej' in lowered or '/11-' in lowered:
            return PublicTransportType.TROLLEY
        return PublicTransportType.BUS

    @classmethod
    def _line_from_url(cls, url: str) -> str:
        """Extracts the public line name from a GZM line URL."""
        match = cls._LINE_PATH_PATTERN.search(url)
        if not match:
            return ''
        identifier = match.group(1)
        if identifier.startswith('0-t'):
            return identifier[3:].upper()
        if identifier.startswith('11-'):
            return identifier[3:].upper()
        if identifier.startswith('3-'):
            return identifier[2:].upper()
        return identifier.upper()

    @classmethod
    def _date_from_url(cls, url: str) -> date | None:
        """Extracts a timetable date from a GZM URL."""
        match = cls._DATE_IN_URL_PATTERN.search(url)
        if not match:
            return None
        try:
            return datetime.strptime(match.group(1), '%Y%m%d').date()
        except ValueError:
            return None

    @classmethod
    def _date_from_text(cls, value: str) -> date | None:
        """Extracts the first Polish numeric date from text."""
        match = cls._POLISH_DATE_PATTERN.search(value)
        if not match:
            return None
        try:
            return date(int(match.group(3)), int(match.group(2)), int(match.group(1)))
        except ValueError:
            return None

    @classmethod
    def _dates(cls, document: _HtmlNode, source_url: str) -> dict[date, str]:
        """Extracts date-selection links from a timetable page."""
        result: dict[date, str] = {}
        for anchor in document.find_all('a'):
            href = anchor.attrs.get('href', '')
            title = anchor.attrs.get('title', '')
            is_date_link = (
                'wybranego dnia' in title.casefold()
                or re.search(r'/rozklady/[^/]+/20\d{6}/?$', href)
                or re.search(
                    r'/rozklady/przystanek/20\d{6}/stop/\d+/$',
                    href
                )
            )
            if not is_date_link:
                continue
            parsed_date = cls._date_from_url(href)
            if parsed_date:
                result.setdefault(parsed_date, cls._absolute_url(href, source_url))
        return result

    @classmethod
    def _color(cls, node: _HtmlNode) -> str:
        """Extracts an HTML color from a node's inline style."""
        match = cls._COLOR_PATTERN.search(node.attrs.get('style', ''))
        return match.group(0).upper() if match else '#000000'

    @classmethod
    def _city_colors(cls, document: _HtmlNode) -> dict[str, PublicTransportCity]:
        """Extracts provider city/color legend entries indexed by color."""
        result: dict[str, PublicTransportCity] = {}
        for item in document.find_all('li'):
            color = cls._color(item)
            name = item.text()
            if color != '#000000' and name:
                result[color] = PublicTransportCity(name=name, color=color)
        return result

    @classmethod
    def _base_line_from_group(
        cls,
        group: _HtmlNode,
        source_url: str,
        free_of_charge: bool = False,
        updated: bool = False
    ) -> PublicTransportBaseLine | None:
        """Parses one GZM line button group."""
        anchors = group.find_all('a')
        line_anchor = next((
            anchor for anchor in reversed(anchors)
            if cls._LINE_PATH_PATTERN.search(anchor.attrs.get('href', ''))
        ), None)
        if not line_anchor:
            return None
        href = line_anchor.attrs.get('href', '')
        image = group.find('img')
        type_source = image.attrs.get('alt', '') if image else href
        return PublicTransportBaseLine(
            line=line_anchor.text() or cls._line_from_url(href),
            type=cls._type_from_text(type_source),
            url=cls._absolute_url(href, source_url),
            free_of_charge=free_of_charge,
            updated=updated
        )

    #endregion Shared parsing

    #region Lines

    @classmethod
    def download_lines(
        cls,
        url: str | None = None,
        refresh: bool = False
    ) -> list[PublicTransportBaseLine]:
        """Loads the complete line list from the relational GTFS cache."""
        del url
        return cls._repository(refresh).lines()

    @classmethod
    def parse_lines(
        cls,
        html: str,
        source_url: str | None = None
    ) -> list[PublicTransportBaseLine]:
        """Parses the provider's complete line list."""
        source_url = source_url or cls.BASE_URL
        document = cls._document(html)
        result: list[PublicTransportBaseLine] = []
        for panel in document.find_all('div', 'panel-default'):
            heading = panel.find(class_name='panel-title')
            body = panel.find('div', 'panel-timetable')
            if not heading or not body:
                continue
            heading_text = heading.text()
            free_of_charge = 'bezpłatna' in heading_text.casefold()
            for anchor in body.find_all('a', 'btn-line-nr'):
                href = anchor.attrs.get('href', '')
                if not href.startswith('/v2/rozklady/'):
                    continue
                result.append(PublicTransportBaseLine(
                    line=anchor.text(),
                    type=cls._type_from_text(heading_text),
                    url=cls._absolute_url(href, source_url),
                    free_of_charge=free_of_charge,
                    updated=anchor.has_class('btn-line-updated')
                ))
        return result

    @classmethod
    def download_line(
        cls,
        url: str,
        include_announcement_content: bool = False
    ) -> PublicTransportLine:
        """Loads one GTFS line and keeps HTML as its announcement source."""
        repository = cls._repository()
        model = repository.line(url)
        announcement_url = cls._legacy_line_url(model.line, model.type)
        try:
            document = cls._document(cls._download_html(
                announcement_url,
                f'Komunikaty linii {model.line}'
            ))
            model.announcements = cls._parse_announcements(
                document,
                announcement_url
            )
        except Exception:
            model.announcements = []
        if include_announcement_content:
            announcements = []
            total = len(model.announcements)
            for index, item in enumerate(model.announcements, start=1):
                announcements.append(
                    cls.download_announcement(
                        item.url,
                        item.description,
                        index,
                        total
                    ) if item.url else item
                )
            model.announcements = announcements
        return model

    @classmethod
    def _legacy_line_url(
        cls,
        line: str,
        transport_type: PublicTransportType
    ) -> str:
        """Builds the HTML timetable URL used only for announcements."""
        if transport_type == PublicTransportType.TRAM:
            identifier = f'0-t{line.casefold()}'
        elif transport_type == PublicTransportType.TROLLEY:
            identifier = f'11-{line.casefold()}'
        else:
            identifier = f'3-{line.casefold()}'
        return urljoin(cls.BASE_URL, f'rozklady/{identifier}/')

    @classmethod
    def parse_line(cls, html: str, source_url: str) -> PublicTransportLine:
        """Parses detailed directions, stops, dates and announcements for one line."""
        document = cls._document(html)
        line = cls._line_from_url(source_url)
        transport_type = cls._type_from_text(source_url)
        city_colors = cls._city_colors(document)
        directions: list[PublicTransportDirection] = []
        for group in document.find_all('div', 'list-group'):
            heading = next((
                node for node in group.children
                if isinstance(node, _HtmlNode)
                and node.has_class('list-group-item-warning')
            ), None)
            if not heading or 'kierunek:' not in heading.text().casefold():
                continue
            strong = heading.find('strong')
            direction_name = strong.text() if strong else heading.text()
            stops: list[PublicTransportDirectionStop] = []
            direction_cities: list[PublicTransportCity] = []
            for anchor in group.find_all('a', 'direction-list-group-item'):
                color = cls._color(anchor)
                city = city_colors.get(
                    color,
                    PublicTransportCity(name='', color=color)
                )
                abbr = anchor.find('abbr')
                platform = abbr.text() if abbr else ''
                name = anchor.text()
                if platform and name.endswith(platform):
                    name = name[:-len(platform)].strip()
                stop = PublicTransportDirectionStop(
                    line=line,
                    type=transport_type,
                    city=city,
                    is_variant=anchor.has_class('direction-non-primary'),
                    name=name,
                    platform=platform,
                    url=cls._absolute_url(anchor.attrs.get('href', ''), source_url)
                )
                stops.append(stop)
                if city.name and city.name not in [item.name for item in direction_cities]:
                    direction_cities.append(city)
            directions.append(PublicTransportDirection(
                name=direction_name,
                cities=direction_cities,
                stops=stops
            ))
        return PublicTransportLine(
            line=line,
            type=transport_type,
            announcements=cls._parse_announcements(document, source_url),
            directions=directions,
            route_variants={},
            dates=cls._dates(document, source_url)
        )

    #endregion Lines

    #region Announcements

    @classmethod
    def _parse_announcements(
        cls,
        document: _HtmlNode,
        source_url: str
    ) -> list[PublicTransportAnnouncement]:
        """Parses announcement summaries embedded in line and stop pages."""
        result: list[PublicTransportAnnouncement] = []
        seen: set[str] = set()
        for row in document.find_all('tr'):
            news_links = [
                anchor for anchor in row.find_all('a')
                if '/news/i/' in anchor.attrs.get('href', '')
            ]
            if not news_links:
                continue
            href = news_links[0].attrs.get('href', '')
            absolute_url = cls._absolute_url(href, source_url)
            if absolute_url in seen:
                continue
            seen.add(absolute_url)
            city_link = next((
                anchor for anchor in news_links
                if anchor.has_class('news_colorized_url')
            ), news_links[0])
            description_link = news_links[-1]
            dates = cls._POLISH_DATE_PATTERN.findall(row.text())
            parsed_dates = [
                date(int(year), int(month), int(day))
                for day, month, year in dates[:2]
            ]
            result.append(PublicTransportAnnouncement(
                lines=[],
                city=city_link.text(),
                content='',
                description=description_link.text(),
                effective_date_from=parsed_dates[0] if parsed_dates else None,
                effective_date_to=parsed_dates[1] if len(parsed_dates) > 1 else None,
                last_updated_datetime=None,
                url=absolute_url
            ))
        return result

    @classmethod
    def download_announcement(
        cls,
        url: str,
        description: str = '',
        current: int = 1,
        total: int = 1
    ) -> PublicTransportAnnouncement:
        """Downloads the full content and validity data of an announcement."""
        return cls.parse_announcement(
            cls._download_html(
                url,
                f'Komunikat „{description}”' if description else 'Komunikat',
                current,
                total
            ),
            url
        )

    @classmethod
    def parse_announcement(
        cls,
        html: str,
        source_url: str
    ) -> PublicTransportAnnouncement:
        """Parses the full content and validity data of an announcement."""
        document = cls._document(html)
        panel = next((
            node for node in document.find_all('div', 'panel-default')
            if node.find('h2') and 'cookie' not in node.find('h2').text().casefold()
        ), document)
        heading = panel.find('h2')
        title = heading.text() if heading else ''
        city, _, description = title.partition('–')
        panel_text = panel.text()
        dates = cls._POLISH_DATE_PATTERN.findall(panel_text)
        parsed_dates = [
            date(int(year), int(month), int(day))
            for day, month, year in dates[:3]
        ]
        updated = None
        updated_match = re.search(
            r'Ostatnia aktualizacja:\s*(\d{2}\.\d{2}\.\d{4})'
            r'(?:\s+(\d{1,2}:\d{2}))?',
            panel_text
        )
        if updated_match:
            updated_date = cls._date_from_text(updated_match.group(1))
            updated_time = time.fromisoformat(updated_match.group(2) or '00:00')
            if updated_date:
                updated = datetime.combine(updated_date, updated_time)
        bodies = panel.find_all('div', 'panel-body')
        lead = panel.find(class_name='list_lead')
        content_body = bodies[-1] if bodies else panel
        return PublicTransportAnnouncement(
            lines=[],
            city=city.strip(),
            content=content_body.text(),
            description=(description.strip() or (lead.text() if lead else title)),
            effective_date_from=parsed_dates[0] if parsed_dates else None,
            effective_date_to=parsed_dates[1] if len(parsed_dates) > 1 else None,
            last_updated_datetime=updated,
            url=source_url
        )

    #endregion Announcements

    #region Stop timetable

    @classmethod
    def download_line_stop_timetable(
        cls,
        url: str,
        include_announcement_content: bool = False
    ) -> PublicTransportLineStopTimetable:
        """Loads one platform timetable from GTFS."""
        model = cls._repository().line_stop(url)
        announcement_url = cls._legacy_line_url(model.line, model.type)
        try:
            model.announcements = cls._parse_announcements(
                cls._document(cls._download_html(
                    announcement_url,
                    f'Komunikaty linii {model.line}'
                )),
                announcement_url
            )
        except Exception:
            model.announcements = []
        if include_announcement_content:
            announcements = []
            total = len(model.announcements)
            for index, item in enumerate(model.announcements, start=1):
                announcements.append(
                    cls.download_announcement(
                        item.url,
                        item.description,
                        index,
                        total
                    ) if item.url else item
                )
            model.announcements = announcements
        return model

    @classmethod
    def parse_line_stop_timetable(
        cls,
        html: str,
        source_url: str,
        stop_locations: dict[str, tuple[float, float]] | None = None
    ) -> PublicTransportLineStopTimetable:
        """Parses all dates and departures shown for one line and platform."""
        document = cls._document(html)
        line = cls._line_from_url(source_url)
        transport_type = cls._type_from_text(source_url)
        stop_name = ''
        platform = ''
        for span in document.find_all('span', 'col-stop-padding'):
            text_value = span.text()
            if text_value.casefold().startswith('przystanek:'):
                stop_name = text_value.split(':', 1)[1].strip()
            elif text_value.casefold().startswith('stanowisko:'):
                platform = text_value.split(':', 1)[1].strip()
        direction_name = ''
        lead = next((
            node for node in document.find_all('div', 'lead')
            if 'kierunek:' in node.text().casefold()
        ), None)
        if lead:
            direction_name = lead.text().split(':', 1)[-1].replace(
                'Zmień kierunek', ''
            ).strip()
        latitude, longitude = cls._location_from_url(
            source_url,
            stop_locations or {}
        )
        timetable: dict[date, PublicTransportDateTimetable] = {}
        panels = [
            panel for panel in document.find_all('div')
            if (
                panel.has_class('panel-info')
                or panel.has_class('panel-default')
            )
            and (heading := panel.find(class_name='panel-title')) is not None
            and 'wszystkie kursy dnia:' in heading.text().casefold()
        ]
        for panel in panels:
            parsed = cls._parse_date_timetable_panel(
                panel,
                source_url,
                direction_name
            )
            if parsed.date:
                timetable[parsed.date] = parsed
        return PublicTransportLineStopTimetable(
            line=line,
            type=transport_type,
            announcements=cls._parse_announcements(document, source_url),
            stop_name=stop_name,
            direction_name=direction_name,
            platform=platform,
            timetable=timetable,
            dates=cls._dates(document, source_url),
            latitude=latitude,
            longitude=longitude
        )

    @classmethod
    def _parse_date_timetable_panel(
        cls,
        panel: _HtmlNode,
        source_url: str,
        direction_name: str = ''
    ) -> PublicTransportDateTimetable:
        """Parses departures, variants and validity from one date panel."""
        heading = panel.find(class_name='panel-title')
        panel_date = cls._date_from_text(heading.text() if heading else '')
        departures: list[PublicTransportDepartureTime] = []
        for arrival in panel.find_all('div', 'arrival-time'):
            hour_match = re.search(r'\d{1,2}', arrival.own_text())
            if not hour_match:
                continue
            hour = int(hour_match.group(0))
            for anchor in arrival.find_all('a', 'btn-stoptime'):
                minute_match = re.search(r'\d{1,2}', anchor.own_text())
                if not minute_match or hour > 23:
                    continue
                minute = int(minute_match.group(0))
                if minute > 59:
                    continue
                variant_node = anchor.find(class_name='route-variant-char')
                title = anchor.attrs.get('title', '')
                departures.append(PublicTransportDepartureTime(
                    departure_time=time(hour, minute),
                    is_high_floor='wysokopodłogowy' in title.casefold(),
                    url=cls._absolute_url(anchor.attrs.get('href', ''), source_url),
                    variant=variant_node.text() if variant_node else ''
                ))
        variants = [
            node.text() for node in panel.find_all('a', 'variant-collapse-btn')
            if node.text()
        ]
        validity_match = re.search(
            r'Rozkład obowiązuje\s+od\s+(\d{2}\.\d{2}\.\d{4})'
            r'(?:\s+r\.)?(?:\s+do\s+(\d{2}\.\d{2}\.\d{4}))?',
            panel.text()
        )
        effective_from = (
            cls._date_from_text(validity_match.group(1))
            if validity_match else None
        )
        effective_to = (
            cls._date_from_text(validity_match.group(2))
            if validity_match and validity_match.group(2) else None
        )
        return PublicTransportDateTimetable(
            date=panel_date,
            direction_name=direction_name,
            effective_date_from=effective_from,
            effective_date_to=effective_to,
            departures=departures,
            variants=list(dict.fromkeys(variants))
        )

    #endregion Stop timetable

    #region Rides

    @classmethod
    def download_ride(
        cls,
        url: str,
        from_first_stop: bool = True
    ) -> PublicTransportRide:
        """Loads a complete ride by joining relational GTFS tables."""
        del from_first_stop
        return cls._repository().ride(url)

    @classmethod
    def _first_ride_stop_url(cls, html: str, source_url: str) -> str:
        """Returns the ride link assigned to the first stop in the detail table."""
        document = cls._document(html)
        table = cls._ride_table(document)
        if not table:
            return ''
        for anchor in table.find_all('a'):
            href = anchor.attrs.get('href', '')
            if re.search(r'/stop/\d+/\d+/\d+/', href):
                return cls._absolute_url(href, source_url)
        return ''

    @staticmethod
    def _without_fragment(url: str) -> str:
        """Removes a URL fragment for stable comparisons."""
        parsed = urlparse(url)
        return parsed._replace(fragment='').geturl()

    @staticmethod
    def _ride_table(document: _HtmlNode) -> _HtmlNode | None:
        """Finds the selected ride details table."""
        for group in document.find_all('div', 'list-group'):
            active = next((
                child for child in group.children
                if isinstance(child, _HtmlNode)
                and child.has_class('list-group-item')
                and child.has_class('active')
            ), None)
            if active and 'szczegóły wybranego kursu' in active.text().casefold():
                return group.find('table')
        return None

    @classmethod
    def parse_ride(
        cls,
        html: str,
        source_url: str,
        stop_locations: dict[str, tuple[float, float]] | None = None
    ) -> PublicTransportRide:
        """Parses the complete stop sequence and metrics for one ride."""
        document = cls._document(html)
        city_colors = cls._city_colors(document)
        table = cls._ride_table(document)
        rows: list[PublicTransportRideStop] = []
        if table:
            for row in table.find_all('tr'):
                cells = row.find_all('td')
                if len(cells) < 4:
                    continue
                stop_link = cells[0].find('a', 'dropdown-toggle')
                stop_name = stop_link.text().removesuffix(' caret').strip() if stop_link else ''
                stop_url = next((
                    anchor.attrs.get('href', '')
                    for anchor in cells[0].find_all('a')
                    if cls._STOP_PATH_PATTERN.search(anchor.attrs.get('href', ''))
                ), '')
                latitude, longitude = cls._location_from_url(
                    stop_url,
                    stop_locations or {}
                )
                departure = cls._parse_clock(cells[1].text())
                travel_sum, travel = cls._parse_metric(cells[2].text(), 'min')
                distance_sum, distance = cls._parse_metric(cells[3].text(), 'km')
                color_node = cells[4] if len(cells) > 4 else row
                color = cls._color(color_node)
                rows.append(PublicTransportRideStop(
                    stop=stop_name,
                    departure_time=departure,
                    travel_time=int(travel),
                    travel_time_sum=int(travel_sum),
                    distance=distance,
                    distance_sum=distance_sum,
                    city=city_colors.get(
                        color,
                        PublicTransportCity(name='', color=color)
                    ),
                    latitude=latitude,
                    longitude=longitude
                ))
        first = rows[0] if rows else None
        page_text = document.text()
        carrier_match = re.search(
            r'Kurs obsługuje:\s*(.+?)\s+Typ pojazdu:',
            page_text
        )
        vehicle_match = re.search(r'Typ pojazdu:\s*([^\[]+?)(?:\s+\[|$)', page_text)
        platform_match = re.search(r'Stanowisko:\s*([^\s]+)', page_text)
        return PublicTransportRide(
            line=cls._line_from_url(source_url),
            type=cls._type_from_text(source_url),
            stop_name=first.stop if first else '',
            platform=platform_match.group(1).strip() if platform_match else '',
            departure_time=first.departure_time if first else None,
            cities=list(city_colors.values()),
            next_stops=rows[1:] if rows else [],
            carrier=carrier_match.group(1).strip() if carrier_match else '',
            vehicle_type=vehicle_match.group(1).strip() if vehicle_match else '',
            latitude=first.latitude if first else None,
            longitude=first.longitude if first else None
        )

    @staticmethod
    def _parse_clock(value: str) -> time | None:
        """Parses an HH:MM clock value."""
        match = re.search(r'(\d{1,2}):(\d{2})', value)
        if not match:
            return None
        try:
            return time(int(match.group(1)), int(match.group(2)))
        except ValueError:
            return None

    @staticmethod
    def _parse_metric(value: str, unit: str) -> tuple[float, float]:
        """Parses a cumulative metric and its parenthesized segment value."""
        matches = re.findall(rf'([\d.,]+)\s*{re.escape(unit)}', value)
        numbers = [float(item.replace(',', '.')) for item in matches]
        if not numbers:
            return 0.0, 0.0
        return numbers[0], numbers[1] if len(numbers) > 1 else numbers[0]

    #endregion Rides

    #region Stops

    @classmethod
    def download_stops(
        cls,
        url: str | None = None,
        progress_callback: Callable[[int, int, str], None] | None = None,
        refresh: bool = False
    ) -> list[PublicTransportStop]:
        """Loads all cities, stops and platforms from GTFS."""
        del url
        stops = cls._repository(refresh).stops()
        if progress_callback:
            progress_callback(1, 1, 'GZM')
        return stops

    @classmethod
    def parse_stop_cities(
        cls,
        html: str,
        source_url: str | None = None
    ) -> list[tuple[str, str]]:
        """Parses city names and URLs from the stop index."""
        source_url = source_url or cls.STOPS_URL
        document = cls._document(html)
        result: list[tuple[str, str]] = []
        for anchor in document.find_all('a'):
            href = anchor.attrs.get('href', '')
            if re.fullmatch(r'/v2/przystanki/[^/]+/', href):
                result.append((anchor.text(), cls._absolute_url(href, source_url)))
        return result

    @classmethod
    def download_city_stops(
        cls,
        url: str,
        city_name: str = '',
        stop_locations: dict[str, tuple[float, float]] | None = None,
        current: int = 1,
        total: int = 1
    ) -> list[PublicTransportStop]:
        """Downloads all stops and platforms for one city."""
        return cls.parse_city_stops(
            cls._download_html(
                url,
                f'Przystanki: {city_name}' if city_name else 'Przystanki miasta',
                current,
                total
            ),
            url,
            city_name,
            stop_locations
        )

    @classmethod
    def parse_city_stops(
        cls,
        html: str,
        source_url: str,
        city_name: str = '',
        stop_locations: dict[str, tuple[float, float]] | None = None
    ) -> list[PublicTransportStop]:
        """Parses all stops and platforms for one city."""
        document = cls._document(html)
        if not city_name:
            heading = next((
                node for node in document.find_all('strong')
                if 'lista przystanków:' in node.text().casefold()
            ), None)
            city_name = heading.text().split(':', 1)[-1].strip() if heading else ''
        city = PublicTransportCity(name=city_name, color='#000000')
        table = next((
            node for node in document.find_all('table')
            if 'stanowisko' in node.text().casefold()
            and 'linie' in node.text().casefold()
        ), None)
        if not table:
            return []
        result: list[PublicTransportStop] = []
        current_stop: PublicTransportStop | None = None
        tbody = table.find('tbody') or table
        for row in [
            child for child in tbody.children
            if isinstance(child, _HtmlNode) and child.tag == 'tr'
        ]:
            if row.has_class('info'):
                strong = row.find('strong')
                current_stop = PublicTransportStop(
                    name=strong.text() if strong else row.text(),
                    city=city,
                    platforms=[]
                )
                result.append(current_stop)
                continue
            if not current_stop:
                continue
            cells = row.find_all('td')
            if len(cells) < 2:
                continue
            all_link = next((
                anchor for anchor in cells[0].find_all('a')
                if re.search(r'/rozklady/przystanek/stop/\d+/$', anchor.attrs.get('href', ''))
            ), None)
            chrono_link = next((
                anchor for anchor in cells[0].find_all('a')
                if re.search(r'/rozklady/przystanek/stop/\d+/c/$', anchor.attrs.get('href', ''))
            ), None)
            lines: list[PublicTransportBaseLine] = []
            for group in cells[1].find_all('div', 'line-btn-group'):
                parsed = cls._base_line_from_group(group, source_url)
                if parsed:
                    lines.append(parsed)
            platform_name = ''
            if all_link:
                small = all_link.find('small')
                platform_name = (small.text() if small else all_link.text()).replace(
                    'Stanowisko', ''
                ).strip()
            all_url = cls._absolute_url(
                all_link.attrs.get('href', '') if all_link else '',
                source_url
            )
            latitude, longitude = cls._location_from_url(
                all_url,
                stop_locations or {}
            )
            current_stop.platforms.append(PublicTransportStopPlatform(
                name=platform_name,
                lines=lines,
                url_all=all_url,
                url_chrono=cls._absolute_url(
                    chrono_link.attrs.get('href', '') if chrono_link else '',
                    source_url
                ),
                latitude=latitude,
                longitude=longitude
            ))
        return result

    @classmethod
    def download_stop_all(cls, url: str) -> PublicTransportStopAll:
        """Loads every line-direction timetable for one GTFS platform."""
        return cls._repository().stop_all(url)

    @classmethod
    def parse_stop_all(
        cls,
        html: str,
        source_url: str,
        stop_locations: dict[str, tuple[float, float]] | None = None
    ) -> PublicTransportStopAll:
        """Parses every line-direction entry shown for one platform."""
        document = cls._document(html)
        stop_name = ''
        platform = ''
        for span in document.find_all('span', 'col-stop-padding'):
            text_value = span.text()
            if text_value.casefold().startswith('przystanek:') and not stop_name:
                stop_name = text_value.split(':', 1)[-1].strip()
            elif text_value.casefold().startswith('stanowisko:') and not platform:
                platform = text_value.split(':', 1)[-1].strip()
        latitude, longitude = cls._location_from_url(
            source_url,
            stop_locations or {}
        )
        nodes = list(document.iter_nodes())
        entries: dict[
            PublicTransportBaseLine,
            PublicTransportDateTimetable
        ] = {}
        for index, node in enumerate(nodes):
            if node.tag != 'div' or not node.has_class('line-btn-group'):
                continue
            base_line = cls._base_line_from_group(node, source_url)
            if not base_line:
                continue
            timetable_panel = None
            direction_name = ''
            for following in nodes[index + 1:]:
                if following.tag == 'div' and following.has_class('line-btn-group'):
                    break
                if (
                    following.tag == 'div'
                    and following.has_class('lead')
                    and 'kierunek:' in following.text().casefold()
                ):
                    direction_name = following.text().split(':', 1)[-1].strip()
                if (
                    following.tag == 'div'
                    and (
                        following.has_class('panel-info')
                        or following.has_class('panel-default')
                    )
                    and (heading := following.find(class_name='panel-title')) is not None
                    and 'wszystkie kursy dnia:' in heading.text().casefold()
                ):
                    timetable_panel = following
                    break
            if not timetable_panel:
                continue
            entries[base_line] = cls._parse_date_timetable_panel(
                timetable_panel,
                source_url,
                direction_name
            )
        return PublicTransportStopAll(
            stop_name=stop_name,
            platform=platform,
            dates=cls._dates(document, source_url),
            lines=entries,
            latitude=latitude,
            longitude=longitude
        )

    #endregion Stops

    #region GTFS-Realtime

    @classmethod
    def download_vehicle_positions(
        cls,
        line: str = ''
    ) -> list[PublicTransportVehiclePosition]:
        """Downloads current GZM vehicle positions from GTFS-Realtime."""
        repository = cls._repository()
        route_names, trip_names, line_types = repository.realtime_maps()
        payload = cls._download_bytes(
            cls.GTFS_RT_VEHICLES_URL,
            'Pojazdy GZM na żywo'
        )
        return cls.parse_vehicle_positions(
            payload,
            route_names,
            trip_names,
            line_types,
            line
        )

    @classmethod
    def parse_vehicle_positions(
        cls,
        payload: bytes,
        route_names: dict[tuple[str, str], str],
        trip_names: dict[tuple[str, str], str],
        line_types: dict[str, PublicTransportType],
        line: str = ''
    ) -> list[PublicTransportVehiclePosition]:
        """Deserializes the official GZM VehiclePositions protobuf feed."""
        try:
            from google.transit import gtfs_realtime_pb2
        except ImportError as error:
            raise RuntimeError(
                'Brak biblioteki gtfs-realtime-bindings.'
            ) from error
        message = gtfs_realtime_pb2.FeedMessage()
        message.ParseFromString(payload)
        result: list[PublicTransportVehiclePosition] = []
        feed_id = GzmGtfsRepository.FEED_ID
        for entity in message.entity:
            if not entity.HasField('vehicle'):
                continue
            vehicle = entity.vehicle
            route_id = str(vehicle.trip.route_id or '')
            trip_id = str(vehicle.trip.trip_id or '')
            line_name = (
                trip_names.get((feed_id, trip_id))
                or route_names.get((feed_id, route_id))
                or route_id
            )
            if line and line_name != line:
                continue
            latitude = float(vehicle.position.latitude)
            longitude = float(vehicle.position.longitude)
            if not (-90 <= latitude <= 90 and -180 <= longitude <= 180):
                continue
            descriptor = vehicle.vehicle
            result.append(PublicTransportVehiclePosition(
                vehicle_id=str(
                    descriptor.id or descriptor.label or entity.id
                ),
                line=line_name,
                trip_id=trip_id,
                type=line_types.get(
                    line_name,
                    PublicTransportType.BUS
                ),
                latitude=latitude,
                longitude=longitude,
                bearing=(
                    float(vehicle.position.bearing)
                    if vehicle.position.HasField('bearing') else None
                ),
                speed=(
                    float(vehicle.position.speed)
                    if vehicle.position.HasField('speed') else None
                ),
                recorded_at=(
                    datetime.fromtimestamp(
                        int(vehicle.timestamp),
                        tz=timezone.utc
                    )
                    if vehicle.timestamp else None
                )
            ))
        return result

    #endregion GTFS-Realtime

    #region Container

    @classmethod
    def download_container(
        cls,
        include_line_details: bool = False,
        include_stops: bool = False,
        include_vehicle_positions: bool = False,
        progress_callback: Callable[[int, int, str], None] | None = None
    ) -> PublicTransportDataContainer:
        """Downloads a selectable provider snapshot into one typed container."""
        base_lines = cls.download_lines()
        lines: list[PublicTransportLine] = []
        if include_line_details:
            total = len(base_lines)
            for index, base_line in enumerate(base_lines, start=1):
                lines.append(cls.download_line(base_line.url))
                if progress_callback:
                    progress_callback(index, total, f'Linia {base_line.line}')
        stops = cls.download_stops(
            progress_callback=progress_callback
        ) if include_stops else []
        positions = (
            cls.download_vehicle_positions()
            if include_vehicle_positions else []
        )
        return PublicTransportDataContainer(
            carrier=cls.CARRIER,
            base_url=cls.BASE_URL,
            base_lines=base_lines,
            lines=lines,
            line_stop_timetables=[],
            rides=[],
            stops=stops,
            stop_all=[],
            vehicle_positions=positions
        )

    #endregion Container

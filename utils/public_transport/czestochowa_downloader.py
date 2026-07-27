from __future__ import annotations
from datetime import date, datetime, time
import json
import re
import ssl
from threading import Lock
from typing import Any, Callable, ClassVar
import unicodedata
from urllib.error import URLError
from urllib.parse import parse_qs, quote, urlencode, urljoin, urlparse, urlunparse
from urllib.request import Request, urlopen

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
from resources.public_transport.public_transport_type import PublicTransportType
from utils.data.overpass_downloader import OverpassDownloader
from utils.public_transport.download_progress import PublicTransportDownloadProgress
from utils.public_transport.html_document import HtmlNode, parse_html


class CzestochowaDownloader:
    """Downloads public transport timetables published by Częstochowa."""

    BASE_URL: ClassVar[str] = 'https://www.czestochowa.pl/'
    TIMETABLE_URL: ClassVar[str] = urljoin(BASE_URL, 'rozklady-jazdy')
    STOPS_URL: ClassVar[str] = f'{TIMETABLE_URL}?lista=przystankow'
    TRIP_URL: ClassVar[str] = urljoin(BASE_URL, 'timetables/trip/stops')
    CARRIER: ClassVar[str] = 'MPK w Częstochowie'
    CITY_NAME: ClassVar[str] = 'Częstochowa'
    CITY_COLOR: ClassVar[str] = '#1F6EAE'
    _USER_AGENT: ClassVar[str] = 'TravelManager/1.0'
    _REQUEST_TIMEOUT: ClassVar[int] = 15
    _DATE_PATTERN: ClassVar[re.Pattern] = re.compile(
        r'(20\d{2})-(\d{2})-(\d{2})'
    )
    _STOP_AREA_BBOX: ClassVar[str] = '50.6500,18.8500,51.0500,19.4500'
    _STOP_LOCATIONS_LOCK: ClassVar[Lock] = Lock()
    _STOP_LOCATIONS_CACHE: ClassVar[
        dict[str, tuple[float, float]] | None
    ] = None

    #region HTTP

    @classmethod
    def _download_html(
        cls,
        url: str,
        item: str = 'Dane przewoźnika',
        current: int = 1,
        total: int = 1
    ) -> str:
        """Downloads and decodes one provider HTML page."""
        request = Request(cls._request_url(url), headers={
            'Accept': 'text/html,application/xhtml+xml',
            'User-Agent': cls._USER_AGENT
        })
        return cls._download_request(
            request,
            item,
            current,
            total
        )

    @classmethod
    def _download_json(
        cls,
        url: str,
        item: str = 'Dane przejazdu',
        current: int = 1,
        total: int = 1
    ) -> dict[str, Any]:
        """Downloads one JSON response from the provider."""
        request = Request(cls._request_url(url), headers={
            'Accept': 'application/json',
            'User-Agent': cls._USER_AGENT,
            'X-Requested-With': 'XMLHttpRequest'
        })
        return json.loads(
            cls._download_request(request, item, current, total)
        )

    @classmethod
    def _download_request(
        cls,
        request: Request,
        item: str,
        current: int,
        total: int
    ) -> str:
        """Downloads one response with retry-aware SSL compatibility."""
        ssl_context: list[ssl.SSLContext | None] = [None]

        def download() -> str:
            try:
                return cls._read_response(request, ssl_context[0])
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
    def _read_response(
        cls,
        request: Request,
        context: ssl.SSLContext | None = None
    ) -> str:
        """Executes one HTTP request and decodes its response body."""
        with urlopen(
            request,
            timeout=cls._REQUEST_TIMEOUT,
            context=context
        ) as response:
            charset = response.headers.get_content_charset() or 'utf-8'
            return response.read().decode(charset, errors='replace')

    @staticmethod
    def _document(html: str) -> HtmlNode:
        """Parses HTML into the shared dependency-free document tree."""
        return parse_html(html)

    @staticmethod
    def _request_url(url: str) -> str:
        """Percent-encodes provider URLs that contain Polish stop names."""
        parsed = urlparse(url)
        return urlunparse(parsed._replace(
            path=quote(parsed.path, safe='/%:@'),
            query=quote(parsed.query, safe='=&%:+,')
        ))

    @classmethod
    def enrich_stop_locations(
        cls,
        stops: list[PublicTransportStop]
    ) -> list[PublicTransportStop]:
        """Adds representative OpenStreetMap coordinates to cached stops."""
        return cls._apply_stop_locations(
            stops,
            cls._safe_stop_locations()
        )

    @classmethod
    def download_stop_locations(
        cls,
        refresh: bool = False,
        current: int = 1,
        total: int = 1
    ) -> dict[str, tuple[float, float]]:
        """Downloads and indexes public transport stop coordinates from OSM."""
        with cls._STOP_LOCATIONS_LOCK:
            if cls._STOP_LOCATIONS_CACHE is not None and not refresh:
                return dict(cls._STOP_LOCATIONS_CACHE)
            PublicTransportDownloadProgress.report(
                'Lokalizacje przystanków',
                current,
                total
            )
            locations = cls.parse_stop_locations(
                OverpassDownloader.download_query(
                    cls._stop_locations_query(),
                    lambda attempt, attempts: (
                        PublicTransportDownloadProgress.report(
                            'Lokalizacje przystanków',
                            current,
                            total,
                            attempt=attempt,
                            max_attempts=attempts
                        )
                    )
                )
            )
            cls._STOP_LOCATIONS_CACHE = locations
            return dict(locations)

    @classmethod
    def parse_stop_locations(
        cls,
        data: dict[str, Any]
    ) -> dict[str, tuple[float, float]]:
        """Converts named Overpass elements to representative stop points."""
        grouped: dict[str, list[tuple[float, float]]] = {}
        elements = data.get('elements', [])
        if not isinstance(elements, list):
            return {}
        for element in elements:
            if not isinstance(element, dict):
                continue
            tags = element.get('tags', {})
            if not isinstance(tags, dict):
                continue
            name = next((
                str(tags.get(field) or '').strip()
                for field in ('name', 'name:pl', 'official_name', 'local_name')
                if str(tags.get(field) or '').strip()
            ), '')
            point = element.get('center', {})
            latitude = element.get('lat', point.get('lat') if isinstance(point, dict) else None)
            longitude = element.get('lon', point.get('lon') if isinstance(point, dict) else None)
            try:
                coordinates = (float(latitude), float(longitude))
            except (TypeError, ValueError):
                continue
            key = cls._normalize_stop_name(name)
            if key:
                grouped.setdefault(key, []).append(coordinates)
        return {
            key: (
                sum(point[0] for point in points) / len(points),
                sum(point[1] for point in points) / len(points)
            )
            for key, points in grouped.items()
        }

    @classmethod
    def _safe_stop_locations(
        cls,
        refresh: bool = False,
        current: int = 1,
        total: int = 1
    ) -> dict[str, tuple[float, float]]:
        """Returns stop coordinates without failing the timetable download."""
        try:
            return cls.download_stop_locations(
                refresh=refresh,
                current=current,
                total=total
            )
        except Exception:
            return {}

    @classmethod
    def _apply_stop_locations(
        cls,
        stops: list[PublicTransportStop],
        locations: dict[str, tuple[float, float]]
    ) -> list[PublicTransportStop]:
        """Applies one representative coordinate to every stop platform."""
        for stop in stops:
            coordinates = cls._find_stop_location(stop.name, locations)
            if not coordinates:
                continue
            for platform in stop.platforms:
                platform.latitude, platform.longitude = coordinates
        return stops

    @classmethod
    def _find_stop_location(
        cls,
        name: str,
        locations: dict[str, tuple[float, float]]
    ) -> tuple[float, float] | None:
        """Finds coordinates using the provider-independent stop name."""
        return locations.get(cls._normalize_stop_name(name))

    @staticmethod
    def _normalize_stop_name(name: str) -> str:
        """Normalizes accents, punctuation and platform suffixes for matching."""
        value = re.sub(
            r'\s*(?:\(\s*\d+[A-Za-z]?\s*\)|'
            r'(?:stanowisko|peron)\s*\d+[A-Za-z]?|'
            r'\d{1,2}[A-Za-z]?)\s*$',
            '',
            name,
            flags=re.IGNORECASE
        )
        value = ''.join(
            character for character in unicodedata.normalize('NFKD', value)
            if not unicodedata.combining(character)
        ).casefold()
        return ' '.join(re.findall(r'[a-z0-9]+', value))

    @classmethod
    def _stop_locations_query(cls) -> str:
        """Builds one bounded Overpass query for all local stop objects."""
        bbox = cls._STOP_AREA_BBOX
        return '\n'.join((
            '[out:json][timeout:30];',
            '(',
            f'  node["highway"="bus_stop"]({bbox});',
            f'  node["public_transport"="platform"]({bbox});',
            f'  node["public_transport"="stop_position"]({bbox});',
            f'  way["public_transport"="platform"]({bbox});',
            f'  relation["public_transport"="stop_area"]({bbox});',
            ');',
            'out center tags;'
        ))

    #endregion HTTP

    #region Shared parsing

    @classmethod
    def _absolute_url(cls, url: str, source_url: str | None = None) -> str:
        """Converts a provider-relative URL to an absolute URL."""
        return urljoin(source_url or cls.BASE_URL, url)

    @staticmethod
    def _query(url: str) -> dict[str, list[str]]:
        """Returns decoded URL query parameters."""
        return parse_qs(urlparse(url).query, keep_blank_values=True)

    @classmethod
    def _query_value(cls, url: str, field: str) -> str:
        """Returns the first decoded query value for a field."""
        values = cls._query(url).get(field, [])
        return values[0] if values else ''

    @classmethod
    def _replace_query(cls, source_url: str, **values: str) -> str:
        """Returns a URL with selected query values replaced."""
        parsed = urlparse(source_url)
        query = cls._query(source_url)
        for key, value in values.items():
            if value:
                query[key] = [value]
            else:
                query.pop(key, None)
        return urlunparse(parsed._replace(query=urlencode(query, doseq=True)))

    @classmethod
    def _line_from_url(cls, url: str) -> str:
        """Extracts a line identifier from a provider URL."""
        return cls._query_value(url, 'linia').strip().upper()

    @classmethod
    def _type_from_line(cls, line: str) -> PublicTransportType:
        """Maps the fixed Częstochowa tram line range to a transport type."""
        return (
            PublicTransportType.TRAM
            if line in {'1', '2', '3'}
            else PublicTransportType.BUS
        )

    @classmethod
    def _date(cls, value: str) -> date | None:
        """Parses an ISO or Polish date embedded in provider markup."""
        match = cls._DATE_PATTERN.search(value or '')
        if match:
            try:
                return date(
                    int(match.group(1)),
                    int(match.group(2)),
                    int(match.group(3))
                )
            except ValueError:
                return None
        polish_match = re.search(
            r'(\d{1,2})\.(\d{1,2})\.(20\d{2})',
            value or ''
        )
        if polish_match:
            try:
                return date(
                    int(polish_match.group(3)),
                    int(polish_match.group(2)),
                    int(polish_match.group(1))
                )
            except ValueError:
                return None
        return None

    @staticmethod
    def _clock(value: str) -> time | None:
        """Parses the first HH:MM clock value."""
        match = re.search(r'(\d{1,2}):(\d{2})', value or '')
        if not match:
            return None
        try:
            return time(int(match.group(1)), int(match.group(2)))
        except ValueError:
            return None

    @classmethod
    def _dates(
        cls,
        document: HtmlNode,
        source_url: str
    ) -> dict[date, str]:
        """Extracts the provider date select as typed URL mappings."""
        select = next((
            node for node in document.find_all('select')
            if node.attrs.get('name') == 'data'
        ), None)
        if not select:
            return {}
        result: dict[date, str] = {}
        for option in select.find_all('option'):
            raw_date = option.attrs.get('value', '')
            parsed_date = cls._date(raw_date)
            if parsed_date:
                result[parsed_date] = cls._replace_query(
                    source_url,
                    data=raw_date
                )
        return result

    @classmethod
    def _selected_date(
        cls,
        document: HtmlNode,
        source_url: str
    ) -> date | None:
        """Returns the currently selected timetable date."""
        query_date = cls._date(cls._query_value(source_url, 'data'))
        if query_date:
            return query_date
        select = next((
            node for node in document.find_all('select')
            if node.attrs.get('name') == 'data'
        ), None)
        if not select:
            return None
        selected = next((
            option for option in select.find_all('option')
            if 'selected' in option.attrs
        ), None)
        return cls._date(
            selected.attrs.get('value', '') if selected else select.text()
        )

    @classmethod
    def _stop_name_from_url(cls, url: str) -> str:
        """Extracts a readable stop name from the provider query."""
        value = cls._query_value(url, 'przystanek')
        name = value.split('-', 1)[1] if '-' in value else value
        return name.replace('-', ' ').strip()

    @classmethod
    def _direction_from_url(cls, url: str) -> str:
        """Extracts a readable direction name from the provider query."""
        value = cls._query_value(url, 'kierunek')
        name = value.split('-', 1)[1] if '-' in value else value
        return name.replace('-', ' ').strip()

    @classmethod
    def _base_line(
        cls,
        line: str,
        url: str,
        updated: bool = False
    ) -> PublicTransportBaseLine:
        """Builds a typed base line with provider defaults."""
        return PublicTransportBaseLine(
            line=line,
            type=cls._type_from_line(line),
            url=url,
            free_of_charge=False,
            updated=updated
        )

    @classmethod
    def _city(cls) -> PublicTransportCity:
        """Builds the shared city value used by this provider."""
        return PublicTransportCity(
            name=cls.CITY_NAME,
            color=cls.CITY_COLOR
        )

    #endregion Shared parsing

    #region Lines

    @classmethod
    def download_lines(
        cls,
        url: str | None = None,
        refresh: bool = False
    ) -> list[PublicTransportBaseLine]:
        """Downloads the tram and bus line lists."""
        del refresh
        source_url = url or cls.TIMETABLE_URL
        return cls.parse_lines(
            cls._download_html(source_url, 'Lista linii'),
            source_url
        )

    @classmethod
    def parse_lines(
        cls,
        html: str,
        source_url: str | None = None
    ) -> list[PublicTransportBaseLine]:
        """Parses line tiles from the provider timetable home page."""
        source_url = source_url or cls.TIMETABLE_URL
        document = cls._document(html)
        result: list[PublicTransportBaseLine] = []
        for class_name in ('tram-routes', 'bus-routes'):
            for group in document.find_all('div', class_name):
                for anchor in group.find_all('a', 'route'):
                    line = anchor.text()
                    href = anchor.attrs.get('href', '')
                    if not line or not href:
                        continue
                    result.append(cls._base_line(
                        line,
                        cls._absolute_url(href, source_url),
                        anchor.has_class('detour')
                    ))
        return list({
            (line.line, line.type): line
            for line in result
        }.values())

    @classmethod
    def download_line(
        cls,
        url: str,
        include_announcement_content: bool = False
    ) -> PublicTransportLine:
        """Downloads directions, stops, dates and related announcements."""
        line = cls._line_from_url(url)
        html = cls._download_html(url, f'Linia {line}')
        model = cls.parse_line(html, url)
        route_options = cls._route_options(cls._document(html), url)
        model.route_variants = dict(route_options)
        return model

    @classmethod
    def _route_options(
        cls,
        document: HtmlNode,
        source_url: str
    ) -> list[tuple[str, str]]:
        """Returns explicit route variants and their URLs."""
        select = next((
            node for node in document.find_all('select')
            if node.attrs.get('name') == 'trasa'
        ), None)
        if not select:
            return []
        return [
            (
                option.text(),
                cls._replace_query(
                    source_url,
                    trasa=option.attrs.get('value', '')
                )
            )
            for option in select.find_all('option')
            if option.attrs.get('value', '') and option.text()
        ]

    @classmethod
    def parse_line(cls, html: str, source_url: str) -> PublicTransportLine:
        """Parses one line page into the shared detailed line model."""
        document = cls._document(html)
        line = cls._line_from_url(source_url)
        transport_type = cls._type_from_line(line)
        directions: list[PublicTransportDirection] = []
        for table in document.find_all('table', 'schedule'):
            heading = table.find('th')
            if not heading or 'kierunek:' not in heading.text().casefold():
                continue
            direction_name = heading.text().split(':', 1)[-1].strip()
            stops: list[PublicTransportDirectionStop] = []
            for anchor in table.find_all('a', 'bus-stop'):
                href = anchor.attrs.get('href', '')
                if (
                    not href
                    or not cls._query_value(href, 'przystanek')
                    or cls._line_from_url(href) != line
                ):
                    continue
                stops.append(PublicTransportDirectionStop(
                    line=line,
                    type=transport_type,
                    city=cls._city(),
                    is_variant=False,
                    name=anchor.text(),
                    platform='',
                    url=cls._absolute_url(href, source_url)
                ))
            if stops:
                directions.append(PublicTransportDirection(
                    name=direction_name,
                    cities=[cls._city()],
                    stops=stops
                ))
        return PublicTransportLine(
            line=line,
            type=transport_type,
            announcements=[],
            directions=directions,
            route_variants={},
            dates=cls._dates(document, source_url)
        )

    #endregion Lines

    #region Announcements

    @classmethod
    def download_announcements(
        cls,
        line: str = '',
        include_content: bool = False
    ) -> list[PublicTransportAnnouncement]:
        """Downloads announcement summaries, optionally filtered by line."""
        announcements = cls.parse_announcements(
            cls._download_html(cls.TIMETABLE_URL, 'Lista komunikatów'),
            cls.TIMETABLE_URL,
            line
        )
        if not include_content:
            return announcements
        result: list[PublicTransportAnnouncement] = []
        total = len(announcements)
        for index, item in enumerate(announcements, start=1):
            if not item.url:
                result.append(item)
                continue
            try:
                downloaded = cls.download_announcement(
                    item.url,
                    item.description,
                    index,
                    total
                )
                downloaded.lines = list(item.lines)
                result.append(downloaded)
            except Exception:
                result.append(item)
        return result

    @classmethod
    def parse_announcements(
        cls,
        html: str,
        source_url: str | None = None,
        line: str = ''
    ) -> list[PublicTransportAnnouncement]:
        """Parses the provider announcement table."""
        source_url = source_url or cls.TIMETABLE_URL
        document = cls._document(html)
        table = document.find('table', 'table-news')
        if not table:
            return []
        result: list[PublicTransportAnnouncement] = []
        for row in table.find_all('tr'):
            cells = row.find_all('td')
            if len(cells) < 3:
                continue
            affected_lines = list(dict.fromkeys(
                re.findall(r'[A-Za-z]?\d+', cells[1].text())
            ))
            if line and line not in affected_lines:
                continue
            anchor = cells[2].find('a')
            if not anchor:
                continue
            published_date = cls._date(cells[0].text())
            result.append(PublicTransportAnnouncement(
                lines=affected_lines,
                city=cls.CITY_NAME,
                content='',
                description=anchor.text(),
                effective_date_from=None,
                effective_date_to=None,
                last_updated_datetime=(
                    datetime.combine(published_date, time())
                    if published_date else None
                ),
                url=cls._absolute_url(
                    anchor.attrs.get('href', ''),
                    source_url
                )
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
        """Downloads one complete announcement."""
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
        """Parses the title, publication date and plaintext announcement."""
        document = cls._document(html)
        wrapper = document.find('div', 'right-news') or document
        heading = wrapper.find('h3')
        published = wrapper.find(class_name='news-date')
        published_date = cls._date(published.text() if published else '')
        body = wrapper.find('div', 'text-element')
        return PublicTransportAnnouncement(
            lines=[],
            city=cls.CITY_NAME,
            content=body.text() if body else '',
            description=heading.text() if heading else '',
            effective_date_from=None,
            effective_date_to=None,
            last_updated_datetime=(
                datetime.combine(published_date, time())
                if published_date else None
            ),
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
        """Downloads departures for one line, stop, route and date."""
        return cls.parse_line_stop_timetable(
            cls._download_html(
                url,
                f'Odjazdy z „{cls._stop_name_from_url(url)}”'
            ),
            url,
            cls._safe_stop_locations()
        )

    @classmethod
    def parse_line_stop_timetable(
        cls,
        html: str,
        source_url: str,
        stop_locations: dict[str, tuple[float, float]] | None = None
    ) -> PublicTransportLineStopTimetable:
        """Parses one stop timetable and ride endpoint references."""
        document = cls._document(html)
        line = cls._line_from_url(source_url)
        current_date = cls._selected_date(document, source_url)
        direction_name = cls._direction_from_url(source_url)
        route_header = document.find('div', 'route-header')
        if route_header:
            match = re.search(
                r'kierunek:\s*(.+?)(?:\s+MAPA|\s+DRUK|\s+PDF|$)',
                route_header.text(),
                re.IGNORECASE
            )
            if match:
                direction_name = match.group(1).strip()
        departures: list[PublicTransportDepartureTime] = []
        selected_route = cls._query_value(source_url, 'trasa')
        for minute in document.find_all('span', 'minute'):
            trip = minute.attrs.get('data-trip', '')
            raw_time = minute.attrs.get('data-time', '')
            if not trip or not raw_time:
                continue
            route = minute.attrs.get('data-route', '')
            ride_query = {
                't': trip,
                'ft': raw_time,
                'dt': current_date.isoformat() if current_date else '',
                'linia': line,
                'przystanek': cls._query_value(source_url, 'przystanek')
            }
            variant = (
                f'Trasa {route}'
                if route and selected_route and route != selected_route
                else ''
            )
            departures.append(PublicTransportDepartureTime(
                departure_time=cls._clock(raw_time),
                is_high_floor=False,
                url=f'{cls.TRIP_URL}?{urlencode(ride_query)}',
                variant=variant
            ))
        variants = list(dict.fromkeys(
            departure.variant for departure in departures
            if departure.variant
        ))
        day = PublicTransportDateTimetable(
            date=current_date,
            direction_name=direction_name,
            effective_date_from=None,
            effective_date_to=None,
            departures=departures,
            variants=variants
        )
        timetable = {current_date: day} if current_date else {}
        stop_name = cls._stop_name_from_url(source_url)
        coordinates = cls._find_stop_location(
            stop_name,
            stop_locations or {}
        )
        return PublicTransportLineStopTimetable(
            line=line,
            type=cls._type_from_line(line),
            announcements=[],
            stop_name=stop_name,
            direction_name=direction_name,
            platform='',
            timetable=timetable,
            dates=cls._dates(document, source_url),
            latitude=coordinates[0] if coordinates else None,
            longitude=coordinates[1] if coordinates else None
        )

    #endregion Stop timetable

    #region Rides

    @classmethod
    def download_ride(
        cls,
        url: str,
        from_first_stop: bool = True
    ) -> PublicTransportRide:
        """Downloads a complete trip through the provider JSON endpoint."""
        data = cls._download_json(url, 'Szczegóły przejazdu')
        html = str(data.get('html') or '') if data.get('success') else ''
        return cls.parse_ride(html, url, cls._safe_stop_locations())

    @classmethod
    def parse_ride(
        cls,
        html: str,
        source_url: str,
        stop_locations: dict[str, tuple[float, float]] | None = None
    ) -> PublicTransportRide:
        """Parses the trip overlay into ordered stop and travel-time values."""
        document = cls._document(html)
        query = cls._query(source_url)
        line = (query.get('linia') or [''])[0]
        rows: list[PublicTransportRideStop] = []
        previous_sum = 0
        for row in document.find_all('tr'):
            cells = row.find_all('td')
            if len(cells) < 3:
                continue
            cumulative_text = cells[0].text()
            cumulative = (
                int(cumulative_text)
                if cumulative_text.isdigit()
                else 0
            )
            stop_name = cells[2].text()
            coordinates = cls._find_stop_location(
                stop_name,
                stop_locations or {}
            )
            rows.append(PublicTransportRideStop(
                stop=stop_name,
                departure_time=cls._clock(cells[1].text()),
                travel_time=max(0, cumulative - previous_sum),
                travel_time_sum=cumulative,
                distance=0.0,
                distance_sum=0.0,
                city=cls._city(),
                latitude=coordinates[0] if coordinates else None,
                longitude=coordinates[1] if coordinates else None
            ))
            previous_sum = cumulative
        first = rows[0] if rows else None
        return PublicTransportRide(
            line=line,
            type=cls._type_from_line(line),
            stop_name=first.stop if first else cls._stop_name_from_url(source_url),
            platform='',
            departure_time=first.departure_time if first else cls._clock(
                (query.get('ft') or [''])[0]
            ),
            cities=[cls._city()],
            next_stops=rows[1:] if rows else [],
            carrier=cls.CARRIER,
            vehicle_type='',
            latitude=first.latitude if first else None,
            longitude=first.longitude if first else None
        )

    #endregion Rides

    #region Stops

    @classmethod
    def download_stops(
        cls,
        url: str | None = None,
        progress_callback: Callable[[int, int, str], None] | None = None,
        refresh: bool = False
    ) -> list[PublicTransportStop]:
        """Downloads the provider's single-page stop index."""
        del refresh
        source_url = url or cls.STOPS_URL
        if progress_callback:
            progress_callback(1, 1, cls.CITY_NAME)
        stops = cls.parse_stops(
            cls._download_html(source_url, 'Lista przystanków', 1, 2),
            source_url
        )
        return cls._apply_stop_locations(
            stops,
            cls._safe_stop_locations(refresh=True, current=2, total=2)
        )

    @classmethod
    def parse_stops(
        cls,
        html: str,
        source_url: str | None = None
    ) -> list[PublicTransportStop]:
        """Parses stops as lazy, provider-wide platform entries."""
        source_url = source_url or cls.STOPS_URL
        document = cls._document(html)
        city = cls._city()
        result: list[PublicTransportStop] = []
        seen: set[str] = set()
        for anchor in document.find_all('a', 'bus-stop'):
            href = anchor.attrs.get('href', '')
            if (
                cls._query_value(href, 'lista') != 'przystankow'
                or not cls._query_value(href, 'przystanek')
            ):
                continue
            absolute_url = cls._absolute_url(href, source_url)
            if absolute_url in seen:
                continue
            seen.add(absolute_url)
            result.append(PublicTransportStop(
                name=anchor.text(),
                city=city,
                platforms=[PublicTransportStopPlatform(
                    name='Wszystkie',
                    lines=[],
                    url_all=absolute_url,
                    url_chrono='',
                    latitude=None,
                    longitude=None
                )]
            ))
        return result

    @classmethod
    def download_stop_all(cls, url: str) -> PublicTransportStopAll:
        """Downloads the route list for one stop without following timetable links."""
        html = cls._download_html(
            url,
            f'Linie przystanku „{cls._stop_name_from_url(url)}”'
        )
        return cls.parse_stop_all(html, url, cls._safe_stop_locations())

    @classmethod
    def parse_stop_all(
        cls,
        html: str,
        source_url: str,
        stop_locations: dict[str, tuple[float, float]] | None = None
    ) -> PublicTransportStopAll:
        """Parses stop routes without downloading their departure pages."""
        document = cls._document(html)
        entries: dict[
            PublicTransportBaseLine,
            PublicTransportDateTimetable
        ] = {}
        for table in document.find_all('table', 'schedule'):
            heading = table.find('th')
            if not heading or 'linie odjeżdżające' in heading.text().casefold():
                continue
            for anchor in table.find_all('a', 'bus-stop'):
                href = anchor.attrs.get('href', '')
                line = cls._line_from_url(href)
                if not line or not cls._query_value(href, 'przystanek'):
                    continue
                detail_url = cls._absolute_url(href, source_url)
                route = cls._query_value(detail_url, 'trasa')
                line_url = cls._replace_query(
                    cls.TIMETABLE_URL,
                    linia=line,
                    trasa=route
                )
                description = anchor.text()
                direction_name = re.sub(
                    rf'^{re.escape(line)}\s*-\s*',
                    '',
                    description
                ).strip()
                entries[cls._base_line(line, line_url)] = (
                    PublicTransportDateTimetable(
                        date=None,
                        direction_name=direction_name,
                        effective_date_from=None,
                        effective_date_to=None,
                        departures=[],
                        variants=[]
                    )
                )
        stop_name = cls._stop_name_from_url(source_url)
        coordinates = cls._find_stop_location(
            stop_name,
            stop_locations or {}
        )
        return PublicTransportStopAll(
            stop_name=stop_name,
            platform='Wszystkie',
            dates={},
            lines=entries,
            latitude=coordinates[0] if coordinates else None,
            longitude=coordinates[1] if coordinates else None
        )

    #endregion Stops

    #region Container

    @classmethod
    def download_container(
        cls,
        include_line_details: bool = False,
        include_stops: bool = False,
        progress_callback: Callable[[int, int, str], None] | None = None
    ) -> PublicTransportDataContainer:
        """Downloads a selectable provider snapshot into one typed container."""
        base_lines = cls.download_lines()
        lines = (
            [cls.download_line(line.url) for line in base_lines]
            if include_line_details else []
        )
        stops = cls.download_stops(
            progress_callback=progress_callback
        ) if include_stops else []
        return PublicTransportDataContainer(
            carrier=cls.CARRIER,
            base_url=cls.BASE_URL,
            base_lines=base_lines,
            lines=lines,
            line_stop_timetables=[],
            rides=[],
            stops=stops,
            stop_all=[]
        )

    #endregion Container

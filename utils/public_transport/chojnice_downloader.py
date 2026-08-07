from __future__ import annotations

from datetime import date, time, timedelta
import html as html_lib
import re
import ssl
from threading import Lock
from typing import ClassVar
from urllib.error import URLError
from urllib.parse import parse_qs, urlencode, urlparse
from urllib.request import Request, urlopen

from models.public_transport.public_transport_announcement import PublicTransportAnnouncement
from models.public_transport.public_transport_base_line import PublicTransportBaseLine
from models.public_transport.public_transport_city import PublicTransportCity
from models.public_transport.public_transport_date_timetable import PublicTransportDateTimetable
from models.public_transport.public_transport_departure_time import PublicTransportDepartureTime
from models.public_transport.public_transport_direction import PublicTransportDirection
from models.public_transport.public_transport_direction_stop import PublicTransportDirectionStop
from models.public_transport.public_transport_line import PublicTransportLine
from models.public_transport.public_transport_line_stop_timetable import PublicTransportLineStopTimetable
from models.public_transport.public_transport_stop import PublicTransportStop
from models.public_transport.public_transport_stop_all import PublicTransportStopAll
from models.public_transport.public_transport_stop_platform import PublicTransportStopPlatform
from resources.public_transport.public_transport_type import PublicTransportType
from utils.public_transport.download_progress import PublicTransportDownloadProgress


# Day-type index → weekday range used for date labels.
_WORKDAY = 0   # Monday–Friday (weekday 0–4)
_SATURDAY = 1  # Saturday (weekday 5)
_SUNDAY = 2    # Sunday / holiday (weekday 6)

_SECTION_LABELS = ['Dni robocze', 'Soboty', 'Niedziele i święta']


def _day_type(weekday: int) -> int:
    if weekday < 5:
        return _WORKDAY
    return _SATURDAY if weekday == 5 else _SUNDAY


def _strip_tags(fragment: str) -> str:
    return html_lib.unescape(re.sub(r'<[^>]+>', '', fragment)).strip()


class ChojniceDownloader:
    """Downloads MZK Chojnice timetables from mzkchojnice.pl via rozklad.com."""

    BASE_URL: ClassVar[str] = 'https://www.mzkchojnice.pl/'
    ROZKLAD_INDEX: ClassVar[str] = 'https://rozklad.com/maps/index.php'
    ROZKLAD_TIMETABLE: ClassVar[str] = 'https://rozklad.com/maps/r7xp.php'
    CLIENT_ID: ClassVar[str] = 'CHOJNICE_MZK'
    URL_PREFIXES: ClassVar[tuple[str, ...]] = (BASE_URL, 'https://rozklad.com/')
    CARRIER: ClassVar[str] = 'MZK Chojnice'
    CITY_NAME: ClassVar[str] = 'Chojnice'
    CITY_COLOR: ClassVar[str] = '#006A8E'
    _USER_AGENT: ClassVar[str] = 'TravelManager/1.0'
    _REQUEST_TIMEOUT: ClassVar[int] = 15
    _LINES_LOCK: ClassVar[Lock] = Lock()
    _LINES_CACHE: ClassVar[list[dict] | None] = None

    # ------------------------------------------------------------------ HTTP

    @classmethod
    def _fetch(cls, url: str, item: str = 'Dane MZK Chojnice') -> str:
        request = Request(url, headers={
            'User-Agent': cls._USER_AGENT,
            'Referer': cls.BASE_URL
        })
        ssl_ctx: list[ssl.SSLContext | None] = [None]

        def execute() -> str:
            try:
                with urlopen(request, timeout=cls._REQUEST_TIMEOUT, context=ssl_ctx[0]) as r:
                    return r.read().decode('utf-8', errors='replace')
            except URLError as error:
                if ssl_ctx[0] is None and isinstance(error.reason, ssl.SSLCertVerificationError):
                    ssl_ctx[0] = ssl._create_unverified_context()
                raise

        return PublicTransportDownloadProgress.retry(execute, item, 1, 1)

    # ------------------------------------------------------------ Line list

    @classmethod
    def _lines(cls, refresh: bool = False) -> list[dict]:
        """Returns [{id, display, url}] for each line, cached in memory."""
        with cls._LINES_LOCK:
            if cls._LINES_CACHE is not None and not refresh:
                return cls._LINES_CACHE
            html = cls._fetch(cls.BASE_URL, 'Lista linii MZK Chojnice')
            entries = re.findall(
                r'href=["\']https?://rozklad\.com/maps/index\.php'
                r'\?IDKlienta=CHOJNICE_MZK&IDLinii=([^"\'&#\s]+)[^"\']*["\']'
                r'\s*[^>]*>\s*([^<]+)\s*</a>',
                html
            )
            seen: set[str] = set()
            result = []
            for lid, display in entries:
                if lid not in seen:
                    seen.add(lid)
                    result.append({
                        'id': lid,
                        'display': display.strip(),
                        'url': (
                            f'{cls.ROZKLAD_INDEX}'
                            f'?IDKlienta={cls.CLIENT_ID}&IDLinii={lid}'
                        )
                    })
            cls._LINES_CACHE = result
            return result

    @staticmethod
    def _query(url: str) -> dict[str, str]:
        return {k: v[0] for k, v in parse_qs(urlparse(url).query).items() if v}

    @staticmethod
    def _city() -> PublicTransportCity:
        return PublicTransportCity(ChojniceDownloader.CITY_NAME, ChojniceDownloader.CITY_COLOR)

    # -------------------------------------------------- Parse line details

    @classmethod
    def _parse_directions(cls, html: str, line_id: str) -> list[dict]:
        """Extracts directions with stop lists from the rozklad.com index page."""
        # Each direction block: button contains "Kierunek: NAME", followed by
        # an accordion div with <ol> of stop <a> elements.
        block_pattern = re.compile(
            r'Kierunek:\s*([^\n<]+)'          # direction name (plain text)
            r'.*?'
            r'<ol[^>]*list-group[^>]*>(.*?)</ol>',
            re.DOTALL
        )
        stop_pattern = re.compile(
            r'<a\s+id=["\']([^"\']+)["\'][^>]+'
            r'title=["\']Poka[żz]\s+rozk[łl]ad\s+z\s+przystanku:\s*([^"\']+)["\']'
        )
        directions = []
        for m in block_pattern.finditer(html):
            direction_name = html_lib.unescape(m.group(1).strip())
            stops_html = m.group(2)
            stops = []
            for sm in stop_pattern.finditer(stops_html):
                stop_id = sm.group(1).strip()
                stop_name = html_lib.unescape(sm.group(2).strip())
                stops.append({'id': stop_id, 'name': stop_name})
            if stops:
                directions.append({'name': direction_name, 'stops': stops})
        return directions

    # --------------------------------------------------- Timetable parsing

    @classmethod
    def _parse_timetable_html(cls, html: str) -> tuple[str, str, date | None, list[dict]]:
        """Returns (stop_name, direction_name, valid_from, [{day_type, departures}])."""
        stop_m = re.search(r'Przystanek:\s*</span>\s*<[^>]+>([^<]+)<', html)
        dir_m = re.search(r'Kierunek:\s*<[^>]+>([^<]+)<', html)
        date_m = re.search(r'Ważny od:\s*([\d.]+)', html)
        stop_name = html_lib.unescape(stop_m.group(1).strip()) if stop_m else ''
        direction_name = html_lib.unescape(dir_m.group(1).strip()) if dir_m else ''
        valid_from: date | None = None
        if date_m:
            try:
                parts = date_m.group(1).split('.')
                valid_from = date(int(parts[2]), int(parts[1]), int(parts[0]))
            except (ValueError, IndexError):
                pass

        # Three day sections keyed by collapse-1/2/3
        sections = []
        for day_type in range(3):
            collapse_id = f'id="collapse-{day_type + 1}"'
            start = html.find(collapse_id)
            if start < 0:
                sections.append({'day_type': day_type, 'departures': []})
                continue
            next_collapse = html.find('id="collapse-', start + len(collapse_id))
            section_html = html[start: next_collapse if next_collapse > 0 else start + 6000]
            hours = re.findall(r'class="godz [^"]+">(\d+)<', section_html)
            mins = re.findall(r'class\s*=\s*"min"><span[^>]*>(\d+)', section_html)
            departures: list[time] = []
            for h, m in zip(hours, mins):
                try:
                    departures.append(time(int(h) % 24, int(m)))
                except ValueError:
                    continue
            sections.append({'day_type': day_type, 'departures': departures})

        return stop_name, direction_name, valid_from, sections

    # ------------------------------------------------------- Date helpers

    @classmethod
    def _dates_for_stop(cls, url: str) -> dict[date, str]:
        """Generates 7 upcoming dates each with the matching day-type URL."""
        q = cls._query(url)
        selected_type = int(q.get('day_type', _day_type(date.today().weekday())))
        today = date.today()
        dates: dict[date, str] = {}
        for offset in range(7):
            d = today + timedelta(days=offset)
            dt = _day_type(d.weekday())
            q_new = dict(q, day_type=dt)
            new_url = urlparse(url)._replace(
                query=urlencode(q_new)
            ).geturl()
            dates[d] = new_url
        return dates

    # =================================================================== API

    @classmethod
    def download_lines(cls, url: str | None = None, refresh: bool = False):
        del url
        lines = cls._lines(refresh)
        return [
            PublicTransportBaseLine(
                line=entry['display'],
                type=PublicTransportType.BUS,
                url=entry['url'],
                free_of_charge=False,
                updated=False
            )
            for entry in lines
        ]

    @classmethod
    def download_line(cls, url: str, include_announcement_content: bool = False):
        del include_announcement_content
        q = cls._query(url)
        line_id = q.get('IDLinii', '')
        display = next(
            (e['display'] for e in cls._lines() if e['id'] == line_id),
            line_id.lstrip('_')
        )
        html = cls._fetch(url, f'Linia {display} – Chojnice')
        raw_directions = cls._parse_directions(html, line_id)

        directions = []
        for dir_data in raw_directions:
            stops = []
            for stop in dir_data['stops']:
                stop_url = (
                    f'{cls.ROZKLAD_TIMETABLE}'
                    f'?IDKlienta={cls.CLIENT_ID}&cmd=rozID'
                    f'&ID={stop["id"]}&IDLinii={line_id}'
                    f'&day_type={_day_type(date.today().weekday())}'
                )
                stops.append(PublicTransportDirectionStop(
                    line=display,
                    type=PublicTransportType.BUS,
                    city=cls._city(),
                    is_variant=False,
                    name=stop['name'],
                    platform='',
                    url=stop_url
                ))
            directions.append(PublicTransportDirection(
                name=dir_data['name'],
                cities=[cls._city()],
                stops=stops,
                route=[]
            ))

        return PublicTransportLine(
            line=display,
            type=PublicTransportType.BUS,
            announcements=[],
            directions=directions,
            route_variants={},
            dates={}
        )

    @classmethod
    def download_line_stop_timetable(
        cls, url: str, include_announcement_content: bool = False
    ):
        del include_announcement_content
        q = cls._query(url)
        line_id = q.get('IDLinii', '')
        stop_id = q.get('ID', '')
        day_type = int(q.get('day_type', _day_type(date.today().weekday())))
        display = next(
            (e['display'] for e in cls._lines() if e['id'] == line_id),
            line_id.lstrip('_')
        )
        # Fetch without day_type param (not part of remote URL)
        remote_url = (
            f'{cls.ROZKLAD_TIMETABLE}'
            f'?IDKlienta={cls.CLIENT_ID}&cmd=rozID'
            f'&ID={stop_id}&IDLinii={line_id}'
        )
        html = cls._fetch(remote_url, f'Rozkład przystanku {stop_id} linii {display}')
        stop_name, direction_name, valid_from, sections = cls._parse_timetable_html(html)

        selected_date = date.today()
        # Shift selected_date to match day_type
        for offset in range(7):
            d = date.today() + timedelta(days=offset)
            if _day_type(d.weekday()) == day_type:
                selected_date = d
                break

        timetable: dict[date, PublicTransportDateTimetable] = {}
        dates = cls._dates_for_stop(url)
        for d, d_url in dates.items():
            dt = _day_type(d.weekday())
            section = next((s for s in sections if s['day_type'] == dt), None)
            if section is None:
                continue
            departures = [
                PublicTransportDepartureTime(
                    departure_time=t,
                    is_high_floor=False,
                    url='',
                    variant=''
                )
                for t in section['departures']
            ]
            if d not in timetable:
                timetable[d] = PublicTransportDateTimetable(
                    date=d,
                    direction_name=direction_name,
                    effective_date_from=valid_from,
                    effective_date_to=None,
                    departures=departures,
                    variants=[]
                )

        return PublicTransportLineStopTimetable(
            line=display,
            type=PublicTransportType.BUS,
            announcements=[],
            stop_name=stop_name or stop_id,
            direction_name=direction_name,
            platform='',
            timetable=timetable,
            dates=dates,
            latitude=None,
            longitude=None
        )

    @classmethod
    def download_stops(cls, url: str | None = None, progress_callback=None, refresh: bool = False):
        del url
        lines = cls._lines(refresh)
        seen: dict[str, PublicTransportStop] = {}
        total = len(lines)
        for i, entry in enumerate(lines):
            if progress_callback:
                progress_callback(i, total)
            try:
                html = cls._fetch(entry['url'], f'Przystanki linii {entry["display"]}')
            except Exception:
                continue
            directions = cls._parse_directions(html, entry['id'])
            for dir_data in directions:
                for stop in dir_data['stops']:
                    if stop['id'] not in seen:
                        seen[stop['id']] = PublicTransportStop(
                            name=stop['name'],
                            city=cls._city(),
                            platforms=[PublicTransportStopPlatform(
                                name='',
                                lines=[],
                                url_all='',
                                url_chrono='',
                                latitude=None,
                                longitude=None
                            )]
                        )
        if progress_callback:
            progress_callback(total, total)
        return list(seen.values())

    @classmethod
    def download_stop_all(cls, url: str):
        return PublicTransportStopAll(stop_name='', platforms=[])

    @classmethod
    def download_ride(cls, url: str, from_first_stop: bool = True):
        del url, from_first_stop
        raise NotImplementedError('Przejazd nie jest dostępny dla Chojnic.')

    @classmethod
    def download_announcements(
        cls,
        include_content: bool = False,
        line: str = ''
    ) -> list[PublicTransportAnnouncement]:
        del include_content, line
        return []

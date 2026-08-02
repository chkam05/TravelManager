from __future__ import annotations
from collections import defaultdict
from datetime import date, datetime, time, timedelta, timezone
from pathlib import Path
import re
import ssl
from threading import Lock
from typing import Any, ClassVar
from urllib.error import URLError
from urllib.parse import parse_qs, urlencode, urljoin, urlparse
from urllib.request import Request, urlopen

from config import SETTINGS_DIR
from models.public_transport.public_transport_announcement import PublicTransportAnnouncement
from models.public_transport.public_transport_base_line import PublicTransportBaseLine
from models.public_transport.public_transport_city import PublicTransportCity
from models.public_transport.public_transport_coordinate import PublicTransportCoordinate
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
from utils.public_transport.download_progress import PublicTransportDownloadProgress
from core.gtfs_database import GtfsDatabase
from utils.public_transport.html_document import HtmlNode, parse_html


class KrakowDownloader:
    """Downloads Kraków timetables from official static and realtime GTFS."""

    BASE_URL: ClassVar[str] = 'https://gtfs.ztp.krakow.pl/'
    ANNOUNCEMENTS_URL: ClassVar[str] = 'https://mpk.krakow.pl/komunikaty'
    ANNOUNCEMENT_BASE_URL: ClassVar[str] = 'https://mpk.krakow.pl/'
    CARRIER: ClassVar[str] = 'Komunikacja Miejska w Krakowie'
    CITY_NAME: ClassVar[str] = 'Kraków i aglomeracja'
    CITY_COLOR: ClassVar[str] = '#005CA9'
    URL_PREFIXES: ClassVar[tuple[str, ...]] = (
        BASE_URL,
        ANNOUNCEMENT_BASE_URL
    )
    _USER_AGENT: ClassVar[str] = 'TravelManager/1.0'
    _REQUEST_TIMEOUT: ClassVar[int] = 45
    _DATE_RANGE_DAYS: ClassVar[int] = 14
    _DATABASE_PATH: ClassVar[Path] = (
        Path(SETTINGS_DIR)
        / 'krakow_gtfs.sqlite3'
    )
    _LEGACY_DATABASE_PATH: ClassVar[Path] = (
        Path(SETTINGS_DIR)
        / 'public_transport'
        / 'krakow'
        / 'gtfs.sqlite3'
    )
    _DATABASE_LOCK: ClassVar[Lock] = Lock()
    _FEEDS: ClassVar[dict[str, dict[str, str]]] = {
        'A': {
            'name': 'Autobusy MPK',
            'static': urljoin(BASE_URL, 'GTFS_KRK_A.zip'),
            'vehicles': urljoin(BASE_URL, 'VehiclePositions_A.pb')
        },
        'M': {
            'name': 'Autobusy Mobilis',
            'static': urljoin(BASE_URL, 'GTFS_KRK_M.zip'),
            'vehicles': urljoin(BASE_URL, 'VehiclePositions_M.pb')
        },
        'T': {
            'name': 'Tramwaje',
            'static': urljoin(BASE_URL, 'GTFS_KRK_T.zip'),
            'vehicles': urljoin(BASE_URL, 'VehiclePositions_T.pb')
        }
    }
    _CARRIERS: ClassVar[dict[str, str]] = {
        'A': 'Miejskie Przedsiębiorstwo Komunikacyjne S.A. w Krakowie',
        'M': 'Mobilis Sp. z o.o.',
        'T': 'Miejskie Przedsiębiorstwo Komunikacyjne S.A. w Krakowie'
    }

    #region HTTP and cache

    @classmethod
    def _download_bytes(
        cls,
        url: str,
        item: str,
        current: int = 1,
        total: int = 1
    ) -> bytes:
        """Downloads one binary provider resource with shared retry reporting."""
        request = Request(url, headers={
            'Accept': '*/*',
            'User-Agent': cls._USER_AGENT
        })
        ssl_context: list[ssl.SSLContext | None] = [None]

        def download() -> bytes:
            try:
                return cls._read_response(request, ssl_context[0])
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
    def _download_html(
        cls,
        url: str,
        item: str,
        current: int = 1,
        total: int = 1
    ) -> str:
        """Downloads and decodes one MPK announcement page."""
        payload = cls._download_bytes(url, item, current, total)
        return payload.decode('utf-8', errors='replace')

    @classmethod
    def _read_response(
        cls,
        request: Request,
        context: ssl.SSLContext | None
    ) -> bytes:
        """Executes one HTTPS request."""
        with urlopen(
            request,
            timeout=cls._REQUEST_TIMEOUT,
            context=context
        ) as response:
            return response.read()

    @classmethod
    def _ensure_database(cls, refresh: bool = False) -> Path:
        """Returns the local relational GTFS cache, rebuilding it when needed."""
        with cls._DATABASE_LOCK:
            GtfsDatabase.migrate_cache(
                cls._LEGACY_DATABASE_PATH,
                cls._DATABASE_PATH
            )
            if not refresh and GtfsDatabase.is_valid_cache(
                cls._DATABASE_PATH
            ):
                return cls._DATABASE_PATH
            total = len(cls._FEEDS) * 2
            archives: dict[str, bytes] = {}
            for index, (feed_id, feed) in enumerate(
                cls._FEEDS.items(),
                start=1
            ):
                archives[feed_id] = cls._download_bytes(
                    feed['static'],
                    f"GTFS: {feed['name']}",
                    index,
                    total
                )

            labels = {
                feed_id: feed['name']
                for feed_id, feed in cls._FEEDS.items()
            }
            GtfsDatabase.build(
                cls._DATABASE_PATH,
                archives,
                lambda feed_id, current, count: (
                    PublicTransportDownloadProgress.report(
                        f'Przetwarzanie GTFS: {labels[feed_id]}',
                        len(cls._FEEDS) + current,
                        len(cls._FEEDS) + count
                    )
                )
            )
            return cls._DATABASE_PATH

    @classmethod
    def _connection(cls, refresh: bool = False):
        """Opens the current GTFS cache."""
        return GtfsDatabase.connect(cls._ensure_database(refresh))

    @classmethod
    def has_local_data(cls) -> bool:
        """Returns whether a reusable local GTFS database is available."""
        GtfsDatabase.migrate_cache(cls._LEGACY_DATABASE_PATH, cls._DATABASE_PATH)
        return GtfsDatabase.is_valid_cache(cls._DATABASE_PATH)

    @classmethod
    def enrich_stop_locations(
        cls,
        stops: list[PublicTransportStop]
    ) -> list[PublicTransportStop]:
        """Returns stops unchanged because GTFS already contains coordinates."""
        return stops

    #endregion HTTP and cache

    #region URL and value helpers

    @classmethod
    def _url(cls, view: str, **values: str) -> str:
        """Builds an internal, provider-valid reference to GTFS data."""
        query = {'view': view}
        query.update({
            key: value
            for key, value in values.items()
            if value not in (None, '')
        })
        return f'{cls.BASE_URL}travel-manager?{urlencode(query)}'

    @staticmethod
    def _query(url: str) -> dict[str, str]:
        """Returns single-value query parameters from a provider URL."""
        return {
            key: values[0]
            for key, values in parse_qs(
                urlparse(url).query,
                keep_blank_values=True
            ).items()
            if values
        }

    @classmethod
    def _selected_date(cls, url: str) -> date:
        """Returns the selected service date or today."""
        value = cls._query(url).get('data', '')
        try:
            return date.fromisoformat(value)
        except ValueError:
            return date.today()

    @classmethod
    def _dates(
        cls,
        view: str,
        source_values: dict[str, str]
    ) -> dict[date, str]:
        """Builds selectable GTFS service dates."""
        result: dict[date, str] = {}
        for offset in range(cls._DATE_RANGE_DAYS):
            service_date = date.today() + timedelta(days=offset)
            values = dict(source_values)
            values['data'] = service_date.isoformat()
            result[service_date] = cls._url(view, **values)
        return result

    @staticmethod
    def _type_from_route(
        route_type: int,
        feed_id: str
    ) -> PublicTransportType:
        """Maps standard and extended GTFS route types."""
        if feed_id == 'T' or route_type in {0, 900, 901, 902, 903, 904}:
            return PublicTransportType.TRAM
        if route_type in {11, 800}:
            return PublicTransportType.TROLLEY
        return PublicTransportType.BUS

    @classmethod
    def _city(cls) -> PublicTransportCity:
        """Builds the common city group used by the Kraków feeds."""
        return PublicTransportCity(
            name=cls.CITY_NAME,
            color=cls.CITY_COLOR
        )

    @staticmethod
    def _line_sort_key(line: str) -> tuple[int, int | str]:
        """Sorts numeric line names before special alphanumeric lines."""
        return (0, int(line)) if line.isdigit() else (1, line.casefold())

    @staticmethod
    def _clock(value: str) -> time | None:
        """Converts a GTFS clock, including values after 24:00."""
        match = re.fullmatch(r'(\d{1,2}):(\d{2})(?::\d{2})?', value or '')
        if not match:
            return None
        try:
            return time(int(match.group(1)) % 24, int(match.group(2)))
        except ValueError:
            return None

    @staticmethod
    def _clock_sort_value(value: str) -> int:
        """Returns seconds from the GTFS service-day origin."""
        match = re.fullmatch(r'(\d{1,2}):(\d{2})(?::(\d{2}))?', value or '')
        if not match:
            return 0
        return (
            int(match.group(1)) * 3600
            + int(match.group(2)) * 60
            + int(match.group(3) or 0)
        )

    @staticmethod
    def _platform_name(row) -> str:
        """Returns the best explicit platform code available in GTFS."""
        platform = str(row['platform_code'] or row['description'] or '').strip()
        if platform:
            return platform
        stop_code = str(row['stop_code'] or '').strip()
        if '-' in stop_code:
            return stop_code.rsplit('-', 1)[-1]
        return ''

    @staticmethod
    def _service_ids(connection, feed_id: str, service_date: date) -> list[str]:
        """Returns sorted service identifiers active on a date."""
        return sorted(
            GtfsDatabase.active_service_ids(
                connection,
                feed_id,
                service_date
            )
        )

    #endregion URL and value helpers

    #region Lines

    @classmethod
    def download_lines(
        cls,
        url: str | None = None,
        refresh: bool = False
    ) -> list[PublicTransportBaseLine]:
        """Loads every bus and tram line from the relational GTFS cache."""
        with cls._connection(refresh) as connection:
            rows = connection.execute("""
                SELECT *
                FROM routes
                WHERE short_name <> ''
                ORDER BY short_name
            """).fetchall()
        lines = [
            PublicTransportBaseLine(
                line=str(row['short_name']),
                type=cls._type_from_route(
                    int(row['route_type']),
                    str(row['feed_id'])
                ),
                url=cls._url(
                    'line',
                    feed=str(row['feed_id']),
                    route=str(row['route_id'])
                ),
                free_of_charge=False,
                updated=False
            )
            for row in rows
        ]
        return sorted(lines, key=lambda item: (
            str(item.type),
            cls._line_sort_key(item.line)
        ))

    @classmethod
    def download_line(
        cls,
        url: str,
        include_announcement_content: bool = False
    ) -> PublicTransportLine:
        """Loads directions, stops and route geometry for one GTFS line."""
        values = cls._query(url)
        feed_id = values.get('feed', '')
        route_id = values.get('route', '')
        selected_trip_id = values.get('trip', '')
        service_date = cls._selected_date(url)
        if feed_id not in cls._FEEDS or not route_id:
            raise ValueError('Nieprawidłowy identyfikator linii GTFS.')

        with cls._connection() as connection:
            route = connection.execute(
                """
                    SELECT *
                    FROM routes
                    WHERE feed_id = ? AND route_id = ?
                """,
                (feed_id, route_id)
            ).fetchone()
            if route is None:
                raise ValueError('Nie znaleziono linii w danych GTFS.')
            variants = cls._line_variants(
                connection,
                feed_id,
                route_id,
                service_date
            )
            selected_variants = [
                variant for variant in variants
                if not selected_trip_id
                or str(variant['trip_id']) == selected_trip_id
            ]
            if selected_trip_id and not selected_variants:
                selected = connection.execute(
                    """
                        SELECT trip_id, headsign, direction_id, shape_id
                        FROM trips
                        WHERE feed_id = ? AND trip_id = ?
                    """,
                    (feed_id, selected_trip_id)
                ).fetchone()
                selected_variants = [selected] if selected else []
            directions = [
                cls._direction(
                    connection,
                    route,
                    variant,
                    service_date
                )
                for variant in (selected_variants or variants[:1])
            ]

        line_name = str(route['short_name'])
        route_variants = cls._variant_urls(
            variants,
            feed_id,
            route_id,
            service_date
        )
        model = PublicTransportLine(
            line=line_name,
            type=cls._type_from_route(
                int(route['route_type']),
                feed_id
            ),
            announcements=[],
            directions=directions,
            route_variants=route_variants,
            dates=cls._dates('line', {
                'feed': feed_id,
                'route': route_id,
                'trip': selected_trip_id
            })
        )
        if include_announcement_content:
            model.announcements = cls.download_announcements(
                include_content=True,
                line=line_name
            )
        return model

    @classmethod
    def _line_variants(
        cls,
        connection,
        feed_id: str,
        route_id: str,
        service_date: date
    ) -> list:
        """Returns one representative trip per direction and headsign."""
        service_ids = cls._service_ids(connection, feed_id, service_date)
        parameters: list[Any] = [feed_id, route_id]
        service_filter = ''
        if service_ids:
            service_filter = (
                ' AND service_id IN ('
                + GtfsDatabase.placeholders(service_ids)
                + ')'
            )
            parameters.extend(service_ids)
        rows = connection.execute(
            f"""
                SELECT MIN(trip_id) AS trip_id,
                       headsign,
                       direction_id,
                       shape_id
                FROM trips
                WHERE feed_id = ? AND route_id = ?
                {service_filter}
                GROUP BY headsign, direction_id, shape_id
                ORDER BY direction_id, headsign, shape_id
            """,
            parameters
        ).fetchall()
        if rows or not service_filter:
            return list(rows)
        return list(connection.execute(
            """
                SELECT MIN(trip_id) AS trip_id,
                       headsign,
                       direction_id,
                       shape_id
                FROM trips
                WHERE feed_id = ? AND route_id = ?
                GROUP BY headsign, direction_id, shape_id
                ORDER BY direction_id, headsign, shape_id
            """,
            (feed_id, route_id)
        ).fetchall())

    @classmethod
    def _variant_urls(
        cls,
        variants: list,
        feed_id: str,
        route_id: str,
        service_date: date
    ) -> dict[str, str]:
        """Builds unique labels and URLs for the direction selector."""
        result: dict[str, str] = {}
        for index, variant in enumerate(variants, start=1):
            name = str(variant['headsign'] or '').strip() or f'Wariant {index}'
            label = name
            suffix = 2
            while label in result:
                label = f'{name} ({suffix})'
                suffix += 1
            result[label] = cls._url(
                'line',
                feed=feed_id,
                route=route_id,
                trip=str(variant['trip_id']),
                data=service_date.isoformat()
            )
        return result

    @classmethod
    def _direction(
        cls,
        connection,
        route,
        variant,
        service_date: date
    ) -> PublicTransportDirection:
        """Builds one ordered line direction from a representative GTFS trip."""
        feed_id = str(route['feed_id'])
        route_id = str(route['route_id'])
        trip_id = str(variant['trip_id'])
        transport_type = cls._type_from_route(
            int(route['route_type']),
            feed_id
        )
        rows = connection.execute(
            """
                SELECT s.*, st.stop_sequence
                FROM stop_times st
                JOIN stops s
                  ON s.feed_id = st.feed_id
                 AND s.stop_id = st.stop_id
                WHERE st.feed_id = ? AND st.trip_id = ?
                ORDER BY st.stop_sequence
            """,
            (feed_id, trip_id)
        ).fetchall()
        stops = [
            PublicTransportDirectionStop(
                line=str(route['short_name']),
                type=transport_type,
                city=cls._city(),
                is_variant=False,
                name=str(row['name']),
                platform=cls._platform_name(row),
                url=cls._url(
                    'line-stop',
                    feed=feed_id,
                    route=route_id,
                    trip=trip_id,
                    stop=str(row['stop_id']),
                    data=service_date.isoformat()
                )
            )
            for row in rows
        ]
        shape_id = str(variant['shape_id'] or '')
        shape = connection.execute(
            """
                SELECT latitude, longitude
                FROM shapes
                WHERE feed_id = ? AND shape_id = ?
                ORDER BY point_sequence
            """,
            (feed_id, shape_id)
        ).fetchall() if shape_id else []
        route_points = [
            PublicTransportCoordinate(
                latitude=float(point['latitude']),
                longitude=float(point['longitude'])
            )
            for point in shape
        ]
        if not route_points:
            route_points = [
                PublicTransportCoordinate(
                    latitude=float(row['latitude']),
                    longitude=float(row['longitude'])
                )
                for row in rows
                if row['latitude'] is not None and row['longitude'] is not None
            ]
        direction_name = str(variant['headsign'] or '').strip()
        if not direction_name and stops:
            direction_name = stops[-1].name
        return PublicTransportDirection(
            name=direction_name,
            cities=[cls._city()],
            stops=stops,
            route=route_points
        )

    #endregion Lines

    #region Line stop timetable

    @classmethod
    def download_line_stop_timetable(
        cls,
        url: str,
        include_announcement_content: bool = False
    ) -> PublicTransportLineStopTimetable:
        """Loads departures of one line direction from a selected platform."""
        values = cls._query(url)
        feed_id = values.get('feed', '')
        route_id = values.get('route', '')
        trip_id = values.get('trip', '')
        stop_id = values.get('stop', '')
        service_date = cls._selected_date(url)
        if (
            feed_id not in cls._FEEDS
            or not route_id
            or not trip_id
            or not stop_id
        ):
            raise ValueError('Nieprawidłowy adres rozkładu GTFS.')

        with cls._connection() as connection:
            route = connection.execute(
                """
                    SELECT * FROM routes
                    WHERE feed_id = ? AND route_id = ?
                """,
                (feed_id, route_id)
            ).fetchone()
            selected_trip = connection.execute(
                """
                    SELECT * FROM trips
                    WHERE feed_id = ? AND trip_id = ?
                """,
                (feed_id, trip_id)
            ).fetchone()
            stop = connection.execute(
                """
                    SELECT * FROM stops
                    WHERE feed_id = ? AND stop_id = ?
                """,
                (feed_id, stop_id)
            ).fetchone()
            if route is None or selected_trip is None or stop is None:
                raise ValueError('Nie znaleziono rozkładu w danych GTFS.')
            service_ids = cls._service_ids(
                connection,
                feed_id,
                service_date
            )
            departures = cls._departures_for_direction(
                connection,
                feed_id,
                route_id,
                stop_id,
                str(selected_trip['headsign']),
                selected_trip['direction_id'],
                str(selected_trip['shape_id'] or ''),
                service_ids,
                service_date
            )

        line_name = str(route['short_name'])
        direction_name = str(selected_trip['headsign'] or '')
        day = PublicTransportDateTimetable(
            date=service_date,
            direction_name=direction_name,
            effective_date_from=service_date,
            effective_date_to=service_date,
            departures=departures,
            variants=list(dict.fromkeys(
                departure.variant
                for departure in departures
                if departure.variant
            ))
        )
        model = PublicTransportLineStopTimetable(
            line=line_name,
            type=cls._type_from_route(
                int(route['route_type']),
                feed_id
            ),
            announcements=[],
            stop_name=str(stop['name']),
            direction_name=direction_name,
            platform=cls._platform_name(stop),
            timetable={service_date: day},
            dates=cls._dates('line-stop', {
                'feed': feed_id,
                'route': route_id,
                'trip': trip_id,
                'stop': stop_id
            }),
            latitude=(
                float(stop['latitude'])
                if stop['latitude'] is not None else None
            ),
            longitude=(
                float(stop['longitude'])
                if stop['longitude'] is not None else None
            )
        )
        if include_announcement_content:
            model.announcements = cls.download_announcements(
                include_content=True,
                line=line_name
            )
        return model

    @classmethod
    def _departures_for_direction(
        cls,
        connection,
        feed_id: str,
        route_id: str,
        stop_id: str,
        headsign: str,
        direction_id,
        shape_id: str,
        service_ids: list[str],
        service_date: date
    ) -> list[PublicTransportDepartureTime]:
        """Queries scheduled departures for one route direction and service day."""
        if not service_ids:
            return []
        rows = connection.execute(
            f"""
                SELECT st.departure_time, st.stop_sequence,
                       t.trip_id, t.headsign
                FROM stop_times st
                JOIN trips t
                  ON t.feed_id = st.feed_id
                 AND t.trip_id = st.trip_id
                WHERE st.feed_id = ?
                  AND st.stop_id = ?
                  AND t.route_id = ?
                  AND t.service_id IN (
                      {GtfsDatabase.placeholders(service_ids)}
                  )
                  AND t.headsign = ?
                  AND (
                      t.direction_id = ?
                      OR (t.direction_id IS NULL AND ? IS NULL)
                  )
                  AND t.shape_id = ?
                ORDER BY st.departure_time
            """,
            [
                feed_id,
                stop_id,
                route_id,
                *service_ids,
                headsign,
                direction_id,
                direction_id,
                shape_id
            ]
        ).fetchall()
        return [
            PublicTransportDepartureTime(
                departure_time=cls._clock(str(row['departure_time'])),
                is_high_floor=False,
                url=cls._url(
                    'ride',
                    feed=feed_id,
                    trip=str(row['trip_id']),
                    data=service_date.isoformat()
                ),
                variant=str(row['headsign'] or '')
            )
            for row in sorted(
                rows,
                key=lambda item: cls._clock_sort_value(
                    str(item['departure_time'])
                )
            )
            if cls._clock(str(row['departure_time'])) is not None
        ]

    #endregion Line stop timetable

    #region Stops

    @classmethod
    def download_stops(
        cls,
        url: str | None = None,
        progress_callback=None,
        refresh: bool = False
    ) -> list[PublicTransportStop]:
        """Builds grouped stops, platforms and serving lines from GTFS."""
        del url
        if progress_callback:
            progress_callback(1, 1, cls.CITY_NAME)
        with cls._connection(refresh) as connection:
            stop_rows = connection.execute("""
                SELECT *
                FROM stops
                WHERE name <> ''
                ORDER BY name, platform_code, description
            """).fetchall()
            line_rows = connection.execute("""
                SELECT DISTINCT
                    st.feed_id,
                    st.stop_id,
                    r.route_id,
                    r.short_name,
                    r.route_type
                FROM stop_times st
                JOIN trips t
                  ON t.feed_id = st.feed_id
                 AND t.trip_id = st.trip_id
                JOIN routes r
                  ON r.feed_id = t.feed_id
                 AND r.route_id = t.route_id
                WHERE r.short_name <> ''
            """).fetchall()

        lines_by_stop: dict[
            tuple[str, str],
            dict[tuple[str, str], PublicTransportBaseLine]
        ] = defaultdict(dict)
        for row in line_rows:
            feed_id = str(row['feed_id'])
            route_id = str(row['route_id'])
            line_name = str(row['short_name'])
            lines_by_stop[(feed_id, str(row['stop_id']))][
                (feed_id, route_id)
            ] = PublicTransportBaseLine(
                line=line_name,
                type=cls._type_from_route(
                    int(row['route_type']),
                    feed_id
                ),
                url=cls._url(
                    'line',
                    feed=feed_id,
                    route=route_id
                ),
                free_of_charge=False,
                updated=False
            )

        grouped: dict[
            tuple[str, str],
            dict[str, Any]
        ] = {}
        for row in stop_rows:
            name = str(row['name']).strip()
            platform_name = cls._platform_name(row)
            key = (name.casefold(), platform_name.casefold())
            item = grouped.setdefault(key, {
                'name': name,
                'platform': platform_name,
                'refs': set(),
                'lines': {},
                'latitude': None,
                'longitude': None
            })
            feed_id = str(row['feed_id'])
            stop_id = str(row['stop_id'])
            item['refs'].add(f'{feed_id}:{stop_id}')
            item['lines'].update(lines_by_stop.get((feed_id, stop_id), {}))
            if item['latitude'] is None and row['latitude'] is not None:
                item['latitude'] = float(row['latitude'])
                item['longitude'] = float(row['longitude'])

        stops_by_name: dict[str, list[PublicTransportStopPlatform]] = defaultdict(list)
        display_names: dict[str, str] = {}
        for item in grouped.values():
            name_key = item['name'].casefold()
            display_names.setdefault(name_key, item['name'])
            stops_by_name[name_key].append(PublicTransportStopPlatform(
                name=item['platform'],
                lines=sorted(
                    item['lines'].values(),
                    key=lambda line: cls._line_sort_key(line.line)
                ),
                url_all=cls._url(
                    'stop',
                    stops='|'.join(sorted(item['refs']))
                ),
                url_chrono='',
                latitude=item['latitude'],
                longitude=item['longitude']
            ))
        return [
            PublicTransportStop(
                name=display_names[name_key],
                city=cls._city(),
                platforms=sorted(
                    platforms,
                    key=lambda platform: platform.name
                )
            )
            for name_key, platforms in sorted(
                stops_by_name.items(),
                key=lambda item: display_names[item[0]].casefold()
            )
        ]

    @classmethod
    def download_stop_all(cls, url: str) -> PublicTransportStopAll:
        """Loads every line and departure serving one grouped platform."""
        values = cls._query(url)
        references = cls._stop_references(values.get('stops', ''))
        service_date = cls._selected_date(url)
        if not references:
            raise ValueError('Nieprawidłowy identyfikator przystanku GTFS.')

        entries: dict[
            tuple[str, str, str, Any],
            dict[str, Any]
        ] = {}
        stop_name = ''
        platform = ''
        latitude = None
        longitude = None
        with cls._connection() as connection:
            for feed_id, stop_id in references:
                stop = connection.execute(
                    """
                        SELECT * FROM stops
                        WHERE feed_id = ? AND stop_id = ?
                    """,
                    (feed_id, stop_id)
                ).fetchone()
                if stop is None:
                    continue
                stop_name = stop_name or str(stop['name'])
                platform = platform or cls._platform_name(stop)
                if latitude is None and stop['latitude'] is not None:
                    latitude = float(stop['latitude'])
                    longitude = float(stop['longitude'])
                service_ids = cls._service_ids(
                    connection,
                    feed_id,
                    service_date
                )
                if not service_ids:
                    continue
                rows = connection.execute(
                    f"""
                        SELECT r.*, t.trip_id, t.headsign, t.direction_id,
                               st.departure_time, st.stop_sequence
                        FROM stop_times st
                        JOIN trips t
                          ON t.feed_id = st.feed_id
                         AND t.trip_id = st.trip_id
                        JOIN routes r
                          ON r.feed_id = t.feed_id
                         AND r.route_id = t.route_id
                        WHERE st.feed_id = ?
                          AND st.stop_id = ?
                          AND t.service_id IN (
                              {GtfsDatabase.placeholders(service_ids)}
                          )
                        ORDER BY r.short_name, t.headsign, st.departure_time
                    """,
                    [feed_id, stop_id, *service_ids]
                ).fetchall()
                for row in rows:
                    key = (
                        feed_id,
                        str(row['route_id']),
                        str(row['headsign'] or ''),
                        row['direction_id']
                    )
                    item = entries.setdefault(key, {
                        'route': row,
                        'trip_id': str(row['trip_id']),
                        'departures': []
                    })
                    item['departures'].append((
                        str(row['departure_time']),
                        str(row['trip_id'])
                    ))

        mapped_lines: dict[
            PublicTransportBaseLine,
            PublicTransportDateTimetable
        ] = {}
        for (feed_id, route_id, headsign, _), item in entries.items():
            row = item['route']
            line = PublicTransportBaseLine(
                line=str(row['short_name']),
                type=cls._type_from_route(
                    int(row['route_type']),
                    feed_id
                ),
                url=cls._url(
                    'line',
                    feed=feed_id,
                    route=route_id,
                    trip=item['trip_id'],
                    data=service_date.isoformat()
                ),
                free_of_charge=False,
                updated=False
            )
            departures = [
                PublicTransportDepartureTime(
                    departure_time=cls._clock(raw_time),
                    is_high_floor=False,
                    url=cls._url(
                        'ride',
                        feed=feed_id,
                        trip=trip_id,
                        data=service_date.isoformat()
                    ),
                    variant=headsign
                )
                for raw_time, trip_id in sorted(
                    set(item['departures']),
                    key=lambda value: cls._clock_sort_value(value[0])
                )
                if cls._clock(raw_time) is not None
            ]
            mapped_lines[line] = PublicTransportDateTimetable(
                date=service_date,
                direction_name=headsign,
                effective_date_from=service_date,
                effective_date_to=service_date,
                departures=departures,
                variants=[headsign] if headsign else []
            )
        return PublicTransportStopAll(
            stop_name=stop_name,
            platform=platform,
            dates=cls._dates('stop', {
                'stops': '|'.join(
                    f'{feed_id}:{stop_id}'
                    for feed_id, stop_id in references
                )
            }),
            lines=mapped_lines,
            latitude=latitude,
            longitude=longitude
        )

    @classmethod
    def _stop_references(cls, value: str) -> list[tuple[str, str]]:
        """Parses grouped feed and stop identifiers from a virtual URL."""
        result: list[tuple[str, str]] = []
        for item in value.split('|'):
            feed_id, separator, stop_id = item.partition(':')
            if separator and feed_id in cls._FEEDS and stop_id:
                result.append((feed_id, stop_id))
        return result

    #endregion Stops

    #region Announcements

    @classmethod
    def download_announcements(
        cls,
        include_content: bool = False,
        line: str = ''
    ) -> list[PublicTransportAnnouncement]:
        """Downloads announcement summaries from the MPK website."""
        announcements = cls.parse_announcements(
            cls._download_html(
                cls.ANNOUNCEMENTS_URL,
                'Lista komunikatów'
            ),
            cls.ANNOUNCEMENTS_URL,
            line
        )
        if not include_content:
            return announcements
        result: list[PublicTransportAnnouncement] = []
        total = len(announcements)
        for index, announcement in enumerate(announcements, start=1):
            try:
                result.append(cls.download_announcement(
                    announcement.url,
                    announcement.description,
                    index,
                    total
                ))
            except Exception:
                result.append(announcement)
        return result

    @classmethod
    def parse_announcements(
        cls,
        html: str,
        source_url: str | None = None,
        line: str = ''
    ) -> list[PublicTransportAnnouncement]:
        """Parses typed announcement summaries and affected lines."""
        document = parse_html(html)
        result: list[PublicTransportAnnouncement] = []
        source_url = source_url or cls.ANNOUNCEMENTS_URL
        for panel in document.find_all('div', 'route-info-panel'):
            anchor = panel.find('a', 'link')
            heading = panel.find('h3', 'title')
            description = panel.find('span', 'description')
            raw_date = panel.find('span', 'date')
            if not anchor or not heading:
                continue
            lines_list = panel.find('div', 'lines-list')
            affected_lines = [
                node.text()
                for node in (
                    lines_list.find_all('p') if lines_list else []
                )
                if node.text()
            ]
            if line and line not in affected_lines:
                continue
            dates = cls._iso_dates(raw_date.text() if raw_date else '')
            result.append(PublicTransportAnnouncement(
                lines=affected_lines,
                city=cls.CITY_NAME,
                content='',
                description=(
                    description.text() if description else heading.text()
                ),
                effective_date_from=dates[0] if dates else None,
                effective_date_to=dates[1] if len(dates) > 1 else None,
                last_updated_datetime=None,
                url=urljoin(source_url, anchor.attrs.get('href', ''))
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
        """Downloads one complete MPK announcement on demand."""
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
        """Parses full announcement text, dates and affected lines."""
        document = parse_html(html)
        main = document.find('main') or document
        heading = main.find('h1', 'section-title')
        subtitle = main.find('h2', 'announcement-subtitle')
        lines_list = main.find('div', 'lines-list')
        affected_lines = [
            node.text()
            for node in (lines_list.find_all('p') if lines_list else [])
            if node.text()
        ]
        text_blocks = main.find_all('div', 'text-content')
        content = max(
            (block.text() for block in text_blocks),
            key=len,
            default=''
        )
        validity = main.find('div', 'suffix-group')
        dates = cls._iso_dates(validity.text() if validity else main.text())
        updated = None
        updated_match = re.search(
            r'Ostatnia aktualizacja:\s*'
            r'(20\d{2}-\d{2}-\d{2})'
            r'(?:\s+(\d{1,2}:\d{2}:\d{2}))?',
            main.text()
        )
        if updated_match:
            updated = datetime.fromisoformat(
                f'{updated_match.group(1)}T'
                f'{updated_match.group(2) or "00:00:00"}'
            )
        return PublicTransportAnnouncement(
            lines=affected_lines,
            city=cls.CITY_NAME,
            content=content,
            description=(
                subtitle.text()
                if subtitle else heading.text() if heading else ''
            ),
            effective_date_from=dates[0] if dates else None,
            effective_date_to=dates[1] if len(dates) > 1 else None,
            last_updated_datetime=updated,
            url=source_url
        )

    @staticmethod
    def _iso_dates(value: str) -> list[date]:
        """Extracts valid ISO dates from provider text."""
        result: list[date] = []
        for raw_date in re.findall(r'20\d{2}-\d{2}-\d{2}', value or ''):
            try:
                result.append(date.fromisoformat(raw_date))
            except ValueError:
                continue
        return result

    #endregion Announcements

    #region GTFS-Realtime

    @classmethod
    def download_vehicle_positions(
        cls,
        line: str = ''
    ) -> list[PublicTransportVehiclePosition]:
        """Downloads current vehicle positions from all Kraków GTFS-RT feeds."""
        with cls._connection() as connection:
            route_query = """
                    SELECT feed_id, route_id, short_name, route_type
                    FROM routes
            """
            route_parameters: tuple[str, ...] = ()
            if line:
                route_query += " WHERE short_name = ?"
                route_parameters = (line,)
            route_rows = connection.execute(
                route_query,
                route_parameters
            ).fetchall()
            route_names = {
                (str(row['feed_id']), str(row['route_id'])): str(
                    row['short_name']
                )
                for row in route_rows
            }
            line_types: dict[str, PublicTransportType] = {}
            for row in route_rows:
                line_name = str(row['short_name'])
                transport_type = cls._type_from_route(
                    int(row['route_type']),
                    str(row['feed_id'])
                )
                if (
                    line_name not in line_types
                    or transport_type == PublicTransportType.TRAM
                ):
                    line_types[line_name] = transport_type
            trip_query = """
                SELECT t.feed_id, t.trip_id, r.short_name
                FROM trips t
                JOIN routes r
                  ON r.feed_id = t.feed_id
                 AND r.route_id = t.route_id
            """
            trip_parameters: tuple[str, ...] = ()
            if line:
                trip_query += " WHERE r.short_name = ?"
                trip_parameters = (line,)
            trip_names = {
                (str(row['feed_id']), str(row['trip_id'])): str(
                    row['short_name']
                )
                for row in connection.execute(
                    trip_query,
                    trip_parameters
                )
            }
        selected_feed_ids = {str(row['feed_id']) for row in route_rows}
        feeds = [
            (feed_id, feed)
            for feed_id, feed in cls._FEEDS.items()
            if not line or feed_id in selected_feed_ids
        ]
        positions: list[PublicTransportVehiclePosition] = []
        total = len(feeds)
        for index, (feed_id, feed) in enumerate(
            feeds,
            start=1
        ):
            payload = cls._download_bytes(
                feed['vehicles'],
                f"Pojazdy na żywo: {feed['name']}",
                index,
                total
            )
            positions.extend(cls.parse_vehicle_positions(
                payload,
                feed_id,
                route_names,
                trip_names,
                line_types,
                line
            ))
        return positions

    @classmethod
    def parse_vehicle_positions(
        cls,
        payload: bytes,
        feed_id: str,
        route_names: dict[tuple[str, str], str],
        trip_names: dict[tuple[str, str], str] | None = None,
        line_types: dict[str, PublicTransportType] | None = None,
        line: str = ''
    ) -> list[PublicTransportVehiclePosition]:
        """Deserializes one GTFS-Realtime VehiclePositions protobuf feed."""
        try:
            from google.transit import gtfs_realtime_pb2
        except ImportError as error:
            raise RuntimeError(
                'Brak biblioteki gtfs-realtime-bindings.'
            ) from error
        message = gtfs_realtime_pb2.FeedMessage()
        message.ParseFromString(payload)
        result: list[PublicTransportVehiclePosition] = []
        for entity in message.entity:
            if not entity.HasField('vehicle'):
                continue
            vehicle = entity.vehicle
            route_id = str(vehicle.trip.route_id or '')
            trip_id = str(vehicle.trip.trip_id or '')
            line_name = (
                (trip_names or {}).get((feed_id, trip_id))
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
            recorded_at = (
                datetime.fromtimestamp(
                    int(vehicle.timestamp),
                    tz=timezone.utc
                )
                if vehicle.timestamp else None
            )
            result.append(PublicTransportVehiclePosition(
                vehicle_id=str(
                    descriptor.id or descriptor.label or entity.id
                ),
                vehicle_label=str(descriptor.label or ''),
                license_plate=str(descriptor.license_plate or ''),
                source_code=feed_id,
                line=line_name,
                trip_id=trip_id,
                type=(line_types or {}).get(
                    line_name,
                    cls._type_from_route(
                        0 if feed_id == 'T' else 3,
                        feed_id
                    )
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
                recorded_at=recorded_at
            ))
        return result

    #endregion GTFS-Realtime

    #region Ride and container

    @classmethod
    def download_ride(cls, url: str) -> PublicTransportRide:
        """Builds a complete ride from relational static GTFS data."""
        values = cls._query(url)
        feed_id = values.get('feed', '')
        trip_id = values.get('trip', '')
        if feed_id not in cls._FEEDS or not trip_id:
            raise ValueError('Nieprawidłowy identyfikator kursu GTFS.')

        with cls._connection() as connection:
            trip = connection.execute(
                """
                    SELECT t.*, r.short_name AS route_short_name,
                           r.route_type
                    FROM trips t
                    JOIN routes r
                      ON r.feed_id = t.feed_id
                     AND r.route_id = t.route_id
                    WHERE t.feed_id = ? AND t.trip_id = ?
                """,
                (feed_id, trip_id)
            ).fetchone()
            rows = connection.execute(
                """
                    SELECT s.*, st.departure_time, st.stop_sequence
                    FROM stop_times st
                    JOIN stops s
                      ON s.feed_id = st.feed_id
                     AND s.stop_id = st.stop_id
                    WHERE st.feed_id = ? AND st.trip_id = ?
                    ORDER BY st.stop_sequence
                """,
                (feed_id, trip_id)
            ).fetchall()

        if trip is None or not rows:
            raise ValueError('Nie znaleziono kursu w danych GTFS.')

        first_seconds = cls._clock_sort_value(
            str(rows[0]['departure_time'])
        )
        previous_seconds = first_seconds
        ride_stops: list[PublicTransportRideStop] = []
        for row in rows:
            current_seconds = cls._clock_sort_value(
                str(row['departure_time'])
            )
            ride_stops.append(PublicTransportRideStop(
                stop=str(row['name']),
                departure_time=cls._clock(str(row['departure_time'])),
                travel_time=max(
                    0,
                    round((current_seconds - previous_seconds) / 60)
                ),
                travel_time_sum=max(
                    0,
                    round((current_seconds - first_seconds) / 60)
                ),
                distance=0.0,
                distance_sum=0.0,
                city=cls._city(),
                latitude=(
                    float(row['latitude'])
                    if row['latitude'] is not None else None
                ),
                longitude=(
                    float(row['longitude'])
                    if row['longitude'] is not None else None
                )
            ))
            previous_seconds = current_seconds

        first = ride_stops[0]
        return PublicTransportRide(
            line=str(trip['route_short_name']),
            type=cls._type_from_route(
                int(trip['route_type']),
                feed_id
            ),
            stop_name=first.stop,
            platform=cls._platform_name(rows[0]),
            departure_time=first.departure_time,
            cities=[cls._city()],
            next_stops=ride_stops[1:],
            carrier=cls._CARRIERS.get(feed_id, cls.CARRIER),
            vehicle_type='',
            latitude=first.latitude,
            longitude=first.longitude
        )

    @classmethod
    def download_container(
        cls,
        include_line_details: bool = False,
        include_stops: bool = False,
        include_vehicle_positions: bool = False,
        progress_callback=None
    ) -> PublicTransportDataContainer:
        """Downloads a selectable typed snapshot of the Kraków provider."""
        base_lines = cls.download_lines()
        lines = (
            [cls.download_line(line.url) for line in base_lines]
            if include_line_details else []
        )
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

    #endregion Unsupported ride and container

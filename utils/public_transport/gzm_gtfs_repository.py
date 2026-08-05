from __future__ import annotations
from collections import defaultdict
from datetime import date, time, timedelta
from pathlib import Path
import re
import sqlite3
from typing import Any, ClassVar, Iterable
from urllib.parse import parse_qs, urlencode, urlparse
from zlib import crc32

from core.gtfs_database import GtfsDatabase
from models.public_transport.public_transport_base_line import PublicTransportBaseLine
from models.public_transport.public_transport_city import PublicTransportCity
from models.public_transport.public_transport_coordinate import PublicTransportCoordinate
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


class GzmGtfsRepository:
    """Maps the relational GZM GTFS cache to application data models."""

    FEED_ID: ClassVar[str] = 'GZM'
    FEED_PATTERN: ClassVar[str] = 'GZM:%'
    DATE_RANGE_DAYS: ClassVar[int] = 14
    _LINE_PATH_PATTERN: ClassVar[re.Pattern[str]] = re.compile(
        r'/rozklady/([^/]+)/'
    )
    _DATE_PATH_PATTERN: ClassVar[re.Pattern[str]] = re.compile(
        r'/(20\d{6})(?:/|$)'
    )
    _STOP_PATH_PATTERN: ClassVar[re.Pattern[str]] = re.compile(
        r'/stop/([^/]+)/'
    )
    _COLORS: ClassVar[tuple[str, ...]] = (
        '#006D77', '#2A6F97', '#6A4C93', '#A44A3F',
        '#3A7D44', '#A66321', '#4F5D75', '#7B2CBF',
        '#0077B6', '#9B2226', '#386641', '#5F0F40'
    )

    def __init__(self, database_path: Path, base_url: str):
        self._database_path = database_path
        self._base_url = base_url

    #region Connection and URLs

    def _connection(self) -> sqlite3.Connection:
        """Opens the current relational GTFS cache."""
        return GtfsDatabase.connect(self._database_path)

    def _url(self, view: str, **values: object) -> str:
        """Builds a provider-valid virtual URL for a relational record."""
        query = {'gtfs_view': view}
        query.update({
            key: str(value)
            for key, value in values.items()
            if value not in (None, '')
        })
        return f'{self._base_url}travel-manager?{urlencode(query)}'

    @staticmethod
    def _query(url: str) -> dict[str, str]:
        """Returns single-value query parameters."""
        return {
            key: values[0]
            for key, values in parse_qs(
                urlparse(url).query,
                keep_blank_values=True
            ).items()
            if values
        }

    @classmethod
    def _date_from_url(cls, url: str) -> date | None:
        """Reads an ISO query date or a compact date from a legacy URL."""
        value = cls._query(url).get('date', '')
        try:
            return date.fromisoformat(value)
        except ValueError:
            pass
        match = cls._DATE_PATH_PATTERN.search(url)
        if not match:
            return None
        try:
            return date(
                int(match.group(1)[:4]),
                int(match.group(1)[4:6]),
                int(match.group(1)[6:])
            )
        except ValueError:
            return None

    @classmethod
    def _selected_date(cls, url: str) -> date:
        """Returns the requested service date or today."""
        return cls._date_from_url(url) or date.today()

    def _dates(
        self,
        view: str,
        source_values: dict[str, object]
    ) -> dict[date, str]:
        """Builds the selectable 14-day date range published by GZM."""
        result: dict[date, str] = {}
        for offset in range(self.DATE_RANGE_DAYS):
            service_date = date.today() + timedelta(days=offset)
            values = dict(source_values)
            values['date'] = service_date.isoformat()
            result[service_date] = self._url(view, **values)
        return result

    #endregion Connection and URLs

    #region Shared values

    @staticmethod
    def _transport_type(route_type: int) -> PublicTransportType:
        """Maps a GTFS route type to the application enum."""
        if route_type == 0:
            return PublicTransportType.TRAM
        if route_type == 11:
            return PublicTransportType.TROLLEY
        return PublicTransportType.BUS

    @staticmethod
    def _public_line_name(short_name: str, route_type: int) -> str:
        """Converts GZM's GTFS tram prefix to the public line number."""
        value = short_name.strip()
        if route_type == 0 and value.casefold().startswith('t'):
            return value[1:]
        return value

    @staticmethod
    def _line_sort_key(value: str) -> tuple[int, int | str]:
        """Sorts numeric line identifiers before special lines."""
        return (0, int(value)) if value.isdigit() else (1, value.casefold())

    @classmethod
    def _city(cls, value: str) -> PublicTransportCity:
        """Builds a deterministic city marker from a GTFS city name."""
        name = value.strip() or 'GZM'
        color = cls._COLORS[
            crc32(name.casefold().encode('utf-8')) % len(cls._COLORS)
        ]
        return PublicTransportCity(name=name, color=color)

    @staticmethod
    def _platform(row) -> str:
        """Returns the provider platform symbol."""
        extended = str(row['extended_platform'] or '').strip()
        if extended:
            return extended.split('/', 1)[0].strip()
        platform = str(row['platform_code'] or '').strip()
        if platform:
            return platform
        code = str(row['stop_code'] or '').strip()
        return code.rsplit('-', 1)[-1] if '-' in code else ''

    @staticmethod
    def _clock(value: str) -> time | None:
        """Converts an extended GTFS clock to a display clock."""
        try:
            hours, minutes, seconds = [
                int(part)
                for part in value.split(':', 2)
            ]
            return time(hours % 24, minutes, seconds)
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _seconds(value: str) -> int:
        """Converts an extended GTFS clock to seconds from service start."""
        try:
            hours, minutes, seconds = [
                int(part)
                for part in value.split(':', 2)
            ]
            return hours * 3600 + minutes * 60 + seconds
        except (TypeError, ValueError):
            return 0

    @classmethod
    def _service_ids(
        cls,
        connection: sqlite3.Connection,
        feed_id: str,
        service_date: date
    ) -> list[str]:
        """Returns service identifiers active on the selected date."""
        return sorted(GtfsDatabase.active_service_ids(
            connection,
            feed_id,
            service_date
        ))

    @classmethod
    def _active_feed_ids(
        cls,
        connection: sqlite3.Connection,
        service_date: date
    ) -> list[str]:
        """Returns GZM packages containing service on a selected date."""
        candidates = {
            str(row['feed_id'])
            for row in connection.execute(
                """
                    SELECT DISTINCT feed_id FROM calendar
                    WHERE feed_id LIKE ?
                    UNION
                    SELECT DISTINCT feed_id FROM calendar_dates
                    WHERE feed_id LIKE ?
                """,
                (cls.FEED_PATTERN, cls.FEED_PATTERN)
            )
        }
        return sorted(
            feed_id
            for feed_id in candidates
            if cls._service_ids(connection, feed_id, service_date)
        )

    @classmethod
    def _active_feed(
        cls,
        connection: sqlite3.Connection,
        service_date: date
    ) -> str:
        """Returns the preferred GTFS package for a selected date."""
        feed_ids = cls._active_feed_ids(connection, service_date)
        if not feed_ids:
            raise ValueError(
                f'Brak rozkładu GTFS GZM na dzień {service_date.isoformat()}.'
            )
        return feed_ids[-1]

    @staticmethod
    def _variant_description(row) -> str:
        """Returns a readable GZM route variant description."""
        code = str(row['variant_code'] or '').strip()
        headsign = str(row['headsign'] or '').strip()
        if code and headsign:
            return f'{code} · {headsign}'
        return code or headsign

    @staticmethod
    def _visible_stop_filter(alias: str = 'st') -> str:
        """Returns the GTFS predicate for passenger-visible stops."""
        return (
            f'NOT ({alias}.pickup_type = 1 '
            f'AND {alias}.drop_off_type = 1)'
        )

    #endregion Shared values

    #region Reference resolution

    def _feed_reference(
        self,
        connection: sqlite3.Connection,
        url: str,
        service_date: date
    ) -> str:
        """Returns a URL feed when active, otherwise resolves it by date."""
        feed_id = self._query(url).get('feed', '')
        if (
            feed_id
            and self._service_ids(connection, feed_id, service_date)
        ):
            return feed_id
        return self._active_feed(connection, service_date)

    def _route_reference(
        self,
        connection: sqlite3.Connection,
        url: str,
        service_date: date
    ) -> sqlite3.Row | None:
        """Resolves virtual and legacy GZM line URLs to a route row."""
        values = self._query(url)
        route_id = values.get('route', '')
        feed_id = values.get('feed', '')
        if route_id:
            feed_ids = (
                [feed_id]
                if feed_id else self._active_feed_ids(
                    connection,
                    service_date
                )
            )
            if not feed_ids:
                return None
            return connection.execute(
                f"""
                    SELECT * FROM routes
                    WHERE feed_id IN (
                        {GtfsDatabase.placeholders(feed_ids)}
                    )
                      AND route_id = ?
                    ORDER BY feed_id DESC
                    LIMIT 1
                """,
                [*feed_ids, route_id]
            ).fetchone()
        match = self._LINE_PATH_PATTERN.search(url)
        if not match:
            return None
        identifier = match.group(1)
        if identifier.startswith('0-t'):
            line_name, route_type = f'T{identifier[3:]}'.upper(), 0
        elif identifier.startswith('11-'):
            line_name, route_type = identifier[3:].upper(), 11
        elif identifier.startswith('3-'):
            line_name, route_type = identifier[2:].upper(), 3
        else:
            line_name, route_type = identifier.upper(), None
        feed_ids = self._active_feed_ids(connection, service_date)
        if not feed_ids:
            return None
        parameters: list[Any] = [*feed_ids, line_name]
        type_filter = ''
        if route_type is not None:
            type_filter = ' AND route_type = ?'
            parameters.append(route_type)
        return connection.execute(
            f"""
                SELECT * FROM routes
                WHERE feed_id IN (
                    {GtfsDatabase.placeholders(feed_ids)}
                )
                  AND UPPER(short_name) = ?
                {type_filter}
                ORDER BY route_id
                LIMIT 1
            """,
            parameters
        ).fetchone()

    def _stop_reference(
        self,
        connection: sqlite3.Connection,
        url: str,
        feed_id: str
    ) -> sqlite3.Row | None:
        """Resolves virtual and legacy platform URLs to a stop row."""
        values = self._query(url)
        stop_id = values.get('stop', '')
        if not stop_id:
            match = self._STOP_PATH_PATTERN.search(url)
            stop_id = match.group(1) if match else ''
        if not stop_id:
            return None
        return connection.execute(
            """
                SELECT s.*, se.platform_code AS extended_platform,
                       se.city
                FROM stops s
                LEFT JOIN stop_extensions se
                  ON se.feed_id = s.feed_id
                 AND se.stop_id = s.stop_id
                WHERE s.feed_id = ?
                  AND (
                      s.stop_id = ?
                      OR s.stop_code = ?
                  )
                ORDER BY s.stop_id
                LIMIT 1
            """,
            (feed_id, stop_id, stop_id)
        ).fetchone()

    def _trip_reference(
        self,
        connection: sqlite3.Connection,
        url: str,
        feed_id: str
    ) -> sqlite3.Row | None:
        """Resolves virtual and legacy ride URLs to a GTFS trip."""
        values = self._query(url)
        trip_id = values.get('trip', '')
        if not trip_id:
            path_parts = [
                part for part in urlparse(url).path.split('/')
                if part
            ]
            trip_id = path_parts[-1] if path_parts else ''
        if not trip_id:
            return None
        return connection.execute(
            """
                SELECT * FROM trips
                WHERE feed_id = ?
                  AND (
                      trip_id = ?
                      OR trip_id LIKE ?
                  )
                ORDER BY trip_id
                LIMIT 1
            """,
            (feed_id, trip_id, f'%_{trip_id}')
        ).fetchone()

    #endregion Reference resolution

    #region Lines

    def lines(self) -> list[PublicTransportBaseLine]:
        """Returns every line contained in the current GTFS cache."""
        with self._connection() as connection:
            feed_id = self._active_feed(connection, date.today())
            rows = connection.execute(
                """
                    SELECT r.*, re.line_type
                    FROM routes r
                    LEFT JOIN route_extensions re
                      ON re.feed_id = r.feed_id
                     AND re.route_id = r.route_id
                    WHERE r.feed_id = ? AND r.short_name <> ''
                """,
                (feed_id,)
            ).fetchall()
        result = [
            self._base_line(row)
            for row in rows
        ]
        return sorted(result, key=lambda item: (
            str(item.type),
            self._line_sort_key(item.line)
        ))

    def _base_line(
        self,
        row,
        trip_id: str = '',
        service_date: date | None = None
    ) -> PublicTransportBaseLine:
        """Maps a joined route row to a base-line model."""
        line_type = str(
            row['line_type'] if 'line_type' in row.keys() else ''
        )
        values: dict[str, object] = {
            'feed': str(row['feed_id']),
            'route': str(row['route_id'])
        }
        if trip_id:
            values['trip'] = trip_id
        if service_date:
            values['date'] = service_date.isoformat()
        return PublicTransportBaseLine(
            line=self._public_line_name(
                str(row['short_name']),
                int(row['route_type'])
            ),
            type=self._transport_type(int(row['route_type'])),
            url=self._url('line', **values),
            free_of_charge='bezpłatna' in line_type.casefold(),
            updated=False
        )

    def line(self, url: str) -> PublicTransportLine:
        """Builds directions, variants and geometry for one line."""
        service_date = self._selected_date(url)
        selected_trip_id = self._query(url).get('trip', '')
        with self._connection() as connection:
            route = self._route_reference(connection, url, service_date)
            if route is None:
                raise ValueError('Nie znaleziono linii w danych GTFS GZM.')
            feed_id = str(route['feed_id'])
            variants = self._line_variants(
                connection,
                feed_id,
                str(route['route_id']),
                service_date
            )
            if selected_trip_id:
                selected = [
                    row for row in variants
                    if str(row['trip_id']) == selected_trip_id
                ]
                if not selected:
                    selected_row = connection.execute(
                        """
                            SELECT t.*, te.variant_code, te.is_base,
                                   te.is_bypass
                            FROM trips t
                            LEFT JOIN trip_extensions te
                              ON te.feed_id = t.feed_id
                             AND te.trip_id = t.trip_id
                            WHERE t.feed_id = ? AND t.trip_id = ?
                        """,
                        (feed_id, selected_trip_id)
                    ).fetchone()
                    selected = [selected_row] if selected_row else []
            else:
                selected = [
                    row for row in variants
                    if int(row['is_base'] or 0) == 1
                ]
                if not selected:
                    selected = variants[:2]
            directions = [
                self._direction(
                    connection,
                    feed_id,
                    route,
                    variant,
                    service_date
                )
                for variant in selected
            ]
        return PublicTransportLine(
            line=self._public_line_name(
                str(route['short_name']),
                int(route['route_type'])
            ),
            type=self._transport_type(int(route['route_type'])),
            announcements=[],
            directions=directions,
            route_variants=self._variant_urls(
                variants,
                feed_id,
                str(route['route_id']),
                service_date
            ),
            dates=self._dates('line', {
                'route': str(route['route_id'])
            })
        )

    def _line_variants(
        self,
        connection: sqlite3.Connection,
        feed_id: str,
        route_id: str,
        service_date: date
    ) -> list[sqlite3.Row]:
        """Returns one representative active trip for each route variant."""
        service_ids = self._service_ids(
            connection,
            feed_id,
            service_date
        )
        service_filter = ''
        parameters: list[Any] = [feed_id, route_id]
        if service_ids:
            service_filter = (
                ' AND t.service_id IN ('
                + GtfsDatabase.placeholders(service_ids)
                + ')'
            )
            parameters.extend(service_ids)
        rows = connection.execute(
            f"""
                WITH variants AS (
                    SELECT t.*, COALESCE(te.variant_code, '') variant_code,
                           COALESCE(te.is_base, 0) is_base,
                           COALESCE(te.is_bypass, 0) is_bypass,
                           ROW_NUMBER() OVER (
                               PARTITION BY t.headsign, t.direction_id,
                                            COALESCE(te.variant_code, '')
                               ORDER BY COALESCE(te.is_base, 0) DESC,
                                        t.trip_id
                           ) AS row_number
                    FROM trips t
                    LEFT JOIN trip_extensions te
                      ON te.feed_id = t.feed_id
                     AND te.trip_id = t.trip_id
                    WHERE t.feed_id = ? AND t.route_id = ?
                    {service_filter}
                )
                SELECT * FROM variants
                WHERE row_number = 1
                ORDER BY direction_id, is_base DESC, variant_code, headsign
            """,
            parameters
        ).fetchall()
        return list(rows)

    def _variant_urls(
        self,
        variants: Iterable[sqlite3.Row],
        feed_id: str,
        route_id: str,
        service_date: date
    ) -> dict[str, str]:
        """Builds unique labels for the line variant selector."""
        result: dict[str, str] = {}
        for index, variant in enumerate(variants, start=1):
            name = self._variant_description(variant) or f'Wariant {index}'
            label = name
            duplicate = 2
            while label in result:
                label = f'{name} ({duplicate})'
                duplicate += 1
            result[label] = self._url(
                'line',
                feed=feed_id,
                route=route_id,
                trip=str(variant['trip_id']),
                date=service_date.isoformat()
            )
        return result

    def _direction(
        self,
        connection: sqlite3.Connection,
        feed_id: str,
        route,
        variant,
        service_date: date
    ) -> PublicTransportDirection:
        """Builds one ordered direction and its route geometry."""
        trip_id = str(variant['trip_id'])
        rows = connection.execute(
            f"""
                SELECT s.*, st.stop_sequence, se.city,
                       se.platform_code AS extended_platform
                FROM stop_times st
                JOIN stops s
                  ON s.feed_id = st.feed_id
                 AND s.stop_id = st.stop_id
                LEFT JOIN stop_extensions se
                  ON se.feed_id = s.feed_id
                 AND se.stop_id = s.stop_id
                WHERE st.feed_id = ? AND st.trip_id = ?
                  AND {self._visible_stop_filter('st')}
                ORDER BY st.stop_sequence
            """,
            (feed_id, trip_id)
        ).fetchall()
        base_stops = self._base_stop_ids(
            connection,
            feed_id,
            str(route['route_id']),
            variant['direction_id']
        )
        transport_type = self._transport_type(int(route['route_type']))
        stops: list[PublicTransportDirectionStop] = []
        cities: list[PublicTransportCity] = []
        for row in rows:
            city = self._city(str(row['city'] or ''))
            if city.name not in {item.name for item in cities}:
                cities.append(city)
            stops.append(PublicTransportDirectionStop(
                line=self._public_line_name(
                    str(route['short_name']),
                    int(route['route_type'])
                ),
                type=transport_type,
                city=city,
                is_variant=(
                    int(variant['is_base'] or 0) == 0
                    and str(row['stop_id']) not in base_stops
                ),
                name=str(row['name']),
                platform=self._platform(row),
                url=self._url(
                    'line-stop',
                    feed=feed_id,
                    route=str(route['route_id']),
                    trip=trip_id,
                    stop=str(row['stop_id']),
                    date=service_date.isoformat()
                )
            ))
        route_points = self._shape(
            connection,
            feed_id,
            str(variant['shape_id'] or '')
        )
        if not route_points:
            route_points = [
                PublicTransportCoordinate(
                    latitude=float(row['latitude']),
                    longitude=float(row['longitude'])
                )
                for row in rows
                if row['latitude'] is not None and row['longitude'] is not None
            ]
        return PublicTransportDirection(
            name=self._variant_description(variant),
            cities=cities,
            stops=stops,
            route=route_points
        )

    def _base_stop_ids(
        self,
        connection: sqlite3.Connection,
        feed_id: str,
        route_id: str,
        direction_id
    ) -> set[str]:
        """Returns stops belonging to the main variant of a direction."""
        trip = connection.execute(
            """
                SELECT t.trip_id
                FROM trips t
                JOIN trip_extensions te
                  ON te.feed_id = t.feed_id
                 AND te.trip_id = t.trip_id
                WHERE t.feed_id = ? AND t.route_id = ?
                  AND (
                      t.direction_id = ?
                      OR (t.direction_id IS NULL AND ? IS NULL)
                  )
                  AND te.is_base = 1
                ORDER BY t.trip_id
                LIMIT 1
            """,
            (feed_id, route_id, direction_id, direction_id)
        ).fetchone()
        if trip is None:
            return set()
        return {
            str(row['stop_id'])
            for row in connection.execute(
                """
                    SELECT stop_id FROM stop_times
                    WHERE feed_id = ? AND trip_id = ?
                """,
                (feed_id, str(trip['trip_id']))
            )
        }

    def _shape(
        self,
        connection: sqlite3.Connection,
        feed_id: str,
        shape_id: str
    ) -> list[PublicTransportCoordinate]:
        """Returns an ordered GTFS shape."""
        if not shape_id:
            return []
        return [
            PublicTransportCoordinate(
                latitude=float(row['latitude']),
                longitude=float(row['longitude'])
            )
            for row in connection.execute(
                """
                    SELECT latitude, longitude FROM shapes
                    WHERE feed_id = ? AND shape_id = ?
                    ORDER BY point_sequence
                """,
                (feed_id, shape_id)
            )
        ]

    #endregion Lines

    #region Timetables

    def line_stop(self, url: str) -> PublicTransportLineStopTimetable:
        """Builds a line timetable for one platform and direction."""
        service_date = self._selected_date(url)
        with self._connection() as connection:
            route = self._route_reference(connection, url, service_date)
            if route is None:
                raise ValueError('Nie znaleziono rozkładu w danych GTFS GZM.')
            feed_id = str(route['feed_id'])
            stop = self._stop_reference(connection, url, feed_id)
            trip = self._trip_reference(connection, url, feed_id)
            if route is None or stop is None:
                raise ValueError('Nie znaleziono rozkładu w danych GTFS GZM.')
            if trip is None:
                direction_id = self._legacy_direction(url)
                trip = self._representative_trip(
                    connection,
                    feed_id,
                    str(route['route_id']),
                    direction_id,
                    service_date
                )
            if trip is None:
                raise ValueError('Nie znaleziono wariantu linii w danych GTFS GZM.')
            departures = self._departures(
                connection,
                feed_id,
                route,
                stop,
                trip,
                service_date
            )
        direction_name = str(trip['headsign'] or '')
        variants = list(dict.fromkeys(
            item.variant
            for item in departures
            if item.variant
        ))
        timetable = PublicTransportDateTimetable(
            date=service_date,
            direction_name=direction_name,
            effective_date_from=service_date,
            effective_date_to=service_date,
            departures=departures,
            variants=variants
        )
        return PublicTransportLineStopTimetable(
            line=self._public_line_name(
                str(route['short_name']),
                int(route['route_type'])
            ),
            type=self._transport_type(int(route['route_type'])),
            announcements=[],
            stop_name=str(stop['name']),
            direction_name=direction_name,
            platform=self._platform(stop),
            timetable={service_date: timetable},
            dates=self._dates('line-stop', {
                'route': str(route['route_id']),
                'stop': str(stop['stop_id']),
                'direction': (
                    trip['direction_id']
                    if trip['direction_id'] is not None else ''
                )
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

    @classmethod
    def _legacy_direction(cls, url: str) -> int | None:
        """Extracts a direction number following a legacy stop identifier."""
        value = cls._query(url).get('direction', '')
        if value:
            try:
                return int(value)
            except ValueError:
                pass
        match = re.search(r'/stop/[^/]+/(\d+)/', urlparse(url).path)
        return int(match.group(1)) if match else None

    def _representative_trip(
        self,
        connection: sqlite3.Connection,
        feed_id: str,
        route_id: str,
        direction_id,
        service_date: date
    ) -> sqlite3.Row | None:
        """Returns a preferred active trip for one route direction."""
        service_ids = self._service_ids(
            connection,
            feed_id,
            service_date
        )
        parameters: list[Any] = [
            feed_id,
            route_id,
            direction_id,
            direction_id
        ]
        service_filter = ''
        if service_ids:
            service_filter = (
                ' AND t.service_id IN ('
                + GtfsDatabase.placeholders(service_ids)
                + ')'
            )
            parameters.extend(service_ids)
        return connection.execute(
            f"""
                SELECT t.*
                FROM trips t
                LEFT JOIN trip_extensions te
                  ON te.feed_id = t.feed_id
                 AND te.trip_id = t.trip_id
                WHERE t.feed_id = ? AND t.route_id = ?
                  AND (
                      t.direction_id = ?
                      OR ? IS NULL
                  )
                  {service_filter}
                ORDER BY COALESCE(te.is_base, 0) DESC, t.trip_id
                LIMIT 1
            """,
            parameters
        ).fetchone()

    def _departures(
        self,
        connection: sqlite3.Connection,
        feed_id: str,
        route,
        stop,
        selected_trip,
        service_date: date
    ) -> list[PublicTransportDepartureTime]:
        """Returns scheduled departures for a selected line direction."""
        service_ids = self._service_ids(
            connection,
            feed_id,
            service_date
        )
        if not service_ids:
            return []
        rows = connection.execute(
            f"""
                SELECT st.departure_time, t.trip_id, t.headsign,
                       t.wheelchair_accessible,
                       COALESCE(te.variant_code, '') variant_code,
                       vc.low_floor, vc.long_name vehicle_name
                FROM stop_times st
                JOIN trips t
                  ON t.feed_id = st.feed_id
                 AND t.trip_id = st.trip_id
                LEFT JOIN trip_extensions te
                  ON te.feed_id = t.feed_id
                 AND te.trip_id = t.trip_id
                LEFT JOIN vehicle_classes vc
                  ON vc.feed_id = te.feed_id
                 AND vc.vehicle_class_id = te.vehicle_class_id
                WHERE st.feed_id = ? AND st.stop_id = ?
                  AND t.route_id = ?
                  AND t.service_id IN (
                      {GtfsDatabase.placeholders(service_ids)}
                  )
                  AND (
                      t.direction_id = ?
                      OR (t.direction_id IS NULL AND ? IS NULL)
                  )
                  AND {self._visible_stop_filter('st')}
                ORDER BY st.departure_time
            """,
            [
                feed_id,
                str(stop['stop_id']),
                str(route['route_id']),
                *service_ids,
                selected_trip['direction_id'],
                selected_trip['direction_id']
            ]
        ).fetchall()
        return [
            PublicTransportDepartureTime(
                departure_time=self._clock(str(row['departure_time'])),
                is_high_floor=(
                    row['low_floor'] is not None
                    and int(row['low_floor']) == 0
                ),
                url=self._url(
                    'ride',
                    feed=feed_id,
                    trip=str(row['trip_id']),
                    date=service_date.isoformat()
                ),
                variant=self._variant_description(row)
            )
            for row in rows
            if self._clock(str(row['departure_time'])) is not None
        ]

    #endregion Timetables

    #region Stops

    def stops(self) -> list[PublicTransportStop]:
        """Builds grouped stops and platforms from relational GTFS data."""
        with self._connection() as connection:
            feed_id = self._active_feed(connection, date.today())
            stop_rows = connection.execute(
                """
                    SELECT s.*, se.city,
                           se.platform_code AS extended_platform
                    FROM stops s
                    LEFT JOIN stop_extensions se
                      ON se.feed_id = s.feed_id
                     AND se.stop_id = s.stop_id
                    WHERE s.feed_id = ? AND s.name <> ''
                    ORDER BY se.city, s.name, se.platform_code, s.stop_code
                """,
                (feed_id,)
            ).fetchall()
            line_rows = connection.execute(
                f"""
                    SELECT DISTINCT st.stop_id, r.*, re.line_type
                    FROM stop_times st
                    JOIN trips t
                      ON t.feed_id = st.feed_id
                     AND t.trip_id = st.trip_id
                    JOIN routes r
                      ON r.feed_id = t.feed_id
                     AND r.route_id = t.route_id
                    LEFT JOIN route_extensions re
                      ON re.feed_id = r.feed_id
                     AND re.route_id = r.route_id
                    WHERE st.feed_id = ?
                      AND {self._visible_stop_filter('st')}
                """,
                (feed_id,)
            ).fetchall()
        lines_by_stop: dict[
            str,
            dict[str, PublicTransportBaseLine]
        ] = defaultdict(dict)
        for row in line_rows:
            lines_by_stop[str(row['stop_id'])][str(row['route_id'])] = (
                self._base_line(row)
            )
        grouped: dict[
            tuple[str, str],
            list[PublicTransportStopPlatform]
        ] = defaultdict(list)
        display: dict[tuple[str, str], tuple[str, PublicTransportCity]] = {}
        for row in stop_rows:
            city = self._city(str(row['city'] or ''))
            name = str(row['name']).strip()
            key = (city.name.casefold(), name.casefold())
            display.setdefault(key, (name, city))
            grouped[key].append(PublicTransportStopPlatform(
                name=self._platform(row),
                lines=sorted(
                    lines_by_stop.get(str(row['stop_id']), {}).values(),
                    key=lambda item: self._line_sort_key(item.line)
                ),
                url_all=self._url(
                    'stop',
                    feed=feed_id,
                    stop=str(row['stop_id'])
                ),
                url_chrono='',
                latitude=(
                    float(row['latitude'])
                    if row['latitude'] is not None else None
                ),
                longitude=(
                    float(row['longitude'])
                    if row['longitude'] is not None else None
                )
            ))
        return [
            PublicTransportStop(
                name=display[key][0],
                city=display[key][1],
                platforms=sorted(
                    platforms,
                    key=lambda item: item.name
                )
            )
            for key, platforms in sorted(
                grouped.items(),
                key=lambda item: (
                    display[item[0]][1].name.casefold(),
                    display[item[0]][0].casefold()
                )
            )
        ]

    def stop_all(self, url: str) -> PublicTransportStopAll:
        """Builds all line-direction departures for one platform."""
        service_date = self._selected_date(url)
        with self._connection() as connection:
            feed_id = self._feed_reference(
                connection,
                url,
                service_date
            )
            stop = self._stop_reference(connection, url, feed_id)
            if stop is None:
                raise ValueError('Nie znaleziono przystanku w danych GTFS GZM.')
            service_ids = self._service_ids(
                connection,
                feed_id,
                service_date
            )
            rows = []
            if service_ids:
                rows = connection.execute(
                    f"""
                        SELECT r.*, re.line_type, t.trip_id, t.headsign,
                               t.direction_id, t.wheelchair_accessible,
                               st.departure_time,
                               COALESCE(te.variant_code, '') variant_code,
                               vc.low_floor
                        FROM stop_times st
                        JOIN trips t
                          ON t.feed_id = st.feed_id
                         AND t.trip_id = st.trip_id
                        JOIN routes r
                          ON r.feed_id = t.feed_id
                         AND r.route_id = t.route_id
                        LEFT JOIN route_extensions re
                          ON re.feed_id = r.feed_id
                         AND re.route_id = r.route_id
                        LEFT JOIN trip_extensions te
                          ON te.feed_id = t.feed_id
                         AND te.trip_id = t.trip_id
                        LEFT JOIN vehicle_classes vc
                          ON vc.feed_id = te.feed_id
                         AND vc.vehicle_class_id = te.vehicle_class_id
                        WHERE st.feed_id = ? AND st.stop_id = ?
                          AND t.service_id IN (
                              {GtfsDatabase.placeholders(service_ids)}
                          )
                          AND {self._visible_stop_filter('st')}
                        ORDER BY r.short_name, t.direction_id,
                                 t.headsign, st.departure_time
                    """,
                    [
                        feed_id,
                        str(stop['stop_id']),
                        *service_ids
                    ]
                ).fetchall()
        entries: dict[tuple[str, str, Any], dict[str, Any]] = {}
        for row in rows:
            key = (
                str(row['route_id']),
                str(row['headsign'] or ''),
                row['direction_id']
            )
            item = entries.setdefault(key, {
                'route': row,
                'trip_id': str(row['trip_id']),
                'departures': []
            })
            departure_time = self._clock(str(row['departure_time']))
            if departure_time is None:
                continue
            item['departures'].append(PublicTransportDepartureTime(
                departure_time=departure_time,
                is_high_floor=(
                    row['low_floor'] is not None
                    and int(row['low_floor']) == 0
                ),
                url=self._url(
                    'ride',
                    feed=feed_id,
                    trip=str(row['trip_id']),
                    date=service_date.isoformat()
                ),
                variant=self._variant_description(row)
            ))
        mapped: dict[
            PublicTransportBaseLine,
            PublicTransportDateTimetable
        ] = {}
        for item in entries.values():
            row = item['route']
            departures = item['departures']
            line = self._base_line(
                row,
                item['trip_id'],
                service_date
            )
            variants = list(dict.fromkeys(
                departure.variant
                for departure in departures
                if departure.variant
            ))
            mapped[line] = PublicTransportDateTimetable(
                date=service_date,
                direction_name=str(row['headsign'] or ''),
                effective_date_from=service_date,
                effective_date_to=service_date,
                departures=departures,
                variants=variants
            )
        return PublicTransportStopAll(
            stop_name=str(stop['name']),
            platform=self._platform(stop),
            dates=self._dates('stop', {
                'stop': str(stop['stop_id'])
            }),
            lines=mapped,
            latitude=(
                float(stop['latitude'])
                if stop['latitude'] is not None else None
            ),
            longitude=(
                float(stop['longitude'])
                if stop['longitude'] is not None else None
            )
        )

    #endregion Stops

    #region Rides

    def ride(self, url: str) -> PublicTransportRide:
        """Builds a complete ride from one GTFS trip."""
        with self._connection() as connection:
            service_date = self._selected_date(url)
            feed_id = self._feed_reference(
                connection,
                url,
                service_date
            )
            trip = self._trip_reference(connection, url, feed_id)
            if trip is None:
                raise ValueError('Nie znaleziono przejazdu w danych GTFS GZM.')
            metadata = connection.execute(
                """
                    SELECT r.*, te.operator_id, te.vehicle_class_id,
                           o.name operator_name,
                           vc.long_name vehicle_name
                    FROM trips t
                    JOIN routes r
                      ON r.feed_id = t.feed_id
                     AND r.route_id = t.route_id
                    LEFT JOIN trip_extensions te
                      ON te.feed_id = t.feed_id
                     AND te.trip_id = t.trip_id
                    LEFT JOIN operators o
                      ON o.feed_id = te.feed_id
                     AND o.operator_id = te.operator_id
                    LEFT JOIN vehicle_classes vc
                      ON vc.feed_id = te.feed_id
                     AND vc.vehicle_class_id = te.vehicle_class_id
                    WHERE t.feed_id = ? AND t.trip_id = ?
                """,
                (feed_id, str(trip['trip_id']))
            ).fetchone()
            rows = connection.execute(
                f"""
                    SELECT s.*, se.city,
                           se.platform_code AS extended_platform,
                           st.arrival_time, st.departure_time,
                           st.stop_sequence, st.shape_dist_traveled
                    FROM stop_times st
                    JOIN stops s
                      ON s.feed_id = st.feed_id
                     AND s.stop_id = st.stop_id
                    LEFT JOIN stop_extensions se
                      ON se.feed_id = s.feed_id
                     AND se.stop_id = s.stop_id
                    WHERE st.feed_id = ? AND st.trip_id = ?
                      AND {self._visible_stop_filter('st')}
                    ORDER BY st.stop_sequence
                """,
                (feed_id, str(trip['trip_id']))
            ).fetchall()
        if metadata is None or not rows:
            raise ValueError('Przejazd GTFS GZM nie zawiera przystanków.')
        first_seconds = self._seconds(str(rows[0]['departure_time']))
        previous_seconds = first_seconds
        previous_distance = float(rows[0]['shape_dist_traveled'] or 0.0)
        ride_stops: list[PublicTransportRideStop] = []
        cities: list[PublicTransportCity] = []
        for row in rows:
            current_seconds = self._seconds(str(row['departure_time']))
            current_distance = float(row['shape_dist_traveled'] or 0.0)
            city = self._city(str(row['city'] or ''))
            if city.name not in {item.name for item in cities}:
                cities.append(city)
            ride_stops.append(PublicTransportRideStop(
                stop=str(row['name']),
                departure_time=self._clock(str(row['departure_time'])),
                travel_time=max(
                    0,
                    round((current_seconds - previous_seconds) / 60)
                ),
                travel_time_sum=max(
                    0,
                    round((current_seconds - first_seconds) / 60)
                ),
                distance=max(0.0, current_distance - previous_distance),
                distance_sum=max(0.0, current_distance),
                city=city,
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
            previous_distance = current_distance
        first = ride_stops[0]
        return PublicTransportRide(
            line=self._public_line_name(
                str(metadata['short_name']),
                int(metadata['route_type'])
            ),
            type=self._transport_type(int(metadata['route_type'])),
            stop_name=first.stop,
            platform=self._platform(rows[0]),
            departure_time=first.departure_time,
            cities=cities,
            next_stops=ride_stops[1:],
            carrier=str(metadata['operator_name'] or ''),
            vehicle_type=str(metadata['vehicle_name'] or ''),
            latitude=first.latitude,
            longitude=first.longitude
        )

    #endregion Rides

    #region Realtime lookup maps

    def realtime_maps(self) -> tuple[
        dict[tuple[str, str], str],
        dict[tuple[str, str], str],
        dict[tuple[str, str], PublicTransportType],
        dict[tuple[str, str], PublicTransportType]
    ]:
        """Returns identifiers required to map GTFS-RT entities."""
        with self._connection() as connection:
            feed_id = self._active_feed(connection, date.today())
            route_rows = connection.execute(
                """
                    SELECT route_id, short_name, route_type
                    FROM routes WHERE feed_id = ?
                """,
                (feed_id,)
            ).fetchall()
            trip_rows = connection.execute(
                """
                    SELECT t.trip_id, r.short_name, r.route_type
                    FROM trips t
                    JOIN routes r
                      ON r.feed_id = t.feed_id
                     AND r.route_id = t.route_id
                    WHERE t.feed_id = ?
                """,
                (feed_id,)
            ).fetchall()
        route_names = {
            (self.FEED_ID, str(row['route_id'])): self._public_line_name(
                str(row['short_name']),
                int(row['route_type'])
            )
            for row in route_rows
        }
        trip_names = {
            (self.FEED_ID, str(row['trip_id'])): self._public_line_name(
                str(row['short_name']),
                int(row['route_type'])
            )
            for row in trip_rows
        }
        route_types = {
            (self.FEED_ID, str(row['route_id'])): self._transport_type(
                int(row['route_type'])
            )
            for row in route_rows
        }
        trip_types = {
            (self.FEED_ID, str(row['trip_id'])): self._transport_type(
                int(row['route_type'])
            )
            for row in trip_rows
        }
        return route_names, trip_names, route_types, trip_types

    #endregion Realtime lookup maps

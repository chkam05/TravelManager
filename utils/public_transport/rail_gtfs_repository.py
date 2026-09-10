"""Application-model adapter for the shared Polish railway GTFS caches."""
from __future__ import annotations

from collections import defaultdict
from datetime import date, datetime, time, timedelta
from pathlib import Path
import sqlite3
from typing import Any
from urllib.parse import parse_qs, urlencode, urlparse
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from core.gtfs_database import GtfsDatabase
from models.public_transport.public_transport_base_line import PublicTransportBaseLine
from models.public_transport.public_transport_city import PublicTransportCity
from models.public_transport.public_transport_coordinate import PublicTransportCoordinate
from models.public_transport.public_transport_departure_time import PublicTransportDepartureTime
from models.public_transport.public_transport_direction import PublicTransportDirection
from models.public_transport.public_transport_direction_stop import PublicTransportDirectionStop
from models.public_transport.public_transport_line import PublicTransportLine
from models.public_transport.public_transport_date_timetable import PublicTransportDateTimetable
from models.public_transport.public_transport_line_stop_timetable import PublicTransportLineStopTimetable
from models.public_transport.public_transport_ride import PublicTransportRide
from models.public_transport.public_transport_ride_stop import PublicTransportRideStop
from models.public_transport.public_transport_stop import PublicTransportStop
from models.public_transport.public_transport_stop_all import PublicTransportStopAll
from models.public_transport.public_transport_stop_platform import PublicTransportStopPlatform
from resources.public_transport.public_transport_messages import PublicTransportValueError
from resources.public_transport.public_transport_type import PublicTransportType
from resources.public_transport.rail_gtfs_sources import (
    RailGtfsSources,
    RailProviderMapping,
)
from utils.public_transport.rail_gtfs_cache import RailGtfsCache
from utils.public_transport.rail_realtime import RailRealtime, RailTripUpdate
from utils.public_transport.download_progress import PublicTransportDownloadProgress


class RailGtfsRepository:
    """Queries one operator without leaking trips from a shared source."""

    DATE_RANGE_DAYS = 14
    _TRAIN_ROUTE_TYPES = {
        2, 100, 101, 102, 103, 104, 105, 106, 107, 108,
        109, 110, 111, 112, 113, 114, 115, 116, 117,
    }
    _LONG_DISTANCE_PROVIDERS = {
        'rail_pkp_intercity', 'rail_regiojet', 'rail_leo_express'
    }

    def __init__(
        self,
        provider_id: str,
        database_path: Path | None = None,
        realtime: bool | None = None
    ) -> None:
        self.provider: RailProviderMapping = RailGtfsSources.provider(provider_id)
        self._database_path = database_path
        # Injected fixture databases stay deterministic unless explicitly opted in.
        self._realtime = database_path is None if realtime is None else realtime

    def _path(self, refresh: bool = False) -> Path:
        return self._database_path or RailGtfsCache.ensure_database(
            self.provider.source_id,
            refresh=refresh,
            cancelled=PublicTransportDownloadProgress.current_cancelled()
        )

    def _connection(self, refresh: bool = False) -> sqlite3.Connection:
        return GtfsDatabase.connect(self._path(refresh))

    @staticmethod
    def _query(url: str) -> dict[str, str]:
        return {
            key: values[0]
            for key, values in parse_qs(
                urlparse(url).query,
                keep_blank_values=True
            ).items()
            if values
        }

    def _url(self, view: str, **values: object) -> str:
        query = {
            'rail_view': view,
            'source': self.provider.source_id,
            'provider': self.provider.provider_id,
            'agency': ','.join(self.provider.agency_ids),
        }
        query.update({
            key: str(value)
            for key, value in values.items()
            if value not in (None, '')
        })
        return f'https://mkuran.pl/gtfs/travel-manager?{urlencode(query)}'

    def _validated_query(self, url: str, view: str) -> dict[str, str]:
        values = self._query(url)
        if (
            values.get('rail_view') != view
            or values.get('source') != self.provider.source_id
            or values.get('provider') != self.provider.provider_id
            or values.get('agency') != ','.join(self.provider.agency_ids)
        ):
            raise PublicTransportValueError(
                'PUBLIC_TRANSPORT_ERROR.INVALID_GTFS_TIMETABLE_URL'
            )
        return values

    def _service_ids(
        self,
        connection: sqlite3.Connection,
        service_date: date
    ) -> list[str]:
        RailGtfsCache.require_service_date(
            self.provider.source_id,
            service_date,
            self._path()
        )
        return sorted(GtfsDatabase.active_service_ids(
            connection,
            self.provider.source_id,
            service_date
        ))

    @classmethod
    def _transport_type(cls, route_type: int) -> PublicTransportType:
        if route_type in cls._TRAIN_ROUTE_TYPES:
            return PublicTransportType.TRAIN
        # Replacement bus routes remain buses instead of being mislabeled.
        return PublicTransportType.BUS

    @staticmethod
    def _clock(value: str) -> time | None:
        try:
            hours, minutes, seconds = (int(part) for part in value.split(':', 2))
            return time(hours % 24, minutes, seconds)
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _seconds(value: str) -> int:
        try:
            hours, minutes, seconds = (int(part) for part in value.split(':', 2))
            return hours * 3600 + minutes * 60 + seconds
        except (TypeError, ValueError):
            return 0

    @staticmethod
    def _city() -> PublicTransportCity:
        return PublicTransportCity(name='Koleje', color='#44546A')

    @staticmethod
    def _line_name(row: sqlite3.Row) -> str:
        return str(row['short_name'] or row['long_name'] or row['route_id'])

    @staticmethod
    def _train_name(row: sqlite3.Row) -> str:
        number = str(row['short_name'] or row['train_number'] or '').strip()
        name = str(row['train_name'] or '').strip()
        if number and name and name.casefold() not in number.casefold():
            return f'{number} · {name}'
        return number or name

    @staticmethod
    def _listed_train_name(row: sqlite3.Row) -> str:
        number = str(row['trip_short_name'] or row['train_number'] or '').strip()
        name = str(row['train_name'] or '').strip()
        if number and name and name.casefold() not in number.casefold():
            return f'{number} · {name}'
        return number or name

    def _trip_relations(
        self,
        connection: sqlite3.Connection,
        trip_ids: list[str]
    ) -> dict[str, tuple[str, str]]:
        """Returns the first and last station name for each listed trip."""
        relations: dict[str, list[str]] = defaultdict(list)
        for offset in range(0, len(trip_ids), 800):
            chunk = trip_ids[offset:offset + 800]
            rows = connection.execute(
                f"""
                    SELECT st.trip_id,
                           COALESCE(parent.name, stop.name) AS station_name
                    FROM stop_times st
                    JOIN stops stop
                      ON stop.feed_id = st.feed_id
                     AND stop.stop_id = st.stop_id
                    LEFT JOIN stops parent
                      ON parent.feed_id = stop.feed_id
                     AND parent.stop_id = stop.parent_station
                    WHERE st.feed_id = ?
                      AND st.trip_id IN ({GtfsDatabase.placeholders(chunk)})
                      AND NOT (st.pickup_type = 1 AND st.drop_off_type = 1)
                    ORDER BY st.trip_id, st.stop_sequence
                """,
                (self.provider.source_id, *chunk)
            ).fetchall()
            for row in rows:
                relations[str(row['trip_id'])].append(str(row['station_name']))
        return {
            trip_id: (stations[0], stations[-1])
            for trip_id, stations in relations.items()
            if len(stations) > 1
        }

    def download_lines(
        self,
        url: str | None = None,
        refresh: bool = False,
        service_date: date | None = None
    ) -> list[PublicTransportBaseLine]:
        """Returns routes active for this operator and service date."""
        del url
        selected_date = service_date or date.today()
        with self._connection(refresh) as connection:
            service_ids = self._service_ids(connection, selected_date)
            if self.provider.provider_id in self._LONG_DISTANCE_PROVIDERS:
                rows = connection.execute(
                    f"""
                        SELECT r.*, t.trip_id, t.short_name AS trip_short_name,
                               t.train_number, t.train_name
                        FROM routes r JOIN trips t
                          ON t.feed_id = r.feed_id AND t.route_id = r.route_id
                        WHERE r.feed_id = ?
                          AND r.agency_id IN ({GtfsDatabase.placeholders(self.provider.agency_ids)})
                          AND t.service_id IN ({GtfsDatabase.placeholders(service_ids)})
                        ORDER BY t.short_name, t.train_number, t.trip_id
                    """,
                    (self.provider.source_id, *self.provider.agency_ids, *service_ids)
                ).fetchall()
                unique = {}
                for row in rows:
                    identity = (str(row['route_id']), str(row['trip_short_name']))
                    unique.setdefault(identity, row)
                relations = self._trip_relations(
                    connection,
                    [str(row['trip_id']) for row in unique.values()]
                )
                return [
                    PublicTransportBaseLine(
                        line=self._listed_train_name(row),
                        type=self._transport_type(int(row['route_type'])),
                        url=self._url(
                            'line', route=row['route_id'],
                            number=row['trip_short_name'],
                            date=selected_date.isoformat()
                        ),
                        free_of_charge=False,
                        updated=False,
                        direction=' – '.join(
                            relations.get(str(row['trip_id']), ())
                        ),
                        sort_name=str(row['train_name'] or '').strip()
                    )
                    for row in unique.values()
                ]
            rows = connection.execute(
                f"""
                    SELECT r.*, t.trip_id
                    FROM routes r
                    JOIN trips t
                      ON t.feed_id = r.feed_id AND t.route_id = r.route_id
                    WHERE r.feed_id = ?
                      AND r.agency_id IN ({GtfsDatabase.placeholders(self.provider.agency_ids)})
                      AND t.service_id IN ({GtfsDatabase.placeholders(service_ids)})
                    ORDER BY r.short_name, r.long_name, r.route_id
                """,
                (
                    self.provider.source_id,
                    *self.provider.agency_ids,
                    *service_ids
                )
            ).fetchall()
            unique_routes: dict[str, sqlite3.Row] = {}
            route_trips: dict[str, list[str]] = defaultdict(list)
            for row in rows:
                route_id = str(row['route_id'])
                unique_routes.setdefault(route_id, row)
                route_trips[route_id].append(str(row['trip_id']))
            relations = self._trip_relations(
                connection,
                [trip_id for trip_ids in route_trips.values() for trip_id in trip_ids]
            )
        return [
            PublicTransportBaseLine(
                line=self._line_name(row),
                type=self._transport_type(int(row['route_type'])),
                url=self._url(
                    'line', route=row['route_id'], date=selected_date.isoformat()
                ),
                free_of_charge=False,
                updated=False,
                direction=self._route_relation(
                    route_trips[str(row['route_id'])], relations
                ),
                sort_name=''
            )
            for row in unique_routes.values()
        ]

    @staticmethod
    def _route_relation(
        trip_ids: list[str],
        relations: dict[str, tuple[str, str]]
    ) -> str:
        """Collapses opposite trips into stable endpoint relations."""
        pairs: list[tuple[str, str]] = []
        seen: set[tuple[str, str]] = set()
        for trip_id in trip_ids:
            pair = relations.get(trip_id)
            if not pair:
                continue
            identity = tuple(sorted(pair, key=str.casefold))
            if identity not in seen:
                seen.add(identity)
                pairs.append(identity)
        return ' • '.join(' – '.join(pair) for pair in pairs)

    def download_stops(
        self,
        url: str | None = None,
        progress_callback=None,
        refresh: bool = False,
        service_date: date | None = None
    ) -> list[PublicTransportStop]:
        """Groups distinct railway platforms under their parent stations."""
        del url, progress_callback
        selected_date = service_date or date.today()
        with self._connection(refresh) as connection:
            service_ids = self._service_ids(connection, selected_date)
            rows = connection.execute(
                f"""
                    SELECT DISTINCT s.*, parent.name AS station_name,
                           r.route_id, r.short_name AS route_short_name,
                           r.long_name AS route_long_name, r.route_type,
                           t.short_name AS trip_short_name,
                           t.train_number, t.train_name
                    FROM stop_times st
                    JOIN stops s
                      ON s.feed_id = st.feed_id AND s.stop_id = st.stop_id
                    LEFT JOIN stops parent
                      ON parent.feed_id = s.feed_id
                     AND parent.stop_id = s.parent_station
                    JOIN trips t
                      ON t.feed_id = st.feed_id AND t.trip_id = st.trip_id
                    JOIN routes r
                      ON r.feed_id = t.feed_id AND r.route_id = t.route_id
                    WHERE r.feed_id = ?
                      AND r.agency_id IN ({GtfsDatabase.placeholders(self.provider.agency_ids)})
                      AND t.service_id IN ({GtfsDatabase.placeholders(service_ids)})
                      AND NOT (st.pickup_type = 1 AND st.drop_off_type = 1)
                    ORDER BY COALESCE(parent.name, s.name), s.platform_code, s.stop_id
                """,
                (
                    self.provider.source_id,
                    *self.provider.agency_ids,
                    *service_ids
                )
            ).fetchall()

        grouped: dict[str, dict[str, Any]] = {}
        for row in rows:
            station_id = str(row['parent_station'] or row['stop_id'])
            station = grouped.setdefault(station_id, {
                'name': str(row['station_name'] or row['name']),
                'platforms': {}
            })
            stop_id = str(row['stop_id'])
            platform = station['platforms'].setdefault(stop_id, {
                'name': str(row['platform_code'] or ''),
                'latitude': row['latitude'],
                'longitude': row['longitude'],
                'lines': {}
            })
            route_id = str(row['route_id'])
            long_distance = self.provider.provider_id in self._LONG_DISTANCE_PROVIDERS
            train_number = str(
                row['trip_short_name'] or row['train_number'] or ''
            ) if long_distance else ''
            identity = f'{route_id}:{train_number}' if train_number else route_id
            line_name = (
                self._listed_train_name(row)
                if train_number
                else str(
                    row['route_short_name']
                    or row['route_long_name']
                    or route_id
                )
            )
            platform['lines'][identity] = PublicTransportBaseLine(
                line=line_name,
                type=self._transport_type(int(row['route_type'])),
                url=self._url(
                    'line', route=route_id, number=train_number,
                    date=selected_date.isoformat()
                ),
                free_of_charge=False,
                updated=False
            )
        return [
            PublicTransportStop(
                name=station['name'],
                city=self._city(),
                platforms=[
                    PublicTransportStopPlatform(
                        name=item['name'],
                        lines=list(item['lines'].values()),
                        url_all=self._url(
                            'stop', stop=stop_id, date=selected_date.isoformat()
                        ),
                        url_chrono=self._url(
                            'stop', stop=stop_id, date=selected_date.isoformat()
                        ),
                        latitude=(float(item['latitude']) if item['latitude'] is not None else None),
                        longitude=(float(item['longitude']) if item['longitude'] is not None else None)
                    )
                    for stop_id, item in station['platforms'].items()
                ]
            )
            for station in grouped.values()
        ]

    def download_line(self, url: str) -> PublicTransportLine:
        """Builds trip variants and stop sequences for one railway route."""
        values = self._validated_query(url, 'line')
        route_id = values.get('route', '')
        selected_trip = values.get('trip', '')
        selected_number = values.get('number', '')
        try:
            service_date = date.fromisoformat(values.get('date', ''))
        except ValueError:
            raise PublicTransportValueError(
                'PUBLIC_TRANSPORT_ERROR.INVALID_GTFS_LINE_ID'
            )
        with self._connection() as connection:
            service_ids = self._service_ids(connection, service_date)
            route = connection.execute(
                f"""
                    SELECT * FROM routes WHERE feed_id = ? AND route_id = ?
                      AND agency_id IN ({GtfsDatabase.placeholders(self.provider.agency_ids)})
                """,
                (self.provider.source_id, route_id, *self.provider.agency_ids)
            ).fetchone()
            if route is None:
                raise PublicTransportValueError(
                    'PUBLIC_TRANSPORT_ERROR.GTFS_LINE_NOT_FOUND'
                )
            trips = connection.execute(
                f"""
                    SELECT * FROM trips WHERE feed_id = ? AND route_id = ?
                      AND service_id IN ({GtfsDatabase.placeholders(service_ids)})
                    ORDER BY short_name, headsign, trip_id
                """,
                (self.provider.source_id, route_id, *service_ids)
            ).fetchall()
            if selected_trip:
                trips = [row for row in trips if row['trip_id'] == selected_trip]
            elif selected_number:
                trips = [
                    row for row in trips
                    if selected_number in {
                        str(row['short_name'] or ''),
                        str(row['train_number'] or '')
                    }
                ]
            if not trips:
                raise PublicTransportValueError(
                    'PUBLIC_TRANSPORT_ERROR.GTFS_LINE_NOT_FOUND'
                )
            trip_ids = [str(row['trip_id']) for row in trips]
            signatures: dict[str, list[str]] = defaultdict(list)
            if trip_ids:
                stop_rows = connection.execute(
                    f"""
                        SELECT st.trip_id, st.stop_id, s.parent_station
                        FROM stop_times st JOIN stops s
                          ON s.feed_id = st.feed_id AND s.stop_id = st.stop_id
                        WHERE st.feed_id = ?
                          AND trip_id IN ({GtfsDatabase.placeholders(trip_ids)})
                          AND NOT (st.pickup_type = 1 AND st.drop_off_type = 1)
                        ORDER BY st.trip_id, st.stop_sequence
                    """,
                    (self.provider.source_id, *trip_ids)
                ).fetchall()
                for stop_row in stop_rows:
                    signatures[str(stop_row['trip_id'])].append(str(
                        stop_row['parent_station'] or stop_row['stop_id']
                    ))
            representatives = {}
            for trip in trips:
                signature = tuple(signatures.get(str(trip['trip_id']), ()))
                relation = (
                    trip['direction_id'],
                    signature[0] if signature else '',
                    signature[-1] if signature else ''
                )
                previous = representatives.get(relation)
                if (
                    previous is None
                    or len(signature) > len(signatures.get(str(previous['trip_id']), ()))
                ):
                    representatives[relation] = trip
            trips = list(representatives.values())
            directions = [
                self._direction(
                    connection, route, trip, service_date, selected_number
                )
                for trip in trips
            ]
            directions.sort(key=lambda direction: direction.name.casefold())
        display_line = (
            self._train_name(trips[0])
            if selected_number and trips else self._line_name(route)
        )
        return PublicTransportLine(
            line=display_line,
            type=self._transport_type(int(route['route_type'])),
            announcements=[],
            directions=directions,
            route_variants={},
            route_variant_groups={},
            dates=self._date_urls(
                'line', route=route_id, number=selected_number
            )
        )

    def _direction(
        self,
        connection: sqlite3.Connection,
        route: sqlite3.Row,
        trip: sqlite3.Row,
        service_date: date,
        selected_number: str = ''
    ) -> PublicTransportDirection:
        rows = connection.execute(
            """
                SELECT st.*, s.name, s.platform_code, s.latitude, s.longitude
                FROM stop_times st JOIN stops s
                  ON s.feed_id = st.feed_id AND s.stop_id = st.stop_id
                WHERE st.feed_id = ? AND st.trip_id = ?
                  AND NOT (st.pickup_type = 1 AND st.drop_off_type = 1)
                ORDER BY st.stop_sequence
            """,
            (self.provider.source_id, trip['trip_id'])
        ).fetchall()
        shape = connection.execute(
            """
                SELECT latitude, longitude FROM shapes
                WHERE feed_id = ? AND shape_id = ? ORDER BY point_sequence
            """,
            (self.provider.source_id, trip['shape_id'])
        ).fetchall() if trip['shape_id'] else []
        approximate = not bool(shape)
        route_points = shape or [
            row for row in rows
            if row['latitude'] is not None and row['longitude'] is not None
        ]
        transport_type = self._transport_type(int(route['route_type']))
        return PublicTransportDirection(
            name=(
                f"{rows[0]['name']} → {rows[-1]['name']}"
                if rows else str(trip['headsign'] or self._train_name(trip))
            ),
            cities=[self._city()],
            stops=[
                PublicTransportDirectionStop(
                    line=self._line_name(route),
                    type=transport_type,
                    city=self._city(),
                    is_variant=False,
                    name=str(row['name']),
                    platform=str(row['platform'] or row['platform_code'] or ''),
                    url=self._url(
                        'line-stop', route=route['route_id'],
                        trip=trip['trip_id'], stop=row['stop_id'],
                        number=selected_number,
                        date=service_date.isoformat()
                    )
                )
                for row in rows
            ],
            route=[
                PublicTransportCoordinate(
                    latitude=float(row['latitude']),
                    longitude=float(row['longitude'])
                )
                for row in route_points
            ],
            route_is_approximate=approximate
        )

    def _date_urls(self, view: str, **values: object) -> dict[date, str]:
        with self._connection() as connection:
            coverage = GtfsDatabase.service_range(
                connection, self.provider.source_id
            )
        if not coverage:
            return {}
        start = max(date.today(), coverage[0])
        end = min(coverage[1], start + timedelta(days=self.DATE_RANGE_DAYS - 1))
        return {
            day: self._url(view, **values, date=day.isoformat())
            for offset in range((end - start).days + 1)
            if (day := start + timedelta(days=offset))
        }

    def operational_datetime(
        self,
        service_date: date,
        gtfs_time: str
    ) -> datetime:
        """Converts an extended GTFS time in the agency's declared timezone."""
        with self._connection() as connection:
            row = connection.execute(
                f"""
                    SELECT timezone FROM agencies WHERE feed_id = ?
                      AND agency_id IN ({GtfsDatabase.placeholders(self.provider.agency_ids)})
                    ORDER BY agency_id LIMIT 1
                """,
                (self.provider.source_id, *self.provider.agency_ids)
            ).fetchone()
        timezone_name = str(row['timezone'] or 'Europe/Warsaw') if row else 'Europe/Warsaw'
        try:
            zone = ZoneInfo(timezone_name)
        except ZoneInfoNotFoundError:
            zone = ZoneInfo('Europe/Warsaw')
        seconds = self._seconds(gtfs_time)
        return datetime.combine(service_date, time(), tzinfo=zone) + timedelta(seconds=seconds)

    def _trip_update(
        self,
        trip_id: str,
        service_date: date,
        *numbers: object
    ) -> tuple[RailTripUpdate | None, str, bool]:
        if not self._realtime:
            return None, '', False
        # Browsing a timetable is strictly offline. Realtime is populated only
        # by the explicit provider update action.
        snapshot = RailRealtime.cached_snapshot(self.provider.source_id)
        update = RailRealtime.match(
            snapshot,
            trip_id,
            service_date,
            self.provider.agency_ids,
            tuple(str(value or '').strip() for value in numbers)
        )
        stale = bool(snapshot is not None and not snapshot.is_fresh())
        return (update,
                snapshot.updated_at.isoformat(timespec='minutes') if snapshot else '',
                stale)

    def _realtime_clock(
        self,
        predicted: datetime | None,
        service_date: date,
        scheduled: str
    ) -> tuple[time | None, int | None]:
        planned_clock = self._clock(scheduled)
        if predicted is None:
            return planned_clock, None
        planned = self.operational_datetime(service_date, scheduled)
        local = predicted.astimezone(planned.tzinfo)
        return local.timetz().replace(tzinfo=None), round((predicted - planned).total_seconds() / 60)

    def download_ride(self, url: str) -> PublicTransportRide:
        """Loads one scoped train run while preserving its operational clock."""
        values = self._validated_query(url, 'ride')
        trip_id = values.get('trip', '')
        selected_stop_id = values.get('stop', '')
        try:
            service_date = date.fromisoformat(values.get('date', ''))
        except ValueError:
            raise PublicTransportValueError(
                'PUBLIC_TRANSPORT_ERROR.INVALID_GTFS_TIMETABLE_URL'
            )
        with self._connection() as connection:
            service_ids = self._service_ids(connection, service_date)
            trip = connection.execute(
                f"""
                    SELECT t.*, r.agency_id, r.route_type,
                           r.short_name AS route_short_name,
                           a.name AS agency_name
                    FROM trips t
                    JOIN routes r
                      ON r.feed_id = t.feed_id AND r.route_id = t.route_id
                    LEFT JOIN agencies a
                      ON a.feed_id = r.feed_id AND a.agency_id = r.agency_id
                    WHERE t.feed_id = ? AND t.trip_id = ?
                      AND r.agency_id IN ({GtfsDatabase.placeholders(self.provider.agency_ids)})
                      AND t.service_id IN ({GtfsDatabase.placeholders(service_ids)})
                """,
                (
                    self.provider.source_id,
                    trip_id,
                    *self.provider.agency_ids,
                    *service_ids
                )
            ).fetchone()
            if trip is None:
                raise PublicTransportValueError(
                    'PUBLIC_TRANSPORT_ERROR.GTFS_TRIP_NOT_FOUND'
                )
            rows = connection.execute(
                """
                    SELECT st.*, s.name, s.platform_code,
                           s.latitude, s.longitude
                    FROM stop_times st
                    JOIN stops s
                      ON s.feed_id = st.feed_id AND s.stop_id = st.stop_id
                    WHERE st.feed_id = ? AND st.trip_id = ?
                    ORDER BY st.stop_sequence
                """,
                (self.provider.source_id, trip_id)
            ).fetchall()
        if not rows:
            raise PublicTransportValueError(
                'PUBLIC_TRANSPORT_ERROR.GTFS_TRIP_NOT_FOUND'
            )
        selected_index = next((
            index for index, row in enumerate(rows)
            if str(row['stop_id']) == selected_stop_id
        ), 0)
        selected = rows[selected_index]
        trip_update, realtime_updated_at, realtime_stale = self._trip_update(
            trip_id, service_date, trip['short_name'], trip['train_number']
        )
        selected_update = trip_update.stop(
            int(selected['stop_sequence']), selected_stop_id
        ) if trip_update else None
        selected_scheduled = str(selected['departure_time'])
        selected_departure, selected_delay = self._realtime_clock(
            selected_update.departure if selected_update else None,
            service_date,
            selected_scheduled
        )
        start_seconds = self._seconds(str(selected['departure_time']))
        previous_seconds = start_seconds
        previous_distance = float(selected['shape_dist_traveled'] or 0.0)
        next_stops = []
        for row in rows[selected_index + 1:]:
            seconds = self._seconds(str(row['arrival_time'] or row['departure_time']))
            distance = float(row['shape_dist_traveled'] or previous_distance)
            stop_update = trip_update.stop(
                int(row['stop_sequence']), str(row['stop_id'])
            ) if trip_update else None
            scheduled_departure = str(row['departure_time'])
            effective_departure, delay = self._realtime_clock(
                (stop_update.departure or stop_update.arrival) if stop_update else None,
                service_date,
                scheduled_departure
            )
            next_stops.append(PublicTransportRideStop(
                stop=str(row['name']),
                departure_time=effective_departure,
                travel_time=max(0, (seconds - previous_seconds) // 60),
                travel_time_sum=max(0, (seconds - start_seconds) // 60),
                distance=max(0.0, distance - previous_distance),
                distance_sum=max(0.0, distance - float(selected['shape_dist_traveled'] or 0.0)),
                city=self._city(),
                latitude=float(row['latitude']) if row['latitude'] is not None else None,
                longitude=float(row['longitude']) if row['longitude'] is not None else None,
                scheduled_departure_time=(self._clock(scheduled_departure)
                                          if delay is not None else None),
                delay_minutes=delay,
                cancelled=bool(trip_update and (
                    trip_update.cancelled or stop_update and stop_update.cancelled
                ))
            ))
            previous_seconds = seconds
            previous_distance = distance
        return PublicTransportRide(
            line=self._train_name(trip) or str(trip['route_short_name']),
            type=self._transport_type(int(trip['route_type'])),
            stop_name=str(selected['name']),
            platform=str(selected['platform'] or selected['platform_code'] or ''),
            departure_time=selected_departure,
            cities=[self._city()],
            next_stops=next_stops,
            carrier=str(trip['agency_name'] or self.provider.display_name),
            vehicle_type=str(trip['category_code'] or ''),
            latitude=float(selected['latitude']) if selected['latitude'] is not None else None,
            longitude=float(selected['longitude']) if selected['longitude'] is not None else None,
            scheduled_departure_time=(self._clock(selected_scheduled)
                                      if selected_delay is not None else None),
            delay_minutes=selected_delay,
            cancelled=bool(trip_update and (
                trip_update.cancelled
                or selected_update and selected_update.cancelled
            )),
            realtime_updated_at=realtime_updated_at,
            realtime_stale=realtime_stale
        )

    def ride_url(
        self,
        trip_id: str,
        stop_id: str,
        service_date: date
    ) -> str:
        """Builds a provider-scoped ride reference for timetable models."""
        return self._url(
            'ride', trip=trip_id, stop=stop_id, date=service_date.isoformat()
        )

    def departures(
        self,
        stop_id: str,
        service_date: date,
        route_id: str = '',
        train_number: str = ''
    ) -> list[PublicTransportDepartureTime]:
        """Returns scoped departures, retaining each train as a separate run."""
        with self._connection() as connection:
            service_ids = self._service_ids(connection, service_date)
            rows = connection.execute(
                f"""
                    SELECT st.departure_time, st.stop_sequence, st.pickup_type,
                           t.trip_id, t.short_name, t.train_number,
                           t.train_name, t.headsign
                    FROM stop_times st
                    JOIN trips t
                      ON t.feed_id = st.feed_id AND t.trip_id = st.trip_id
                    JOIN routes r
                      ON r.feed_id = t.feed_id AND r.route_id = t.route_id
                    WHERE st.feed_id = ? AND st.stop_id = ?
                      AND r.agency_id IN ({GtfsDatabase.placeholders(self.provider.agency_ids)})
                      AND t.service_id IN ({GtfsDatabase.placeholders(service_ids)})
                      AND st.pickup_type <> 1
                      AND (? = '' OR r.route_id = ?)
                      AND (? = '' OR t.short_name = ? OR t.train_number = ?)
                    ORDER BY
                      CAST(SUBSTR(st.departure_time, 1, 2) AS INTEGER),
                      st.departure_time, t.trip_id
                """,
                (
                    self.provider.source_id,
                    stop_id,
                    *self.provider.agency_ids,
                    *service_ids,
                    route_id,
                    route_id,
                    train_number,
                    train_number,
                    train_number
                )
            ).fetchall()
        departures = []
        for row in rows:
            scheduled = str(row['departure_time'])
            update, updated_at, realtime_stale = self._trip_update(
                str(row['trip_id']), service_date,
                row['short_name'], row['train_number']
            )
            stop_update = update.stop(int(row['stop_sequence']), stop_id) if update else None
            effective, delay = self._realtime_clock(
                stop_update.departure if stop_update else None,
                service_date,
                scheduled
            )
            departures.append(PublicTransportDepartureTime(
                departure_time=effective,
                is_high_floor=False,
                url=self.ride_url(
                    str(row['trip_id']), stop_id, service_date
                ),
                variant=(
                    f"{self._train_name(row)} → {row['headsign']}"
                    if row['headsign']
                    else self._train_name(row)
                ),
                scheduled_departure_time=(self._clock(scheduled) if delay is not None else None),
                delay_minutes=delay,
                cancelled=bool(update and (
                    update.cancelled or stop_update and stop_update.cancelled
                )),
                realtime_updated_at=updated_at,
                realtime_stale=realtime_stale
            ))
        return departures

    def download_line_stop_timetable(
        self,
        url: str,
        include_announcement_content: bool = False
    ) -> PublicTransportLineStopTimetable:
        """Builds departures for one railway route and physical platform."""
        del include_announcement_content
        values = self._validated_query(url, 'line-stop')
        route_id = values.get('route', '')
        trip_id = values.get('trip', '')
        stop_id = values.get('stop', '')
        train_number = values.get('number', '')
        try:
            service_date = date.fromisoformat(values.get('date', ''))
        except ValueError:
            raise PublicTransportValueError(
                'PUBLIC_TRANSPORT_ERROR.INVALID_GTFS_TIMETABLE_URL'
            )
        with self._connection() as connection:
            service_ids = self._service_ids(connection, service_date)
            row = connection.execute(
                f"""
                    SELECT r.short_name AS line_name, r.long_name,
                           r.route_type, t.headsign, t.short_name,
                           t.train_number, t.train_name, s.name,
                           s.platform_code, s.latitude, s.longitude
                    FROM trips t JOIN routes r
                      ON r.feed_id = t.feed_id AND r.route_id = t.route_id
                    JOIN stop_times st
                      ON st.feed_id = t.feed_id AND st.trip_id = t.trip_id
                    JOIN stops s
                      ON s.feed_id = st.feed_id AND s.stop_id = st.stop_id
                    WHERE t.feed_id = ? AND t.trip_id = ?
                      AND r.route_id = ? AND s.stop_id = ?
                      AND r.agency_id IN ({GtfsDatabase.placeholders(self.provider.agency_ids)})
                      AND t.service_id IN ({GtfsDatabase.placeholders(service_ids)})
                """,
                (
                    self.provider.source_id, trip_id, route_id, stop_id,
                    *self.provider.agency_ids, *service_ids
                )
            ).fetchone()
        if row is None:
            raise PublicTransportValueError(
                'PUBLIC_TRANSPORT_ERROR.GTFS_TIMETABLE_NOT_FOUND'
            )
        departures = self.departures(
            stop_id, service_date, route_id, train_number
        )
        day = PublicTransportDateTimetable(
            date=service_date,
            direction_name=str(row['headsign'] or ''),
            effective_date_from=service_date,
            effective_date_to=service_date,
            departures=departures,
            variants=list(dict.fromkeys(
                item.variant for item in departures if item.variant
            ))
        )
        return PublicTransportLineStopTimetable(
            line=(self._train_name(row) if train_number else
                  str(row['line_name'] or row['long_name'] or route_id)),
            type=self._transport_type(int(row['route_type'])),
            announcements=[],
            stop_name=str(row['name']),
            direction_name=str(row['headsign'] or ''),
            platform=str(row['platform_code'] or ''),
            timetable={service_date: day},
            dates=self._date_urls(
                'line-stop', route=route_id, trip=trip_id, stop=stop_id,
                number=train_number
            ),
            latitude=float(row['latitude']) if row['latitude'] is not None else None,
            longitude=float(row['longitude']) if row['longitude'] is not None else None,
            stop_lines_url=self._url(
                'stop', stop=stop_id, date=service_date.isoformat()
            )
        )

    def route_for_trip(
        self,
        trip_id: str,
        service_date: date
    ) -> list[PublicTransportCoordinate]:
        """Returns an exact GTFS shape, or no geometry when none is published."""
        with self._connection() as connection:
            service_ids = self._service_ids(connection, service_date)
            trip = connection.execute(
                f"""
                    SELECT t.shape_id
                    FROM trips t
                    JOIN routes r
                      ON r.feed_id = t.feed_id AND r.route_id = t.route_id
                    WHERE t.feed_id = ? AND t.trip_id = ?
                      AND r.agency_id IN ({GtfsDatabase.placeholders(self.provider.agency_ids)})
                      AND t.service_id IN ({GtfsDatabase.placeholders(service_ids)})
                """,
                (
                    self.provider.source_id,
                    trip_id,
                    *self.provider.agency_ids,
                    *service_ids
                )
            ).fetchone()
            if trip is None:
                raise PublicTransportValueError(
                    'PUBLIC_TRANSPORT_ERROR.GTFS_TRIP_NOT_FOUND'
                )
            shape_id = str(trip['shape_id'] or '')
            if not shape_id:
                return []
            rows = connection.execute(
                """
                    SELECT latitude, longitude FROM shapes
                    WHERE feed_id = ? AND shape_id = ?
                    ORDER BY point_sequence
                """,
                (self.provider.source_id, shape_id)
            ).fetchall()
        return [
            PublicTransportCoordinate(
                latitude=float(row['latitude']),
                longitude=float(row['longitude'])
            )
            for row in rows
        ]

    def download_stop_all(self, url: str) -> PublicTransportStopAll:
        """Returns all scoped railway departures from one physical platform."""
        values = self._validated_query(url, 'stop')
        stop_id = values.get('stop', '')
        try:
            service_date = date.fromisoformat(values.get('date', ''))
        except ValueError:
            raise PublicTransportValueError(
                'PUBLIC_TRANSPORT_ERROR.INVALID_GTFS_TIMETABLE_URL'
            )
        with self._connection() as connection:
            service_ids = self._service_ids(connection, service_date)
            stop = connection.execute(
                'SELECT * FROM stops WHERE feed_id = ? AND stop_id = ?',
                (self.provider.source_id, stop_id)
            ).fetchone()
            trips = connection.execute(
                f"""
                    SELECT DISTINCT r.*, t.trip_id,
                           t.short_name AS trip_short_name,
                           t.train_number, t.train_name,
                           COALESCE(
                               NULLIF(t.headsign, ''),
                               (
                                   SELECT COALESCE(parent.name, destination.name)
                                   FROM stop_times destination_time
                                   JOIN stops destination
                                     ON destination.feed_id = destination_time.feed_id
                                    AND destination.stop_id = destination_time.stop_id
                                   LEFT JOIN stops parent
                                     ON parent.feed_id = destination.feed_id
                                    AND parent.stop_id = destination.parent_station
                                   WHERE destination_time.feed_id = t.feed_id
                                     AND destination_time.trip_id = t.trip_id
                                   ORDER BY destination_time.stop_sequence DESC
                                   LIMIT 1
                               )
                           ) AS direction_name
                    FROM routes r JOIN trips t
                      ON t.feed_id = r.feed_id AND t.route_id = r.route_id
                    JOIN stop_times st
                      ON st.feed_id = t.feed_id AND st.trip_id = t.trip_id
                    WHERE r.feed_id = ? AND st.stop_id = ?
                      AND r.agency_id IN ({GtfsDatabase.placeholders(self.provider.agency_ids)})
                      AND t.service_id IN ({GtfsDatabase.placeholders(service_ids)})
                      AND st.pickup_type <> 1
                    ORDER BY r.short_name, t.short_name, direction_name, t.trip_id
                """,
                (self.provider.source_id, stop_id,
                 *self.provider.agency_ids, *service_ids)
            ).fetchall()
        if stop is None:
            raise PublicTransportValueError(
                'PUBLIC_TRANSPORT_ERROR.INVALID_GTFS_STOP_ID'
            )
        long_distance = self.provider.provider_id in self._LONG_DISTANCE_PROVIDERS
        grouped: dict[tuple[str, str], dict[str, Any]] = {}
        for trip in trips:
            route_id = str(trip['route_id'])
            train_number = str(
                trip['trip_short_name'] or trip['train_number'] or ''
            ) if long_distance else ''
            key = (route_id, train_number)
            item = grouped.setdefault(key, {'row': trip, 'directions': []})
            direction = str(trip['direction_name'] or '').strip()
            if direction and direction not in item['directions']:
                item['directions'].append(direction)

        lines = {}
        for (route_id, train_number), item in grouped.items():
            trip = item['row']
            departures = self.departures(
                stop_id, service_date, route_id, train_number
            )
            line = PublicTransportBaseLine(
                line=(self._listed_train_name(trip) if train_number
                      else self._line_name(trip)),
                type=self._transport_type(int(trip['route_type'])),
                url=self._url(
                    'line', route=route_id, number=train_number,
                    date=service_date.isoformat()
                ),
                free_of_charge=False,
                updated=False
            )
            lines[line] = PublicTransportDateTimetable(
                date=service_date,
                direction_name=' / '.join(item['directions']),
                effective_date_from=service_date,
                effective_date_to=service_date,
                departures=departures,
                variants=list(dict.fromkeys(
                    item.variant for item in departures if item.variant
                ))
            )
        return PublicTransportStopAll(
            stop_name=str(stop['name']),
            platform=str(stop['platform_code'] or ''),
            dates=self._date_urls('stop', stop=stop_id),
            lines=lines,
            latitude=float(stop['latitude']) if stop['latitude'] is not None else None,
            longitude=float(stop['longitude']) if stop['longitude'] is not None else None
        )

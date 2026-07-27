from __future__ import annotations
import csv
from datetime import date, timedelta
from io import BytesIO, TextIOWrapper
from pathlib import Path
import sqlite3
import tempfile
from typing import Callable, ClassVar, Iterable
from zipfile import ZipFile


GtfsBuildProgress = Callable[[str, int, int], None]


class _GtfsConnection(sqlite3.Connection):
    """Closes SQLite connections after their transaction context exits."""

    def __exit__(self, exc_type, exc_value, traceback) -> bool:
        try:
            return bool(super().__exit__(exc_type, exc_value, traceback))
        finally:
            self.close()


class GtfsDatabase:
    """Builds a compact relational cache from one or more static GTFS feeds."""

    _BATCH_SIZE: ClassVar[int] = 5000
    _SCHEMA_VERSION: ClassVar[str] = '2'
    _SCHEMA: ClassVar[str] = """
        CREATE TABLE routes (
            feed_id TEXT NOT NULL,
            route_id TEXT NOT NULL,
            agency_id TEXT NOT NULL,
            short_name TEXT NOT NULL,
            long_name TEXT NOT NULL,
            description TEXT NOT NULL,
            route_type INTEGER NOT NULL,
            url TEXT NOT NULL,
            color TEXT NOT NULL,
            text_color TEXT NOT NULL,
            PRIMARY KEY (feed_id, route_id)
        );
        CREATE TABLE stops (
            feed_id TEXT NOT NULL,
            stop_id TEXT NOT NULL,
            stop_code TEXT NOT NULL,
            name TEXT NOT NULL,
            description TEXT NOT NULL,
            latitude REAL,
            longitude REAL,
            parent_station TEXT NOT NULL,
            platform_code TEXT NOT NULL,
            url TEXT NOT NULL,
            PRIMARY KEY (feed_id, stop_id)
        );
        CREATE TABLE trips (
            feed_id TEXT NOT NULL,
            trip_id TEXT NOT NULL,
            route_id TEXT NOT NULL,
            service_id TEXT NOT NULL,
            headsign TEXT NOT NULL,
            short_name TEXT NOT NULL,
            direction_id INTEGER,
            shape_id TEXT NOT NULL,
            wheelchair_accessible INTEGER NOT NULL,
            block_id TEXT NOT NULL,
            PRIMARY KEY (feed_id, trip_id)
        );
        CREATE TABLE stop_times (
            feed_id TEXT NOT NULL,
            trip_id TEXT NOT NULL,
            arrival_time TEXT NOT NULL,
            departure_time TEXT NOT NULL,
            stop_id TEXT NOT NULL,
            stop_sequence INTEGER NOT NULL,
            stop_headsign TEXT NOT NULL,
            pickup_type INTEGER NOT NULL,
            drop_off_type INTEGER NOT NULL,
            shape_dist_traveled REAL,
            timepoint INTEGER,
            PRIMARY KEY (feed_id, trip_id, stop_sequence)
        ) WITHOUT ROWID;
        CREATE TABLE calendar (
            feed_id TEXT NOT NULL,
            service_id TEXT NOT NULL,
            monday INTEGER NOT NULL,
            tuesday INTEGER NOT NULL,
            wednesday INTEGER NOT NULL,
            thursday INTEGER NOT NULL,
            friday INTEGER NOT NULL,
            saturday INTEGER NOT NULL,
            sunday INTEGER NOT NULL,
            start_date TEXT NOT NULL,
            end_date TEXT NOT NULL,
            PRIMARY KEY (feed_id, service_id)
        );
        CREATE TABLE calendar_dates (
            feed_id TEXT NOT NULL,
            service_id TEXT NOT NULL,
            service_date TEXT NOT NULL,
            exception_type INTEGER NOT NULL
        );
        CREATE TABLE shapes (
            feed_id TEXT NOT NULL,
            shape_id TEXT NOT NULL,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL,
            point_sequence INTEGER NOT NULL,
            PRIMARY KEY (feed_id, shape_id, point_sequence)
        ) WITHOUT ROWID;
        CREATE TABLE service_extensions (
            feed_id TEXT NOT NULL,
            service_id TEXT NOT NULL,
            name TEXT NOT NULL,
            PRIMARY KEY (feed_id, service_id)
        );
        CREATE TABLE stop_extensions (
            feed_id TEXT NOT NULL,
            stop_id TEXT NOT NULL,
            platform_code TEXT NOT NULL,
            community_ids TEXT NOT NULL,
            vehicle_type_ids TEXT NOT NULL,
            attribute_ids TEXT NOT NULL,
            long_name TEXT NOT NULL,
            city TEXT NOT NULL,
            street TEXT NOT NULL,
            PRIMARY KEY (feed_id, stop_id)
        );
        CREATE TABLE route_extensions (
            feed_id TEXT NOT NULL,
            route_id TEXT NOT NULL,
            start_date TEXT NOT NULL,
            end_date TEXT NOT NULL,
            line_type TEXT NOT NULL,
            PRIMARY KEY (feed_id, route_id)
        );
        CREATE TABLE trip_extensions (
            feed_id TEXT NOT NULL,
            trip_id TEXT NOT NULL,
            operator_id TEXT NOT NULL,
            vehicle_class_id TEXT NOT NULL,
            variant_code TEXT NOT NULL,
            is_base INTEGER NOT NULL,
            is_bypass INTEGER NOT NULL,
            chained_with_next INTEGER NOT NULL,
            PRIMARY KEY (feed_id, trip_id)
        );
        CREATE TABLE operators (
            feed_id TEXT NOT NULL,
            operator_id TEXT NOT NULL,
            name TEXT NOT NULL,
            url TEXT NOT NULL,
            PRIMARY KEY (feed_id, operator_id)
        );
        CREATE TABLE vehicle_classes (
            feed_id TEXT NOT NULL,
            vehicle_class_id TEXT NOT NULL,
            short_name TEXT NOT NULL,
            long_name TEXT NOT NULL,
            low_floor INTEGER NOT NULL,
            PRIMARY KEY (feed_id, vehicle_class_id)
        );
        CREATE TABLE metadata (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        );
    """
    _INDEXES: ClassVar[str] = """
        CREATE INDEX idx_routes_short_name
            ON routes(short_name);
        CREATE INDEX idx_stops_name
            ON stops(name);
        CREATE INDEX idx_trips_route
            ON trips(feed_id, route_id, service_id);
        CREATE INDEX idx_trips_shape
            ON trips(feed_id, shape_id);
        CREATE INDEX idx_stop_times_stop
            ON stop_times(feed_id, stop_id, trip_id);
        CREATE INDEX idx_calendar_dates_date
            ON calendar_dates(feed_id, service_date, service_id);
        CREATE INDEX idx_trip_extensions_variant
            ON trip_extensions(feed_id, trip_id, variant_code);
    """

    def __new__(cls):
        """Prevents creating instances of this shared GTFS utility."""
        raise TypeError(f'{cls.__name__} cannot be instantiated.')

    #region Building

    @classmethod
    def build(
        cls,
        destination: Path,
        feeds: dict[str, bytes],
        progress: GtfsBuildProgress | None = None,
        coverage_days: int = 32,
        compact_shapes: bool = False
    ) -> None:
        """Builds a new database and atomically replaces the previous cache."""
        coverage_from = date.today()
        coverage_to = coverage_from + timedelta(
            days=max(1, coverage_days) - 1
        )
        service_dates = [
            coverage_from + timedelta(days=offset)
            for offset in range((coverage_to - coverage_from).days + 1)
        ]
        destination.parent.mkdir(parents=True, exist_ok=True)
        temporary_path: Path | None = None
        try:
            with tempfile.NamedTemporaryFile(
                suffix='.sqlite3',
                dir=destination.parent,
                delete=False
            ) as temporary:
                temporary_path = Path(temporary.name)
            connection = sqlite3.connect(temporary_path)
            try:
                connection.row_factory = sqlite3.Row
                connection.execute('PRAGMA journal_mode = OFF')
                connection.execute('PRAGMA synchronous = OFF')
                connection.execute('PRAGMA temp_store = MEMORY')
                connection.executescript(cls._SCHEMA)
                total = len(feeds)
                for index, (feed_id, payload) in enumerate(
                    feeds.items(),
                    start=1
                ):
                    if progress:
                        progress(feed_id, index, total)
                    cls._import_feed(
                        connection,
                        feed_id,
                        payload,
                        service_dates,
                        compact_shapes
                    )
                    connection.commit()
                connection.executescript(cls._INDEXES)
                connection.execute(
                    'INSERT INTO metadata(key, value) VALUES (?, ?)',
                    ('schema_version', cls._SCHEMA_VERSION)
                )
                connection.executemany(
                    'INSERT INTO metadata(key, value) VALUES (?, ?)',
                    (
                        ('coverage_from', coverage_from.isoformat()),
                        ('coverage_to', coverage_to.isoformat())
                    )
                )
                connection.commit()
            finally:
                connection.close()
            temporary_path.replace(destination)
            temporary_path = None
        finally:
            if temporary_path and temporary_path.exists():
                temporary_path.unlink()

    @classmethod
    def _import_feed(
        cls,
        connection: sqlite3.Connection,
        feed_id: str,
        payload: bytes,
        service_dates: list[date],
        compact_shapes: bool
    ) -> None:
        """Imports all relevant files from one GTFS ZIP archive."""
        with ZipFile(BytesIO(payload)) as archive:
            cls._insert_rows(
                connection,
                archive,
                'routes.txt',
                """
                    INSERT INTO routes VALUES (
                        ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
                    )
                """,
                lambda row: (
                    feed_id,
                    cls._value(row, 'route_id'),
                    cls._value(row, 'agency_id'),
                    cls._value(row, 'route_short_name'),
                    cls._value(row, 'route_long_name'),
                    cls._value(row, 'route_desc'),
                    cls._integer(row, 'route_type'),
                    cls._value(row, 'route_url'),
                    cls._value(row, 'route_color'),
                    cls._value(row, 'route_text_color')
                )
            )
            cls._insert_rows(
                connection,
                archive,
                'stops.txt',
                """
                    INSERT INTO stops VALUES (
                        ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
                    )
                """,
                lambda row: (
                    feed_id,
                    cls._value(row, 'stop_id'),
                    cls._value(row, 'stop_code'),
                    cls._value(row, 'stop_name'),
                    cls._value(row, 'stop_desc'),
                    cls._float(row, 'stop_lat'),
                    cls._float(row, 'stop_lon'),
                    cls._value(row, 'parent_station'),
                    cls._value(row, 'platform_code'),
                    cls._value(row, 'stop_url')
                )
            )
            cls._insert_rows(
                connection,
                archive,
                'calendar.txt',
                """
                    INSERT INTO calendar VALUES (
                        ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
                    )
                """,
                lambda row: (
                    feed_id,
                    cls._value(row, 'service_id'),
                    cls._integer(row, 'monday'),
                    cls._integer(row, 'tuesday'),
                    cls._integer(row, 'wednesday'),
                    cls._integer(row, 'thursday'),
                    cls._integer(row, 'friday'),
                    cls._integer(row, 'saturday'),
                    cls._integer(row, 'sunday'),
                    cls._value(row, 'start_date'),
                    cls._value(row, 'end_date')
                ),
                required=False
            )
            cls._insert_rows(
                connection,
                archive,
                'calendar_dates.txt',
                """
                    INSERT INTO calendar_dates VALUES (?, ?, ?, ?)
                """,
                lambda row: (
                    feed_id,
                    cls._value(row, 'service_id'),
                    cls._value(row, 'date'),
                    cls._integer(row, 'exception_type')
                ),
                required=False
            )
            active_services: set[str] = set()
            for service_date in service_dates:
                active_services.update(cls.active_service_ids(
                    connection,
                    feed_id,
                    service_date
                ))
            has_service_calendar = bool(connection.execute(
                """
                    SELECT 1
                    FROM (
                        SELECT service_id FROM calendar
                        WHERE feed_id = ?
                        UNION ALL
                        SELECT service_id FROM calendar_dates
                        WHERE feed_id = ?
                    )
                    LIMIT 1
                """,
                (feed_id, feed_id)
            ).fetchone())
            active_trip_ids: set[str] = set()
            active_shape_ids: set[str] = set()

            def trip_row(row: dict[str, str]) -> tuple | None:
                service_id = cls._value(row, 'service_id')
                if (
                    has_service_calendar
                    and service_id not in active_services
                ):
                    return None
                trip_id = cls._value(row, 'trip_id')
                shape_id = cls._value(row, 'shape_id')
                active_trip_ids.add(trip_id)
                if shape_id:
                    active_shape_ids.add(shape_id)
                return (
                    feed_id,
                    trip_id,
                    cls._value(row, 'route_id'),
                    service_id,
                    cls._value(row, 'trip_headsign'),
                    cls._value(row, 'trip_short_name'),
                    cls._optional_integer(row, 'direction_id'),
                    shape_id,
                    cls._integer(row, 'wheelchair_accessible'),
                    cls._value(row, 'block_id')
                )

            cls._insert_rows(
                connection,
                archive,
                'trips.txt',
                """
                    INSERT INTO trips VALUES (
                        ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
                    )
                """,
                trip_row
            )
            cls._insert_rows(
                connection,
                archive,
                'stop_times.txt',
                """
                    INSERT INTO stop_times VALUES (
                        ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
                    )
                """,
                lambda row: (
                    (
                        feed_id,
                        cls._value(row, 'trip_id'),
                        cls._value(row, 'arrival_time'),
                        cls._value(row, 'departure_time')
                        or cls._value(row, 'arrival_time'),
                        cls._value(row, 'stop_id'),
                        cls._integer(row, 'stop_sequence'),
                        cls._value(row, 'stop_headsign'),
                        cls._integer(row, 'pickup_type'),
                        cls._integer(row, 'drop_off_type'),
                        cls._float(row, 'shape_dist_traveled'),
                        cls._optional_integer(row, 'timepoint')
                    )
                    if cls._value(row, 'trip_id') in active_trip_ids
                    else None
                )
            )
            cls._import_extensions(
                connection,
                archive,
                feed_id,
                active_trip_ids
            )
            if compact_shapes:
                active_shape_ids = cls._representative_shape_ids(
                    connection,
                    feed_id
                )
            cls._insert_rows(
                connection,
                archive,
                'shapes.txt',
                """
                    INSERT INTO shapes VALUES (?, ?, ?, ?, ?)
                """,
                lambda row: (
                    (
                        feed_id,
                        cls._value(row, 'shape_id'),
                        cls._float(row, 'shape_pt_lat') or 0.0,
                        cls._float(row, 'shape_pt_lon') or 0.0,
                        cls._integer(row, 'shape_pt_sequence')
                    )
                    if cls._value(row, 'shape_id') in active_shape_ids
                    else None
                ),
                required=False
            )

    @staticmethod
    def _representative_shape_ids(
        connection: sqlite3.Connection,
        feed_id: str
    ) -> set[str]:
        """Returns one geometry for every semantic route variant."""
        return {
            str(row['shape_id'])
            for row in connection.execute(
                """
                    WITH ranked AS (
                        SELECT t.shape_id,
                               ROW_NUMBER() OVER (
                                   PARTITION BY
                                       t.route_id,
                                       t.headsign,
                                       t.direction_id,
                                       COALESCE(te.variant_code, '')
                                   ORDER BY
                                       COALESCE(te.is_base, 0) DESC,
                                       t.trip_id
                               ) row_number
                        FROM trips t
                        LEFT JOIN trip_extensions te
                          ON te.feed_id = t.feed_id
                         AND te.trip_id = t.trip_id
                        WHERE t.feed_id = ? AND t.shape_id <> ''
                    )
                    SELECT shape_id FROM ranked WHERE row_number = 1
                """,
                (feed_id,)
            )
        }

    @classmethod
    def _import_extensions(
        cls,
        connection: sqlite3.Connection,
        archive: ZipFile,
        feed_id: str,
        active_trip_ids: set[str]
    ) -> None:
        """Imports optional provider extensions used by richer GTFS feeds."""
        cls._insert_rows(
            connection,
            archive,
            'service_ext.txt',
            'INSERT INTO service_extensions VALUES (?, ?, ?)',
            lambda row: (
                feed_id,
                cls._value(row, 'service_id'),
                cls._value(row, 'name')
            ),
            required=False
        )
        cls._insert_rows(
            connection,
            archive,
            'stops_ext.txt',
            """
                INSERT INTO stop_extensions VALUES (
                    ?, ?, ?, ?, ?, ?, ?, ?, ?
                )
            """,
            lambda row: (
                feed_id,
                cls._value(row, 'stop_id'),
                cls._value(row, 'stop_code_add'),
                cls._value(row, 'community_ids'),
                cls._value(row, 'stop_vehicle_type_ids'),
                cls._value(row, 'stop_attribute_ids'),
                cls._value(row, 'stop_long_name'),
                cls._value(row, 'city'),
                cls._value(row, 'street')
            ),
            required=False
        )
        cls._insert_rows(
            connection,
            archive,
            'routes_ext.txt',
            'INSERT INTO route_extensions VALUES (?, ?, ?, ?, ?)',
            lambda row: (
                feed_id,
                cls._value(row, 'route_id'),
                cls._value(row, 'route_start_date'),
                cls._value(row, 'route_end_date'),
                cls._value(row, 'route_type_1')
            ),
            required=False
        )
        cls._insert_rows(
            connection,
            archive,
            'trips_ext.txt',
            """
                INSERT INTO trip_extensions VALUES (
                    ?, ?, ?, ?, ?, ?, ?, ?
                )
            """,
            lambda row: (
                (
                    feed_id,
                    cls._value(row, 'trip_id'),
                    cls._value(row, 'operator_id'),
                    cls._value(row, 'vehicle_class_id'),
                    cls._value(row, 'route_trip_short_name'),
                    cls._integer(row, 'is_base_route_trip'),
                    cls._integer(row, 'is_bypass_trip'),
                    cls._integer(row, 'chained_with_next')
                )
                if cls._value(row, 'trip_id') in active_trip_ids
                else None
            ),
            required=False
        )
        cls._insert_rows(
            connection,
            archive,
            'operators_ext.txt',
            'INSERT INTO operators VALUES (?, ?, ?, ?)',
            lambda row: (
                feed_id,
                cls._value(row, 'operator_id'),
                cls._value(row, 'operator_name'),
                cls._value(row, 'operator_url')
            ),
            required=False
        )
        cls._insert_rows(
            connection,
            archive,
            'vehicles_ext.txt',
            'INSERT INTO vehicle_classes VALUES (?, ?, ?, ?, ?)',
            lambda row: (
                feed_id,
                cls._value(row, 'vehicle_class_id'),
                cls._value(row, 'vehicle_short_name'),
                cls._value(row, 'vehicle_long_name'),
                cls._integer(row, 'low_floor')
            ),
            required=False
        )

    @classmethod
    def _insert_rows(
        cls,
        connection: sqlite3.Connection,
        archive: ZipFile,
        file_name: str,
        query: str,
        mapper: Callable[[dict[str, str]], tuple | None],
        required: bool = True
    ) -> None:
        """Streams one CSV file into SQLite without loading it into memory."""
        try:
            source = archive.open(file_name)
        except KeyError:
            if required:
                raise ValueError(f'Brak wymaganego pliku GTFS: {file_name}')
            return
        with source, TextIOWrapper(source, encoding='utf-8-sig', newline='') as text:
            reader = csv.DictReader(text)
            batch: list[tuple] = []
            for row in reader:
                mapped = mapper(row)
                if mapped is None:
                    continue
                batch.append(mapped)
                if len(batch) >= cls._BATCH_SIZE:
                    connection.executemany(query, batch)
                    batch.clear()
            if batch:
                connection.executemany(query, batch)

    #endregion Building

    #region Queries

    @staticmethod
    def migrate_cache(source: Path, destination: Path) -> None:
        """Moves an existing cache to a new location when needed."""
        if destination.exists() or not source.exists():
            return
        destination.parent.mkdir(parents=True, exist_ok=True)
        source.replace(destination)

    @staticmethod
    def connect(path: Path) -> sqlite3.Connection:
        """Opens a typed, read-only-style connection to a built GTFS cache."""
        connection = sqlite3.connect(path, factory=_GtfsConnection)
        connection.row_factory = sqlite3.Row
        return connection

    @staticmethod
    def covers(path: Path, required_date: date) -> bool:
        """Checks whether a built cache includes a required service date."""
        if not path.exists():
            return False
        try:
            connection = sqlite3.connect(path)
            try:
                rows = connection.execute(
                    """
                        SELECT key, value FROM metadata
                        WHERE key IN ('coverage_to', 'schema_version')
                    """
                ).fetchall()
            finally:
                connection.close()
            metadata = {
                str(key): str(value)
                for key, value in rows
            }
            return bool(
                metadata.get('schema_version') == GtfsDatabase._SCHEMA_VERSION
                and date.fromisoformat(metadata['coverage_to']) >= required_date
            )
        except (KeyError, OSError, sqlite3.Error, ValueError):
            return False

    @staticmethod
    def active_service_ids(
        connection: sqlite3.Connection,
        feed_id: str,
        service_date
    ) -> set[str]:
        """Returns service identifiers active on one calendar date."""
        compact_date = service_date.strftime('%Y%m%d')
        weekday = service_date.strftime('%A').lower()
        if weekday not in {
            'monday', 'tuesday', 'wednesday', 'thursday',
            'friday', 'saturday', 'sunday'
        }:
            return set()
        regular = {
            str(row['service_id'])
            for row in connection.execute(
                f"""
                    SELECT service_id
                    FROM calendar
                    WHERE feed_id = ?
                      AND start_date <= ?
                      AND end_date >= ?
                      AND {weekday} = 1
                """,
                (feed_id, compact_date, compact_date)
            )
        }
        for row in connection.execute(
            """
                SELECT service_id, exception_type
                FROM calendar_dates
                WHERE feed_id = ? AND service_date = ?
            """,
            (feed_id, compact_date)
        ):
            service_id = str(row['service_id'])
            if int(row['exception_type']) == 1:
                regular.add(service_id)
            elif int(row['exception_type']) == 2:
                regular.discard(service_id)
        return regular

    @staticmethod
    def placeholders(values: Iterable[object]) -> str:
        """Builds SQL placeholders for a known non-empty value collection."""
        return ','.join('?' for _ in values)

    #endregion Queries

    #region Conversion

    @staticmethod
    def _value(row: dict[str, str], field: str) -> str:
        """Returns a stripped CSV field."""
        return str(row.get(field) or '').strip()

    @classmethod
    def _integer(cls, row: dict[str, str], field: str) -> int:
        """Returns an integer CSV field or zero."""
        try:
            return int(cls._value(row, field))
        except ValueError:
            return 0

    @classmethod
    def _optional_integer(
        cls,
        row: dict[str, str],
        field: str
    ) -> int | None:
        """Returns an optional integer CSV field."""
        value = cls._value(row, field)
        try:
            return int(value) if value else None
        except ValueError:
            return None

    @classmethod
    def _float(cls, row: dict[str, str], field: str) -> float | None:
        """Returns an optional float CSV field."""
        value = cls._value(row, field)
        try:
            return float(value) if value else None
        except ValueError:
            return None

    #endregion Conversion

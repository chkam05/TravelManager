"""Shared, source-level cache for Polish railway GTFS schedules."""
from __future__ import annotations

from concurrent.futures import CancelledError
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
import ssl
from threading import Condition, Event, Lock, Thread
from typing import Callable, ClassVar
from urllib.error import URLError
from urllib.request import Request, urlopen

from config import SETTINGS_DIR
from core.gtfs_database import GtfsDatabase
from resources.public_transport.public_transport_messages import (
    PublicTransportMessage,
    PublicTransportValueError,
    public_transport_message,
)
from resources.public_transport.rail_gtfs_sources import RailGtfsSources
from utils.public_transport.download_progress import (
    ProgressCallback,
    PublicTransportDownloadProgress,
)


@dataclass
class _RailGtfsFlight:
    """One source update observed independently by multiple consumers."""

    condition: Condition = field(default_factory=Condition)
    subscribers: list[ProgressCallback] = field(default_factory=list)
    result: Path | None = None
    error: Exception | None = None
    done: bool = False
    waiters: int = 0
    cancelled: Event = field(default_factory=Event)

    def report(
        self,
        item: object,
        current: int,
        total: int,
        attempt: int,
        max_attempts: int
    ) -> None:
        """Broadcasts a progress snapshot without holding the condition."""
        with self.condition:
            subscribers = tuple(self.subscribers)
        for subscriber in subscribers:
            try:
                subscriber(item, current, total, attempt, max_attempts)
            except Exception:
                # A closed request must not interrupt a shared source update.
                continue


@dataclass(frozen=True)
class RailScheduleAvailability:
    """Explains whether a source can answer for one service date."""

    source_id: str
    service_date: date
    status: str
    coverage_from: date | None = None
    coverage_to: date | None = None
    feed_version: str = ''
    built_at: str = ''
    stale: bool = False
    message: PublicTransportMessage | None = None

    @property
    def available(self) -> bool:
        return self.status == 'available'


class RailGtfsCache:
    """Downloads and builds exactly one database per physical rail source."""

    _REQUEST_TIMEOUT: ClassVar[int] = 90
    _COVERAGE_DAYS: ClassVar[int] = 62
    _USER_AGENT: ClassVar[str] = 'TravelManager/1.0'
    _DATABASE_PATHS: ClassVar[dict[str, Path]] = {
        source_id: Path(SETTINGS_DIR) / f'{source_id}_gtfs.sqlite3'
        for source_id in RailGtfsSources.SOURCES
    }
    _FLIGHTS_LOCK: ClassVar[Lock] = Lock()
    _FLIGHTS: ClassVar[dict[str, _RailGtfsFlight]] = {}

    def __new__(cls):
        raise TypeError(f'{cls.__name__} cannot be instantiated.')

    @classmethod
    def database_path(cls, source_id: str) -> Path:
        """Returns a cache path only for a configured physical source."""
        try:
            return cls._DATABASE_PATHS[source_id]
        except KeyError:
            raise ValueError(f'Unknown railway GTFS source: {source_id}')

    @classmethod
    def _is_current(cls, path: Path, source_id: str) -> bool:
        """Checks schema validity and whether the feed covers today."""
        if not GtfsDatabase.is_valid_cache(path):
            return False
        try:
            with GtfsDatabase.connect(path) as connection:
                coverage = GtfsDatabase.service_range(connection, source_id)
            return bool(
                coverage
                and coverage[0] <= date.today() <= coverage[1]
            )
        except Exception:
            return False

    @classmethod
    def _download(cls, source_id: str) -> bytes:
        """Downloads one source into a resumable partial file."""
        source = RailGtfsSources.SOURCES[source_id]
        partial_path = cls.database_path(source_id).with_suffix('.zip.part')
        partial_path.parent.mkdir(parents=True, exist_ok=True)
        ssl_context: list[ssl.SSLContext | None] = [None]
        item = public_transport_message('DOWNLOAD_STATUS.GTFS_FEED', feed=source_id)

        def operation() -> bytes:
            existing = partial_path.stat().st_size if partial_path.exists() else 0
            headers = {
                'Accept': 'application/zip,*/*',
                'User-Agent': cls._USER_AGENT
            }
            if existing:
                headers['Range'] = f'bytes={existing}-'
            request = Request(source.schedule_url, headers=headers)
            try:
                with urlopen(
                    request,
                    timeout=cls._REQUEST_TIMEOUT,
                    context=ssl_context[0]
                ) as response:
                    resumed = existing > 0 and response.getcode() == 206
                    current = existing if resumed else 0
                    total = current + int(response.headers.get('Content-Length') or 0)
                    mode = 'ab' if resumed else 'wb'
                    with partial_path.open(mode) as output:
                        while True:
                            cancelled = PublicTransportDownloadProgress.current_cancelled()
                            if cancelled and cancelled():
                                raise CancelledError(f'{source_id} download cancelled')
                            chunk = response.read(256 * 1024)
                            if not chunk:
                                break
                            output.write(chunk)
                            current += len(chunk)
                            PublicTransportDownloadProgress.report(
                                item, current, total or current
                            )
                payload = partial_path.read_bytes()
                partial_path.unlink()
                return payload
            except CancelledError:
                if partial_path.exists():
                    partial_path.unlink()
                raise
            except URLError as error:
                if (
                    ssl_context[0] is None
                    and isinstance(error.reason, ssl.SSLCertVerificationError)
                ):
                    ssl_context[0] = ssl._create_unverified_context()
                raise

        return PublicTransportDownloadProgress.retry(
            operation,
            item,
            1,
            2
        )

    @classmethod
    def ensure_database(
        cls,
        source_id: str,
        refresh: bool = False,
        cancelled: Callable[[], bool] | None = None
    ) -> Path:
        """Waits for one shared update; cancellation detaches only this caller."""
        path = cls.database_path(source_id)
        if not refresh and cls._is_current(path, source_id):
            return path

        callback = PublicTransportDownloadProgress.current_callback()
        with cls._FLIGHTS_LOCK:
            flight = cls._FLIGHTS.get(source_id)
            if flight is None:
                flight = _RailGtfsFlight()
                cls._FLIGHTS[source_id] = flight
                if callback:
                    flight.subscribers.append(callback)
                Thread(
                    target=cls._run_flight,
                    args=(source_id, path, refresh, flight),
                    daemon=True,
                    name=f'rail-gtfs-{source_id}'
                ).start()
            elif callback:
                with flight.condition:
                    flight.subscribers.append(callback)

        with flight.condition:
            flight.waiters += 1
        detached_by_cancel = False
        try:
            with flight.condition:
                while not flight.done:
                    if cancelled and cancelled():
                        detached_by_cancel = True
                        raise CancelledError(
                            f'Waiting for {source_id} GTFS was cancelled'
                        )
                    flight.condition.wait(timeout=0.1)
                if flight.error:
                    raise flight.error
                if flight.result is None:
                    raise RuntimeError(
                        f'{source_id} GTFS update returned no database'
                    )
                return flight.result
        finally:
            with flight.condition:
                flight.waiters = max(0, flight.waiters - 1)
                if detached_by_cancel and flight.waiters == 0:
                    flight.cancelled.set()
                if callback:
                    if callback in flight.subscribers:
                        flight.subscribers.remove(callback)

    @classmethod
    def _run_flight(
        cls,
        source_id: str,
        path: Path,
        refresh: bool,
        flight: _RailGtfsFlight
    ) -> None:
        """Builds a source cache in the background for all current callers."""
        result: Path | None = None
        error: Exception | None = None
        try:
            with PublicTransportDownloadProgress.bind(
                flight.report, flight.cancelled.is_set
            ):
                result = cls._build_database(source_id, path, refresh)
        except Exception as caught:
            error = caught
        with flight.condition:
            flight.result = result
            flight.error = error
            flight.done = True
            flight.condition.notify_all()
        with cls._FLIGHTS_LOCK:
            if cls._FLIGHTS.get(source_id) is flight:
                del cls._FLIGHTS[source_id]

    @classmethod
    def _build_database(
        cls,
        source_id: str,
        path: Path,
        refresh: bool
    ) -> Path:
        """Downloads and atomically builds one physical source database."""
        had_valid_cache = GtfsDatabase.is_valid_cache(path)
        try:
            archive = cls._download(source_id)
            if PublicTransportDownloadProgress.current_cancelled() and PublicTransportDownloadProgress.current_cancelled()():
                raise CancelledError(f'{source_id} build cancelled')
            GtfsDatabase.build(
                path,
                {source_id: archive},
                lambda feed_id, current, count: (
                    (_ for _ in ()).throw(CancelledError(f'{source_id} build cancelled'))
                    if PublicTransportDownloadProgress.current_cancelled()
                    and PublicTransportDownloadProgress.current_cancelled()()
                    else PublicTransportDownloadProgress.report(
                        public_transport_message(
                            'DOWNLOAD_STATUS.PROCESSING_GTFS',
                            feed=feed_id
                        ),
                        1 + current,
                        1 + count
                    )
                ),
                coverage_days=cls._COVERAGE_DAYS
            )
        except Exception:
            # Offline mode may keep using an expired but structurally valid
            # database. Explicit refreshes still report the update failure.
            if had_valid_cache and not refresh:
                return path
            raise
        return path

    @classmethod
    def has_local_data(cls, source_id: str) -> bool:
        """Returns whether any structurally valid offline cache is present."""
        return GtfsDatabase.is_valid_cache(cls.database_path(source_id))

    @classmethod
    def has_partial_download(cls, source_id: str) -> bool:
        """Detects an interrupted archive which can be resumed after restart."""
        partial = cls.database_path(source_id).with_suffix('.zip.part')
        return partial.exists() and partial.stat().st_size > 0

    @classmethod
    def source_metadata(cls, source_id: str) -> dict[str, str]:
        """Returns cache build and source validity metadata for the UI."""
        path = cls.database_path(source_id)
        result = GtfsDatabase.metadata(path)
        if (
            not GtfsDatabase.is_valid_cache(path)
            or result.get('schema_version') != '4'
        ):
            return result
        with GtfsDatabase.connect(path) as connection:
            coverage = GtfsDatabase.service_range(connection, source_id)
            row = connection.execute(
                """
                    SELECT publisher_name, publisher_url, language, version
                    FROM feed_info WHERE feed_id = ?
                """,
                (source_id,)
            ).fetchone()
        if coverage:
            result['source_coverage_from'] = coverage[0].isoformat()
            result['source_coverage_to'] = coverage[1].isoformat()
        if row:
            result.update({
                'publisher_name': str(row['publisher_name']),
                'publisher_url': str(row['publisher_url']),
                'feed_language': str(row['language']),
                'feed_version': str(row['version'])
            })
        return result

    @classmethod
    def schedule_availability(
        cls,
        source_id: str,
        service_date: date,
        database_path: Path | None = None
    ) -> RailScheduleAvailability:
        """Returns an explicit date status instead of an unexplained empty list."""
        path = database_path or cls.database_path(source_id)
        if database_path is None:
            metadata = cls.source_metadata(source_id)
        else:
            metadata = GtfsDatabase.metadata(path)
            if metadata.get('schema_version') == '4':
                with GtfsDatabase.connect(path) as connection:
                    row = connection.execute(
                        """
                            SELECT version FROM feed_info WHERE feed_id = ?
                        """,
                        (source_id,)
                    ).fetchone()
                if row:
                    metadata['feed_version'] = str(row['version'])
        common = {
            'source_id': source_id,
            'service_date': service_date,
            'feed_version': metadata.get('feed_version', ''),
            'built_at': metadata.get('built_at', '')
        }
        if not GtfsDatabase.is_valid_cache(path):
            return RailScheduleAvailability(
                **common,
                status='missing',
                message=public_transport_message(
                    'PUBLIC_TRANSPORT_ERROR.RAIL_SCHEDULE_UNAVAILABLE',
                    source=source_id
                )
            )
        if metadata.get('schema_version') != '4':
            return RailScheduleAvailability(
                **common,
                status='missing',
                message=public_transport_message(
                    'PUBLIC_TRANSPORT_ERROR.RAIL_SCHEDULE_UNAVAILABLE',
                    source=source_id
                )
            )

        with GtfsDatabase.connect(path) as connection:
            coverage = GtfsDatabase.service_range(connection, source_id)
            service_ids = (
                GtfsDatabase.active_service_ids(
                    connection,
                    source_id,
                    service_date
                )
                if coverage and coverage[0] <= service_date <= coverage[1]
                else set()
            )
        if not coverage:
            return RailScheduleAvailability(
                **common,
                status='missing',
                message=public_transport_message(
                    'PUBLIC_TRANSPORT_ERROR.RAIL_SCHEDULE_RANGE_UNKNOWN',
                    source=source_id
                )
            )

        coverage_from, coverage_to = coverage
        stale = coverage_to < date.today()
        range_values = {
            **common,
            'coverage_from': coverage_from,
            'coverage_to': coverage_to,
            'stale': stale
        }
        if not coverage_from <= service_date <= coverage_to:
            return RailScheduleAvailability(
                **range_values,
                status='outside_range',
                message=public_transport_message(
                    'PUBLIC_TRANSPORT_ERROR.RAIL_SCHEDULE_DATE_OUTSIDE_RANGE',
                    date=service_date.isoformat(),
                    start=coverage_from.isoformat(),
                    end=coverage_to.isoformat()
                )
            )
        if not service_ids:
            return RailScheduleAvailability(
                **range_values,
                status='no_service',
                message=public_transport_message(
                    'PUBLIC_TRANSPORT_ERROR.RAIL_SCHEDULE_DATE_UNAVAILABLE',
                    date=service_date.isoformat()
                )
            )
        return RailScheduleAvailability(
            **range_values,
            status='available',
            message=(
                public_transport_message(
                    'PUBLIC_TRANSPORT_ERROR.RAIL_SCHEDULE_STALE',
                    end=coverage_to.isoformat()
                )
                if stale
                else None
            )
        )

    @classmethod
    def require_service_date(
        cls,
        source_id: str,
        service_date: date,
        database_path: Path | None = None
    ) -> RailScheduleAvailability:
        """Returns availability or raises its localized missing-data reason."""
        availability = cls.schedule_availability(
            source_id,
            service_date,
            database_path
        )
        if availability.available:
            return availability
        message = availability.message or public_transport_message(
            'PUBLIC_TRANSPORT_ERROR.RAIL_SCHEDULE_UNAVAILABLE',
            source=source_id
        )
        raise PublicTransportValueError(message.key, **message.parameters)

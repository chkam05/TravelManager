"""Source-scoped, fail-safe railway trip updates.

Realtime is an optional overlay.  A missing, invalid or expired feed never
prevents the static GTFS timetable from being displayed.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, timezone
import json
from io import BytesIO
import ssl
from threading import Lock
from typing import ClassVar
from urllib.error import URLError
from urllib.request import Request, urlopen

from resources.public_transport.rail_gtfs_sources import RailGtfsSources
from resources.public_transport.public_transport_messages import public_transport_message
from utils.public_transport.download_progress import PublicTransportDownloadProgress


@dataclass(frozen=True)
class RailStopUpdate:
    stop_sequence: int | None = None
    stop_id: str = ''
    arrival: datetime | None = None
    departure: datetime | None = None
    cancelled: bool = False


@dataclass(frozen=True)
class RailTripUpdate:
    trip_id: str
    service_date: date | None
    agency_id: str = ''
    numbers: tuple[str, ...] = ()
    cancelled: bool = False
    stops: tuple[RailStopUpdate, ...] = ()

    def stop(self, sequence: int | None = None, stop_id: str = '') -> RailStopUpdate | None:
        """Matches sequence first; stop_id is used by feeds which omit it."""
        if sequence is not None:
            match = next((item for item in self.stops if item.stop_sequence == sequence), None)
            if match is not None:
                return match
        return next((item for item in self.stops if stop_id and item.stop_id == stop_id), None)


@dataclass(frozen=True)
class RailRealtimeSnapshot:
    source_id: str
    updated_at: datetime
    trips: tuple[RailTripUpdate, ...]
    received_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def is_fresh(self, now: datetime | None = None) -> bool:
        current = now or datetime.now(timezone.utc)
        stamp = self.updated_at
        if stamp.tzinfo is None:
            stamp = stamp.replace(tzinfo=timezone.utc)
        return -120 <= (current - stamp.astimezone(timezone.utc)).total_seconds() <= RailRealtime.FRESH_SECONDS


class RailRealtime:
    """Downloads a physical feed once and shares its parsed snapshot."""

    FRESH_SECONDS: ClassVar[int] = 15 * 60
    CACHE_SECONDS: ClassVar[int] = 60
    REQUEST_TIMEOUT: ClassVar[int] = 12
    _cache: ClassVar[dict[str, RailRealtimeSnapshot]] = {}
    _locks: ClassVar[dict[str, Lock]] = {
        source_id: Lock() for source_id in RailGtfsSources.SOURCES
    }

    def __new__(cls):
        raise TypeError(f'{cls.__name__} cannot be instantiated.')

    @staticmethod
    def _datetime(value: object) -> datetime | None:
        if not value:
            return None
        try:
            parsed = datetime.fromisoformat(str(value).replace('Z', '+00:00'))
            return parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)
        except ValueError:
            return None

    @staticmethod
    def _date(value: object) -> date | None:
        try:
            text = str(value or '')
            if len(text) == 8 and text.isdigit():
                return datetime.strptime(text, '%Y%m%d').date()
            return date.fromisoformat(text)
        except ValueError:
            return None

    @classmethod
    def parse_polish_trains(cls, payload: bytes) -> RailRealtimeSnapshot:
        data = json.loads(payload)
        updated_at = cls._datetime(data.get('timestamp'))
        if updated_at is None or not isinstance(data.get('trip_updates'), list):
            raise ValueError('Invalid Polish Trains updates feed')
        trips = []
        for item in data['trip_updates']:
            if not isinstance(item, dict) or not item.get('trip_id'):
                continue
            stops = []
            for stop in item.get('stop_times') or ():
                if not isinstance(stop, dict):
                    continue
                sequence = stop.get('stop_sequence')
                stops.append(RailStopUpdate(
                    stop_sequence=int(sequence) if sequence is not None else None,
                    stop_id=str(stop.get('stop_id') or ''),
                    arrival=cls._datetime(stop.get('arrival')),
                    departure=cls._datetime(stop.get('departure')),
                    cancelled=bool(stop.get('cancelled', False))
                ))
                # platform/track are deliberately ignored: the publisher does
                # not guarantee these values as confirmed live changes.
            trips.append(RailTripUpdate(
                trip_id=str(item['trip_id']),
                service_date=cls._date(item.get('start_date')),
                agency_id=str(item.get('agency_id') or ''),
                numbers=tuple(str(value) for value in item.get('numbers') or ()),
                cancelled=bool(item.get('cancelled', False)),
                stops=tuple(stops)
            ))
        return RailRealtimeSnapshot('polish_trains', updated_at, tuple(trips))

    @classmethod
    def parse_wkd(cls, payload: bytes) -> RailRealtimeSnapshot:
        from google.transit import gtfs_realtime_pb2

        message = gtfs_realtime_pb2.FeedMessage()
        message.ParseFromString(payload)
        updated_at = datetime.fromtimestamp(message.header.timestamp, timezone.utc)
        trips = []
        for entity in message.entity:
            if not entity.HasField('trip_update'):
                continue
            update = entity.trip_update
            descriptor = update.trip
            relationship = descriptor.schedule_relationship
            cancelled = relationship in (
                gtfs_realtime_pb2.TripDescriptor.CANCELED,
                gtfs_realtime_pb2.TripDescriptor.DELETED,
            )
            stops = []
            for item in update.stop_time_update:
                stop_relationship = item.schedule_relationship
                skipped = stop_relationship in (
                    gtfs_realtime_pb2.TripUpdate.StopTimeUpdate.SKIPPED,
                    gtfs_realtime_pb2.TripUpdate.StopTimeUpdate.NO_DATA,
                )
                arrival = (datetime.fromtimestamp(item.arrival.time, timezone.utc)
                           if item.HasField('arrival') and item.arrival.time else None)
                departure = (datetime.fromtimestamp(item.departure.time, timezone.utc)
                             if item.HasField('departure') and item.departure.time else None)
                stops.append(RailStopUpdate(
                    stop_sequence=item.stop_sequence or None,
                    stop_id=item.stop_id,
                    arrival=arrival,
                    departure=departure,
                    cancelled=skipped
                ))
            trips.append(RailTripUpdate(
                trip_id=descriptor.trip_id,
                service_date=cls._date(descriptor.start_date),
                agency_id=descriptor.route_id,
                cancelled=cancelled,
                stops=tuple(stops)
            ))
        return RailRealtimeSnapshot('wkd', updated_at, tuple(trips))

    @classmethod
    def _download(cls, source_id: str) -> bytes:
        source = RailGtfsSources.SOURCES[source_id]
        request = Request(source.realtime_url, headers={
            'Accept': 'application/json,application/x-protobuf,*/*',
            'User-Agent': 'TravelManager/1.0'
        })
        context: ssl.SSLContext | None = None
        last_error: Exception | None = None
        for _attempt in range(2):
            try:
                with urlopen(request, timeout=cls.REQUEST_TIMEOUT, context=context) as response:
                    total = int(response.headers.get('Content-Length') or 0)
                    current = 0
                    output = BytesIO()
                    while True:
                        chunk = response.read(256 * 1024)
                        if not chunk:
                            break
                        output.write(chunk)
                        current += len(chunk)
                        PublicTransportDownloadProgress.report(
                            public_transport_message(
                                'DOWNLOAD_STATUS.GTFS_REALTIME', feed=source_id
                            ),
                            current,
                            total or current
                        )
                    return output.getvalue()
            except URLError as error:
                last_error = error
                if context is None and isinstance(error.reason, ssl.SSLCertVerificationError):
                    context = ssl._create_unverified_context()
        assert last_error is not None
        raise last_error

    @classmethod
    def snapshot(cls, source_id: str) -> RailRealtimeSnapshot | None:
        """Returns memory-only updates and never performs network I/O."""
        return cls._cache.get(source_id)

    @classmethod
    def cached_snapshot(cls, source_id: str) -> RailRealtimeSnapshot | None:
        """Returns memory-only updates and never performs network I/O."""
        return cls.snapshot(source_id)

    @classmethod
    def refresh(cls, source_id: str) -> RailRealtimeSnapshot | None:
        """Explicitly refreshes updates; called only by the update action."""
        cached = cls._cache.get(source_id)
        now = datetime.now(timezone.utc)
        if cached and (now - cached.received_at).total_seconds() < cls.CACHE_SECONDS:
            return cached
        with cls._locks[source_id]:
            cached = cls._cache.get(source_id)
            if cached and (now - cached.received_at).total_seconds() < cls.CACHE_SECONDS:
                return cached
            try:
                payload = cls._download(source_id)
                parsed = (
                    cls.parse_polish_trains(payload)
                    if source_id == RailGtfsSources.POLISH_TRAINS
                    else cls.parse_wkd(payload)
                )
                cls._cache[source_id] = parsed
                return parsed
            except Exception:
                return cls._cache.get(source_id)

    @classmethod
    def match(
        cls,
        snapshot: RailRealtimeSnapshot | None,
        trip_id: str,
        service_date: date,
        agency_ids: tuple[str, ...],
        numbers: tuple[str, ...] = ()
    ) -> RailTripUpdate | None:
        """Uses exact identity, then the documented unambiguous PL fallback."""
        if snapshot is None or not snapshot.is_fresh():
            return None
        exact = [item for item in snapshot.trips if item.trip_id == trip_id
                 and (item.service_date is None or item.service_date == service_date)
                 and (not item.agency_id or item.agency_id in agency_ids)]
        if len(exact) == 1:
            return exact[0]
        if snapshot.source_id != RailGtfsSources.POLISH_TRAINS:
            return None
        wanted = {value.strip() for value in numbers if value.strip()}
        fallback = [item for item in snapshot.trips
                    if item.service_date == service_date
                    and item.agency_id in agency_ids
                    and wanted.intersection(item.numbers)]
        return fallback[0] if len(fallback) == 1 else None

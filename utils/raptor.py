"""Small, dependency-free, round-based public transport router.

The module deliberately knows nothing about GTFS or SQLite.  Callers provide a
normalised timetable for one service day; this keeps the algorithm reusable by
all public-transport providers in TravelManager.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


INFINITY = 10**12


@dataclass(frozen=True)
class RaptorStopTime:
    stop_id: str
    arrival: int
    departure: int
    sequence: int


@dataclass(frozen=True)
class RaptorTrip:
    trip_id: str
    route_id: str
    line: str
    mode: str
    headsign: str
    stops: tuple[RaptorStopTime, ...]
    source_feed_id: str = ''
    source_trip_id: str = ''


@dataclass(frozen=True)
class RaptorFootpath:
    from_stop_id: str
    to_stop_id: str
    duration: int


@dataclass(frozen=True)
class RaptorLeg:
    trip_id: str
    route_id: str
    line: str
    mode: str
    headsign: str
    from_stop_id: str
    to_stop_id: str
    departure: int
    arrival: int
    from_sequence: int
    to_sequence: int
    source_feed_id: str = ''
    source_trip_id: str = ''


@dataclass(frozen=True)
class RaptorJourney:
    legs: tuple[RaptorLeg, ...]

    @property
    def departure(self) -> int:
        return self.legs[0].departure

    @property
    def arrival(self) -> int:
        return self.legs[-1].arrival

    @property
    def transfers(self) -> int:
        rides = sum(leg.mode != 'walk' for leg in self.legs)
        return max(0, rides - 1)


class Raptor:
    """Finds journeys in rounds, where every round adds one vehicle boarding."""

    def __init__(
        self, trips: Iterable[RaptorTrip], footpaths: Iterable[RaptorFootpath] = ()
    ):
        self.trips = tuple(trip for trip in trips if len(trip.stops) >= 2)
        self.footpaths = tuple(footpaths)

    @staticmethod
    def _leg(trip: RaptorTrip, start: RaptorStopTime, end: RaptorStopTime) -> RaptorLeg:
        return RaptorLeg(
            trip.trip_id, trip.route_id, trip.line, trip.mode, trip.headsign,
            start.stop_id, end.stop_id, start.departure, end.arrival,
            start.sequence, end.sequence, trip.source_feed_id,
            trip.source_trip_id
        )

    @staticmethod
    def _walk(footpath: RaptorFootpath, departure: int) -> RaptorLeg:
        return RaptorLeg(
            '', '', 'Dojście', 'walk', '', footpath.from_stop_id,
            footpath.to_stop_id, departure, departure + footpath.duration,
            0, 1
        )

    def _walk_forward(
        self, times: dict[str, int], paths: dict[str, tuple[RaptorLeg, ...]]
    ) -> tuple[dict[str, int], dict[str, tuple[RaptorLeg, ...]]]:
        result, result_paths = dict(times), dict(paths)
        for footpath in self.footpaths:
            departure = times.get(footpath.from_stop_id)
            source_path = paths.get(footpath.from_stop_id, ())
            if (
                departure is None
                or not source_path
                or source_path[-1].mode == 'walk'
            ):
                continue
            arrival = departure + footpath.duration
            if arrival < result.get(footpath.to_stop_id, INFINITY):
                result[footpath.to_stop_id] = arrival
                result_paths[footpath.to_stop_id] = (
                    *source_path,
                    self._walk(footpath, departure)
                )
        return result, result_paths

    def _walk_backward(
        self, times: dict[str, int], paths: dict[str, tuple[RaptorLeg, ...]]
    ) -> tuple[dict[str, int], dict[str, tuple[RaptorLeg, ...]]]:
        result, result_paths = dict(times), dict(paths)
        for footpath in self.footpaths:
            deadline = times.get(footpath.to_stop_id)
            suffix_path = paths.get(footpath.to_stop_id, ())
            if (
                deadline is None
                or not suffix_path
                or suffix_path[0].mode == 'walk'
            ):
                continue
            departure = deadline - footpath.duration
            if departure > result.get(footpath.from_stop_id, -INFINITY):
                result[footpath.from_stop_id] = departure
                result_paths[footpath.from_stop_id] = (
                    self._walk(footpath, departure),
                    *suffix_path
                )
        return result, result_paths

    def depart_after(
        self,
        origin: str,
        destination: str,
        departure: int,
        max_transfers: int = 3,
        minimum_transfer: int = 120,
        maximum_transfer: int | None = None,
        limit: int = 5,
    ) -> list[RaptorJourney]:
        previous = {origin: departure}
        paths: dict[str, tuple[RaptorLeg, ...]] = {origin: ()}
        candidates: list[RaptorJourney] = []

        for round_index in range(max_transfers + 1):
            current = dict(previous)
            current_paths = dict(paths)
            for trip in self.trips:
                boarded: RaptorStopTime | None = None
                prefix: tuple[RaptorLeg, ...] = ()
                for stop in trip.stops:
                    ready = previous.get(stop.stop_id)
                    if boarded is None and ready is not None:
                        prefix_path = paths.get(stop.stop_id, ())
                        earliest = ready + (minimum_transfer if prefix_path else 0)
                        wait = stop.departure - ready
                        if stop.departure >= earliest and (
                            round_index == 0
                            or maximum_transfer is None
                            or wait <= maximum_transfer
                        ):
                            boarded = stop
                            prefix = prefix_path
                    if boarded is None or stop.sequence <= boarded.sequence:
                        continue
                    if stop.arrival < current.get(stop.stop_id, INFINITY):
                        leg = self._leg(trip, boarded, stop)
                        current[stop.stop_id] = stop.arrival
                        current_paths[stop.stop_id] = (*prefix, leg)
            current, current_paths = self._walk_forward(current, current_paths)
            if destination in current_paths and current_paths[destination]:
                candidates.append(RaptorJourney(current_paths[destination]))
            if current == previous:
                break
            previous, paths = current, current_paths
        return self._distinct(candidates, limit, arrive_by=False)

    def arrive_by(
        self,
        origin: str,
        destination: str,
        arrival: int,
        max_transfers: int = 3,
        minimum_transfer: int = 120,
        maximum_transfer: int | None = None,
        limit: int = 5,
    ) -> list[RaptorJourney]:
        following = {destination: arrival}
        paths: dict[str, tuple[RaptorLeg, ...]] = {destination: ()}
        candidates: list[RaptorJourney] = []

        for round_index in range(max_transfers + 1):
            current = dict(following)
            current_paths = dict(paths)
            for trip in self.trips:
                alight: RaptorStopTime | None = None
                suffix: tuple[RaptorLeg, ...] = ()
                for stop in reversed(trip.stops):
                    deadline = following.get(stop.stop_id)
                    if alight is None and deadline is not None:
                        suffix_path = paths.get(stop.stop_id, ())
                        latest = deadline - (minimum_transfer if suffix_path else 0)
                        wait = deadline - stop.arrival
                        if stop.arrival <= latest and (
                            round_index == 0
                            or maximum_transfer is None
                            or wait <= maximum_transfer
                        ):
                            alight = stop
                            suffix = suffix_path
                    if alight is None or stop.sequence >= alight.sequence:
                        continue
                    if stop.departure > current.get(stop.stop_id, -INFINITY):
                        leg = self._leg(trip, stop, alight)
                        current[stop.stop_id] = stop.departure
                        current_paths[stop.stop_id] = (leg, *suffix)
            current, current_paths = self._walk_backward(current, current_paths)
            if origin in current_paths and current_paths[origin]:
                candidates.append(RaptorJourney(current_paths[origin]))
            if current == following:
                break
            following, paths = current, current_paths
        return self._distinct(candidates, limit, arrive_by=True)

    @staticmethod
    def _distinct(
        journeys: Iterable[RaptorJourney], limit: int, arrive_by: bool
    ) -> list[RaptorJourney]:
        unique: dict[tuple[tuple[str, int, int], ...], RaptorJourney] = {}
        for journey in journeys:
            key = tuple((leg.trip_id, leg.from_sequence, leg.to_sequence) for leg in journey.legs)
            unique[key] = journey
        return sorted(
            unique.values(),
            key=(lambda item: (-item.departure, item.arrival, item.transfers))
            if arrive_by else
            (lambda item: (item.arrival, item.transfers, -item.departure))
        )[:max(1, limit)]

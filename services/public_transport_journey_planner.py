from __future__ import annotations

from collections import defaultdict
from datetime import date
from pathlib import Path
from math import asin, cos, radians, sin, sqrt
from hashlib import sha1
import re
import sqlite3
import unicodedata

from core.gtfs_database import GtfsDatabase
from utils.raptor import (
    Raptor, RaptorFootpath, RaptorJourney, RaptorStopTime, RaptorTrip
)


class PublicTransportJourneyPlanner:
    """Adapts one TravelManager GTFS cache to the provider-neutral RAPTOR core."""

    MODES = {0: 'tram', 1: 'metro', 2: 'train', 11: 'trolley'}

    def __init__(self, database_path: Path, agency_ids: tuple[str, ...] = ()):
        self.database_path = database_path
        self.agency_ids = agency_ids

    @staticmethod
    def seconds(value: str) -> int:
        hours, minutes, seconds = (int(part) for part in value.split(':', 2))
        return hours * 3600 + minutes * 60 + seconds

    @staticmethod
    def clock(value: int) -> str:
        return f'{(value // 3600) % 24:02d}:{(value % 3600) // 60:02d}'

    def catalog(self, service_date: date) -> dict:
        with GtfsDatabase.connect(self.database_path) as connection:
            feeds = self._active_feeds(connection, service_date)
            stops, _stop_groups = self._stops(connection, feeds)
            if self.agency_ids:
                trips = self._trips(connection, feeds, service_date, _stop_groups)
                served = {
                    stop.stop_id for trip in trips for stop in trip.stops
                }
                stops = {
                    stop_id: stop for stop_id, stop in stops.items()
                    if stop_id in served
                }
        cities: dict[str, list[dict]] = defaultdict(list)
        for stop in stops.values():
            cities[stop['city']].append({
                'id': stop['id'], 'name': stop['name'],
                'latitude': stop['latitude'], 'longitude': stop['longitude']
            })
        return {'cities': [
            {'name': city, 'stops': sorted(items, key=lambda item: item['name'].casefold())}
            for city, items in sorted(cities.items(), key=lambda item: item[0].casefold())
        ]}

    def search(
        self, service_date: date, origin: str, destination: str,
        seconds: int, arrive_by: bool, max_transfer_minutes: int,
        max_transfers: int = 3, limit: int = 5
    ) -> dict:
        with GtfsDatabase.connect(self.database_path) as connection:
            feeds = self._active_feeds(connection, service_date)
            stops, stop_groups = self._stops(connection, feeds)
            trips = self._trips(connection, feeds, service_date, stop_groups)
            if origin not in stops or destination not in stops:
                raise ValueError('Nieprawidłowy przystanek początkowy lub docelowy.')
            footpaths = self._footpaths(stops)
            arguments = dict(
                origin=origin, destination=destination,
                max_transfers=max_transfers, minimum_transfer=120,
                maximum_transfer=max(1, max_transfer_minutes) * 60, limit=limit
            )
            journeys = self._journey_variants(
                trips, footpaths, arrive_by, seconds, arguments,
                maximum_searches=max(8, limit * 3)
            )
            journeys = self._rank_journeys(journeys, stops, arrive_by)
            return {'journeys': [
                self._payload(item, stops, service_date, connection)
                for item in journeys[:limit]
            ]}

    @staticmethod
    def _journey_variants(
        trips: list[RaptorTrip], footpaths: list[RaptorFootpath],
        arrive_by: bool, seconds: int, arguments: dict,
        maximum_searches: int
    ) -> list[RaptorJourney]:
        """Finds alternatives by progressively excluding trips already used."""
        all_footpaths = frozenset(
            (footpath.from_stop_id, footpath.to_stop_id)
            for footpath in footpaths
        )
        pending: list[tuple[frozenset[str], frozenset[tuple[str, str]]]] = [
            (frozenset(), frozenset()),
            # A no-walking seed preserves same-stop alternatives that an
            # earlier walking label would otherwise suppress.
            (frozenset(), all_footpaths)
        ]
        visited: set[tuple[frozenset[str], frozenset[tuple[str, str]]]] = set()
        journeys: dict[tuple[tuple[str, str, str, int], ...], RaptorJourney] = {}
        while pending and len(visited) < maximum_searches:
            state = pending.pop(0)
            if state in visited:
                continue
            visited.add(state)
            excluded_trips, excluded_footpaths = state
            router = Raptor(
                (trip for trip in trips if trip.trip_id not in excluded_trips),
                (
                    footpath for footpath in footpaths
                    if (footpath.from_stop_id, footpath.to_stop_id)
                    not in excluded_footpaths
                )
            )
            found = (
                router.arrive_by(arrival=seconds, **arguments)
                if arrive_by else
                router.depart_after(departure=seconds, **arguments)
            )
            for journey in found:
                identity = tuple(
                    (leg.trip_id, leg.from_stop_id, leg.to_stop_id, leg.departure)
                    for leg in journey.legs
                )
                journeys.setdefault(identity, journey)
                for trip_id in {
                    leg.trip_id for leg in journey.legs if leg.trip_id
                }:
                    candidate = (
                        frozenset((*excluded_trips, trip_id)),
                        excluded_footpaths
                    )
                    if candidate not in visited and candidate not in pending:
                        pending.append(candidate)
                for footpath in {
                    (leg.from_stop_id, leg.to_stop_id)
                    for leg in journey.legs if leg.mode == 'walk'
                }:
                    candidate = (
                        excluded_trips,
                        frozenset((*excluded_footpaths, footpath))
                    )
                    if candidate not in visited and candidate not in pending:
                        pending.append(candidate)
        return list(journeys.values())

    def _rank_journeys(
        self, journeys: list[RaptorJourney], stops: dict[str, dict], arrive_by: bool
    ) -> list[RaptorJourney]:
        """Prefers useful journeys over small time gains bought with backtracking."""
        if len(journeys) < 2:
            return journeys

        def backward_distance(journey: RaptorJourney) -> float:
            destination = stops[journey.legs[-1].to_stop_id]
            total = 0.0
            for leg in journey.legs:
                before = self._distance(stops[leg.from_stop_id], destination)
                after = self._distance(stops[leg.to_stop_id], destination)
                total += max(0.0, after - before)
            return total

        def initial_regression(journey: RaptorJourney) -> float:
            destination = stops[journey.legs[-1].to_stop_id]
            first = journey.legs[0]
            return max(0.0, (
                self._distance(stops[first.to_stop_id], destination)
                - self._distance(stops[first.from_stop_id], destination)
            ))

        def score(journey: RaptorJourney) -> float:
            # Ten minutes per transfer reflects the inconvenience and failure
            # risk; every kilometre travelled away from the destination adds
            # another ten minutes of perceived cost.
            return (
                journey.arrival - journey.departure
                + journey.transfers * 600
                + backward_distance(journey) * 600
            )

        reasonable = []
        for candidate in journeys:
            discard = False
            for alternative in journeys:
                if (
                    initial_regression(candidate) > 0.25
                    and initial_regression(alternative) <= 0.10
                ):
                    discard = True
                    break
                extra_transfers = candidate.transfers - alternative.transfers
                if extra_transfers <= 0:
                    continue
                time_gain = (
                    candidate.departure - alternative.departure
                    if arrive_by else alternative.arrival - candidate.arrival
                )
                # Do not recommend another transfer for a gain smaller than
                # ten minutes.  This removes technically fast but absurd
                # zig-zags such as the Brynów -> Stara Ligota detour.
                if time_gain <= extra_transfers * 600 and score(alternative) < score(candidate):
                    discard = True
                    break
            if not discard:
                reasonable.append(candidate)
        selected = reasonable or journeys
        return sorted(selected, key=lambda journey: (
            score(journey),
            -journey.departure if arrive_by else journey.arrival,
            journey.transfers
        ))

    @classmethod
    def _footpaths(cls, stops: dict[str, dict]) -> list[RaptorFootpath]:
        """Connects nearby named stops without an expensive all-pairs scan."""
        maximum_km = 0.9
        cell_size = 0.01
        cells: dict[tuple[int, int], list[dict]] = defaultdict(list)
        for stop in stops.values():
            cell = (
                int(stop['latitude'] // cell_size),
                int(stop['longitude'] // cell_size)
            )
            cells[cell].append(stop)
        result: list[RaptorFootpath] = []
        seen: set[tuple[str, str]] = set()
        for stop in stops.values():
            latitude_cell = int(stop['latitude'] // cell_size)
            longitude_cell = int(stop['longitude'] // cell_size)
            for latitude_offset in (-1, 0, 1):
                for longitude_offset in (-2, -1, 0, 1, 2):
                    for target in cells.get((
                        latitude_cell + latitude_offset,
                        longitude_cell + longitude_offset
                    ), ()):
                        identity = (stop['id'], target['id'])
                        if stop['id'] == target['id'] or identity in seen:
                            continue
                        distance = cls._distance(stop, target)
                        if not 0.03 <= distance <= maximum_km:
                            continue
                        seen.add(identity)
                        # 4.5 km/h plus one minute for crossings and finding
                        # the correct stop post.
                        duration = max(60, round(distance / 4.5 * 3600) + 60)
                        result.append(RaptorFootpath(
                            stop['id'], target['id'], duration
                        ))
        return result

    @staticmethod
    def _active_feeds(connection: sqlite3.Connection, service_date: date) -> dict[str, set[str]]:
        feed_ids = {str(row[0]) for row in connection.execute(
            'SELECT feed_id FROM calendar UNION SELECT feed_id FROM calendar_dates'
        )}
        return {
            feed_id: GtfsDatabase.active_service_ids(connection, feed_id, service_date)
            for feed_id in feed_ids
            if GtfsDatabase.active_service_ids(connection, feed_id, service_date)
        }

    @staticmethod
    def _normalise_stop_name(value: str) -> str:
        """Builds a stable identity for platform variants of one named stop."""
        folded = unicodedata.normalize('NFKD', value.casefold())
        return re.sub(r'[^a-z0-9]+', ' ', ''.join(
            character for character in folded if not unicodedata.combining(character)
        )).strip()

    @classmethod
    def _stops(
        cls, connection: sqlite3.Connection, feeds: dict[str, set[str]]
    ) -> tuple[dict[str, dict], dict[tuple[str, str], str]]:
        result: dict[str, dict] = {}
        stop_groups: dict[tuple[str, str], str] = {}
        if not feeds:
            return result, stop_groups
        placeholders = GtfsDatabase.placeholders(feeds)
        rows = connection.execute(f"""
            SELECT s.feed_id, s.stop_id,
                   COALESCE(NULLIF(parent.name, ''), s.name) AS group_name,
                   COALESCE(s.latitude, parent.latitude) AS latitude,
                   COALESCE(s.longitude, parent.longitude) AS longitude,
                   s.parent_station,
                   COALESCE(
                       NULLIF(se.city, ''),
                       (
                           SELECT NULLIF(child_extension.city, '')
                           FROM stops child
                           JOIN stop_extensions child_extension
                             ON child_extension.feed_id=child.feed_id
                            AND child_extension.stop_id=child.stop_id
                           WHERE child.feed_id=s.feed_id
                             AND child.parent_station=s.stop_id
                             AND child_extension.city <> ''
                           LIMIT 1
                       ),
                       ''
                   ) AS city
            FROM stops s LEFT JOIN stop_extensions se
              ON se.feed_id=s.feed_id AND se.stop_id=s.stop_id
            LEFT JOIN stops parent ON parent.feed_id=s.feed_id
              AND parent.stop_id=s.parent_station
            WHERE s.feed_id IN ({placeholders})
              AND COALESCE(s.latitude, parent.latitude) IS NOT NULL
              AND COALESCE(s.longitude, parent.longitude) IS NOT NULL
            ORDER BY group_name, s.stop_id
        """, tuple(feeds)).fetchall()
        for row in rows:
            feed_id = str(row['feed_id'])
            city = str(row['city'] or 'Pozostałe').strip() or 'Pozostałe'
            name = str(row['group_name']).strip()
            # Feed packages may overlap in validity (notably dated GZM
            # archives), so feed_id must not split one passenger-facing stop.
            identity = f'{cls._normalise_stop_name(city)}\0{cls._normalise_stop_name(name)}'
            key = f'group:{sha1(identity.encode("utf-8")).hexdigest()[:16]}'
            item = result.setdefault(key, {
                'id': key, 'name': name, 'city': city,
                'latitude': float(row['latitude']), 'longitude': float(row['longitude']),
                'members': set()
            })
            stop_id = str(row['stop_id'])
            item['members'].add(stop_id)
            stop_groups[(feed_id, stop_id)] = key
            parent_id = str(row['parent_station'] or '')
            if parent_id:
                stop_groups[(feed_id, parent_id)] = key
        return result, stop_groups

    def _trips(
        self, connection: sqlite3.Connection, feeds: dict[str, set[str]], service_date: date,
        stop_groups: dict[tuple[str, str], str]
    ) -> list[RaptorTrip]:
        del service_date
        result: list[RaptorTrip] = []
        for feed_id, services in feeds.items():
            agency_filter = ''
            parameters: list[object] = [feed_id, *services]
            if self.agency_ids:
                agency_filter = (
                    ' AND r.agency_id IN ('
                    + GtfsDatabase.placeholders(self.agency_ids) + ')'
                )
                parameters.extend(self.agency_ids)
            rows = connection.execute(f"""
                SELECT t.trip_id, t.route_id, t.headsign, r.short_name, r.long_name,
                       r.route_type, st.stop_id, st.arrival_time, st.departure_time,
                       st.stop_sequence, s.parent_station
                FROM trips t JOIN routes r ON r.feed_id=t.feed_id AND r.route_id=t.route_id
                JOIN stop_times st ON st.feed_id=t.feed_id AND st.trip_id=t.trip_id
                JOIN stops s ON s.feed_id=st.feed_id AND s.stop_id=st.stop_id
                WHERE t.feed_id=? AND t.service_id IN ({GtfsDatabase.placeholders(services)})
                  {agency_filter}
                  AND NOT (st.pickup_type=1 AND st.drop_off_type=1)
                ORDER BY t.trip_id, st.stop_sequence
            """, parameters).fetchall()
            grouped: dict[str, list] = defaultdict(list)
            for row in rows:
                grouped[str(row['trip_id'])].append(row)
            for trip_id, items in grouped.items():
                first = items[0]
                stop_times = []
                for row in items:
                    try:
                        group_id = stop_groups.get((feed_id, str(row['stop_id'])))
                        if not group_id:
                            continue
                        stop_times.append(RaptorStopTime(
                            group_id,
                            self.seconds(str(row['arrival_time'])),
                            self.seconds(str(row['departure_time'])), int(row['stop_sequence'])
                        ))
                    except (TypeError, ValueError):
                        continue
                result.append(RaptorTrip(
                    trip_id=f'{feed_id}:{trip_id}', route_id=f"{feed_id}:{first['route_id']}",
                    line=str(first['short_name'] or first['long_name'] or first['route_id']),
                    mode=self.MODES.get(int(first['route_type']), 'bus'),
                    headsign=str(first['headsign'] or ''), stops=tuple(stop_times),
                    source_feed_id=feed_id, source_trip_id=trip_id
                ))
        return result

    def _payload(
        self, journey: RaptorJourney, stops: dict[str, dict],
        service_date: date, connection: sqlite3.Connection | None = None
    ) -> dict:
        legs = []
        distance = 0.0
        previous = None
        for leg in journey.legs:
            start, end = stops[leg.from_stop_id], stops[leg.to_stop_id]
            if (
                previous is not None
                and previous.mode != 'walk'
                and leg.mode != 'walk'
            ):
                transfer_minutes = max(0, (leg.departure - previous.arrival) // 60)
                legs.append({
                    'type': 'transfer', 'line': 'Przesiadka', 'headsign': '',
                    'from': start['name'], 'from_stop_id': leg.from_stop_id,
                    'to': start['name'], 'to_stop_id': leg.from_stop_id,
                    'departure': self.clock(previous.arrival),
                    'arrival': self.clock(leg.departure),
                    'duration_minutes': transfer_minutes, 'distance_km': 0.0,
                    'geometry': [[start['latitude'], start['longitude']]]
                })
            leg_distance = self._distance(start, end)
            distance += leg_distance
            legs.append({
                'type': leg.mode, 'line': leg.line, 'headsign': leg.headsign,
                'from': start['name'], 'from_stop_id': leg.from_stop_id,
                'to': end['name'], 'to_stop_id': leg.to_stop_id,
                'departure': self.clock(leg.departure), 'arrival': self.clock(leg.arrival),
                'duration_minutes': max(0, (leg.arrival - leg.departure) // 60),
                'distance_km': leg_distance,
                'geometry': self._leg_geometry(connection, leg, start, end)
            })
            previous = leg
        return {
            'date': service_date.isoformat(), 'from': stops[journey.legs[0].from_stop_id]['name'],
            'to': stops[journey.legs[-1].to_stop_id]['name'],
            'departure': self.clock(journey.departure), 'arrival': self.clock(journey.arrival),
            'duration_minutes': max(0, (journey.arrival - journey.departure) // 60),
            'distance_km': distance, 'transfers': journey.transfers, 'legs': legs
        }

    @classmethod
    def _leg_geometry(
        cls, connection: sqlite3.Connection | None, leg,
        start: dict, end: dict
    ) -> list[list[float]]:
        """Returns the part of a GTFS shape actually travelled by this leg."""
        fallback = [
            [start['latitude'], start['longitude']],
            [end['latitude'], end['longitude']]
        ]
        if connection is None or leg.mode == 'walk' or not leg.trip_id:
            return fallback

        feed_id = str(leg.source_feed_id or '')
        trip_id = str(leg.source_trip_id or '')
        if not feed_id or not trip_id:
            return fallback
        trip = connection.execute(
            'SELECT shape_id FROM trips WHERE feed_id=? AND trip_id=?',
            (feed_id, trip_id)
        ).fetchone()
        shape_id = str(trip['shape_id'] or '') if trip else ''
        if shape_id:
            rows = connection.execute("""
                SELECT latitude, longitude FROM shapes
                WHERE feed_id=? AND shape_id=? ORDER BY point_sequence
            """, (feed_id, shape_id)).fetchall()
            points = [[float(row['latitude']), float(row['longitude'])] for row in rows]
            section = cls._shape_section(points, fallback[0], fallback[1])
            if len(section) >= 2:
                return section

        # Some feeds do not publish shapes.  Their ordered intermediate stops
        # still describe the travelled corridor better than one diagonal line.
        rows = connection.execute("""
            SELECT s.latitude, s.longitude
            FROM stop_times st
            JOIN stops s ON s.feed_id=st.feed_id AND s.stop_id=st.stop_id
            WHERE st.feed_id=? AND st.trip_id=?
              AND st.stop_sequence BETWEEN ? AND ?
              AND s.latitude IS NOT NULL AND s.longitude IS NOT NULL
            ORDER BY st.stop_sequence
        """, (feed_id, trip_id, leg.from_sequence, leg.to_sequence)).fetchall()
        points = [[float(row['latitude']), float(row['longitude'])] for row in rows]
        return points if len(points) >= 2 else fallback

    @staticmethod
    def _shape_section(
        points: list[list[float]], start: list[float], end: list[float]
    ) -> list[list[float]]:
        """Crops a possibly looping shape while preserving travel direction."""
        if len(points) < 2:
            return []

        def squared(point: list[float], target: list[float]) -> float:
            latitude_scale = cos(radians(target[0]))
            return (
                (point[0] - target[0]) ** 2
                + ((point[1] - target[1]) * latitude_scale) ** 2
            )

        end_distances = [squared(point, end) for point in points]
        best_end_from = [0] * len(points)
        best_index = len(points) - 1
        for index in range(len(points) - 1, -1, -1):
            if end_distances[index] <= end_distances[best_index]:
                best_index = index
            best_end_from[index] = best_index
        start_index = min(
            range(len(points)),
            key=lambda index: squared(points[index], start)
            + end_distances[best_end_from[index]]
        )
        end_index = best_end_from[start_index]
        section = points[start_index:end_index + 1]
        if not section:
            return []
        # Exact stop coordinates close tiny gaps between adjacent leg layers.
        return [start, *section, end]

    @staticmethod
    def _distance(start: dict, end: dict) -> float:
        """Returns an approximate great-circle distance for result summaries."""
        lat1, lon1 = radians(start['latitude']), radians(start['longitude'])
        lat2, lon2 = radians(end['latitude']), radians(end['longitude'])
        value = sin((lat2 - lat1) / 2) ** 2 + cos(lat1) * cos(lat2) * sin((lon2 - lon1) / 2) ** 2
        return round(12742.0 * asin(sqrt(value)), 2)

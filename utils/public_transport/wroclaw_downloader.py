from __future__ import annotations

from datetime import date, datetime, timedelta
import json
import math
from pathlib import Path
import re
from threading import Lock
from typing import Any, ClassVar
from urllib.parse import urljoin

from config import SETTINGS_DIR
from core.gtfs_database import GtfsDatabase
from models.public_transport.public_transport_vehicle_position import (
    PublicTransportVehiclePosition
)
from resources.public_transport.public_transport_type import PublicTransportType
from utils.public_transport.warsaw_downloader import WarsawDownloader


class WroclawDownloader(WarsawDownloader):
    """Downloads Wrocław's official static GTFS and live vehicle data."""

    BASE_URL: ClassVar[str] = 'https://open-data.cui.wroclaw.pl/'
    CARRIER: ClassVar[str] = 'Urząd Miejski Wrocławia / MPK Wrocław'
    CITY_NAME: ClassVar[str] = 'Wrocław i okolice'
    CITY_COLOR: ClassVar[str] = '#005CA9'
    URL_PREFIXES: ClassVar[tuple[str, ...]] = (BASE_URL,)
    _STATIC_INDEX: ClassVar[str] = urljoin(BASE_URL, 'hdb/ft/6/')
    _VEHICLES_URL: ClassVar[str] = urljoin(
        BASE_URL,
        'hdb/db/14?download=json'
    )
    _DATABASE_PATH: ClassVar[Path] = Path(SETTINGS_DIR) / 'wroclaw_gtfs.sqlite3'
    _LEGACY_DATABASE_PATH: ClassVar[Path] = (
        Path(SETTINGS_DIR) / 'public_transport' / 'wroclaw' / 'gtfs.sqlite3'
    )
    _DATABASE_LOCK: ClassVar[Lock] = Lock()
    _FEEDS: ClassVar[dict[str, dict[str, str]]] = {
        'W': {
            'name': 'Komunikacja miejska we Wrocławiu',
            'static': _STATIC_INDEX,
            'vehicles': _VEHICLES_URL
        }
    }
    _CARRIERS: ClassVar[dict[str, str]] = {
        'W': 'Urząd Miejski Wrocławia / MPK Wrocław'
    }

    @classmethod
    def _current_static_url(cls) -> str:
        """Selects the newest official GTFS archive effective today."""
        payload = super()._download_bytes(
            cls._STATIC_INDEX,
            'Lista archiwów GTFS: Wrocław'
        )
        html = payload.decode('utf-8', errors='replace')
        candidates: list[tuple[date, str]] = []
        pattern = re.compile(
            r'<tr>.*?GTFS_(\d{8}).*?href=["\']'
            r'([^"\']*/hdb/download/\d+/?)',
            re.IGNORECASE | re.DOTALL
        )
        for raw_date, href in pattern.findall(html):
            try:
                effective_date = datetime.strptime(raw_date, '%d%m%Y').date()
            except ValueError:
                continue
            candidates.append((effective_date, urljoin(cls.BASE_URL, href)))
        if not candidates:
            raise RuntimeError('Nie udało się ustalić aktualnego pliku GTFS Wrocławia.')
        today = date.today()
        active = [candidate for candidate in candidates if candidate[0] <= today]
        return max(active or candidates, key=lambda candidate: candidate[0])[1]

    @classmethod
    def _download_bytes(
        cls, url: str, item: str, current: int = 1, total: int = 1
    ) -> bytes:
        """Resolves the date-versioned Wrocław archive before download."""
        if url == cls._STATIC_INDEX:
            url = cls._current_static_url()
        return super()._download_bytes(url, item, current, total)

    @classmethod
    def download_vehicle_positions(
        cls,
        line: str = '',
        transport_type: str = '',
        feed_id: str = ''
    ) -> list[PublicTransportVehiclePosition]:
        """Downloads and converts Wrocław's live vehicle JSON."""
        if feed_id and feed_id != 'W':
            return []
        with cls._connection() as connection:
            line_types = {
                str(row['short_name']): cls._type_from_route(
                    int(row['route_type']),
                    str(row['feed_id'])
                )
                for row in connection.execute(
                    'SELECT feed_id, short_name, route_type FROM routes'
                )
            }
            active_services = set(GtfsDatabase.active_service_ids(
                connection,
                'W',
                date.today()
            ))
            schedules = cls._vehicle_schedules(
                connection,
                active_services
            )
        payload = cls._download_bytes(
            cls._VEHICLES_URL,
            'Pojazdy na żywo: Wrocław'
        )
        try:
            document = json.loads(payload.decode('utf-8-sig'))
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            raise RuntimeError('Nieprawidłowa odpowiedź pojazdów Wrocławia.') from error
        rows = document.get('dane', []) if isinstance(document, dict) else []
        positions = cls._parse_vehicle_rows(
            rows,
            line_types,
            line,
            transport_type
        )
        cls._enrich_vehicle_positions(positions, schedules)
        return positions

    @classmethod
    def _vehicle_schedules(
        cls,
        connection,
        active_services: set[str]
    ) -> dict[str, list[dict[str, Any]]]:
        """Loads today's trips and stops used to enrich live positions."""
        if not active_services:
            return {}
        placeholders = ','.join('?' for _service in active_services)
        rows = connection.execute(
            f"""
                SELECT r.short_name, t.trip_id, t.headsign, t.block_id,
                       st.departure_time, st.stop_sequence,
                       s.name stop_name, s.latitude, s.longitude
                FROM trips t
                JOIN routes r
                  ON r.feed_id = t.feed_id AND r.route_id = t.route_id
                JOIN stop_times st
                  ON st.feed_id = t.feed_id AND st.trip_id = t.trip_id
                JOIN stops s
                  ON s.feed_id = st.feed_id AND s.stop_id = st.stop_id
                WHERE t.feed_id = 'W'
                  AND t.service_id IN ({placeholders})
                ORDER BY r.short_name, t.trip_id, st.stop_sequence
            """,
            tuple(sorted(active_services))
        )
        trips: dict[str, dict[str, dict[str, Any]]] = {}
        for row in rows:
            line_name = str(row['short_name'])
            trip_id = str(row['trip_id'])
            trip = trips.setdefault(line_name, {}).setdefault(trip_id, {
                'trip_id': trip_id,
                'headsign': str(row['headsign'] or ''),
                'brigade': str(row['block_id'] or ''),
                'stops': []
            })
            seconds = cls._schedule_seconds(str(row['departure_time'] or ''))
            if seconds is None:
                continue
            trip['stops'].append({
                'seconds': seconds,
                'name': str(row['stop_name'] or ''),
                'latitude': row['latitude'],
                'longitude': row['longitude']
            })
        return {
            line_name: [trip for trip in line_trips.values() if trip['stops']]
            for line_name, line_trips in trips.items()
        }

    @staticmethod
    def _schedule_seconds(value: str) -> int | None:
        """Converts a GTFS clock, including hours after midnight."""
        match = re.fullmatch(r'(\d{1,2}):(\d{2})(?::(\d{2}))?', value)
        if not match:
            return None
        return (
            int(match.group(1)) * 3600
            + int(match.group(2)) * 60
            + int(match.group(3) or 0)
        )

    @classmethod
    def _enrich_vehicle_positions(
        cls,
        positions: list[PublicTransportVehiclePosition],
        schedules: dict[str, list[dict[str, Any]]]
    ) -> None:
        """Matches live rows with today's scheduled trip."""
        for position in positions:
            if position.recorded_at is None:
                continue
            seconds = (
                position.recorded_at.hour * 3600
                + position.recorded_at.minute * 60
                + position.recorded_at.second
            )
            candidates = []
            for trip in schedules.get(position.line, []):
                stops = trip['stops']
                if seconds < stops[0]['seconds'] - 300:
                    continue
                if seconds > stops[-1]['seconds'] + 300:
                    continue
                if position.brigade and not cls._brigade_matches(
                    position.brigade,
                    str(trip['brigade'])
                ):
                    continue
                next_index = next(
                    (
                        index for index, stop in enumerate(stops)
                        if stop['seconds'] >= seconds
                    ),
                    len(stops) - 1
                )
                nearby = stops[max(0, next_index - 1):next_index + 2]
                distance = min(
                    cls._distance_squared(
                        position.latitude,
                        position.longitude,
                        stop['latitude'],
                        stop['longitude']
                    )
                    for stop in nearby
                    if stop['latitude'] is not None and stop['longitude'] is not None
                )
                candidates.append((distance, trip, next_index))
            if not candidates:
                continue
            distance, trip, next_index = min(candidates, key=lambda item: item[0])
            if not position.brigade and distance > 0.0005:
                continue
            stops = trip['stops']
            position.trip_id = str(trip['trip_id'])
            position.direction = str(trip['headsign'])
            position.destination = str(stops[-1]['name'])
            position.next_stop = str(stops[next_index]['name'])

    @staticmethod
    def _brigade_matches(raw_brigade: str, gtfs_brigade: str) -> bool:
        """Matches values such as 01906 with GTFS brigade 6."""
        raw_digits = ''.join(character for character in raw_brigade if character.isdigit())
        gtfs_digits = ''.join(character for character in gtfs_brigade if character.isdigit())
        if not raw_digits or not gtfs_digits:
            return False
        return raw_digits.endswith(gtfs_digits.zfill(2))

    @staticmethod
    def _distance_squared(
        latitude: float,
        longitude: float,
        other_latitude: float,
        other_longitude: float
    ) -> float:
        """Returns a small-area coordinate distance adjusted for longitude."""
        longitude_scale = math.cos(math.radians(latitude))
        return (
            (latitude - float(other_latitude)) ** 2
            + ((longitude - float(other_longitude)) * longitude_scale) ** 2
        )

    @classmethod
    def _parse_vehicle_rows(
        cls,
        rows: list[dict[str, Any]],
        line_types: dict[str, PublicTransportType],
        line: str = '',
        transport_type: str = ''
    ) -> list[PublicTransportVehiclePosition]:
        """Converts current rows and discards historical positions."""
        parsed: list[tuple[datetime, PublicTransportVehiclePosition]] = []
        for row in rows:
            line_name = str(row.get('Nazwa_Linii') or '').strip()
            fleet_number = str(row.get('Nr_Boczny') or '').strip()
            if not line_name or not fleet_number or (line and line_name != line):
                continue
            vehicle_type = line_types.get(line_name, PublicTransportType.BUS)
            if transport_type and str(vehicle_type) != transport_type:
                continue
            try:
                latitude = float(row.get('Ostatnia_Pozycja_Szerokosc'))
                longitude = float(row.get('Ostatnia_Pozycja_Dlugosc'))
                recorded_at = datetime.fromisoformat(
                    str(row.get('Data_Aktualizacji') or '')
                )
            except (TypeError, ValueError):
                continue
            if not (50 <= latitude <= 52 and 15 <= longitude <= 18):
                continue
            parsed.append((recorded_at, PublicTransportVehiclePosition(
                vehicle_id=fleet_number,
                vehicle_label=fleet_number,
                license_plate=str(row.get('Nr_Rej') or '').strip(),
                source_code='W',
                line=line_name,
                trip_id='',
                direction='',
                next_stop='',
                destination='',
                status='',
                type=vehicle_type,
                latitude=latitude,
                longitude=longitude,
                bearing=None,
                speed=None,
                recorded_at=recorded_at,
                brigade=str(row.get('Brygada') or '').strip()
            )))
        if not parsed:
            return []
        newest = max(recorded_at for recorded_at, _position in parsed)
        current = [
            item for item in parsed
            if newest - item[0] <= timedelta(minutes=10)
        ]
        by_vehicle: dict[str, tuple[datetime, PublicTransportVehiclePosition]] = {}
        for item in current:
            previous = by_vehicle.get(item[1].vehicle_id)
            if previous is None or item[0] > previous[0]:
                by_vehicle[item[1].vehicle_id] = item
        return [item[1] for item in by_vehicle.values()]

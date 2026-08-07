from __future__ import annotations

from datetime import date, time, timedelta
import ssl
from threading import Lock
from typing import ClassVar
from urllib.error import URLError
from urllib.parse import parse_qs, urlencode, urlparse
from urllib.request import Request, urlopen

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
from utils.public_transport.download_progress import PublicTransportDownloadProgress


class GrudziadzDownloader:
    """Downloads the machine-readable Rozkładzik timetable for Grudziądz."""

    BASE_URL: ClassVar[str] = 'https://www.rozkladzik.pl/grudziadz/'
    DATA_URL: ClassVar[str] = f'{BASE_URL}data.txt'
    TIMETABLE_URL: ClassVar[str] = f'{BASE_URL}timetable.txt'
    URL_PREFIXES: ClassVar[tuple[str, ...]] = (BASE_URL,)
    CARRIER: ClassVar[str] = 'Wydział Transportu w Grudziądzu'
    CITY_NAME: ClassVar[str] = 'Grudziądz i okolice'
    CITY_COLOR: ClassVar[str] = '#006A8E'
    _USER_AGENT: ClassVar[str] = 'TravelManager/1.0'
    _REQUEST_TIMEOUT: ClassVar[int] = 20
    _DATA_LOCK: ClassVar[Lock] = Lock()
    _DATA_CACHE: ClassVar[dict | None] = None

    @classmethod
    def _download(cls, url: str, item: str) -> str:
        request = Request(url, headers={'User-Agent': cls._USER_AGENT})
        ssl_context: list[ssl.SSLContext | None] = [None]

        def execute() -> str:
            try:
                return cls._read_response(request, ssl_context[0])
            except URLError as error:
                if (
                    ssl_context[0] is None
                    and isinstance(
                        error.reason,
                        ssl.SSLCertVerificationError
                    )
                ):
                    ssl_context[0] = ssl._create_unverified_context()
                raise

        return PublicTransportDownloadProgress.retry(execute, item, 1, 1)

    @classmethod
    def _read_response(
        cls,
        request: Request,
        context: ssl.SSLContext | None = None
    ) -> str:
        """Executes a request with the selected SSL context."""
        with urlopen(
            request,
            timeout=cls._REQUEST_TIMEOUT,
            context=context
        ) as response:
            return response.read().decode('utf-8', errors='replace')

    @classmethod
    def _data(cls, refresh: bool = False) -> dict:
        with cls._DATA_LOCK:
            if cls._DATA_CACHE is not None and not refresh:
                return cls._DATA_CACHE
            cls._DATA_CACHE = cls.parse_data(
                cls._download(cls.DATA_URL, 'Rozkład Grudziądza')
            )
            return cls._DATA_CACHE

    @staticmethod
    def _numbers(value: str) -> list[int]:
        return [int(item or 0) for item in value.split(';')]

    @classmethod
    def parse_data(cls, raw: str) -> dict:
        """Decodes the public repository format used by Rozkładzik.pl."""
        sections = raw.split('#SEP#')
        if len(sections) < 12:
            raise ValueError('Źródło Grudziądza zwróciło niepełne dane.')
        names = sections[0].split(';')
        table_names = sections[2].split(';')
        latitudes = [float(value or 0) for value in sections[3].split(';')]
        longitudes = [float(value or 0) for value in sections[4].split(';')]
        table_to_stop = cls._numbers(sections[7])
        variant_to_table = cls._numbers(sections[8])
        lines = []
        for encoded in sections[11].split('#!#'):
            values = encoded.split(';')
            if len(values) < 7:
                continue
            directions = []
            for index in range(2, len(values) - 4, 5):
                directions.append({
                    'name_id': int(values[index] or 0),
                    'variant_ids': [int(value) for value in values[index + 1].split('|') if value],
                    'on_request': [bool(value) for value in values[index + 2].split('|')],
                    'variant_stops': [bool(value) for value in values[index + 3].split('|')],
                    'patterns': values[index + 4]
                })
            lines.append({
                'name': values[0],
                'vehicle_type': int(values[1] or 0),
                'directions': directions
            })
        path_parts = sections[12].split('#!ax', 1) if len(sections) > 12 else []
        paths = {}
        if len(path_parts) == 2:
            keys = path_parts[0].split(';')
            for index, encoded in enumerate(path_parts[1].split('#!wy')):
                offset = index * 3
                if offset + 2 < len(keys):
                    paths[(int(keys[offset]), int(keys[offset + 1]), int(keys[offset + 2]))] = encoded
        return {
            'names': names,
            'table_names': table_names,
            'latitudes': latitudes,
            'longitudes': longitudes,
            'table_to_stop': table_to_stop,
            'variant_to_table': variant_to_table,
            'schedule_id': int(sections[10]),
            'lines': lines,
            'paths': paths
        }

    @staticmethod
    def _decode_path(encoded: str) -> list[PublicTransportCoordinate]:
        """Decodes the Google encoded polyline used by the source."""
        coordinates = []
        latitude = longitude = index = 0
        while index < len(encoded):
            deltas = []
            for _ in range(2):
                result = shift = 0
                while index < len(encoded):
                    value = ord(encoded[index]) - 63
                    index += 1
                    result |= (value & 31) << shift
                    shift += 5
                    if value < 32:
                        break
                deltas.append(~(result >> 1) if result & 1 else result >> 1)
            latitude += deltas[0]
            longitude += deltas[1]
            coordinates.append(PublicTransportCoordinate(latitude / 1e5, longitude / 1e5))
        return coordinates

    @classmethod
    def _city(cls) -> PublicTransportCity:
        return PublicTransportCity(cls.CITY_NAME, cls.CITY_COLOR)

    @staticmethod
    def _type(line: dict) -> PublicTransportType:
        return PublicTransportType.TRAM if line['vehicle_type'] == 2 else PublicTransportType.BUS

    @classmethod
    def _line(cls, data: dict, name: str) -> dict:
        line = next((item for item in data['lines'] if item['name'] == name), None)
        if not line:
            raise ValueError(f'Nie znaleziono linii {name}.')
        return line

    @staticmethod
    def _query(url: str) -> dict[str, str]:
        return {key: values[0] for key, values in parse_qs(urlparse(url).query).items() if values}

    @classmethod
    def _url(cls, screen: str, **values) -> str:
        return f'{cls.BASE_URL}{screen}?{urlencode(values)}'

    @classmethod
    def _base_line(cls, line: dict) -> PublicTransportBaseLine:
        return PublicTransportBaseLine(
            line=line['name'], type=cls._type(line),
            url=cls._url('line', line=line['name']),
            free_of_charge=False, updated=False
        )

    @classmethod
    def _table(cls, data: dict, variant_id: int) -> int:
        return data['variant_to_table'][variant_id]

    @classmethod
    def _stop_name(cls, data: dict, table_id: int) -> str:
        stop_id = data['table_to_stop'][table_id]
        name = data['names'][stop_id]
        platform = data['table_names'][table_id] if table_id < len(data['table_names']) else ''
        return f'{name} ({platform})' if platform else name

    @classmethod
    def _coordinates(cls, data: dict, table_id: int) -> tuple[float | None, float | None]:
        latitude = data['latitudes'][table_id] if table_id < len(data['latitudes']) else 0
        longitude = data['longitudes'][table_id] if table_id < len(data['longitudes']) else 0
        return (latitude or None, longitude or None)

    @staticmethod
    def _primary_pattern(direction: dict) -> list[int]:
        """Returns the main stop-index sequence, excluding variant branches."""
        encoded = str(direction.get('patterns') or '').split('|', 1)[0]
        return [int(value) for value in encoded.split(',') if value != '']

    @classmethod
    def _route_for_pattern(
        cls,
        data: dict,
        line: dict,
        direction: dict,
        stop_indexes: list[int]
    ) -> list[PublicTransportCoordinate]:
        """Builds one continuous path without joining separate variants."""
        route = []
        previous_table = 0
        for stop_index in stop_indexes:
            if stop_index >= len(direction['variant_ids']):
                continue
            table_id = cls._table(
                data,
                direction['variant_ids'][stop_index]
            )
            encoded_path = data['paths'].get(
                (line['vehicle_type'], previous_table, table_id),
                ''
            )
            if encoded_path:
                fragment = cls._decode_path(encoded_path)
                if route and fragment and route[-1] == fragment[0]:
                    fragment = fragment[1:]
                route.extend(fragment)
            else:
                latitude, longitude = cls._coordinates(data, table_id)
                if latitude is not None and longitude is not None:
                    route.append(PublicTransportCoordinate(
                        latitude,
                        longitude
                    ))
            previous_table = table_id
        return route

    @classmethod
    def download_lines(cls, url: str | None = None, refresh: bool = False):
        del url
        return [cls._base_line(line) for line in cls._data(refresh)['lines']]

    @classmethod
    def download_line(cls, url: str, include_announcement_content: bool = False):
        del include_announcement_content
        data = cls._data()
        query = cls._query(url)
        line = cls._line(data, query.get('line', ''))
        transport_type = cls._type(line)
        directions = []
        for direction_index, direction in enumerate(line['directions']):
            stops = []
            for stop_index, variant_id in enumerate(direction['variant_ids']):
                table_id = cls._table(data, variant_id)
                name = cls._stop_name(data, table_id)
                stops.append(PublicTransportDirectionStop(
                    line=line['name'], type=transport_type, city=cls._city(),
                    is_variant=direction['variant_stops'][stop_index] if stop_index < len(direction['variant_stops']) else False,
                    name=name, platform='',
                    url=cls._url('line-stop', line=line['name'], direction=direction_index, stop=stop_index, day=date.today().weekday())
                ))
            directions.append(PublicTransportDirection(
                name=data['names'][direction['name_id']], cities=[cls._city()],
                stops=stops,
                route=cls._route_for_pattern(
                    data,
                    line,
                    direction,
                    cls._primary_pattern(direction)
                )
            ))
        return PublicTransportLine(
            line=line['name'], type=transport_type, announcements=[],
            directions=directions, route_variants={}, dates={}
        )

    @classmethod
    def _day_dates(cls, url: str) -> tuple[date, dict[date, str]]:
        query = cls._query(url)
        selected_day = int(query.get('day', date.today().weekday()))
        today = date.today()
        dates = {}
        for offset in range(7):
            item = today + timedelta(days=offset)
            values = dict(query, day=item.weekday())
            dates[item] = f'{urlparse(url).scheme}://{urlparse(url).netloc}{urlparse(url).path}?{urlencode(values)}'
        selected = next((item for item in dates if item.weekday() == selected_day), today)
        return selected, dates

    @classmethod
    def download_line_stop_timetable(cls, url: str, include_announcement_content: bool = False):
        del include_announcement_content
        data = cls._data()
        query = cls._query(url)
        line = cls._line(data, query['line'])
        direction_index = int(query['direction'])
        stop_index = int(query['stop'])
        day = int(query.get('day', date.today().weekday()))
        direction = line['directions'][direction_index]
        endpoint = f'{cls.TIMETABLE_URL}?{urlencode({"c": "bs", "l": line["name"], "d": direction_index, "b": stop_index, "sid": data["schedule_id"], "day": day})}'
        raw = cls._download(endpoint, f'Odjazdy linii {line["name"]}')
        parts = raw.split('#$#')
        if len(parts) < 3:
            raise ValueError('Nie udało się odczytać rozkładu przystanku.')
        table_id = int(parts[0])
        values = parts[2].split(';')
        departures = []
        for index in range(0, len(values) - 2, 3):
            minutes = int(values[index] or -1)
            if minutes < 0:
                continue
            ride_index = values[index + 2]
            departures.append(PublicTransportDepartureTime(
                departure_time=time((minutes // 60) % 24, minutes % 60),
                is_high_floor=False,
                url=cls._url('ride', line=line['name'], direction=direction_index, day=day, ride=ride_index, stop=stop_index),
                variant=values[index + 1].replace('_', '')
            ))
        selected_date, dates = cls._day_dates(url)
        direction_name = data['names'][direction['name_id']]
        latitude, longitude = cls._coordinates(data, table_id)
        timetable = PublicTransportDateTimetable(
            date=selected_date, direction_name=direction_name,
            effective_date_from=None, effective_date_to=None,
            departures=departures,
            variants=list(dict.fromkeys(item.variant for item in departures if item.variant))
        )
        return PublicTransportLineStopTimetable(
            line=line['name'], type=cls._type(line), announcements=[],
            stop_name=cls._stop_name(data, table_id), direction_name=direction_name,
            platform='', timetable={selected_date: timetable}, dates=dates,
            latitude=latitude, longitude=longitude
        )

    @classmethod
    def download_ride(cls, url: str, from_first_stop: bool = True):
        del from_first_stop
        data = cls._data()
        query = cls._query(url)
        line = cls._line(data, query['line'])
        direction_index = int(query['direction'])
        direction = line['directions'][direction_index]
        endpoint = f'{cls.TIMETABLE_URL}?{urlencode({"c": "bs", "l": line["name"], "d": direction_index, "sid": data["schedule_id"], "day": query["day"], "i": query["ride"]})}'
        values = [int(value or -1) for value in cls._download(endpoint, 'Szczegóły przejazdu').split(';')]
        rows = []
        previous_minutes = None
        for index, minutes in enumerate(values):
            if minutes < 0 or index >= len(direction['variant_ids']):
                continue
            table_id = cls._table(data, direction['variant_ids'][index])
            latitude, longitude = cls._coordinates(data, table_id)
            travel = max(0, minutes - previous_minutes) if previous_minutes is not None else 0
            rows.append(PublicTransportRideStop(
                stop=cls._stop_name(data, table_id),
                departure_time=time((minutes // 60) % 24, minutes % 60),
                travel_time=travel, travel_time_sum=minutes - values[0] if values and values[0] >= 0 else 0,
                distance=0.0, distance_sum=0.0, city=cls._city(),
                latitude=latitude, longitude=longitude
            ))
            previous_minutes = minutes
        first = rows[0] if rows else None
        return PublicTransportRide(
            line=line['name'], type=cls._type(line),
            stop_name=first.stop if first else '', platform='',
            departure_time=first.departure_time if first else None,
            cities=[cls._city()], next_stops=rows[1:], carrier=cls.CARRIER,
            vehicle_type='', latitude=first.latitude if first else None,
            longitude=first.longitude if first else None
        )

    @classmethod
    def download_stops(cls, url: str | None = None, progress_callback=None, refresh: bool = False):
        del url
        if progress_callback:
            progress_callback(1, 1, cls.CITY_NAME)
        data = cls._data(refresh)
        serving: dict[int, dict[str, PublicTransportBaseLine]] = {}
        tables: dict[int, list[int]] = {}
        for line in data['lines']:
            base = cls._base_line(line)
            for direction in line['directions']:
                for variant_id in direction['variant_ids']:
                    table_id = cls._table(data, variant_id)
                    stop_id = data['table_to_stop'][table_id]
                    serving.setdefault(stop_id, {})[line['name']] = base
                    tables.setdefault(stop_id, []).append(table_id)
        result = []
        for stop_id, lines in serving.items():
            table_id = next((item for item in tables[stop_id] if cls._coordinates(data, item)[0] is not None), tables[stop_id][0])
            latitude, longitude = cls._coordinates(data, table_id)
            result.append(PublicTransportStop(
                name=data['names'][stop_id], city=cls._city(),
                platforms=[PublicTransportStopPlatform(
                    name='Wszystkie', lines=list(lines.values()),
                    url_all=cls._url('stop', stop=stop_id), url_chrono='',
                    latitude=latitude, longitude=longitude
                )]
            ))
        return sorted(result, key=lambda item: item.name.casefold())

    @classmethod
    def download_stop_all(cls, url: str):
        data = cls._data()
        stop_id = int(cls._query(url)['stop'])
        entries = {}
        coordinates = (None, None)
        for line in data['lines']:
            matched_direction = ''
            for direction in line['directions']:
                for variant_id in direction['variant_ids']:
                    table_id = cls._table(data, variant_id)
                    if data['table_to_stop'][table_id] == stop_id:
                        matched_direction = data['names'][direction['name_id']]
                        coordinates = cls._coordinates(data, table_id)
                        break
                if matched_direction:
                    break
            if matched_direction:
                entries[cls._base_line(line)] = PublicTransportDateTimetable(
                    date=None, direction_name=matched_direction,
                    effective_date_from=None, effective_date_to=None,
                    departures=[], variants=[]
                )
        return PublicTransportStopAll(
            stop_name=data['names'][stop_id], platform='', dates={}, lines=entries,
            latitude=coordinates[0], longitude=coordinates[1]
        )

    @classmethod
    def download_announcements(cls, line: str = '', include_content: bool = False):
        del line, include_content
        return []

    @classmethod
    def enrich_stop_locations(cls, stops):
        return stops

from __future__ import annotations
from typing import Any, ClassVar
import json
import math
import ssl
from urllib.parse import urlencode
from urllib.error import URLError
from urllib.request import Request, urlopen

from flask import jsonify, request

from core.api.base_controller import BaseController
from models.map.map_element_data_model import MapElementDataModel
from models.map.map_place_data_model import MapPlaceDataModel
from models.map_data_model import MapDataModel
from resources.map_legend import MapLegend


class MapController(BaseController):
    CONTROLLER_NAME: ClassVar[str] = 'MapController'
    _NOMINATIM_URL: ClassVar[str] = 'https://nominatim.openstreetmap.org'
    _OVERPASS_URL: ClassVar[str] = 'https://overpass-api.de/api/interpreter'
    _OVERPASS_FALLBACK_URLS: ClassVar[tuple[str, ...]] = (
        'https://overpass.kumi.systems/api/interpreter',
        'https://overpass.osm.ch/api/interpreter'
    )
    _OSRM_URL: ClassVar[str] = 'https://router.project-osrm.org'
    _OSM_ROUTING_URL: ClassVar[str] = 'https://routing.openstreetmap.de'
    _VALHALLA_URL: ClassVar[str] = 'https://valhalla1.openstreetmap.de'
    _ROUTE_PROFILES: ClassVar[dict[str, tuple[str, str]]] = {
        'car': (_OSRM_URL, 'driving'),
        'bicycle': (f'{_OSM_ROUTING_URL}/routed-bike', 'bike'),
        'foot': (f'{_OSM_ROUTING_URL}/routed-foot', 'foot')
    }
    _USER_AGENT: ClassVar[str] = 'TravelManager/1.0'
    _ADVANCED_SEARCH_GROUPS: ClassVar[dict[str, tuple[str, ...]]] = {
        'food': ('bar', 'cafe', 'takeaway', 'restaurant', 'delivery', 'fast_food', 'pub', 'food_court'),
        'attractions': (
            'attraction',
            'library',
            'cinema',
            'museum',
            'live_music',
            'park',
            'gym',
            'art',
            'nightlife',
            'theatre',
            'zoo'
        ),
        'shopping': (
            'mall',
            'garden',
            'chemist',
            'electronics',
            'local',
            'sports',
            'grocery',
            'car_sales',
            'clothes',
            'books'
        ),
        'services': (
            'pharmacy',
            'car_wash',
            'atm',
            'hotel',
            'parking',
            'laundry',
            'beauty',
            'charging',
            'fuel',
            'healthcare',
            'courier',
            'car_rental',
            'post_office'
        )
    }
    _ADVANCED_SEARCH_FILTERS: ClassVar[dict[str, list[dict[str, str | tuple[str, ...] | None]]]] = {
        'bar': [{'amenity': ('bar', 'pub', 'biergarten')}],
        'cafe': [{'amenity': 'cafe'}, {'shop': 'coffee'}],
        'takeaway': [
            {'amenity': ('restaurant', 'fast_food', 'cafe', 'bar', 'pub'), 'takeaway': ('yes', 'only')},
            {'shop': ('food', 'deli', 'bakery', 'confectionery'), 'takeaway': ('yes', 'only')},
            {'amenity': ('fast_food', 'food_court')},
            {'shop': ('bakery', 'confectionery', 'deli')}
        ],
        'restaurant': [{'amenity': 'restaurant'}],
        'delivery': [
            {'amenity': ('restaurant', 'fast_food', 'cafe'), 'delivery': 'yes'},
            {'shop': ('food', 'deli', 'bakery', 'confectionery'), 'delivery': 'yes'},
            {'amenity': ('restaurant', 'fast_food')}
        ],
        'fast_food': [{'amenity': 'fast_food'}],
        'pub': [{'amenity': ('pub', 'bar', 'biergarten')}],
        'food_court': [{'amenity': 'food_court'}],
        'attraction': [{'tourism': 'attraction'}, {'tourism': 'theme_park'}],
        'library': [{'amenity': 'library'}],
        'cinema': [{'amenity': 'cinema'}],
        'museum': [{'tourism': 'museum'}],
        'live_music': [{'amenity': 'music_venue'}, {'live_music': 'yes'}],
        'park': [{'leisure': ('park', 'garden')}, {'boundary': 'national_park'}],
        'gym': [{'leisure': 'fitness_centre'}, {'amenity': 'gym'}, {'sport': 'fitness'}],
        'art': [{'tourism': 'gallery'}, {'amenity': 'arts_centre'}, {'shop': 'art'}],
        'nightlife': [{'amenity': ('nightclub', 'bar', 'pub', 'biergarten')}],
        'theatre': [{'amenity': 'theatre'}],
        'zoo': [{'tourism': 'zoo'}],
        'mall': [{'shop': ('mall', 'department_store')}, {'landuse': 'retail'}],
        'garden': [{'shop': ('garden_centre', 'doityourself', 'hardware', 'houseware', 'furniture', 'interior_decoration')}],
        'chemist': [{'shop': ('chemist', 'cosmetics', 'perfumery', 'beauty')}],
        'electronics': [{'shop': ('electronics', 'computer', 'mobile_phone', 'hifi', 'appliance')}],
        'local': [{'shop': ('convenience', 'kiosk', 'general', 'variety_store')}],
        'sports': [{'shop': ('sports', 'outdoor', 'bicycle', 'fishing', 'hunting')}],
        'grocery': [{'shop': ('supermarket', 'convenience', 'grocery', 'greengrocer', 'bakery', 'butcher', 'deli')}],
        'car_sales': [{'shop': ('car', 'car_repair', 'car_parts', 'tyres')}],
        'clothes': [{'shop': ('clothes', 'shoes', 'fashion', 'boutique', 'jewelry', 'bag')}],
        'books': [{'shop': ('books', 'stationery', 'newsagent')}],
        'pharmacy': [{'amenity': 'pharmacy'}, {'healthcare': 'pharmacy'}],
        'car_wash': [{'amenity': 'car_wash'}],
        'atm': [{'amenity': 'atm'}, {'amenity': 'bank', 'atm': 'yes'}],
        'hotel': [{'tourism': ('hotel', 'motel', 'guest_house', 'hostel', 'apartment')}],
        'parking': [{'amenity': ('parking', 'parking_entrance')}],
        'laundry': [{'shop': ('laundry', 'dry_cleaning')}],
        'beauty': [{'shop': ('beauty', 'hairdresser', 'massage', 'tattoo')}],
        'charging': [{'amenity': 'charging_station'}],
        'fuel': [{'amenity': 'fuel'}],
        'healthcare': [
            {'amenity': ('hospital', 'clinic', 'doctors', 'dentist')},
            {'healthcare': ('hospital', 'clinic', 'doctor', 'dentist', 'centre')}
        ],
        'courier': [
            {'amenity': ('parcel_locker', 'post_office', 'post_depot')},
            {'parcel_pickup': 'yes'},
            {'parcel_dropoff': 'yes'},
            {'office': ('courier', 'logistics')}
        ],
        'car_rental': [{'amenity': ('car_rental', 'car_sharing')}],
        'post_office': [{'amenity': ('post_office', 'post_box', 'post_depot')}]
    }
    _ADVANCED_SEARCH_FALLBACK_QUERIES: ClassVar[dict[str, tuple[str, ...]]] = {
        'food': ('restaurant', 'cafe', 'fast food', 'bar', 'pub'),
        'bar': ('bar', 'pub'),
        'cafe': ('cafe', 'kawiarnia'),
        'takeaway': ('fast food', 'takeaway', 'restaurant'),
        'restaurant': ('restaurant', 'restauracja'),
        'delivery': ('pizza', 'restaurant', 'food delivery'),
        'fast_food': ('fast food', 'kebab', 'burger'),
        'pub': ('pub', 'bar'),
        'food_court': ('food court', 'restaurant'),
        'attractions': ('attraction', 'museum', 'park', 'cinema', 'theatre'),
        'attraction': ('attraction',),
        'library': ('library', 'biblioteka'),
        'cinema': ('cinema', 'kino'),
        'museum': ('museum', 'muzeum'),
        'live_music': ('music venue', 'live music', 'club'),
        'park': ('park',),
        'gym': ('gym', 'fitness'),
        'art': ('gallery', 'art'),
        'nightlife': ('nightclub', 'club', 'bar'),
        'theatre': ('theatre', 'teatr'),
        'zoo': ('zoo',),
        'shopping': ('shop', 'mall', 'supermarket'),
        'mall': ('mall', 'shopping centre', 'centrum handlowe'),
        'garden': ('garden centre', 'doityourself', 'hardware'),
        'chemist': ('chemist', 'drogeria', 'cosmetics'),
        'electronics': ('electronics', 'computer', 'mobile phone'),
        'local': ('convenience', 'kiosk'),
        'sports': ('sports shop', 'bicycle shop'),
        'grocery': ('supermarket', 'grocery', 'bakery'),
        'car_sales': ('car dealer', 'car sales', 'samochody'),
        'clothes': ('clothes', 'shoes'),
        'books': ('books', 'bookshop', 'newsagent', 'księgarnia'),
        'services': ('pharmacy', 'atm', 'parking', 'hotel', 'fuel'),
        'pharmacy': ('pharmacy', 'apteka'),
        'car_wash': ('car wash', 'automyjnia'),
        'atm': ('atm', 'bankomat'),
        'hotel': ('hotel',),
        'parking': ('parking',),
        'laundry': ('laundry', 'dry cleaning'),
        'beauty': ('beauty salon', 'hairdresser'),
        'charging': ('charging station',),
        'fuel': ('fuel station', 'petrol station', 'stacja paliw'),
        'healthcare': ('hospital', 'clinic', 'doctors'),
        'courier': ('parcel locker', 'post office', 'courier'),
        'car_rental': ('car rental',),
        'post_office': ('post office', 'poczta')
    }
    _ADVANCED_SEARCH_KEYWORD_ALIASES: ClassVar[dict[str, str]] = {
        'cafe': 'cafe',
        'café': 'cafe',
        'kawiarnia': 'cafe',
        'kawiarnie': 'cafe',
        'restauracja': 'restaurant',
        'restauracje': 'restaurant',
        'restaurant': 'restaurant',
        'fast food': 'fast_food',
        'fastfood': 'fast_food',
        'pub': 'pub',
        'bar': 'bar',
        'apteka': 'pharmacy',
        'apteki': 'pharmacy',
        'pharmacy': 'pharmacy',
        'bankomat': 'atm',
        'bankomaty': 'atm',
        'atm': 'atm'
    }

    def register_routes(self):
        self.add_url_rule('/api/map/legend', view_func=self.legend, methods=['GET'])
        self.add_url_rule('/api/map/reverse', view_func=self.reverse, methods=['GET'])
        self.add_url_rule('/api/map/route', view_func=self.route, methods=['POST'])
        self.add_url_rule('/api/map/search', view_func=self.search, methods=['GET'])
        self.add_url_rule('/api/map/advanced-search', view_func=self.advanced_search, methods=['GET'])

    #region HTTP

    @classmethod
    def _get_json(cls, path: str, params: dict[str, Any]) -> Any:
        """Loads JSON from Nominatim using a desktop-app friendly user agent."""
        url = f'{cls._NOMINATIM_URL}{path}?{urlencode(params)}'
        return cls._get_json_url(url)

    @classmethod
    def _get_json_url(cls, url: str) -> Any:
        """Loads JSON from an external map service."""
        req = Request(url, headers={
            'Accept': 'application/json',
            'User-Agent': cls._USER_AGENT
        })

        try:
            return cls._load_json(req)
        except URLError as error:
            if not isinstance(error.reason, ssl.SSLCertVerificationError):
                raise

            context = ssl._create_unverified_context()
            return cls._load_json(req, context)

    @staticmethod
    def _load_json(req: Request, context: ssl.SSLContext | None = None, timeout: int = 25) -> Any:
        """Executes a request and decodes its JSON body."""
        with urlopen(req, timeout=timeout, context=context) as response:
            return json.loads(response.read().decode('utf-8'))

    @classmethod
    def _post_form_json(cls, url: str, data: dict[str, str]) -> Any:
        """Posts form data to an external JSON endpoint."""
        req = Request(
            url,
            data=urlencode(data).encode('utf-8'),
            headers={
                'Accept': 'application/json',
                'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
                'User-Agent': cls._USER_AGENT
            },
            method='POST'
        )

        try:
            return cls._load_json(req, timeout=14)
        except URLError as error:
            if not isinstance(error.reason, ssl.SSLCertVerificationError):
                raise

            context = ssl._create_unverified_context()
            return cls._load_json(req, context, timeout=14)

    @classmethod
    def _post_json_url(cls, url: str, data: dict[str, Any]) -> Any:
        """Posts a JSON payload to an external JSON endpoint."""
        req = Request(
            url,
            data=json.dumps(data).encode('utf-8'),
            headers={
                'Accept': 'application/json',
                'Content-Type': 'application/json; charset=utf-8',
                'User-Agent': cls._USER_AGENT
            },
            method='POST'
        )

        try:
            return cls._load_json(req, timeout=20)
        except URLError as error:
            if not isinstance(error.reason, ssl.SSLCertVerificationError):
                raise

            context = ssl._create_unverified_context()
            return cls._load_json(req, context, timeout=20)

    #endregion HTTP

    #region Routing

    @classmethod
    def _decode_valhalla_shape(cls, shape: str) -> list[list[float]]:
        """Decodes a Valhalla polyline shape to GeoJSON coordinates."""
        coordinates: list[list[float]] = []
        index = 0
        latitude = 0
        longitude = 0
        factor = 1e6

        while index < len(shape):
            result = 1
            shift = 0

            while True:
                byte = ord(shape[index]) - 63 - 1
                index += 1
                result += byte << shift
                shift += 5

                if byte < 0x1f:
                    break

            latitude += ~(result >> 1) if result & 1 else result >> 1
            result = 1
            shift = 0

            while True:
                byte = ord(shape[index]) - 63 - 1
                index += 1
                result += byte << shift
                shift += 5

                if byte < 0x1f:
                    break

            longitude += ~(result >> 1) if result & 1 else result >> 1
            coordinates.append([longitude / factor, latitude / factor])

        return coordinates

    @staticmethod
    def _valhalla_maneuver_type(maneuver_type: int | None) -> str:
        """Maps Valhalla maneuver types to the simpler frontend maneuver names."""
        if maneuver_type in (1, 2, 3):
            return 'depart'

        if maneuver_type in (4, 5, 6):
            return 'arrive'

        if maneuver_type in (26, 27):
            return 'roundabout'

        if maneuver_type in (18, 19):
            return 'merge'

        return 'continue'

    @staticmethod
    def _valhalla_maneuver_modifier(maneuver: dict[str, Any]) -> str:
        """Maps Valhalla maneuver bearing changes to frontend modifiers."""
        instruction = str(maneuver.get('instruction') or '').lower()

        if 'left' in instruction:
            return 'left'

        if 'right' in instruction:
            return 'right'

        return 'straight'

    @classmethod
    def _valhalla_step(cls, maneuver: dict[str, Any]) -> dict[str, Any]:
        """Converts one Valhalla maneuver to the route step shape used by the frontend."""
        maneuver_type = maneuver.get('type')

        try:
            maneuver_type = int(maneuver_type)
        except (TypeError, ValueError):
            maneuver_type = None

        street_names = maneuver.get('street_names') if isinstance(maneuver.get('street_names'), list) else []

        return {
            'distance': max(0.0, float(maneuver.get('length') or 0) * 1000),
            'duration': max(0.0, float(maneuver.get('time') or 0)),
            'name': street_names[0] if street_names else '',
            'instruction': str(maneuver.get('instruction') or ''),
            'maneuver': {
                'type': cls._valhalla_maneuver_type(maneuver_type),
                'modifier': cls._valhalla_maneuver_modifier(maneuver),
                'exit': maneuver.get('roundabout_exit_count')
            }
        }

    @classmethod
    def _valhalla_route(cls, points: list[dict[str, float]]) -> dict[str, Any]:
        """Calculates a car route with Valhalla configured to avoid toll roads."""
        payload = {
            'locations': [
                {
                    'lat': point['latitude'],
                    'lon': point['longitude']
                }
                for point in points
            ],
            'costing': 'auto',
            'costing_options': {
                'auto': {
                    'use_tolls': 0
                }
            },
            'directions_options': {
                'units': 'kilometers'
            }
        }
        data = cls._post_json_url(f'{cls._VALHALLA_URL}/route', payload)
        trip = data.get('trip') if isinstance(data, dict) else None

        if not isinstance(trip, dict):
            raise RuntimeError(data.get('error') if isinstance(data, dict) else 'Invalid Valhalla response.')

        summary = trip.get('summary') if isinstance(trip.get('summary'), dict) else {}
        legs_data = trip.get('legs') if isinstance(trip.get('legs'), list) else []
        coordinates: list[list[float]] = []
        legs: list[dict[str, Any]] = []

        for leg in legs_data:
            if not isinstance(leg, dict):
                continue

            leg_summary = leg.get('summary') if isinstance(leg.get('summary'), dict) else {}
            shape = str(leg.get('shape') or '')
            leg_coordinates = cls._decode_valhalla_shape(shape) if shape else []

            if coordinates and leg_coordinates:
                coordinates.extend(leg_coordinates[1:])
            else:
                coordinates.extend(leg_coordinates)

            maneuvers = leg.get('maneuvers') if isinstance(leg.get('maneuvers'), list) else []
            legs.append({
                'distance': max(0.0, float(leg_summary.get('length') or 0) * 1000),
                'duration': max(0.0, float(leg_summary.get('time') or 0)),
                'steps': [
                    cls._valhalla_step(maneuver)
                    for maneuver in maneuvers
                    if isinstance(maneuver, dict)
                ]
            })

        return {
            'distance': max(0.0, float(summary.get('length') or 0) * 1000),
            'duration': max(0.0, float(summary.get('time') or 0)),
            'geometry': {
                'type': 'LineString',
                'coordinates': coordinates
            },
            'legs': legs,
            'waypoints': [],
            'toll_exclusion_requested': True,
            'toll_exclusion_applied': True,
            'toll_exclusion_warning': None if not summary.get('has_toll') else (
                'Router znalazł trasę z możliwym płatnym odcinkiem mimo ustawienia omijania opłat.'
            )
        }

    #endregion Routing

    #region Serialization

    @staticmethod
    def _response(model: MapDataModel, status: int = 200):
        """Returns a Flask JSON response from the map data model."""
        return jsonify(model.to_dict()), status

    @classmethod
    def _ok(cls, place: MapPlaceDataModel) -> MapDataModel:
        """Builds a successful map API response."""
        return MapDataModel(
            status='ok',
            message=None,
            place=place
        )

    @classmethod
    def _error(cls, message: str) -> MapDataModel:
        """Builds a failed map API response."""
        return MapDataModel(
            status='error',
            message=message,
            place=None
        )

    #endregion Serialization

    #region Legend

    @classmethod
    def _legend_item(cls, key: str, data: dict[str, Any]) -> dict[str, Any]:
        """Serializes a single map legend item to a frontend-friendly shape."""
        icon_type = data.get(MapLegend.FIELD_ICON)

        return {
            'id': key,
            'title': data.get(MapLegend.FIELD_TITLE, key),
            'icon_type': icon_type,
            'image': f'/assets/images/legend/{key}.{icon_type}' if icon_type else None,
            'requirements': data.get(MapLegend.FIELD_REQUIREMENTS, [])
        }

    @classmethod
    def _legend_group(cls, group_key: str, items: dict[str, Any]) -> dict[str, Any]:
        """Serializes one legend group with its child items."""
        return {
            'id': group_key,
            'title': group_key.replace('_', ' ').title(),
            'items': [
                cls._legend_item(item_key, item_data)
                for item_key, item_data in items.items()
            ]
        }

    @classmethod
    def _legend_tab(cls, tab_id: str, label: str, groups: dict[str, Any]) -> dict[str, Any]:
        """Serializes one legend tab."""
        return {
            'id': tab_id,
            'label': label,
            'groups': [
                cls._legend_group(group_key, group_items)
                for group_key, group_items in groups.items()
            ]
        }

    #endregion Legend

    #region Endpoints

    def legend(self):
        """Returns the OpenStreetMap map legend used by the legend details panel."""
        return jsonify({
            'status': 'ok',
            'legend': {
                'tabs': [
                    self._legend_tab('symbols', 'Symbole', MapLegend.SYMBOLS),
                    self._legend_tab('lines', 'Linie', MapLegend.LINES),
                    self._legend_tab('areas', 'Obszary', MapLegend.AREAS)
                ]
            }
        })

    def route(self):
        """Returns an OSRM route through supplied points in their current order."""
        data = request.get_json(silent=True) or {}
        points = data.get('points') if isinstance(data, dict) else None
        transport = str(data.get('transport', 'car') if isinstance(data, dict) else 'car')
        include_toll_roads = bool(data.get('include_toll_roads', True)) if isinstance(data, dict) else True
        routing_base_url, routing_profile = self._ROUTE_PROFILES.get(transport, self._ROUTE_PROFILES['car'])

        if not isinstance(points, list) or not 2 <= len(points) <= 25:
            return jsonify({
                'status': 'error',
                'message': 'Route requires between 2 and 25 points.'
            }), 400

        coordinates = []
        route_points: list[dict[str, float]] = []
        for point in points:
            if not isinstance(point, dict):
                return jsonify({'status': 'error', 'message': 'Invalid route point.'}), 400

            try:
                latitude = float(point.get('latitude'))
                longitude = float(point.get('longitude'))
            except (TypeError, ValueError):
                return jsonify({'status': 'error', 'message': 'Invalid route coordinates.'}), 400

            if not -90 <= latitude <= 90 or not -180 <= longitude <= 180:
                return jsonify({'status': 'error', 'message': 'Route coordinates are out of range.'}), 400

            coordinates.append(f'{longitude},{latitude}')
            route_points.append({
                'latitude': latitude,
                'longitude': longitude
            })

        if transport == 'car' and not include_toll_roads:
            try:
                return jsonify({
                    'status': 'ok',
                    'route': self._valhalla_route(route_points)
                })
            except Exception as error:
                return jsonify({
                    'status': 'error',
                    'message': f'Nie udało się obliczyć trasy bez płatnych dróg: {error}'
                }), 502

        params = {
            'overview': 'full',
            'geometries': 'geojson',
            'steps': 'true'
        }

        url = f'{routing_base_url}/route/v1/{routing_profile}/{";".join(coordinates)}?{urlencode(params)}'

        try:
            route_data = self._get_json_url(url)
        except Exception as error:
            return jsonify({
                'status': 'error',
                'message': f'Could not calculate route: {error}'
            }), 502

        if route_data.get('code') != 'Ok' or not route_data.get('routes'):
            return jsonify({
                'status': 'error',
                'message': route_data.get('message') or 'No route found.'
            }), 422

        selected_route = route_data['routes'][0]

        return jsonify({
            'status': 'ok',
            'route': {
                'distance': selected_route.get('distance'),
                'duration': selected_route.get('duration'),
                'geometry': selected_route.get('geometry'),
                'legs': selected_route.get('legs', []),
                'waypoints': route_data.get('waypoints', []),
                'toll_exclusion_requested': False,
                'toll_exclusion_applied': False,
                'toll_exclusion_warning': None
            }
        })

    def reverse(self):
        """Returns structured OpenStreetMap data for clicked map coordinates."""
        lat = request.args.get('lat')
        lon = request.args.get('lon')

        if not lat or not lon:
            return self._response(self._error('Missing lat or lon.'), 400)

        try:
            data = self._get_json('/reverse', {
                'format': 'jsonv2',
                'lat': lat,
                'lon': lon,
                'addressdetails': 1,
                'extratags': 1,
                'namedetails': 1
            })
        except Exception as error:
            return self._response(self._error(f'Could not load map data: {error}'), 502)

        selected = MapElementDataModel.from_dict(data)
        place = MapPlaceDataModel(
            query=f'{lat},{lon}',
            source='nominatim_reverse',
            selected=selected,
            elements=[selected]
        )

        return self._response(self._ok(place))

    def search(self):
        """Returns structured OpenStreetMap data for a place search query."""
        query = request.args.get('q', '').strip()

        if not query and not category_id and not subcategory_id:
            return self._response(self._error('Missing search query.'), 400)

        try:
            data = self._get_json('/search', {
                'format': 'jsonv2',
                'q': query,
                'limit': 5,
                'addressdetails': 1,
                'extratags': 1,
                'namedetails': 1
            })
        except Exception as error:
            return self._response(self._error(f'Could not search map data: {error}'), 502)

        elements = [MapElementDataModel.from_dict(item) for item in data]
        place = MapPlaceDataModel(
            query=query,
            source='nominatim_search',
            selected=elements[0] if elements else None,
            elements=elements
        )

        return self._response(self._ok(place))

    def advanced_search(self):
        """Returns map search results constrained to the current map area."""
        query = request.args.get('q', '').strip()
        keyword = request.args.get('keyword', '').strip()
        category_id = request.args.get('category_id', '').strip()
        subcategory_id = request.args.get('subcategory_id', '').strip()

        if not query and not category_id and not subcategory_id:
            return self._response(self._error('Missing search query.'), 400)

        try:
            limit = max(1, min(50, int(request.args.get('limit', 20))))
        except (TypeError, ValueError):
            limit = 20

        if category_id or subcategory_id:
            inferred_subcategory_id = subcategory_id or self._subcategory_from_keyword(keyword, category_id)

            try:
                elements = self._overpass_results(
                    category_id,
                    inferred_subcategory_id,
                    self._effective_keyword(keyword, inferred_subcategory_id),
                    limit
                )
            except Exception as error:
                try:
                    elements = self._nominatim_category_fallback(
                        query,
                        keyword,
                        category_id,
                        inferred_subcategory_id,
                        limit
                    )
                except Exception:
                    return self._response(self._error(f'Could not search OpenStreetMap tags: {error}'), 502)

            if not elements:
                try:
                    elements = self._nominatim_category_fallback(
                        query,
                        keyword,
                        category_id,
                        inferred_subcategory_id,
                        limit
                    )
                except Exception:
                    elements = []

            place = MapPlaceDataModel(
                query=query,
                source='advanced_search',
                selected=MapElementDataModel.from_dict(elements[0]) if elements else None,
                elements=[MapElementDataModel.from_dict(item) for item in elements]
            )

            return self._response(self._ok(place))

        params: dict[str, Any] = {
            'format': 'jsonv2',
            'q': query,
            'limit': limit,
            'addressdetails': 1,
            'extratags': 1,
            'namedetails': 1
        }

        viewbox = self._advanced_search_viewbox()
        if viewbox:
            params['viewbox'] = viewbox
            params['bounded'] = 1

        try:
            elements = self._nominatim_advanced_elements(query, limit, params)
        except Exception as error:
            return self._response(self._error(f'Could not search map data: {error}'), 502)

        place = MapPlaceDataModel(
            query=query,
            source='nominatim_advanced_search',
            selected=elements[0] if elements else None,
            elements=elements
        )

        return self._response(self._ok(place))

    @classmethod
    def _nominatim_advanced_elements(
        cls,
        query: str,
        limit: int,
        base_params: dict[str, Any] | None = None
    ) -> list[MapElementDataModel]:
        """Loads fallback advanced-search results from Nominatim."""
        params: dict[str, Any] = base_params or {
            'format': 'jsonv2',
            'q': query,
            'limit': limit,
            'addressdetails': 1,
            'extratags': 1,
            'namedetails': 1
        }

        if base_params is None:
            viewbox = cls._advanced_search_viewbox()
            if viewbox:
                params['viewbox'] = viewbox
                params['bounded'] = 1

        data = cls._get_json('/search', params)

        return [MapElementDataModel.from_dict(item) for item in data]

    @classmethod
    def _subcategory_from_keyword(cls, keyword: str, category_id: str) -> str:
        """Maps common user keywords to known subcategories for tag-based search."""
        normalized = ' '.join(keyword.strip().lower().split())

        if not normalized:
            return ''

        subcategory = cls._ADVANCED_SEARCH_KEYWORD_ALIASES.get(normalized, '')

        if not subcategory:
            return ''

        return subcategory if subcategory in cls._ADVANCED_SEARCH_GROUPS.get(category_id, ()) else ''

    @classmethod
    def _effective_keyword(cls, keyword: str, subcategory_id: str) -> str:
        """Keeps real names as a filter, but removes generic category words."""
        normalized = ' '.join(keyword.strip().lower().split())

        if subcategory_id and cls._ADVANCED_SEARCH_KEYWORD_ALIASES.get(normalized) == subcategory_id:
            return ''

        return keyword

    @classmethod
    def _nominatim_category_fallback(
        cls,
        query: str,
        keyword: str,
        category_id: str,
        subcategory_id: str,
        limit: int
    ) -> list[dict[str, Any]]:
        """Loads fallback results for categories using several Nominatim search terms."""
        base_terms = cls._ADVANCED_SEARCH_FALLBACK_QUERIES.get(
            subcategory_id,
            cls._ADVANCED_SEARCH_FALLBACK_QUERIES.get(category_id, (query,))
        )
        user_term = keyword.strip()
        terms = tuple(dict.fromkeys((
            *([user_term] if user_term else []),
            *base_terms
        )))
        results: list[dict[str, Any]] = []
        seen: set[str] = set()

        for term in terms:
            if not term:
                continue

            try:
                elements = cls._nominatim_advanced_elements(term, max(1, min(limit, 10)))
            except Exception:
                continue

            for element in elements:
                payload = element.to_dict()
                key = str(payload.get(MapElementDataModel.FIELD_PLACE_ID) or '')

                if not key:
                    coordinates = payload.get(MapElementDataModel.FIELD_COORDINATES, {}) or {}
                    key = f'{coordinates.get("latitude")}:{coordinates.get("longitude")}:{payload.get("display_name")}'

                if key in seen:
                    continue

                seen.add(key)
                results.append(payload)

                if len(results) >= limit:
                    return results

        return results

    @staticmethod
    def _advanced_search_viewbox() -> str | None:
        """Builds a Nominatim viewbox from visible bounds or radius around map center."""
        try:
            radius_km = float(request.args.get('radius_km', 0) or 0)
            center_lat = float(request.args.get('center_lat'))
            center_lon = float(request.args.get('center_lon'))
        except (TypeError, ValueError):
            radius_km = 0
            center_lat = 0
            center_lon = 0

        if radius_km > 0 and -90 <= center_lat <= 90 and -180 <= center_lon <= 180:
            lat_delta = radius_km / 111.32
            lon_delta = radius_km / max(1.0, 111.32 * math.cos(math.radians(center_lat)))
            west = max(-180, center_lon - lon_delta)
            east = min(180, center_lon + lon_delta)
            south = max(-90, center_lat - lat_delta)
            north = min(90, center_lat + lat_delta)

            return f'{west},{north},{east},{south}'

        try:
            west = float(request.args.get('west'))
            east = float(request.args.get('east'))
            south = float(request.args.get('south'))
            north = float(request.args.get('north'))
        except (TypeError, ValueError):
            return None

        if not (-180 <= west <= 180 and -180 <= east <= 180 and -90 <= south <= 90 and -90 <= north <= 90):
            return None

        if abs(east - west) > 0.9 or abs(north - south) > 0.7:
            try:
                center_lat = float(request.args.get('center_lat'))
                center_lon = float(request.args.get('center_lon'))
            except (TypeError, ValueError):
                return f'{west},{north},{east},{south}'

            if -90 <= center_lat <= 90 and -180 <= center_lon <= 180:
                lat_delta = 20.0 / 111.32
                lon_delta = 20.0 / max(1.0, 111.32 * math.cos(math.radians(center_lat)))
                west = max(-180, center_lon - lon_delta)
                east = min(180, center_lon + lon_delta)
                south = max(-90, center_lat - lat_delta)
                north = min(90, center_lat + lat_delta)

        return f'{west},{north},{east},{south}'

    @staticmethod
    def _advanced_search_bbox() -> str | None:
        """Builds an Overpass bbox from visible bounds or radius around map center."""
        viewbox = MapController._advanced_search_viewbox()

        if not viewbox:
            return None

        try:
            west, north, east, south = [float(item) for item in viewbox.split(',')]
        except ValueError:
            return None

        return f'{south},{west},{north},{east}'

    @classmethod
    def _advanced_search_filters(
        cls,
        category_id: str,
        subcategory_id: str
    ) -> list[dict[str, str | tuple[str, ...] | None]]:
        """Returns Overpass tag filters for the selected category."""
        if subcategory_id in cls._ADVANCED_SEARCH_FILTERS:
            return cls._ADVANCED_SEARCH_FILTERS[subcategory_id]

        filters: list[dict[str, str | tuple[str, ...] | None]] = []
        for item in cls._ADVANCED_SEARCH_GROUPS.get(category_id, ()):
            filters.extend(cls._ADVANCED_SEARCH_FILTERS.get(item, []))

        return filters

    @staticmethod
    def _overpass_escape(value: str) -> str:
        """Escapes a value for a simple Overpass string/regex literal."""
        return value.replace('\\', '\\\\').replace('"', '\\"')

    @classmethod
    def _overpass_selector(cls, tags: dict[str, str | tuple[str, ...] | None]) -> str:
        """Builds a tag selector for one Overpass filter."""
        parts = []

        for key, value in tags.items():
            escaped_key = cls._overpass_escape(key)

            if value is None:
                parts.append(f'["{escaped_key}"]')
                continue

            if isinstance(value, tuple):
                pattern = '|'.join(cls._overpass_escape(item) for item in value)
                parts.append(f'["{escaped_key}"~"^({pattern})$"]')
                continue

            parts.append(f'["{escaped_key}"="{cls._overpass_escape(value)}"]')

        return ''.join(parts)

    @classmethod
    def _overpass_query(
        cls,
        filters: list[dict[str, str | tuple[str, ...] | None]],
        bbox: str
    ) -> str:
        """Builds an Overpass query for nodes, ways and relations in the selected bbox."""
        lines = ['[out:json][timeout:12];', '(']

        for tags in filters:
            selector = cls._overpass_selector(tags)
            lines.append(f'  node{selector}({bbox});')
            lines.append(f'  way{selector}({bbox});')
            lines.append(f'  relation{selector}({bbox});')

        lines.extend([
            ');',
            'out center;'
        ])

        return '\n'.join(lines)

    @staticmethod
    def _text_matches_keyword(tags: dict[str, Any], keyword: str) -> bool:
        """Checks whether an Overpass result matches the optional keyword."""
        phrase = keyword.strip().lower()

        if not phrase:
            return True

        values = [
            tags.get('name'),
            tags.get('official_name'),
            tags.get('short_name'),
            tags.get('brand'),
            tags.get('operator'),
            tags.get('addr:street'),
            tags.get('addr:city'),
            tags.get('cuisine'),
            tags.get('description')
        ]

        return any(phrase in str(value or '').lower() for value in values)

    @classmethod
    def _tagged_value(cls, tags: dict[str, Any]) -> tuple[str | None, str | None]:
        """Returns the first main OSM key/value pair from element tags."""
        for key in ('amenity', 'shop', 'tourism', 'leisure', 'healthcare', 'office', 'landuse', 'boundary', 'sport'):
            value = tags.get(key)

            if value:
                return key, str(value)

        return None, None

    @staticmethod
    def _overpass_display_name(tags: dict[str, Any], latitude: float, longitude: float) -> str:
        """Builds a human readable display name for an Overpass element."""
        address_parts = [
            tags.get('addr:street'),
            tags.get('addr:housenumber'),
            tags.get('addr:city')
        ]
        address = ', '.join(str(item) for item in address_parts if item)
        name = tags.get('name') or tags.get('brand') or tags.get('operator')

        if name and address:
            return f'{name}, {address}'

        if name:
            return str(name)

        if address:
            return address

        return f'{latitude:.6f}, {longitude:.6f}'

    @classmethod
    def _overpass_element_payload(cls, item: dict[str, Any]) -> dict[str, Any] | None:
        """Converts one Overpass element to the map element payload shape."""
        tags = dict(item.get('tags') or {})
        latitude = item.get('lat', item.get('center', {}).get('lat'))
        longitude = item.get('lon', item.get('center', {}).get('lon'))

        try:
            lat = float(latitude)
            lon = float(longitude)
        except (TypeError, ValueError):
            return None

        if not -90 <= lat <= 90 or not -180 <= lon <= 180:
            return None

        category, element_type = cls._tagged_value(tags)
        display_name = cls._overpass_display_name(tags, lat, lon)

        return MapElementDataModel.from_dict({
            'place_id': f'overpass:{item.get("type")}:{item.get("id")}',
            'osm_type': item.get('type'),
            'osm_id': item.get('id'),
            'category': category,
            'type': element_type,
            'display_name': display_name,
            'coordinates': {
                'latitude': lat,
                'longitude': lon
            },
            'address': tags,
            'name': tags,
            'annotations': tags,
            'properties': tags,
            'references': tags,
            'restrictions': tags,
            'primary_features': tags,
            'raw_data': {
                **item,
                'source': 'overpass_advanced_search'
            }
        }).to_dict()

    @classmethod
    def _overpass_results(
        cls,
        category_id: str,
        subcategory_id: str,
        keyword: str,
        limit: int
    ) -> list[dict[str, Any]]:
        """Loads advanced-search results by exact OSM tags from Overpass."""
        bbox = cls._advanced_search_bbox()

        if not bbox:
            return []

        filters = cls._advanced_search_filters(category_id, subcategory_id)

        if not filters:
            return []

        query = cls._overpass_query(filters, bbox)
        data = None
        last_error: Exception | None = None

        for index, url in enumerate((cls._OVERPASS_URL, *cls._OVERPASS_FALLBACK_URLS)):
            for _ in range(2 if index == 0 else 1):
                try:
                    data = cls._post_form_json(url, {'data': query})
                    break
                except Exception as error:
                    last_error = error

            if data is not None:
                break

        if data is None:
            raise last_error or RuntimeError('Overpass request failed.')

        results: list[dict[str, Any]] = []
        seen: set[tuple[str, Any]] = set()

        for item in data.get('elements', []):
            key = (str(item.get('type')), item.get('id'))
            tags = dict(item.get('tags') or {})

            if key in seen or not cls._text_matches_keyword(tags, keyword):
                continue

            payload = cls._overpass_element_payload(item)

            if not payload:
                continue

            seen.add(key)
            results.append(payload)

            if len(results) >= limit:
                break

        return results

    #endregion Endpoints

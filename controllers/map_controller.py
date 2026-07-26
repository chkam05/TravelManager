from __future__ import annotations
from typing import Any, ClassVar

from flask import jsonify, request

from core.api.base_controller import BaseController
from models.map.map_place_data_model import MapPlaceDataModel
from models.map_data_model import MapDataModel
from resources.map_legend import MapLegend
from services.map_search_service import MapSearchService
from utils.converters.map_legend_converter import MapLegendConverter
from utils.data.nominatim_downloader import NominatimDownloader
from utils.data.route_downloader import RouteDownloader


class MapController(BaseController):
    """Exposes map endpoints and delegates domain work to map services."""

    CONTROLLER_NAME: ClassVar[str] = 'MapController'

    def register_routes(self):
        self.add_url_rule('/api/map/legend', view_func=self.legend, methods=['GET'])
        self.add_url_rule('/api/map/reverse', view_func=self.reverse, methods=['GET'])
        self.add_url_rule('/api/map/route', view_func=self.route, methods=['POST'])
        self.add_url_rule('/api/map/search', view_func=self.search, methods=['GET'])
        self.add_url_rule('/api/map/advanced-search', view_func=self.advanced_search, methods=['GET'])

    #region Responses

    @staticmethod
    def _response(model: MapDataModel, status: int = 200):
        """Returns a Flask JSON response from a map data model."""
        return jsonify(model.to_dict()), status

    @staticmethod
    def _ok(place: MapPlaceDataModel) -> MapDataModel:
        """Builds a successful map API response."""
        return MapDataModel(status='ok', message=None, place=place)

    @staticmethod
    def _error(message: str) -> MapDataModel:
        """Builds a failed map API response."""
        return MapDataModel(status='error', message=message, place=None)

    #endregion Responses

    #region Validation

    @staticmethod
    def _route_points(value: Any) -> list[dict[str, float]]:
        """Validates and normalizes route point payloads."""
        if not isinstance(value, list) or not 2 <= len(value) <= 25:
            raise ValueError('Route requires between 2 and 25 points.')

        result: list[dict[str, float]] = []
        for point in value:
            if not isinstance(point, dict):
                raise ValueError('Invalid route point.')

            try:
                latitude = float(point.get('latitude'))
                longitude = float(point.get('longitude'))
            except (TypeError, ValueError) as error:
                raise ValueError('Invalid route coordinates.') from error

            if not -90 <= latitude <= 90 or not -180 <= longitude <= 180:
                raise ValueError('Route coordinates are out of range.')

            result.append({'latitude': latitude, 'longitude': longitude})

        return result

    #endregion Validation

    #region Endpoints

    def legend(self):
        """Returns the OpenStreetMap legend used by the frontend."""
        return jsonify({
            'status': 'ok',
            'legend': {
                'tabs': [
                    MapLegendConverter.convert_tab('symbols', 'Symbole', MapLegend.SYMBOLS),
                    MapLegendConverter.convert_tab('lines', 'Linie', MapLegend.LINES),
                    MapLegendConverter.convert_tab('areas', 'Obszary', MapLegend.AREAS)
                ]
            }
        })

    def route(self):
        """Returns a route through supplied points in their current order."""
        data = request.get_json(silent=True) or {}

        try:
            points = self._route_points(data.get('points') if isinstance(data, dict) else None)
        except ValueError as error:
            return jsonify({'status': 'error', 'message': str(error)}), 400

        transport = str(data.get('transport', 'car'))
        include_toll_roads = bool(data.get('include_toll_roads', True))

        try:
            route = RouteDownloader.download(points, transport, include_toll_roads)
        except ValueError as error:
            return jsonify({'status': 'error', 'message': str(error)}), 422
        except Exception as error:
            message = (
                f'Nie udało się obliczyć trasy bez płatnych dróg: {error}'
                if transport == 'car' and not include_toll_roads
                else f'Could not calculate route: {error}'
            )
            return jsonify({'status': 'error', 'message': message}), 502

        return jsonify({'status': 'ok', 'route': route.to_dict()})

    def reverse(self):
        """Returns structured OpenStreetMap data for clicked coordinates."""
        latitude = request.args.get('lat')
        longitude = request.args.get('lon')

        if not latitude or not longitude:
            return self._response(self._error('Missing lat or lon.'), 400)

        try:
            selected = NominatimDownloader.reverse(latitude, longitude)
        except Exception as error:
            return self._response(self._error(f'Could not load map data: {error}'), 502)

        return self._response(self._ok(MapPlaceDataModel(
            query=f'{latitude},{longitude}',
            source='nominatim_reverse',
            selected=selected,
            elements=[selected]
        )))

    def search(self):
        """Returns structured OpenStreetMap data for a place query."""
        query = request.args.get('q', '').strip()

        if not query:
            return self._response(self._error('Missing search query.'), 400)

        try:
            place = MapSearchService.search(query)
        except Exception as error:
            return self._response(self._error(f'Could not search map data: {error}'), 502)

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

        try:
            place = MapSearchService.advanced_search(
                query=query,
                keyword=keyword,
                category_id=category_id,
                subcategory_id=subcategory_id,
                limit=limit,
                bounds=request.args.to_dict()
            )
        except Exception as error:
            return self._response(self._error(str(error)), 502)

        return self._response(self._ok(place))

    #endregion Endpoints

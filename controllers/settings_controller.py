from __future__ import annotations
import json
from math import isfinite
from typing import Any, ClassVar, Dict
from uuid import uuid4

from flask import jsonify, request

from core.api.base_controller import BaseController
from models.settings.ui_settings import UiSettings
from models.settings.car_profile import CarProfile
from models.settings.favourite_place import FavouritePlace
from models.settings.favourite_tag import FavouriteTag
from models.settings.saved_route import SavedRoute
from resources.settings_transfer import SettingsTransferTypes
from storage.settings_storage import SettingsStorage


class SettingsController(BaseController):
    """Controller for application settings."""

    CONTROLLER_NAME: ClassVar[str] = 'SettingsController'

    def __init__(self, settings_storage: SettingsStorage):
        self._settings_storage = settings_storage
        super().__init__()

    def register_routes(self):
        self.add_url_rule('/api/settings/ui', view_func=self.get_ui_settings, methods=['GET'])
        self.add_url_rule('/api/settings/ui', view_func=self.update_ui_settings, methods=['PATCH'])
        self.add_url_rule('/api/settings/export/<data_type>', view_func=self.export_data, methods=['GET'])
        self.add_url_rule('/api/settings/import/<data_type>', view_func=self.import_data, methods=['POST'])
        self.add_url_rule('/api/favourites', view_func=self.get_favourites, methods=['GET'])
        self.add_url_rule('/api/favourites', view_func=self.save_favourite, methods=['POST'])
        self.add_url_rule('/api/favourites/<favourite_id>', view_func=self.delete_favourite, methods=['DELETE'])
        self.add_url_rule('/api/favourite-tags', view_func=self.get_favourite_tags, methods=['GET'])
        self.add_url_rule('/api/favourite-tags', view_func=self.save_favourite_tag, methods=['POST'])
        self.add_url_rule('/api/favourite-tags/<tag_id>', view_func=self.delete_favourite_tag, methods=['DELETE'])
        self.add_url_rule('/api/car-profiles', view_func=self.get_car_profiles, methods=['GET'])
        self.add_url_rule('/api/car-profiles', view_func=self.save_car_profile, methods=['POST'])
        self.add_url_rule('/api/car-profiles/active', view_func=self.set_active_car_profile, methods=['PATCH'])
        self.add_url_rule('/api/car-profiles/<profile_id>', view_func=self.delete_car_profile, methods=['DELETE'])
        self.add_url_rule('/api/routes', view_func=self.get_routes, methods=['GET'])
        self.add_url_rule('/api/routes', view_func=self.save_route, methods=['POST'])
        self.add_url_rule('/api/routes/<route_id>', view_func=self.delete_route, methods=['DELETE'])

    # --- ENDPOINTS ---

    def get_ui_settings(self):
        settings = self._settings_storage.load()

        return jsonify({
            'status': 'ok',
            'ui': settings.ui.to_dict()
        })

    def update_ui_settings(self):
        data = request.get_json(silent=True) or {}

        if not isinstance(data, dict):
            return jsonify({
                'status': 'error',
                'message': 'Invalid JSON body.'
            }), 400

        settings = self._settings_storage.load()
        settings.ui = self._merge_ui_settings(settings.ui, data)
        self._settings_storage.save(settings)

        return jsonify({
            'status': 'ok',
            'ui': settings.ui.to_dict()
        })

    def export_data(self, data_type: str):
        if not SettingsTransferTypes.is_supported(data_type):
            return jsonify({'status': 'error', 'message': 'Unsupported export data type.'}), 404

        plaintext = self._export_settings_text(data_type)

        return jsonify({
            'status': 'ok',
            'filename': SettingsTransferTypes.file_name(data_type),
            'payload': json.loads(plaintext)
        })

    def import_data(self, data_type: str):
        if not SettingsTransferTypes.is_supported(data_type):
            return jsonify({'status': 'error', 'message': 'Unsupported import data type.'}), 404

        payload = request.get_json(silent=True)

        try:
            plaintext = json.dumps(payload, ensure_ascii=False)
            self._import_settings_text(data_type, plaintext)
        except (TypeError, ValueError, json.JSONDecodeError):
            return jsonify({
                'status': 'error',
                'message': 'Selected JSON does not match the requested data type.'
            }), 400

        return jsonify({
            'status': 'imported',
            'type': data_type,
            'label': SettingsTransferTypes.label(data_type)
        })

    def get_favourites(self):
        settings = self._settings_storage.load()
        tags = {tag.id: tag.to_dict() for tag in settings.favourite_tags}

        return jsonify({
            'status': 'ok',
            'favourites': [
                {
                    **favourite.to_dict(),
                    'tag': tags.get(favourite.tag_id)
                }
                for favourite in settings.favourites
            ]
        })

    def save_favourite(self):
        data = request.get_json(silent=True) or {}
        required = ('source_key', 'name', 'tag_id', 'latitude', 'longitude', 'place_data')

        if not isinstance(data, dict) or any(key not in data for key in required):
            return jsonify({'status': 'error', 'message': 'Invalid favourite data.'}), 400

        settings = self._settings_storage.load()
        tag_ids = {tag.id for tag in settings.favourite_tags}
        favourite_id = str(data.get('id') or '')
        existing = next((
            item for item in settings.favourites
            if item.id == favourite_id or item.source_key == str(data['source_key'])
        ), None)
        payload = {
            **data,
            'id': existing.id if existing else (favourite_id or uuid4().hex)
        }

        try:
            favourite = FavouritePlace.from_dict(payload)
        except (TypeError, ValueError):
            return jsonify({'status': 'error', 'message': 'Invalid favourite coordinates.'}), 400

        if (
            not favourite.source_key
            or not favourite.name.strip()
            or favourite.tag_id not in tag_ids
            or (favourite.icon is not None and len(favourite.icon) > 16)
            or not isfinite(favourite.latitude)
            or not isfinite(favourite.longitude)
            or not (-90 <= favourite.latitude <= 90)
            or not (-180 <= favourite.longitude <= 180)
        ):
            return jsonify({'status': 'error', 'message': 'Invalid favourite data.'}), 400

        settings.favourites = [
            item for item in settings.favourites
            if item.id != favourite.id and item.source_key != favourite.source_key
        ]
        settings.favourites.append(favourite)
        self._settings_storage.save(settings)
        tag = next((item for item in settings.favourite_tags if item.id == favourite.tag_id), None)

        return jsonify({
            'status': 'ok',
            'favourite': {
                **favourite.to_dict(),
                'tag': tag.to_dict() if tag else None
            }
        })

    def delete_favourite(self, favourite_id: str):
        settings = self._settings_storage.load()
        remaining = [item for item in settings.favourites if item.id != favourite_id]

        if len(remaining) == len(settings.favourites):
            return jsonify({'status': 'error', 'message': 'Favourite not found.'}), 404

        settings.favourites = remaining
        self._settings_storage.save(settings)

        return jsonify({'status': 'ok'})

    def get_favourite_tags(self):
        settings = self._settings_storage.load()

        return jsonify({
            'status': 'ok',
            'tags': FavouriteTag.to_dict_list(settings.favourite_tags)
        })

    def save_favourite_tag(self):
        data = request.get_json(silent=True) or {}
        required = ('name', 'icon')

        if not isinstance(data, dict) or any(key not in data for key in required):
            return jsonify({'status': 'error', 'message': 'Invalid favourite tag data.'}), 400

        payload = {
            **data,
            'id': str(data.get('id') or uuid4().hex)
        }

        try:
            tag = FavouriteTag.from_dict(payload)
        except (TypeError, ValueError):
            return jsonify({'status': 'error', 'message': 'Invalid favourite tag data.'}), 400

        if not tag.id or not tag.name.strip() or not tag.icon or len(tag.icon) > 16:
            return jsonify({'status': 'error', 'message': 'Invalid favourite tag data.'}), 400

        settings = self._settings_storage.load()
        settings.favourite_tags = [item for item in settings.favourite_tags if item.id != tag.id]
        settings.favourite_tags.append(tag)
        self._settings_storage.save(settings)

        return jsonify({'status': 'ok', 'tag': tag.to_dict()})

    def delete_favourite_tag(self, tag_id: str):
        if tag_id == FavouriteTag.DEFAULT_TAG_ID:
            return jsonify({'status': 'error', 'message': 'Default tag cannot be deleted.'}), 400

        settings = self._settings_storage.load()
        remaining = [item for item in settings.favourite_tags if item.id != tag_id]

        if len(remaining) == len(settings.favourite_tags):
            return jsonify({'status': 'error', 'message': 'Favourite tag not found.'}), 404

        for favourite in settings.favourites:
            if favourite.tag_id == tag_id:
                favourite.tag_id = FavouriteTag.DEFAULT_TAG_ID

        settings.favourite_tags = remaining or [FavouriteTag.default()]
        self._settings_storage.save(settings)

        return jsonify({'status': 'ok'})

    def get_car_profiles(self):
        settings = self._settings_storage.load()
        active = next((
            profile
            for profile in settings.car_profiles
            if profile.id == settings.active_car_profile_id
        ), None)

        return jsonify({
            'status': 'ok',
            'active_car_profile_id': settings.active_car_profile_id,
            'active_car_profile': active.to_dict() if active else None,
            'profiles': CarProfile.to_dict_list(settings.car_profiles)
        })

    def save_car_profile(self):
        data = request.get_json(silent=True) or {}

        if not isinstance(data, dict):
            return jsonify({'status': 'error', 'message': 'Invalid car profile data.'}), 400

        profile_id = str(data.get('id') or uuid4().hex)
        existing = next((
            profile
            for profile in self._settings_storage.load().car_profiles
            if profile.id == profile_id
        ), None)
        payload = {
            **data,
            'id': existing.id if existing else profile_id
        }

        try:
            profile = CarProfile.from_dict(payload)
        except (TypeError, ValueError):
            return jsonify({'status': 'error', 'message': 'Invalid car profile data.'}), 400

        if not profile.brand.strip() and not profile.model.strip() and not profile.name.strip():
            return jsonify({'status': 'error', 'message': 'Car profile requires at least name, brand or model.'}), 400

        settings = self._settings_storage.load()
        settings.car_profiles = [item for item in settings.car_profiles if item.id != profile.id]
        settings.car_profiles.append(profile)

        if not settings.active_car_profile_id:
            settings.active_car_profile_id = profile.id

        self._settings_storage.save(settings)

        return jsonify({
            'status': 'ok',
            'active_car_profile_id': settings.active_car_profile_id,
            'profile': profile.to_dict()
        })

    def set_active_car_profile(self):
        data = request.get_json(silent=True) or {}
        profile_id = data.get('profile_id') if isinstance(data, dict) else None
        profile_id = str(profile_id) if profile_id else None
        settings = self._settings_storage.load()

        if profile_id and not any(profile.id == profile_id for profile in settings.car_profiles):
            return jsonify({'status': 'error', 'message': 'Car profile not found.'}), 404

        settings.active_car_profile_id = profile_id
        self._settings_storage.save(settings)

        active = next((
            profile
            for profile in settings.car_profiles
            if profile.id == settings.active_car_profile_id
        ), None)

        return jsonify({
            'status': 'ok',
            'active_car_profile_id': settings.active_car_profile_id,
            'active_car_profile': active.to_dict() if active else None
        })

    def delete_car_profile(self, profile_id: str):
        settings = self._settings_storage.load()
        remaining = [item for item in settings.car_profiles if item.id != profile_id]

        if len(remaining) == len(settings.car_profiles):
            return jsonify({'status': 'error', 'message': 'Car profile not found.'}), 404

        settings.car_profiles = remaining

        if settings.active_car_profile_id == profile_id:
            settings.active_car_profile_id = None

        self._settings_storage.save(settings)

        return jsonify({
            'status': 'ok',
            'active_car_profile_id': settings.active_car_profile_id
        })

    def get_routes(self):
        settings = self._settings_storage.load()

        return jsonify({
            'status': 'ok',
            'routes': SavedRoute.to_dict_list(settings.routes)
        })

    def save_route(self):
        data = request.get_json(silent=True) or {}

        if not isinstance(data, dict):
            return jsonify({'status': 'error', 'message': 'Invalid route data.'}), 400

        route_id = str(data.get('id') or uuid4().hex)
        existing = next((
            route
            for route in self._settings_storage.load().routes
            if route.id == route_id
        ), None)
        payload = {
            **data,
            'id': existing.id if existing else route_id
        }

        try:
            route = SavedRoute.from_dict(payload)
        except (TypeError, ValueError):
            return jsonify({'status': 'error', 'message': 'Invalid route data.'}), 400

        if (
            not route.id
            or not route.name.strip()
            or not route.icon
            or len(route.icon) > 16
            or len(route.points) < 2
            or not isfinite(route.distance)
            or route.distance < 0
            or not isfinite(route.duration)
            or route.duration < 0
        ):
            return jsonify({'status': 'error', 'message': 'Invalid route data.'}), 400

        for point in route.points:
            if (
                not point.title.strip()
                or not isfinite(point.latitude)
                or not isfinite(point.longitude)
                or not (-90 <= point.latitude <= 90)
                or not (-180 <= point.longitude <= 180)
            ):
                return jsonify({'status': 'error', 'message': 'Invalid route point data.'}), 400

        settings = self._settings_storage.load()
        settings.routes = [item for item in settings.routes if item.id != route.id]
        settings.routes.append(route)
        self._settings_storage.save(settings)

        return jsonify({
            'status': 'ok',
            'route': route.to_dict()
        })

    def delete_route(self, route_id: str):
        settings = self._settings_storage.load()
        remaining = [item for item in settings.routes if item.id != route_id]

        if len(remaining) == len(settings.routes):
            return jsonify({'status': 'error', 'message': 'Route not found.'}), 404

        settings.routes = remaining
        self._settings_storage.save(settings)

        return jsonify({'status': 'ok'})

    #region Helpers

    @classmethod
    def _merge_ui_settings(cls, current: UiSettings, data: Dict[str, Any]) -> UiSettings:
        """Merges partial UI settings payload with the current settings model."""
        merged = current.to_dict()

        for key in UiSettings.field_names():
            if key in data:
                merged[key] = data[key]

        return UiSettings.from_dict(merged)

    def _export_settings_text(self, data_type: str) -> str:
        """Calls the explicit storage exporter assigned to a settings type."""
        if data_type == SettingsTransferTypes.FUEL_COSTS:
            return self._settings_storage.export_fuel_costs()
        if data_type == SettingsTransferTypes.ROUTES:
            return self._settings_storage.export_routes()
        if data_type == SettingsTransferTypes.FAVOURITES:
            return self._settings_storage.export_favourites_and_tags()
        if data_type == SettingsTransferTypes.CARS:
            return self._settings_storage.export_cars()
        raise ValueError('Unsupported export data type.')

    def _import_settings_text(self, data_type: str, plaintext: str) -> None:
        """Calls the explicit storage importer assigned to a settings type."""
        if data_type == SettingsTransferTypes.FUEL_COSTS:
            self._settings_storage.import_fuel_costs(plaintext)
            return
        if data_type == SettingsTransferTypes.ROUTES:
            self._settings_storage.import_routes(plaintext)
            return
        if data_type == SettingsTransferTypes.FAVOURITES:
            self._settings_storage.import_favourites_and_tags(plaintext)
            return
        if data_type == SettingsTransferTypes.CARS:
            self._settings_storage.import_cars(plaintext)
            return
        raise ValueError('Unsupported import data type.')

    #endregion Helpers

from __future__ import annotations
import json
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from functools import wraps
from math import isfinite
from typing import Any, ClassVar, Dict
from uuid import uuid4

from flask import jsonify, request

from core.api.base_controller import BaseController
from core.language_service import LanguageService
from models.settings.ui_settings import UiSettings
from models.settings.appearance import Appearance
from models.settings.car_profile import CarProfile
from models.settings.favourite_place import FavouritePlace
from models.settings.favourite_tag import FavouriteTag
from models.settings.saved_route import SavedRoute
from models.settings.custom_layer import CustomLayer
from resources.settings_transfer import SettingsTransferTypes
from resources.public_transport.public_transport_providers import PublicTransportProviders
from resources.public_transport.rail_gtfs_sources import RailGtfsSources
from storage.settings_storage import SettingsStorage
from storage.layer_draft_storage import LayerDraftStorage
from services.layer_transfer import import_layer, export_layer


def settings_transaction(method):
    """Keep settings mutations atomic with other writers of the settings file."""
    @wraps(method)
    def wrapped(self, *args, **kwargs):
        with self._settings_storage.transaction():
            return method(self, *args, **kwargs)
    return wrapped


class SettingsController(BaseController):
    """Controller for application settings."""

    CONTROLLER_NAME: ClassVar[str] = 'SettingsController'

    def __init__(self, settings_storage: SettingsStorage):
        self._settings_storage = settings_storage
        self._layer_draft_storage = LayerDraftStorage(settings_storage.directory)
        super().__init__()

    def register_routes(self):
        self.add_url_rule('/api/custom-layers/parse', view_func=self.parse_layer_file, methods=['POST'])
        self.add_url_rule('/api/custom-layers/<layer_id>/export/<format>', view_func=self.export_layer_file, methods=['GET'])
        self.add_url_rule('/api/custom-layer-draft', view_func=self.layer_draft, methods=['GET', 'PUT', 'DELETE'])
        self.add_url_rule('/api/settings/ui', view_func=self.get_ui_settings, methods=['GET'])
        self.add_url_rule('/api/settings/ui', view_func=self.update_ui_settings, methods=['PATCH'])
        self.add_url_rule('/api/settings/appearance', view_func=self.get_appearance, methods=['GET'])
        self.add_url_rule('/api/settings/appearance', view_func=self.update_appearance, methods=['PATCH'])
        self.add_url_rule('/api/settings/public-transport', view_func=self.get_public_transport_settings, methods=['GET'])
        self.add_url_rule('/api/settings/public-transport', view_func=self.update_public_transport_settings, methods=['PATCH'])
        self.add_url_rule('/api/settings/export/<data_type>', view_func=self.export_data, methods=['GET'])
        self.add_url_rule('/api/settings/import/<data_type>', view_func=self.import_data, methods=['POST'])
        self.add_url_rule('/api/settings/storage', view_func=self.get_storage_usage, methods=['GET'])
        self.add_url_rule('/api/settings/storage/<data_type>/<path:item_id>', view_func=self.delete_stored_data, methods=['DELETE'])
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
        self.add_url_rule('/api/custom-layers', view_func=self.get_custom_layers, methods=['GET'])
        self.add_url_rule('/api/custom-layers', view_func=self.save_custom_layer, methods=['POST'])
        self.add_url_rule('/api/custom-layers/<layer_id>', view_func=self.delete_custom_layer, methods=['DELETE'])

    # --- ENDPOINTS ---

    def layer_draft(self):
        if request.method == 'GET':
            return jsonify({'draft': self._layer_draft_storage.load()})
        if request.method == 'DELETE':
            self._layer_draft_storage.clear()
        else:
            try:
                self._layer_draft_storage.save(request.get_json(silent=True))
            except (TypeError, ValueError) as error:
                return jsonify({'status': 'error', 'message': str(error)}), 400
        return jsonify({'status': 'ok'})

    def parse_layer_file(self):
        try:
            data = request.get_json(silent=True)
            layer = import_layer(data['text'], data.get('filename', 'Imported layer'))
            return jsonify({'layer': layer})
        except (ValueError, TypeError, KeyError, IndexError, AttributeError, RecursionError, OverflowError, ET.ParseError) as error:
            return jsonify({'message': str(error)}), 400

    def export_layer_file(self, layer_id, format):
        layer = next((e for e in self._settings_storage.load().custom_layers if e.id == layer_id), None)
        if layer is None:
            return jsonify({'message': 'Layer not found'}), 404
        try:
            return jsonify({'text': export_layer(layer.to_dict(), format), 'filename': f'layer-{layer.id}.{format}'})
        except ValueError as error:
            return jsonify({'message': str(error)}), 400

    def get_custom_layers(self):
        settings = self._settings_storage.load()
        return jsonify({'status': 'ok', 'layers': [item.to_dict() for item in settings.custom_layers]})

    @settings_transaction
    def save_custom_layer(self):
        data = request.get_json(silent=True)
        if isinstance(data, dict) and data.get('id') in (None, ''):
            data = {**data, 'id': uuid4().hex}
        try:
            layer = CustomLayer.from_payload(data)
        except ValueError as error:
            return jsonify({'status': 'error', 'message': str(error)}), 400
        settings = self._settings_storage.load()
        settings.custom_layers = [item for item in settings.custom_layers if item.id != layer.id]
        settings.custom_layers.append(layer)
        self._settings_storage.save(settings)
        return jsonify({'status': 'ok', 'layer': layer.to_dict()})

    @settings_transaction
    def delete_custom_layer(self, layer_id: str):
        settings = self._settings_storage.load()
        remaining = [item for item in settings.custom_layers if item.id != layer_id]
        if len(remaining) == len(settings.custom_layers):
            return jsonify({'status': 'error', 'message': 'Layer not found'}), 404
        settings.custom_layers = remaining
        self._settings_storage.save(settings)
        return jsonify({'status': 'ok'})

    def get_ui_settings(self):
        settings = self._settings_storage.load()

        return jsonify({
            'status': 'ok',
            'ui': settings.ui.to_dict()
        })

    @settings_transaction
    def update_ui_settings(self):
        data = request.get_json(silent=True) or {}

        if not isinstance(data, dict):
            return jsonify({
                'status': 'error',
                'message': LanguageService.translate_current('SETTINGS_VIEW.INVALID_JSON_BODY')
            }), 400

        settings = self._settings_storage.load()
        settings.ui = self._merge_ui_settings(settings.ui, data)
        self._settings_storage.save(settings)

        return jsonify({
            'status': 'ok',
            'ui': settings.ui.to_dict()
        })

    def get_appearance(self):
        """Returns persisted application appearance settings."""
        settings = self._settings_storage.load()
        return jsonify({
            'status': 'ok',
            'appearance': settings.appearance.to_dict()
        })

    @settings_transaction
    def update_appearance(self):
        """Updates selected appearance fields and persists recent colors."""
        data = request.get_json(silent=True) or {}
        if not isinstance(data, dict):
            return jsonify({
                'status': 'error',
                'message': LanguageService.translate_current('SETTINGS_VIEW.INVALID_JSON_BODY')
            }), 400
        settings = self._settings_storage.load()
        merged = settings.appearance.to_dict()
        for key in Appearance.field_names():
            if key in data:
                merged[key] = data[key]
        settings.appearance = Appearance.from_dict(merged)
        self._settings_storage.save(settings)
        return jsonify({
            'status': 'ok',
            'appearance': settings.appearance.to_dict()
        })

    def get_public_transport_settings(self):
        settings = self._settings_storage.load()
        return jsonify({
            'status': 'ok',
            'provider': settings.selected_public_transport_provider,
            'providers': settings.selected_public_transport_providers,
            'mode': settings.selected_public_transport_mode
        })

    @staticmethod
    def _payload_size(payload: Any) -> int:
        return len(json.dumps(payload, ensure_ascii=False, separators=(',', ':')).encode('utf-8'))

    def get_storage_usage(self):
        """Lists independently removable user data and downloaded timetables."""
        settings = self._settings_storage.load()
        transport = []
        database_ids = set()
        for path in sorted(self._settings_storage.directory.glob('*_gtfs.sqlite3')):
            item_id = path.name.removesuffix('_gtfs.sqlite3')
            if item_id not in PublicTransportProviders.VALUES and item_id not in RailGtfsSources.SOURCES:
                continue
            database_ids.add(item_id)
            stat = path.stat()
            if item_id in RailGtfsSources.SOURCES:
                name = LanguageService.translate_current(
                    f'SETTINGS_MEMORY.RAIL_SOURCE_{item_id.upper()}'
                )
            else:
                name_key = PublicTransportProviders.NAME_KEYS.get(item_id)
                name = LanguageService.translate_current(name_key) if name_key else item_id
            transport.append({
                'id': item_id,
                'kind': 'gtfs',
                'name': name,
                'size': stat.st_size,
                'updated_at': datetime.fromtimestamp(
                    stat.st_mtime, tz=timezone.utc
                ).isoformat()
            })
        for carrier, cache in sorted(settings.public_transport_cache.items()):
            if carrier in database_ids:
                continue
            name_key = PublicTransportProviders.NAME_KEYS.get(carrier)
            transport.append({
                'id': carrier,
                'kind': 'provider',
                'name': LanguageService.translate_current(name_key) if name_key else carrier,
                'size': self._payload_size(cache.to_dict()),
                'updated_at': datetime.fromtimestamp(
                    self._settings_storage.file_path.stat().st_mtime,
                    tz=timezone.utc
                ).isoformat() if self._settings_storage.file_path.exists() else None
            })
        serialized = settings.to_dict()
        application = [
            {'id': 'fuel_costs', 'name_key': 'SETTINGS_MEMORY.FUEL_PRICES', 'payload': [serialized['fuel_data'], serialized['exchange_rates']]},
            {'id': 'cars', 'name_key': 'SETTINGS_MEMORY.CARS', 'payload': [serialized['active_car_profile_id'], serialized['car_profiles']]},
            {'id': 'routes', 'name_key': 'SETTINGS_MEMORY.ROUTES', 'payload': serialized['routes']},
            {'id': 'favourites', 'name_key': 'SETTINGS_MEMORY.FAVOURITES', 'payload': [serialized['favourites'], serialized['favourite_tags']]},
            {'id': 'layers', 'name_key': 'SETTINGS_MEMORY.LAYERS', 'payload': serialized['custom_layers']}
        ]
        return jsonify({
            'status': 'ok',
            'public_transport': transport,
            'application': [{
                'id': item['id'],
                'name': LanguageService.translate_current(item['name_key']),
                'size': self._payload_size(item['payload'])
            } for item in application]
        })

    @settings_transaction
    def delete_stored_data(self, data_type: str, item_id: str):
        settings = self._settings_storage.load()
        if data_type == 'provider' and item_id in settings.public_transport_cache:
            del settings.public_transport_cache[item_id]
        elif data_type == 'gtfs' and (
            item_id in PublicTransportProviders.VALUES
            or item_id in RailGtfsSources.SOURCES
        ):
            base = self._settings_storage.directory / f'{item_id}_gtfs.sqlite3'
            for path in (base, base.with_suffix('.zip.part'),
                         base.with_suffix('.sqlite3-wal'), base.with_suffix('.sqlite3-shm')):
                try:
                    path.unlink()
                except FileNotFoundError:
                    pass
            return jsonify({'status': 'ok'})
        elif data_type == 'application':
            if item_id == 'fuel_costs':
                settings.fuel_data = []
                settings.exchange_rates = []
            elif item_id == 'cars':
                settings.car_profiles = []
                settings.active_car_profile_id = None
            elif item_id == 'routes':
                settings.routes = []
            elif item_id == 'favourites':
                settings.favourites = []
                settings.favourite_tags = [FavouriteTag.default()]
            elif item_id == 'layers':
                settings.custom_layers = []
                self._layer_draft_storage.clear()
            else:
                return jsonify({'status': 'error'}), 404
        else:
            return jsonify({'status': 'error'}), 404
        self._settings_storage.save(settings)
        return jsonify({'status': 'ok'})

    @settings_transaction
    def update_public_transport_settings(self):
        data = request.get_json(silent=True) or {}
        provider = str(data.get('provider') or '')
        if provider not in PublicTransportProviders.VALUES:
            return jsonify({
                'status': 'error',
                'message': LanguageService.translate_current('PUBLIC_TRANSPORT_ERROR.UNSUPPORTED_PROVIDER')
            }), 400
        mode = str(data.get('mode') or '').strip()
        expected_mode = 'rail' if provider.startswith('rail_') else 'city'
        if mode not in {'city', 'rail'} or mode != expected_mode:
            mode = expected_mode
        settings = self._settings_storage.load()
        settings.selected_public_transport_provider = provider
        settings.selected_public_transport_providers[mode] = provider
        settings.selected_public_transport_mode = mode
        self._settings_storage.save(settings)
        return jsonify({
            'status': 'ok', 'provider': provider,
            'providers': settings.selected_public_transport_providers,
            'mode': mode
        })

    def export_data(self, data_type: str):
        if not SettingsTransferTypes.is_supported(data_type):
            return jsonify({
                'status': 'error',
                'message': LanguageService.translate_current('SETTINGS_BACKUP.UNSUPPORTED_EXPORT_TYPE')
            }), 404

        plaintext = self._export_settings_text(data_type)

        return jsonify({
            'status': 'ok',
            'filename': SettingsTransferTypes.file_name(data_type),
            'payload': json.loads(plaintext)
        })

    @settings_transaction
    def import_data(self, data_type: str):
        if not SettingsTransferTypes.is_supported(data_type):
            return jsonify({
                'status': 'error',
                'message': LanguageService.translate_current('SETTINGS_BACKUP.UNSUPPORTED_IMPORT_TYPE')
            }), 404

        payload = request.get_json(silent=True)

        try:
            plaintext = json.dumps(payload, ensure_ascii=False)
            self._import_settings_text(data_type, plaintext)
        except (TypeError, ValueError, json.JSONDecodeError):
            return jsonify({
                'status': 'error',
                'message': LanguageService.translate_current('SETTINGS_BACKUP.INVALID_IMPORT_FILE')
            }), 400

        return jsonify({
            'status': 'imported',
            'type': data_type,
            'label': LanguageService.translate_current(SettingsTransferTypes.label_key(data_type))
        })

    @staticmethod
    def _favourite_tag_payload(tag: FavouriteTag) -> dict[str, Any]:
        """Returns a tag with its built-in name translated for presentation."""
        payload = tag.to_dict()
        if (
            tag.id == FavouriteTag.DEFAULT_TAG_ID
            and tag.name == FavouriteTag.DEFAULT_NAME_KEY
        ):
            payload[FavouriteTag.FIELD_NAME] = LanguageService.translate_current(FavouriteTag.DEFAULT_NAME_KEY)
        return payload

    def get_favourites(self):
        settings = self._settings_storage.load()
        tags = {
            tag.id: self._favourite_tag_payload(tag)
            for tag in settings.favourite_tags
        }

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

    @settings_transaction
    def save_favourite(self):
        data = request.get_json(silent=True) or {}
        required = ('source_key', 'name', 'tag_id', 'latitude', 'longitude', 'place_data')

        if not isinstance(data, dict) or any(key not in data for key in required):
            return jsonify({
                'status': 'error',
                'message': LanguageService.translate_current('FAVOURITES_VIEW.INVALID_DATA')
            }), 400

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
            return jsonify({
                'status': 'error',
                'message': LanguageService.translate_current('FAVOURITES_VIEW.INVALID_COORDINATES')
            }), 400

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
            return jsonify({
                'status': 'error',
                'message': LanguageService.translate_current('FAVOURITES_VIEW.INVALID_DATA')
            }), 400

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
                'tag': self._favourite_tag_payload(tag) if tag else None
            }
        })

    @settings_transaction
    def delete_favourite(self, favourite_id: str):
        settings = self._settings_storage.load()
        remaining = [item for item in settings.favourites if item.id != favourite_id]

        if len(remaining) == len(settings.favourites):
            return jsonify({
                'status': 'error',
                'message': LanguageService.translate_current('FAVOURITES_VIEW.NOT_FOUND')
            }), 404

        settings.favourites = remaining
        self._settings_storage.save(settings)

        return jsonify({'status': 'ok'})

    def get_favourite_tags(self):
        settings = self._settings_storage.load()

        return jsonify({
            'status': 'ok',
            'tags': [
                self._favourite_tag_payload(tag)
                for tag in settings.favourite_tags
            ]
        })

    @settings_transaction
    def save_favourite_tag(self):
        data = request.get_json(silent=True) or {}
        required = ('name', 'icon')

        if not isinstance(data, dict) or any(key not in data for key in required):
            return jsonify({
                'status': 'error',
                'message': LanguageService.translate_current('FAVOURITE_TAGS_VIEW.INVALID_DATA')
            }), 400

        payload = {
            **data,
            'id': str(data.get('id') or uuid4().hex)
        }

        try:
            tag = FavouriteTag.from_dict(payload)
        except (TypeError, ValueError):
            return jsonify({
                'status': 'error',
                'message': LanguageService.translate_current('FAVOURITE_TAGS_VIEW.INVALID_DATA')
            }), 400

        if not tag.id or not tag.name.strip() or not tag.icon or len(tag.icon) > 16:
            return jsonify({
                'status': 'error',
                'message': LanguageService.translate_current('FAVOURITE_TAGS_VIEW.INVALID_DATA')
            }), 400

        if (
            tag.id == FavouriteTag.DEFAULT_TAG_ID
            and tag.name == LanguageService.translate_current(FavouriteTag.DEFAULT_NAME_KEY)
        ):
            tag.name = FavouriteTag.DEFAULT_NAME_KEY

        settings = self._settings_storage.load()
        settings.favourite_tags = [item for item in settings.favourite_tags if item.id != tag.id]
        settings.favourite_tags.append(tag)
        self._settings_storage.save(settings)

        return jsonify({'status': 'ok', 'tag': self._favourite_tag_payload(tag)})

    @settings_transaction
    def delete_favourite_tag(self, tag_id: str):
        if tag_id == FavouriteTag.DEFAULT_TAG_ID:
            return jsonify({
                'status': 'error',
                'message': LanguageService.translate_current('FAVOURITE_TAGS_VIEW.DEFAULT_DELETE_FORBIDDEN')
            }), 400

        settings = self._settings_storage.load()
        remaining = [item for item in settings.favourite_tags if item.id != tag_id]

        if len(remaining) == len(settings.favourite_tags):
            return jsonify({
                'status': 'error',
                'message': LanguageService.translate_current('FAVOURITE_TAGS_VIEW.NOT_FOUND')
            }), 404

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

    @settings_transaction
    def save_car_profile(self):
        data = request.get_json(silent=True) or {}

        if not isinstance(data, dict):
            return jsonify({
                'status': 'error',
                'message': LanguageService.translate_current('CAR_PROFILES_VIEW.INVALID_DATA')
            }), 400

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
            return jsonify({
                'status': 'error',
                'message': LanguageService.translate_current('CAR_PROFILES_VIEW.INVALID_DATA')
            }), 400

        if not profile.brand.strip() and not profile.model.strip() and not profile.name.strip():
            return jsonify({
                'status': 'error',
                'message': LanguageService.translate_current('CAR_PROFILES_VIEW.REQUIRES_IDENTITY')
            }), 400

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

    @settings_transaction
    def set_active_car_profile(self):
        data = request.get_json(silent=True) or {}
        profile_id = data.get('profile_id') if isinstance(data, dict) else None
        profile_id = str(profile_id) if profile_id else None
        settings = self._settings_storage.load()

        if profile_id and not any(profile.id == profile_id for profile in settings.car_profiles):
            return jsonify({
                'status': 'error',
                'message': LanguageService.translate_current('CAR_PROFILES_VIEW.NOT_FOUND')
            }), 404

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

    @settings_transaction
    def delete_car_profile(self, profile_id: str):
        settings = self._settings_storage.load()
        remaining = [item for item in settings.car_profiles if item.id != profile_id]

        if len(remaining) == len(settings.car_profiles):
            return jsonify({
                'status': 'error',
                'message': LanguageService.translate_current('CAR_PROFILES_VIEW.NOT_FOUND')
            }), 404

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

    @settings_transaction
    def save_route(self):
        data = request.get_json(silent=True) or {}

        if not isinstance(data, dict):
            return jsonify({
                'status': 'error',
                'message': LanguageService.translate_current('ROUTE_ERROR.INVALID_ROUTE_DATA')
            }), 400

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
            return jsonify({
                'status': 'error',
                'message': LanguageService.translate_current('ROUTE_ERROR.INVALID_ROUTE_DATA')
            }), 400

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
            return jsonify({
                'status': 'error',
                'message': LanguageService.translate_current('ROUTE_ERROR.INVALID_ROUTE_DATA')
            }), 400

        for point in route.points:
            if (
                not point.title.strip()
                or not isfinite(point.latitude)
                or not isfinite(point.longitude)
                or not (-90 <= point.latitude <= 90)
                or not (-180 <= point.longitude <= 180)
            ):
                return jsonify({
                    'status': 'error',
                    'message': LanguageService.translate_current('ROUTE_ERROR.INVALID_ROUTE_POINT_DATA')
                }), 400

        settings = self._settings_storage.load()
        settings.routes = [item for item in settings.routes if item.id != route.id]
        settings.routes.append(route)
        self._settings_storage.save(settings)

        return jsonify({
            'status': 'ok',
            'route': route.to_dict()
        })

    @settings_transaction
    def delete_route(self, route_id: str):
        settings = self._settings_storage.load()
        remaining = [item for item in settings.routes if item.id != route_id]

        if len(remaining) == len(settings.routes):
            return jsonify({
                'status': 'error',
                'message': LanguageService.translate_current('ROUTE_ERROR.ROUTE_NOT_FOUND')
            }), 404

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
        if data_type == SettingsTransferTypes.LAYERS:
            return self._settings_storage.export_layers()
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
        if data_type == SettingsTransferTypes.LAYERS:
            self._settings_storage.import_layers(plaintext)
            return
        raise ValueError('Unsupported import data type.')

    #endregion Helpers

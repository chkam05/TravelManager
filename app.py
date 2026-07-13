import base64
import json
import mimetypes
import webbrowser
from pathlib import Path
from time import time, sleep
from threading import Lock
from typing import ClassVar
import socket
import webview

from config import *
from models.settings.favourite_place import FavouritePlace
from models.settings.favourite_tag import FavouriteTag
from models.settings.fuel_cost_cache import FuelCostCache
from models.settings.saved_route import SavedRoute
from models.settings.window_settings import WindowSettings
from core.service import Service
from storage.settings_storage import SettingsStorage
from utils.webview_runtime import WebviewRuntime


class AppApi:
    """API exposed to JavaScript inside the WebView window."""

    _EXPORT_TYPES: ClassVar[dict[str, dict[str, str]]] = {
        'fuel_costs': {
            'filename': 'travel-manager-ceny-paliwa.json',
            'label': 'Ceny paliwa'
        },
        'routes': {
            'filename': 'travel-manager-trasy.json',
            'label': 'Trasy'
        },
        'favourites': {
            'filename': 'travel-manager-ulubione-i-tagi.json',
            'label': 'Ulubione i Tagi'
        }
    }

    def __init__(self, settings_storage: SettingsStorage):
        self._settings_storage = settings_storage

    def open_external_url(self, url: str) -> dict:
        """Opens an external URL in the default system browser."""
        if not isinstance(url, str) or not url.startswith(('http://', 'https://')):
            return {
                'status': 'error',
                'message': 'Unsupported URL.'
            }

        webbrowser.open_new(url)

        return {
            'status': 'opened'
        }

    def save_place_data(self, data: dict, filename: str = 'place-data.json') -> dict:
        """Open a save dialog and persist selected map element data as JSON."""
        window = webview.windows[0] if webview.windows else None

        if not window:
            return {
                'status': 'error',
                'message': 'No active WebView window.'
            }

        save_path = window.create_file_dialog(
            webview.FileDialog.SAVE,
            save_filename=filename,
            file_types=('JSON Files (*.json)',)
        )

        if not save_path:
            return {
                'status': 'cancelled'
            }

        if isinstance(save_path, (list, tuple)):
            save_path = save_path[0] if save_path else None

        if not save_path:
            return {
                'status': 'cancelled'
            }

        path = Path(save_path)

        if path.suffix.lower() != '.json':
            path = path.with_suffix('.json')

        path.write_text(
            json.dumps(data or {}, ensure_ascii=False, indent=2),
            encoding='utf-8'
        )

        return {
            'status': 'saved',
            'path': str(path)
        }

    def export_settings_data(self, data_type: str) -> dict:
        """Open a save dialog and export selected application data as JSON."""
        if data_type not in self._EXPORT_TYPES:
            return {
                'status': 'error',
                'message': 'Unsupported export data type.'
            }

        window = webview.windows[0] if webview.windows else None

        if not window:
            return {
                'status': 'error',
                'message': 'No active WebView window.'
            }

        save_path = window.create_file_dialog(
            webview.FileDialog.SAVE,
            save_filename=self._EXPORT_TYPES[data_type]['filename'],
            file_types=('JSON Files (*.json)',)
        )

        if isinstance(save_path, (list, tuple)):
            save_path = save_path[0] if save_path else None

        if not save_path:
            return {'status': 'cancelled'}

        path = Path(save_path)

        if path.suffix.lower() != '.json':
            path = path.with_suffix('.json')

        payload = self._export_payload(data_type)
        path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2),
            encoding='utf-8'
        )

        return {
            'status': 'saved',
            'path': str(path),
            'type': data_type,
            'label': self._EXPORT_TYPES[data_type]['label']
        }

    def import_settings_data(self, data_type: str) -> dict:
        """Open a file dialog and import selected application data from JSON."""
        if data_type not in self._EXPORT_TYPES:
            return {
                'status': 'error',
                'message': 'Unsupported import data type.'
            }

        window = webview.windows[0] if webview.windows else None

        if not window:
            return {
                'status': 'error',
                'message': 'No active WebView window.'
            }

        selected = window.create_file_dialog(
            webview.FileDialog.OPEN,
            file_types=('JSON Files (*.json)',)
        )

        if isinstance(selected, (list, tuple)):
            selected = selected[0] if selected else None

        if not selected:
            return {'status': 'cancelled'}

        path = Path(selected)

        try:
            payload = json.loads(path.read_text(encoding='utf-8'))
        except (OSError, json.JSONDecodeError):
            return {
                'status': 'error',
                'message': 'Could not read selected JSON file.'
            }

        try:
            counts = self._import_payload(data_type, payload)
        except (TypeError, ValueError):
            return {
                'status': 'error',
                'message': 'Selected JSON does not match the requested data type.'
            }

        return {
            'status': 'imported',
            'path': str(path),
            'type': data_type,
            'label': self._EXPORT_TYPES[data_type]['label'],
            'counts': counts
        }

    def select_car_image(self) -> dict:
        """Open a file dialog and return a selected car image as text."""
        window = webview.windows[0] if webview.windows else None

        if not window:
            return {
                'status': 'error',
                'message': 'No active WebView window.'
            }

        selected = window.create_file_dialog(
            webview.FileDialog.OPEN,
            file_types=(
                'Image Files (*.png;*.jpg;*.jpeg;*.webp)',
                'PNG Files (*.png)',
                'JPEG Files (*.jpg;*.jpeg)',
                'WebP Files (*.webp)'
            )
        )

        if not selected:
            return {'status': 'cancelled'}

        if isinstance(selected, (list, tuple)):
            selected = selected[0] if selected else None

        if not selected:
            return {'status': 'cancelled'}

        path = Path(selected)
        mime_type = mimetypes.guess_type(path.name)[0] or 'application/octet-stream'
        image = f'data:{mime_type};base64,{base64.b64encode(path.read_bytes()).decode("ascii")}'

        return {
            'status': 'selected',
            'image': image,
            'name': path.name
        }

    def _export_payload(self, data_type: str) -> dict:
        """Builds the JSON payload for a selected export type."""
        settings = self._settings_storage.load()

        if data_type == 'fuel_costs':
            data = settings.fuel_cost_cache.to_dict() if settings.fuel_cost_cache else FuelCostCache.from_dict({}).to_dict()
        elif data_type == 'routes':
            data = {
                'routes': SavedRoute.to_dict_list(settings.routes)
            }
        elif data_type == 'favourites':
            data = {
                'favourite_tags': FavouriteTag.to_dict_list(settings.favourite_tags),
                'favourites': FavouritePlace.to_dict_list(settings.favourites)
            }
        else:
            data = {}

        return {
            'application': APP_NAME,
            'version': APP_VERSION,
            'type': data_type,
            'label': self._EXPORT_TYPES[data_type]['label'],
            'data': data
        }

    def _import_payload(self, data_type: str, payload: dict) -> dict:
        """Imports selected data into settings storage."""
        if not isinstance(payload, dict):
            raise ValueError('Invalid JSON root.')

        data = payload.get('data', payload)
        settings = self._settings_storage.load()

        if data_type == 'fuel_costs':
            settings.fuel_cost_cache = FuelCostCache.from_dict(data if isinstance(data, dict) else {})
            counts = {'fuel_costs': len(settings.fuel_cost_cache.data.get('rows', []))}
        elif data_type == 'routes':
            routes = data.get('routes', data) if isinstance(data, dict) else data

            if not isinstance(routes, list):
                raise ValueError('Invalid routes data.')

            settings.routes = SavedRoute.from_dict_list(routes)
            counts = {'routes': len(settings.routes)}
        elif data_type == 'favourites':
            if not isinstance(data, dict):
                raise ValueError('Invalid favourites data.')

            tags = FavouriteTag.from_dict_list(data.get('favourite_tags', []))
            favourites = FavouritePlace.from_dict_list(data.get('favourites', []))
            has_default_tag = any(tag.id == FavouriteTag.DEFAULT_TAG_ID for tag in tags)

            if not has_default_tag:
                tags.insert(0, FavouriteTag.default())

            tag_ids = {tag.id for tag in tags}

            for favourite in favourites:
                if favourite.tag_id not in tag_ids:
                    favourite.tag_id = FavouriteTag.DEFAULT_TAG_ID

            settings.favourite_tags = tags
            settings.favourites = favourites
            counts = {
                'favourite_tags': len(settings.favourite_tags),
                'favourites': len(settings.favourites)
            }
        else:
            raise ValueError('Unsupported import data type.')

        self._settings_storage.save(settings)

        return counts


class App:
    _CONNECTION_TIMEOUT: ClassVar[float] = 0.3
    _CONNECTION_EXCEPTION_TIMEOUT: ClassVar[float] = 0.1

    def __init__(self):
        WebviewRuntime.validate_webview_runtime()

        self._configure_app_metadata()

        self._app_url = f'http://{HOST}:{PORT}'
        self._backend = WebviewRuntime.choose_webview_backend()
        self._app_icon = APP_ICON_WINDOWS if WebviewRuntime.is_windows() else APP_ICON
        self._settings_storage = SettingsStorage()
        self._window_count = 0
        self._window_lock = Lock()
        self._api = AppApi(self._settings_storage)
        self._service = Service(
            HOST,
            PORT,
            settings_storage = self._settings_storage,
            template_folder = TEMPLATE_FOLDER,
            static_folder = STATIC_FOLDER,
            static_url_path = STATIC_URL_PATH
        )

    def _create_window(self):
        settings = self._settings_storage.load()

        with self._window_lock:
            self._window_count += 1

        window = webview.create_window(
            title=APP_NAME,
            url=self._app_url,
            width=settings.window.width,
            height=settings.window.height,
            x=settings.window.x,
            y=settings.window.y,
            js_api=self._api
        )
        window.events.closing += lambda: self._on_window_closing(window)
        window.events.closed += self._on_window_closed

        return window

    def _on_window_closing(self, window):
        try:
            current_settings = self._settings_storage.load()
            current_settings.window = WindowSettings(
                height=window.height,
                x=window.x,
                y=window.y,
                width=window.width
            )
        except Exception:
            return

        self._settings_storage.save(current_settings)

    def _on_window_closed(self):
        with self._window_lock:
            self._window_count -= 1
            has_open_windows = self._window_count > 0

        if not has_open_windows:
            self._service.stop()

    @classmethod
    def _configure_app_metadata(cls):
        if not WebviewRuntime.is_macos():
            return

        try:
            from AppKit import NSBundle
        except ImportError:
            return

        info = NSBundle.mainBundle().infoDictionary()
        info.setObject_forKey_(APP_NAME, 'CFBundleName')
        info.setObject_forKey_(APP_NAME, 'CFBundleDisplayName')

    @classmethod
    def __wait_for_server__(cls, host: str, port: int, timeout: int):
        start = time()

        while time() - start < timeout:
            try:
                with socket.create_connection((host, port), timeout=cls._CONNECTION_TIMEOUT):
                    return True
            except OSError:
                sleep(cls._CONNECTION_EXCEPTION_TIMEOUT)
        
        return False
    
    def startup(self):
        self._service.run_async()
        
        if not self.__wait_for_server__(HOST, PORT, SERVICE_TIMEOUT):
            raise RuntimeError('Flask server failed to start.')
        
        self._create_window()

        try:
            if self._backend:
                webview.start(gui=self._backend, icon=self._app_icon)
            else:
                webview.start(icon=self._app_icon)
        finally:
            self._service.stop()


if __name__ == "__main__":
    App().startup()

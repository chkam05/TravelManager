from __future__ import annotations
import base64
import json
import mimetypes
import webbrowser
from pathlib import Path
from threading import Lock
from typing import Any, Callable

import webview

from config import APP_ICON, APP_ICON_WINDOWS, APP_NAME, PROJECT_ROOT
from core.language_service import LanguageService
from core.webview_window_interface import WebViewWindowInterface
from models.settings.window_settings import WindowSettings
from resources.settings_transfer import SettingsTransferTypes
from storage.settings_storage import SettingsStorage
from utils.webview_runtime import WebviewRuntime


class WebViewWindow(WebViewWindowInterface):
    """Owns the native WebView window and its JavaScript bridge."""

    def __init__(
        self,
        url: str,
        settings_storage: SettingsStorage,
        on_all_windows_closed: Callable[[], None] | None = None,
        forced_locale: str | None = None
    ):
        self._url = url
        self._settings_storage = settings_storage
        self._language_service = LanguageService()
        self._forced_locale = (
            self._language_service.normalize_locale(forced_locale)
            if forced_locale is not None
            else None
        )
        WebviewRuntime.validate_webview_runtime(self._translate)
        self._configure_app_metadata()
        self._on_all_windows_closed = on_all_windows_closed
        self._backend = WebviewRuntime.choose_webview_backend()
        self._icon = APP_ICON_WINDOWS if WebviewRuntime.is_windows() else APP_ICON
        self._window: Any | None = None
        self._window_count = 0
        self._window_lock = Lock()

    #region Lifecycle

    def create(self) -> Any:
        """Creates and configures the native application window."""
        settings = self._settings_storage.load()

        with self._window_lock:
            self._window_count += 1

        self._window = webview.create_window(
            title=APP_NAME,
            url=self._url,
            width=settings.window.width,
            height=settings.window.height,
            x=settings.window.x,
            y=settings.window.y,
            js_api=self
        )
        self._window.events.closing += lambda: self._on_window_closing(self._window)
        self._window.events.closed += self._on_window_closed

        return self._window

    def start(self) -> None:
        """Starts the native WebView event loop."""
        if self._backend:
            webview.start(gui=self._backend, icon=self._icon)
        else:
            webview.start(icon=self._icon)

    def _on_window_closing(self, window: Any) -> None:
        """Persists the current native window geometry."""
        try:
            settings = self._settings_storage.load()
            settings.window = WindowSettings(
                height=window.height,
                x=window.x,
                y=window.y,
                width=window.width
            )
            self._settings_storage.save(settings)
        except Exception:
            return

    def _on_window_closed(self) -> None:
        """Notifies the application after the last window is closed."""
        with self._window_lock:
            self._window_count -= 1
            has_open_windows = self._window_count > 0

        if not has_open_windows and self._on_all_windows_closed:
            self._on_all_windows_closed()

    @classmethod
    def _configure_app_metadata(cls) -> None:
        """Configures native macOS application names."""
        if not WebviewRuntime.is_macos():
            return

        try:
            from AppKit import NSBundle
        except ImportError:
            return

        info = NSBundle.mainBundle().infoDictionary()
        info.setObject_forKey_(APP_NAME, 'CFBundleName')
        info.setObject_forKey_(APP_NAME, 'CFBundleDisplayName')

    #endregion Lifecycle

    #region JavaScript API

    def open_external_url(self, url: str) -> dict[str, str]:
        """Opens an external URL in the default system browser."""
        if not isinstance(url, str) or not url.startswith(('http://', 'https://')):
            return {
                'status': 'error',
                'message': self._translate('NATIVE_APP.UNSUPPORTED_URL')
            }

        webbrowser.open_new(url)
        return {'status': 'opened'}

    def save_place_data(self, data: dict, filename: str = 'place-data.json') -> dict[str, str]:
        """Opens a save dialog and persists selected map element data as JSON."""
        window = self._active_window()
        if not window:
            return {
                'status': 'error',
                'message': self._translate('NATIVE_APP.NO_ACTIVE_WINDOW')
            }

        save_path = self._selected_path(window.create_file_dialog(
            webview.FileDialog.SAVE,
            save_filename=filename,
            file_types=self._json_file_types()
        ))
        if not save_path:
            return {'status': 'cancelled'}

        path = self._json_path(save_path)
        path.write_text(
            json.dumps(data or {}, ensure_ascii=False, indent=2),
            encoding='utf-8'
        )
        return {'status': 'saved', 'path': str(path)}

    def export_settings_data(self, data_type: str) -> dict[str, str]:
        """Opens a save dialog and exports selected application data."""
        if not SettingsTransferTypes.is_supported(data_type):
            return {
                'status': 'error',
                'message': self._translate('SETTINGS_BACKUP.UNSUPPORTED_EXPORT_TYPE')
            }

        window = self._active_window()
        if not window:
            return {
                'status': 'error',
                'message': self._translate('SETTINGS_BACKUP.NO_ACTIVE_WINDOW')
            }

        save_path = self._selected_path(window.create_file_dialog(
            webview.FileDialog.SAVE,
            save_filename=SettingsTransferTypes.file_name(data_type),
            file_types=self._json_file_types()
        ))
        if not save_path:
            return {'status': 'cancelled'}

        path = self._json_path(save_path)
        path.write_text(self._export_settings_text(data_type), encoding='utf-8')
        return {
            'status': 'saved',
            'path': str(path),
            'type': data_type,
            'label': self._translate(SettingsTransferTypes.label_key(data_type))
        }

    def import_settings_data(self, data_type: str) -> dict[str, str]:
        """Opens a file dialog and imports selected application data."""
        if not SettingsTransferTypes.is_supported(data_type):
            return {
                'status': 'error',
                'message': self._translate('SETTINGS_BACKUP.UNSUPPORTED_IMPORT_TYPE')
            }

        window = self._active_window()
        if not window:
            return {
                'status': 'error',
                'message': self._translate('SETTINGS_BACKUP.NO_ACTIVE_WINDOW')
            }

        selected = self._selected_path(window.create_file_dialog(
            webview.FileDialog.OPEN,
            file_types=self._json_file_types()
        ))
        if not selected:
            return {'status': 'cancelled'}

        path = Path(selected)
        try:
            plaintext = path.read_text(encoding='utf-8')
            self._import_settings_text(data_type, plaintext)
        except (OSError, TypeError, ValueError, json.JSONDecodeError):
            return {
                'status': 'error',
                'message': self._translate('SETTINGS_BACKUP.INVALID_IMPORT_FILE')
            }

        return {
            'status': 'imported',
            'path': str(path),
            'type': data_type,
            'label': self._translate(SettingsTransferTypes.label_key(data_type))
        }

    def select_car_image(self) -> dict[str, str]:
        """Opens a file dialog and returns a selected car image as text."""
        window = self._active_window()
        if not window:
            return {
                'status': 'error',
                'message': self._translate('NATIVE_APP.NO_ACTIVE_WINDOW')
            }

        selected = self._selected_path(window.create_file_dialog(
            webview.FileDialog.OPEN,
            file_types=self._image_file_types()
        ))
        if not selected:
            return {'status': 'cancelled'}

        path = Path(selected)
        mime_type = mimetypes.guess_type(path.name)[0] or 'application/octet-stream'
        image = f'data:{mime_type};base64,{base64.b64encode(path.read_bytes()).decode("ascii")}'
        return {'status': 'selected', 'image': image, 'name': path.name}

    #endregion JavaScript API

    #region Helpers

    def _active_window(self) -> Any | None:
        """Returns the window owned by this instance when it is active."""
        return self._window

    def _translate(self, key: str, **parameters: object) -> str:
        """Translates a native bridge message using the effective UI locale."""
        locale = self._forced_locale or self._settings_storage.load().ui.language
        return self._language_service.translate(key, locale, parameters)

    def _json_file_types(self) -> tuple[str, ...]:
        """Returns a localized native JSON file filter."""
        return (self._translate('NATIVE_APP.JSON_FILES'),)

    def _image_file_types(self) -> tuple[str, ...]:
        """Returns localized native image file filters."""
        return (
            self._translate('NATIVE_APP.IMAGE_FILES'),
            self._translate('NATIVE_APP.PNG_FILES'),
            self._translate('NATIVE_APP.JPEG_FILES'),
            self._translate('NATIVE_APP.WEBP_FILES')
        )

    @staticmethod
    def _selected_path(selected: Any) -> str | None:
        """Normalizes pywebview dialog results to a single path."""
        if isinstance(selected, (list, tuple)):
            return str(selected[0]) if selected else None
        return str(selected) if selected else None

    @staticmethod
    def _json_path(path: str) -> Path:
        """Ensures that an exported path has a JSON extension."""
        result = Path(path)
        return result if result.suffix.lower() == '.json' else result.with_suffix('.json')

    def _export_settings_text(self, data_type: str) -> str:
        """Calls the explicit settings exporter assigned to a transfer type."""
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
        """Calls the explicit settings importer assigned to a transfer type."""
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

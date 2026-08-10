import socket
import sys
from time import sleep, time
from typing import ClassVar

from config import (
    HOST,
    PORT,
    SERVICE_TIMEOUT,
    STATIC_FOLDER,
    STATIC_URL_PATH,
    TEMPLATE_FOLDER
)

from core.language_service import LanguageService
from core.service import Service
from core.webview_window import WebViewWindow
from core.webview_window_interface import WebViewWindowInterface
from storage.settings_storage import SettingsStorage
from utils.command_line_manager import CommandLineManager
from utils.network_utils import NetworkUtils


class App:
    """Coordinates the local service and native application window."""

    _CONNECTION_TIMEOUT: ClassVar[float] = 0.3
    _CONNECTION_EXCEPTION_TIMEOUT: ClassVar[float] = 0.1

    def __init__(
        self,
        webview_window: WebViewWindowInterface | None = None,
        ip: str | None = None,
        port: int | None = None,
        no_window: bool = False,
        locale: str | None = None
    ):
        self._settings_storage = SettingsStorage()
        settings = self._settings_storage.load()
        self._forced_locale = (
            LanguageService.normalize_locale(locale)
            if locale is not None
            else None
        )
        self._locale = self._forced_locale or LanguageService.normalize_locale(
            settings.ui.language
        )
        network_ip = (
            NetworkUtils.get_local_ip()
            if ip is None and settings.ui.move_to_network
            else None
        )
        self._host = ip or network_ip or HOST
        self._port = port if port is not None else PORT
        self._no_window = no_window
        self._app_url = f'http://{self._host}:{self._port}'
        self._service = Service(
            self._host,
            self._port,
            settings_storage=self._settings_storage,
            forced_locale=self._forced_locale,
            template_folder=TEMPLATE_FOLDER,
            static_folder=STATIC_FOLDER,
            static_url_path=STATIC_URL_PATH
        )
        self._webview_window = webview_window
        if not self._no_window and self._webview_window is None:
            self._webview_window = WebViewWindow(
                url=self._app_url,
                settings_storage=self._settings_storage,
                on_all_windows_closed=self._service.stop,
                forced_locale=self._forced_locale
            )

    @classmethod
    def __wait_for_server__(cls, host: str, port: int, timeout: int) -> bool:
        """Waits until the local application service accepts connections."""
        start = time()

        while time() - start < timeout:
            try:
                with socket.create_connection((host, port), timeout=cls._CONNECTION_TIMEOUT):
                    return True
            except OSError:
                sleep(cls._CONNECTION_EXCEPTION_TIMEOUT)

        return False

    def startup(self) -> None:
        """Starts the local service and native WebView application."""
        if self._no_window:
            self._print_console(
                CommandLineManager.translate(
                    'CLI.SERVER_RUNNING', self._locale, url=self._app_url
                )
            )
            self._print_console(
                CommandLineManager.translate('CLI.PRESS_CTRL_C', self._locale)
            )
            try:
                self._service.run()
            except KeyboardInterrupt:
                self._print_console(
                    '\n' + CommandLineManager.translate(
                        'CLI.STOPPING_SERVER', self._locale
                    )
                )
            finally:
                self._service.stop()
            return

        self._service.run_async()

        if not self.__wait_for_server__(self._host, self._port, SERVICE_TIMEOUT):
            self._service.stop()
            raise RuntimeError(CommandLineManager.translate(
                'CLI.SERVER_START_FAILED', self._locale
            ))

        if self._webview_window is None:
            raise RuntimeError(CommandLineManager.translate(
                'CLI.WINDOW_NOT_CONFIGURED', self._locale
            ))

        self._webview_window.create()

        try:
            self._webview_window.start()
        finally:
            self._service.stop()

    @staticmethod
    def _print_console(message: str) -> None:
        """Writes a status message when a console is available."""
        if sys.stdout is not None:
            print(message, flush=True)


if __name__ == '__main__':
    CommandLineManager.prepare_console()
    arguments = CommandLineManager.parse_arguments()
    App(
        ip=arguments.ip,
        port=arguments.port,
        no_window=arguments.no_window,
        locale=CommandLineManager.language_locale(arguments.language)
    ).startup()

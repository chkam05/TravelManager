import socket
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

from core.service import Service
from core.webview_window import WebViewWindow
from core.webview_window_interface import WebViewWindowInterface
from storage.settings_storage import SettingsStorage


class App:
    """Coordinates the local service and native application window."""

    _CONNECTION_TIMEOUT: ClassVar[float] = 0.3
    _CONNECTION_EXCEPTION_TIMEOUT: ClassVar[float] = 0.1

    def __init__(self, webview_window: WebViewWindowInterface | None = None):
        self._settings_storage = SettingsStorage()
        self._service = Service(
            HOST,
            PORT,
            settings_storage=self._settings_storage,
            template_folder=TEMPLATE_FOLDER,
            static_folder=STATIC_FOLDER,
            static_url_path=STATIC_URL_PATH
        )
        self._webview_window = webview_window or WebViewWindow(
            url=f'http://{HOST}:{PORT}',
            settings_storage=self._settings_storage,
            on_all_windows_closed=self._service.stop
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
        self._service.run_async()

        if not self.__wait_for_server__(HOST, PORT, SERVICE_TIMEOUT):
            self._service.stop()
            raise RuntimeError('Flask server failed to start.')

        self._webview_window.create()

        try:
            self._webview_window.start()
        finally:
            self._service.stop()


if __name__ == '__main__':
    App().startup()

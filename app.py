import argparse
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

from core.service import Service
from core.webview_window import WebViewWindow
from core.webview_window_interface import WebViewWindowInterface
from storage.settings_storage import SettingsStorage
from utils.network_utils import NetworkUtils


def _ipv4_argument(value: str) -> str:
    """Validates an IPv4 command-line argument."""
    try:
        return NetworkUtils.normalize_ipv4(value)
    except (TypeError, ValueError) as error:
        raise argparse.ArgumentTypeError(str(error)) from error


def _port_argument(value: str) -> int:
    """Validates a TCP port command-line argument."""
    try:
        port = int(value)
    except ValueError as error:
        raise argparse.ArgumentTypeError('Port musi być liczbą całkowitą.') from error

    if not 1 <= port <= 65535:
        raise argparse.ArgumentTypeError('Port musi mieścić się w zakresie 1–65535.')

    return port


def create_argument_parser() -> argparse.ArgumentParser:
    """Creates a parser supporting Unix and Windows-style options."""
    parser = argparse.ArgumentParser(
        description='Uruchamia aplikację Travel Manager.',
        add_help=False,
        prefix_chars='-/'
    )
    parser.add_argument(
        '--ip', '/ip',
        type=_ipv4_argument,
        help='Adres IPv4, pod którym serwer ma nasłuchiwać.'
    )
    parser.add_argument(
        '--port', '/port',
        type=_port_argument,
        help='Port serwera z zakresu 1–65535.'
    )
    parser.add_argument(
        '--no-window', '/no-window',
        action='store_true',
        help='Uruchom wyłącznie serwer, bez okna WebView.'
    )
    parser.add_argument(
        '-h', '--help', '/h', '/help',
        action='help',
        help='Pokaż ten komunikat pomocy i zakończ.'
    )
    return parser


def prepare_cli_console() -> None:
    """Attaches windowed builds to a terminal when CLI options are used."""
    if len(sys.argv) <= 1 or (sys.stdout is not None and sys.stderr is not None):
        return

    if sys.platform == 'win32':
        try:
            import ctypes

            kernel32 = ctypes.windll.kernel32
            if not kernel32.AttachConsole(-1):
                kernel32.AllocConsole()
            kernel32.SetConsoleCtrlHandler(None, False)
            sys.stdin = open('CONIN$', 'r', encoding='utf-8')
            sys.stdout = open('CONOUT$', 'w', encoding='utf-8', buffering=1)
            sys.stderr = open('CONOUT$', 'w', encoding='utf-8', buffering=1)
        except (OSError, AttributeError):
            return
        return

    try:
        sys.stdin = open('/dev/tty', 'r', encoding='utf-8')
        sys.stdout = open('/dev/tty', 'w', encoding='utf-8', buffering=1)
        sys.stderr = open('/dev/tty', 'w', encoding='utf-8', buffering=1)
    except OSError:
        return


class App:
    """Coordinates the local service and native application window."""

    _CONNECTION_TIMEOUT: ClassVar[float] = 0.3
    _CONNECTION_EXCEPTION_TIMEOUT: ClassVar[float] = 0.1

    def __init__(
        self,
        webview_window: WebViewWindowInterface | None = None,
        ip: str | None = None,
        port: int | None = None,
        no_window: bool = False
    ):
        self._settings_storage = SettingsStorage()
        settings = self._settings_storage.load()
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
            template_folder=TEMPLATE_FOLDER,
            static_folder=STATIC_FOLDER,
            static_url_path=STATIC_URL_PATH
        )
        self._webview_window = webview_window
        if not self._no_window and self._webview_window is None:
            self._webview_window = WebViewWindow(
                url=self._app_url,
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
        if self._no_window:
            self._print_console(
                f'Serwer aplikacji działa pod adresem: {self._app_url}'
            )
            self._print_console('Naciśnij Ctrl+C, aby go zatrzymać.')
            try:
                self._service.run()
            except KeyboardInterrupt:
                self._print_console('\nZatrzymywanie serwera…')
            finally:
                self._service.stop()
            return

        self._service.run_async()

        if not self.__wait_for_server__(self._host, self._port, SERVICE_TIMEOUT):
            self._service.stop()
            raise RuntimeError('Flask server failed to start.')

        if self._webview_window is None:
            raise RuntimeError('WebView window is not configured.')

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
    prepare_cli_console()
    arguments = create_argument_parser().parse_args()
    App(
        ip=arguments.ip,
        port=arguments.port,
        no_window=arguments.no_window
    ).startup()

from pathlib import Path

from utils.path_utils import PathUtils


# Main application resource directories.
PROJECT_ROOT = Path(__file__).resolve().parent

APP_ICON = str(PROJECT_ROOT / 'assets' / 'icons' / 'favicon.png')
APP_ICON_WINDOWS = str(PROJECT_ROOT / 'assets' / 'icons' / 'favicon.ico')
STATIC_FOLDER = str(PROJECT_ROOT / 'assets')
STATIC_URL_PATH = '/assets'
TEMPLATE_FOLDER = str(PROJECT_ROOT / 'templates')

# Application and package informations.
APP_NAME = 'Travel Manager'
APP_AUTHOR = 'Kamil Karpiński'
APP_DESCRIPTION = (
    'Aplikacja desktopowa do przeglądania map OpenStreetMap, wyszukiwania miejsc, '
    'planowania i zapisywania tras oraz szacowania kosztów podróży na podstawie '
    'profili samochodów i aktualnych cen paliw.'
)
APP_VERSION = '1.0.0.0'

# Application settings storage.
SETTINGS_DIR = PathUtils.get_settings_dir(APP_NAME)
SETTINGS_FILE_NAME = 'settings.json'

# Backend service configuration.
HOST = '127.0.0.1'
PORT = 5000
SERVICE_TIMEOUT = 10

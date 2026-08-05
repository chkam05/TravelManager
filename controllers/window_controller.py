from typing import ClassVar
from flask import render_template

from config import APP_AUTHOR, APP_NAME, APP_VERSION
from core.api.base_controller import BaseController
from resources.menu import Menu
from storage.settings_storage import SettingsStorage


class WindowController(BaseController):
    CONTROLLER_NAME: ClassVar[str] = 'WindowController'

    def __init__(self, app_url: str, settings_storage: SettingsStorage):
        self._app_url = app_url
        self._settings_storage = settings_storage
        super().__init__()
    
    def register_routes(self):
        self.add_url_rule('/', view_func=self.index, methods=['GET'])
    
    # --- ENDPOINTS ---

    def index(self):
        settings = self._settings_storage.load()
        initial_view = 'home' if settings.ui.open_home_on_startup else 'map'
        appearance = settings.appearance

        return render_template(
            'index/index.html',
            app_name=APP_NAME,
            app_version=APP_VERSION,
            app_copyright=f'Copyright (c) {APP_AUTHOR}',
            app_url=self._app_url,
            menu_sections=Menu.menu_sections(),
            initial_view=initial_view,
            appearance=appearance
        )

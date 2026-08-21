from typing import ClassVar
from flask import abort, render_template, send_file, url_for

from config import APP_NAME
from core.api.base_controller import BaseController
from resources.menu import Menu
from resources.language_definitions import LANGUAGE_DEFINITIONS
from resources.language_enum import Language
from storage.settings_storage import SettingsStorage


class WindowController(BaseController):
    CONTROLLER_NAME: ClassVar[str] = 'WindowController'

    def __init__(self, settings_storage: SettingsStorage):
        self._settings_storage = settings_storage
        super().__init__()
    
    def register_routes(self):
        self.add_url_rule('/', view_func=self.index, methods=['GET'])
        self.add_url_rule(
            '/api/languages/<locale>',
            view_func=self.language_catalog,
            methods=['GET']
        )
    
    # --- ENDPOINTS ---

    def index(self):
        settings = self._settings_storage.load()
        initial_view = 'home' if settings.ui.open_home_on_startup else 'map'
        appearance = settings.appearance
        languages = [
            {
                'locale': language.value,
                'label_key': language.label_key,
                'catalog_url': url_for(
                    f'{self.CONTROLLER_NAME}.language_catalog',
                    locale=language.value
                )
            }
            for language in LANGUAGE_DEFINITIONS
        ]

        return render_template(
            'index/index.html',
            app_name=APP_NAME,
            menu_sections=Menu.menu_sections(),
            initial_view=initial_view,
            appearance=appearance,
            language=settings.ui.language,
            languages=languages
        )

    def language_catalog(self, locale: str):
        """Serves a registered language catalog to the browser."""
        try:
            language = Language(locale)
            path = LANGUAGE_DEFINITIONS[language]
        except (KeyError, ValueError):
            abort(404)

        return send_file(path, mimetype='application/json', conditional=True)

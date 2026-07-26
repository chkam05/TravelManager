from typing import ClassVar
from flask import render_template

from config import APP_AUTHOR, APP_DESCRIPTION, APP_NAME, APP_VERSION, HOST, PORT
from core.api.base_controller import BaseController
from resources.emojis import Emojis


class ViewController(BaseController):
    CONTROLLER_NAME: ClassVar[str] = 'ViewController'

    def register_routes(self):
        self.add_url_rule('/api/views/map', view_func=self.map_view, methods=['GET'])
        self.add_url_rule('/api/views/favourites', view_func=self.favourites_view, methods=['GET'])
        self.add_url_rule('/api/views/favourites-tags', view_func=self.favourites_tags_view, methods=['GET'])
        self.add_url_rule('/api/views/car-profiles', view_func=self.car_profiles_view, methods=['GET'])
        self.add_url_rule('/api/views/my-routes', view_func=self.my_routes_view, methods=['GET'])
        self.add_url_rule('/api/views/fuel-cost', view_func=self.fuel_cost_view, methods=['GET'])
        self.add_url_rule('/api/views/settings', view_func=self.settings_view, methods=['GET'])
        self.add_url_rule('/api/views/information', view_func=self.information_view, methods=['GET'])
        self.add_url_rule('/api/panels/legend-details', view_func=self.legend_details_panel, methods=['GET'])
        self.add_url_rule('/api/panels/layer-details', view_func=self.layer_details_panel, methods=['GET'])
        self.add_url_rule('/api/panels/place-details', view_func=self.place_details_panel, methods=['GET'])
        self.add_url_rule('/api/panels/route-details', view_func=self.route_details_panel, methods=['GET'])
        self.add_url_rule('/api/panels/car-details', view_func=self.car_details_panel, methods=['GET'])
        self.add_url_rule('/api/panels/search-results', view_func=self.search_results_panel, methods=['GET'])
        self.add_url_rule('/api/dialogs/yesno', view_func=self.yesno_dialog, methods=['GET'])
        self.add_url_rule('/api/dialogs', view_func=self.dialogs, methods=['GET'])
        self.add_url_rule('/api/emojis/groups', view_func=Emojis.emoji_groups, methods=['GET'])
        self.add_url_rule('/api/emojis', view_func=Emojis.emojis, methods=['GET'])

    # --- ENDPOINTS ---

    def map_view(self):
        return render_template('views/map.html')

    def favourites_view(self):
        return render_template('views/favourites.html')

    def favourites_tags_view(self):
        return render_template('views/favourites_tags.html')

    def car_profiles_view(self):
        return render_template('views/car_profiles.html')

    def my_routes_view(self):
        return render_template('views/my_routes.html')

    def fuel_cost_view(self):
        return render_template('views/fuel_cost.html')

    def settings_view(self):
        return render_template('views/settings.html')

    def information_view(self):
        return render_template(
            'views/information.html',
            app_name=APP_NAME,
            app_author=f'Copyright (C) {APP_AUTHOR}',
            app_description=APP_DESCRIPTION,
            app_version=APP_VERSION,
            app_url=f'http://{HOST}:{PORT}'
        )

    def legend_details_panel(self):
        return render_template('panels/legend_details.html')

    def layer_details_panel(self):
        return render_template('panels/layer_details.html')

    def place_details_panel(self):
        return render_template('panels/place_details.html')

    def route_details_panel(self):
        return render_template('panels/route_details.html')

    def car_details_panel(self):
        return render_template('panels/car_details.html')

    def search_results_panel(self):
        return render_template('panels/search_results.html')

    def yesno_dialog(self):
        return render_template('dialogs/yesno_dialog.html')

    def dialogs(self):
        return render_template('dialogs/dialogs.html')

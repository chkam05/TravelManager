from typing import ClassVar
from flask import jsonify, render_template, request

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
        self.add_url_rule('/api/emojis/groups', view_func=self.emoji_groups, methods=['GET'])
        self.add_url_rule('/api/emojis', view_func=self.emojis, methods=['GET'])

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

    def emoji_groups(self):
        response = jsonify({
            'status': 'ok',
            'groups': [
                {
                    'key': group_key,
                    'name': Emojis.get_group_name(group_key),
                    'label': Emojis.get_group_name(group_key),
                    'emoji': Emojis.get_group_first_symbol(group_key),
                    'support_color': Emojis.supports_color(group_key),
                    'support_sex': Emojis.supports_sex(group_key)
                }
                for group_key in Emojis.groups()
            ]
        })
        response.headers['Cache-Control'] = 'no-store'

        return response

    def emojis(self):
        group_key = request.args.get('group', Emojis.groups()[0])
        group_name = Emojis.get_group_name(group_key)

        response = jsonify({
            'status': 'ok',
            'group': {
                'key': group_key,
                'name': group_name,
                'label': group_name,
                'support_color': Emojis.supports_color(group_key),
                'support_sex': Emojis.supports_sex(group_key)
            },
            'emojis': [
                {
                    'key': key,
                    'name': data.get(Emojis.FIELD_NAME, key),
                    'label': data.get(Emojis.FIELD_NAME, key),
                    'emoji': data.get(Emojis.FIELD_SYMBOL, ''),
                    'support_color': bool(data.get(Emojis.FIELD_SUPPORT_COLOR)),
                    'support_sex': bool(data.get(Emojis.FIELD_SUPPORT_SEX)),
                    'supports_skin_tone': bool(data.get(Emojis.FIELD_SUPPORT_COLOR)),
                    'supports_gender': bool(data.get(Emojis.FIELD_SUPPORT_SEX))
                }
                for key, data in Emojis.get_group(group_key).items()
            ]
        })
        response.headers['Cache-Control'] = 'no-store'

        return response

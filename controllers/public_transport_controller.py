from __future__ import annotations
from collections import defaultdict
from datetime import date
from threading import Lock
from time import monotonic
from typing import Any, Callable, ClassVar

from flask import jsonify, render_template, request

from core.api.base_controller import BaseController
from resources.public_transport.public_transport_providers import PublicTransportProviders
from resources.public_transport.public_transport_translation import PublicTransportTranslation
from resources.public_transport.public_transport_type import PublicTransportType
from storage.settings_storage import SettingsStorage


class PublicTransportController(BaseController):
    """Renders public transport fragments backed by registered downloaders."""

    CONTROLLER_NAME: ClassVar[str] = 'PublicTransportController'
    _CACHE_TTL_SECONDS: ClassVar[int] = 300

    def __init__(self, settings_storage: SettingsStorage):
        self._settings_storage = settings_storage
        self._cache: dict[str, tuple[float, Any]] = {}
        self._stop_progress: dict[str, dict[str, Any]] = {}
        self._cache_lock = Lock()
        super().__init__()

    def register_routes(self):
        self.add_url_rule(
            '/api/public-transport/<provider_id>/lines',
            view_func=self.lines,
            methods=['GET']
        )
        self.add_url_rule(
            '/api/public-transport/<provider_id>/stops',
            view_func=self.stops,
            methods=['GET']
        )
        self.add_url_rule(
            '/api/public-transport/<provider_id>/stops-progress',
            view_func=self.stops_progress,
            methods=['GET']
        )
        self.add_url_rule(
            '/api/public-transport/<provider_id>/line',
            view_func=self.line_view,
            methods=['GET']
        )
        self.add_url_rule(
            '/api/public-transport/<provider_id>/line-stop',
            view_func=self.line_stop,
            methods=['GET']
        )
        self.add_url_rule(
            '/api/public-transport/<provider_id>/ride',
            view_func=self.ride,
            methods=['GET']
        )
        self.add_url_rule(
            '/api/public-transport/<provider_id>/stop-lines',
            view_func=self.stop_lines,
            methods=['GET']
        )

    #region Endpoints

    def lines(self, provider_id: str):
        """Renders the line tile view."""
        return self._render(provider_id, lambda downloader: render_template(
            'public_transport/lines.html',
            groups=self._line_groups(self._load_lines(provider_id, downloader))
        ))

    def stops(self, provider_id: str):
        """Renders the grouped stop list view."""
        return self._render(provider_id, lambda downloader: render_template(
            'public_transport/stops.html',
            city_groups=self._stop_groups(self._load_stops(provider_id, downloader))
        ))

    def stops_progress(self, provider_id: str):
        """Returns the current city download progress for a provider."""
        try:
            PublicTransportProviders.downloader(provider_id)
        except ValueError as error:
            return jsonify({'error': str(error)}), 400
        with self._cache_lock:
            progress = dict(self._stop_progress.get(provider_id, {
                'status': 'idle',
                'city': '',
                'current': 0,
                'total': 0
            }))
        return jsonify(progress)

    def line_view(self, provider_id: str):
        """Renders directions and announcements for one line."""
        return self._render_url(provider_id, lambda downloader, url: (
            lambda model: render_template(
                'public_transport/line_view.html',
                line=model,
                date_options=self._date_options(model.dates)
            )
        )(self._cached(
            f'{provider_id}:line:{url}',
            lambda: downloader.download_line(url)
        )))

    def line_stop(self, provider_id: str):
        """Renders departures for one line, stop and direction."""
        return self._render_url(provider_id, lambda downloader, url: (
            lambda model: render_template(
                'public_transport/line_stop.html',
                timetable=model,
                timetable_days=sorted(model.timetable.items()),
                date_options=self._date_options(model.dates)
            )
        )(self._cached(
            f'{provider_id}:line-stop:{url}',
            lambda: downloader.download_line_stop_timetable(url)
        )))

    def ride(self, provider_id: str):
        """Renders one complete ride table."""
        return self._render_url(provider_id, lambda downloader, url: (
            lambda model: render_template(
                'public_transport/ride.html',
                ride=model,
                route_points=self._ride_route_points(model)
            )
        )(self._cached(
                f'{provider_id}:ride:{url}',
                lambda: downloader.download_ride(url)
            )))

    def stop_lines(self, provider_id: str):
        """Renders all lines serving one platform."""
        return self._render_url(provider_id, lambda downloader, url: (
            lambda model: render_template(
                'public_transport/stop_lines.html',
                stop=model
            )
        )(self._cached(
                f'{provider_id}:stop-lines:{url}',
                lambda: downloader.download_stop_all(url)
        )))

    #endregion Endpoints

    #region Rendering

    def _render(self, provider_id: str, renderer: Callable):
        """Runs a provider renderer and returns a consistent error fragment."""
        try:
            downloader = PublicTransportProviders.downloader(provider_id)
            return renderer(downloader)
        except ValueError as error:
            return render_template(
                'public_transport/error.html',
                message=str(error)
            ), 400
        except Exception as error:
            return render_template(
                'public_transport/error.html',
                message=f'Nie udało się pobrać danych komunikacji miejskiej: {error}'
            ), 502

    def _render_url(self, provider_id: str, renderer: Callable):
        """Validates the requested provider URL before rendering details."""
        def render_for_provider(downloader):
            url = PublicTransportProviders.validate_url(
                provider_id,
                str(request.args.get('url') or '')
            )
            return renderer(downloader, url)
        return self._render(provider_id, render_for_provider)

    def _cached(
        self,
        key: str,
        loader: Callable[[], Any],
        refresh: bool = False
    ) -> Any:
        """Returns a cached model unless an explicit refresh was requested."""
        if not refresh:
            with self._cache_lock:
                cached = self._cache.get(key)
                if cached and monotonic() - cached[0] < self._CACHE_TTL_SECONDS:
                    return cached[1]
        value = loader()
        with self._cache_lock:
            self._cache[key] = (monotonic(), value)
        return value

    def _download_stops(self, provider_id: str, downloader) -> Any:
        """Downloads stops while publishing real city-level progress."""
        self._set_stop_progress(provider_id, 'downloading', '', 0, 0)
        progress = {'current': 0, 'total': 0}

        def update(current: int, total: int, city: str) -> None:
            progress['current'] = current
            progress['total'] = total
            self._set_stop_progress(
                provider_id,
                'downloading',
                city,
                current,
                total
            )

        try:
            stops = downloader.download_stops(progress_callback=update)
        except Exception:
            self._set_stop_progress(provider_id, 'error', '', 0, 0)
            raise
        self._set_stop_progress(
            provider_id,
            'complete',
            '',
            progress['current'],
            progress['total']
        )
        return stops

    def _load_lines(self, provider_id: str, downloader) -> Any:
        """Loads persistent lines or refreshes them explicitly."""
        cache = self._settings_storage.load_public_transport_cache(provider_id)
        if cache and cache.lines and not self._refresh_requested():
            return cache.lines

        lines = downloader.download_lines()
        self._settings_storage.save_public_transport_lines(provider_id, lines)
        return lines

    def _load_stops(self, provider_id: str, downloader) -> Any:
        """Loads persistent stops or refreshes them explicitly."""
        cache = self._settings_storage.load_public_transport_cache(provider_id)
        if cache and cache.stops and not self._refresh_requested():
            if not any(
                platform.latitude is not None and platform.longitude is not None
                for stop in cache.stops
                for platform in stop.platforms
            ):
                stops = downloader.enrich_stop_locations(cache.stops)
                self._settings_storage.save_public_transport_stops(
                    provider_id,
                    stops
                )
                return stops
            return cache.stops

        stops = self._download_stops(provider_id, downloader)
        self._settings_storage.save_public_transport_stops(provider_id, stops)
        return stops

    def _set_stop_progress(
        self,
        provider_id: str,
        status: str,
        city: str,
        current: int,
        total: int
    ) -> None:
        """Stores one immutable snapshot of stop download progress."""
        with self._cache_lock:
            self._stop_progress[provider_id] = {
                'status': status,
                'city': city,
                'current': current,
                'total': total
            }

    @staticmethod
    def _refresh_requested() -> bool:
        """Returns whether the caller requested bypassing the view cache."""
        return request.args.get('refresh') == '1'

    @staticmethod
    def _date_options(
        dates: dict[date, str],
        screen: str = ''
    ) -> list[dict[str, str]]:
        """Converts date links to select-compatible dictionaries."""
        return [
            {
                'date': key.isoformat(),
                'label': key.strftime('%d.%m.%Y'),
                'url': value,
                'screen': screen
            }
            for key, value in sorted(dates.items())
        ]

    @staticmethod
    def _ride_route_points(ride) -> list[dict[str, float]]:
        """Builds an ordered map path from geolocated ride stops."""
        points = []
        if ride.latitude is not None and ride.longitude is not None:
            points.append({
                'latitude': ride.latitude,
                'longitude': ride.longitude
            })
        points.extend({
            'latitude': stop.latitude,
            'longitude': stop.longitude
        } for stop in ride.next_stops if (
            stop.latitude is not None and stop.longitude is not None
        ))
        return points

    @staticmethod
    def _line_groups(lines) -> list[dict[str, Any]]:
        """Groups base lines in the fixed vehicle-type display order."""
        return [
            {
                'type': transport_type,
                'label': PublicTransportTranslation.get(transport_type),
                'lines': [line for line in lines if line.type == transport_type]
            }
            for transport_type in (
                PublicTransportType.TRAM,
                PublicTransportType.TROLLEY,
                PublicTransportType.BUS
            )
            if any(line.type == transport_type for line in lines)
        ]

    @staticmethod
    def _stop_groups(stops) -> list[dict[str, Any]]:
        """Groups stops by city while preserving typed stop models."""
        grouped = defaultdict(list)
        for stop in sorted(stops, key=lambda item: (item.city.name, item.name)):
            grouped[stop.city.name].append(stop)
        return [
            {'city': city, 'stops': city_stops}
            for city, city_stops in grouped.items()
        ]

    #endregion Rendering

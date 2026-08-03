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
from utils.public_transport.download_progress import PublicTransportDownloadProgress


class PublicTransportController(BaseController):
    """Renders public transport fragments backed by registered downloaders."""

    CONTROLLER_NAME: ClassVar[str] = 'PublicTransportController'
    _CACHE_TTL_SECONDS: ClassVar[int] = 300

    def __init__(self, settings_storage: SettingsStorage):
        self._settings_storage = settings_storage
        self._settings_storage.remove_public_transport_caches(
            PublicTransportProviders.providers_without_settings_cache()
        )
        self._cache: dict[str, tuple[float, Any]] = {}
        self._download_progress: dict[str, dict[str, Any]] = {}
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
            '/api/public-transport/<provider_id>/progress',
            view_func=self.download_progress,
            methods=['GET']
        )
        self.add_url_rule(
            '/api/public-transport/<provider_id>/availability',
            view_func=self.availability,
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
        self.add_url_rule(
            '/api/public-transport/<provider_id>/announcement',
            view_func=self.announcement,
            methods=['GET']
        )
        self.add_url_rule(
            '/api/public-transport/<provider_id>/vehicles',
            view_func=self.vehicle_positions,
            methods=['GET']
        )

    #region Endpoints

    def lines(self, provider_id: str):
        """Renders the line tile view."""
        return self._render(provider_id, lambda downloader: render_template(
            'public_transport/lines.html',
            groups=self._line_groups(self._load_lines(provider_id, downloader)),
            capabilities=PublicTransportProviders.capabilities(provider_id)
        ))

    def stops(self, provider_id: str):
        """Renders the grouped stop list view."""
        return self._render(provider_id, lambda downloader: render_template(
            'public_transport/stops.html',
            city_groups=self._stop_groups(self._load_stops(provider_id, downloader)),
            capabilities=PublicTransportProviders.capabilities(provider_id)
        ))

    def download_progress(self, provider_id: str):
        """Returns the current download progress for a provider."""
        try:
            PublicTransportProviders.downloader(provider_id)
        except ValueError as error:
            return jsonify({'error': str(error)}), 400
        with self._cache_lock:
            progress = dict(self._download_progress.get(provider_id, {
                'status': 'idle',
                'item': '',
                'current': 0,
                'total': 0,
                'attempt': 1,
                'max_attempts': PublicTransportDownloadProgress.MAX_ATTEMPTS
            }))
        return jsonify(progress)

    def availability(self, provider_id: str):
        """Returns whether the provider already has persistent local data."""
        try:
            downloader = PublicTransportProviders.downloader(provider_id)
            if PublicTransportProviders.uses_settings_cache(provider_id):
                cache = self._settings_storage.load_public_transport_cache(provider_id)
                available = bool(cache and cache.lines)
            else:
                available = bool(getattr(downloader, 'has_local_data', lambda: False)())
            return jsonify({'available': available})
        except ValueError as error:
            return jsonify({'error': str(error)}), 400

    def stops_progress(self, provider_id: str):
        """Keeps compatibility with the original stop progress endpoint."""
        return self.download_progress(provider_id)

    def line_view(self, provider_id: str):
        """Renders directions and announcements for one line."""
        return self._render_url(provider_id, lambda downloader, url: (
            lambda model: render_template(
                'public_transport/line_view.html',
                line=model,
                route_points=self._line_route_points(model),
                routes_by_direction=self._line_routes_by_direction(model),
                date_options=self._date_options(model.dates),
                capabilities=PublicTransportProviders.capabilities(provider_id)
            )
        )(self._attach_cached_announcements(
            provider_id,
            downloader,
            self._cached(
                f'{provider_id}:line:{url}',
                lambda: downloader.download_line(url)
            )
        )))

    def line_stop(self, provider_id: str):
        """Renders departures for one line, stop and direction."""
        return self._render_url(provider_id, lambda downloader, url: (
            lambda model: render_template(
                'public_transport/line_stop.html',
                timetable=model,
                timetable_days=sorted(model.timetable.items()),
                variant_codes=self._variant_codes(
                    model.timetable.values()
                ),
                date_options=self._date_options(model.dates),
                capabilities=PublicTransportProviders.capabilities(provider_id)
            )
        )(self._attach_cached_announcements(
            provider_id,
            downloader,
            self._cached(
                f'{provider_id}:line-stop:{url}',
                lambda: downloader.download_line_stop_timetable(url)
            )
        )))

    def ride(self, provider_id: str):
        """Renders one complete ride table."""
        return self._render_url(provider_id, lambda downloader, url: (
            lambda model: render_template(
                'public_transport/ride.html',
                ride=model,
                route_points=self._ride_route_points(model),
                capabilities=PublicTransportProviders.capabilities(provider_id)
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
                stop=model,
                line_rows=self._stop_line_rows(model),
                capabilities=PublicTransportProviders.capabilities(provider_id)
            )
        )(self._cached(
                f'{provider_id}:stop-lines:{url}',
                lambda: downloader.download_stop_all(url)
        )))

    def announcement(self, provider_id: str):
        """Returns full announcement content downloaded on demand."""
        try:
            downloader = PublicTransportProviders.downloader(provider_id)
            url = PublicTransportProviders.validate_url(
                provider_id,
                str(request.args.get('url') or '')
            )
            model = self._cached(
                f'{provider_id}:announcement:{url}',
                lambda: downloader.download_announcement(url)
            )
            return jsonify(model.to_dict())
        except ValueError as error:
            return jsonify({'error': str(error)}), 400
        except Exception as error:
            return jsonify({
                'error': (
                    'Nie udało się pobrać treści komunikatu: '
                    f'{error}'
                )
            }), 502

    def vehicle_positions(self, provider_id: str):
        """Returns current GTFS-Realtime vehicle positions."""
        try:
            capabilities = PublicTransportProviders.capabilities(provider_id)
            if not capabilities.get(
                PublicTransportProviders.CAPABILITY_SHOW_VEHICLE_POSITIONS,
                False
            ):
                raise ValueError(
                    'Ten przewoźnik nie udostępnia pozycji pojazdów.'
                )
            downloader = PublicTransportProviders.downloader(provider_id)
            line = str(request.args.get('line') or '').strip()
            positions = downloader.download_vehicle_positions(line=line)
            return jsonify({
                'positions': [
                    position.to_dict()
                    for position in positions
                ]
            })
        except ValueError as error:
            return jsonify({'error': str(error)}), 400
        except Exception as error:
            return jsonify({
                'error': (
                    'Nie udało się pobrać pozycji pojazdów: '
                    f'{error}'
                )
            }), 502

    #endregion Endpoints

    #region Rendering

    def _render(self, provider_id: str, renderer: Callable):
        """Runs a provider renderer and returns a consistent error fragment."""
        self._set_download_progress(
            provider_id,
            'downloading',
            '',
            0,
            0
        )

        def update(
            item: str,
            current: int,
            total: int,
            attempt: int,
            max_attempts: int
        ) -> None:
            self._set_download_progress(
                provider_id,
                'downloading',
                item,
                current,
                total,
                attempt,
                max_attempts
            )

        try:
            downloader = PublicTransportProviders.downloader(provider_id)
            with PublicTransportDownloadProgress.bind(update):
                result = renderer(downloader)
            self._set_download_progress(
                provider_id,
                'complete',
                '',
                1,
                1
            )
            return result
        except ValueError as error:
            self._set_download_progress(
                provider_id,
                'error',
                str(error),
                0,
                0
            )
            return render_template(
                'public_transport/error.html',
                message=str(error)
            ), 400
        except Exception as error:
            self._set_download_progress(
                provider_id,
                'error',
                str(error),
                0,
                0
            )
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
        """Downloads stops using the shared request progress context."""
        return downloader.download_stops()

    def _load_lines(self, provider_id: str, downloader) -> Any:
        """Loads persistent lines or refreshes them explicitly."""
        refresh = self._refresh_requested()
        uses_settings_cache = PublicTransportProviders.uses_settings_cache(
            provider_id
        )
        if uses_settings_cache:
            cache = self._settings_storage.load_public_transport_cache(
                provider_id
            )
            if cache and cache.lines and not refresh:
                return cache.lines

        lines = downloader.download_lines(refresh=refresh)
        if uses_settings_cache:
            self._settings_storage.save_public_transport_lines(
                provider_id,
                lines
            )
        if refresh:
            self._invalidate_provider_cache(provider_id)
            self._refresh_cached_announcements(provider_id, downloader)
        return lines

    def _load_stops(self, provider_id: str, downloader) -> Any:
        """Loads persistent stops or refreshes them explicitly."""
        refresh = self._refresh_requested()
        uses_settings_cache = PublicTransportProviders.uses_settings_cache(
            provider_id
        )
        if uses_settings_cache:
            cache = self._settings_storage.load_public_transport_cache(
                provider_id
            )
            if cache and cache.stops and not refresh:
                if not cache.stop_locations_initialized:
                    stops = cache.stops
                    if not any(
                        platform.latitude is not None
                        and platform.longitude is not None
                        for stop in stops
                        for platform in stop.platforms
                    ):
                        stops = downloader.enrich_stop_locations(stops)
                    self._settings_storage.save_public_transport_stops(
                        provider_id,
                        stops,
                        stop_locations_initialized=True
                    )
                    return stops
                return cache.stops

        stops = downloader.download_stops(refresh=refresh)
        if uses_settings_cache:
            self._settings_storage.save_public_transport_stops(
                provider_id,
                stops,
                stop_locations_initialized=True
            )
        if refresh:
            self._invalidate_provider_cache(provider_id)
            self._refresh_cached_announcements(provider_id, downloader)
        return stops

    def _attach_cached_announcements(
        self,
        provider_id: str,
        downloader,
        model
    ):
        """Attaches provider-wide cached announcements matching a model line."""
        capabilities = PublicTransportProviders.capabilities(provider_id)
        if not capabilities.get(
            PublicTransportProviders.CAPABILITY_CACHE_ANNOUNCEMENTS,
            False
        ):
            return model
        announcements = self._load_cached_announcements(
            provider_id,
            downloader
        )
        model.announcements = [
            announcement for announcement in announcements
            if model.line in announcement.lines
        ]
        return model

    def _load_cached_announcements(
        self,
        provider_id: str,
        downloader,
        refresh: bool = False
    ):
        """Loads persistent provider announcements or downloads them once."""
        if not PublicTransportProviders.uses_settings_cache(provider_id):
            try:
                return self._cached(
                    f'{provider_id}:announcements',
                    lambda: downloader.download_announcements(
                        include_content=False
                    ),
                    refresh=refresh
                )
            except Exception:
                return []
        cache = self._settings_storage.load_public_transport_cache(provider_id)
        if cache and cache.announcements and not refresh:
            return cache.announcements
        try:
            announcements = downloader.download_announcements(
                include_content=False
            )
        except Exception:
            return list(cache.announcements) if cache else []
        self._settings_storage.save_public_transport_announcements(
            provider_id,
            announcements
        )
        return announcements

    def _invalidate_provider_cache(self, provider_id: str) -> None:
        """Invalidates temporary detail models after a provider refresh."""
        prefix = f'{provider_id}:'
        with self._cache_lock:
            self._cache = {
                key: value
                for key, value in self._cache.items()
                if not key.startswith(prefix)
            }

    def _refresh_cached_announcements(
        self,
        provider_id: str,
        downloader
    ) -> None:
        """Refreshes announcements when the provider supports their cache."""
        capabilities = PublicTransportProviders.capabilities(provider_id)
        if capabilities.get(
            PublicTransportProviders.CAPABILITY_CACHE_ANNOUNCEMENTS,
            False
        ):
            self._load_cached_announcements(
                provider_id,
                downloader,
                refresh=True
            )

    def _set_download_progress(
        self,
        provider_id: str,
        status: str,
        item: str,
        current: int,
        total: int,
        attempt: int = 1,
        max_attempts: int = PublicTransportDownloadProgress.MAX_ATTEMPTS
    ) -> None:
        """Stores one immutable snapshot of provider download progress."""
        with self._cache_lock:
            self._download_progress[provider_id] = {
                'status': status,
                'item': item,
                'current': current,
                'total': total,
                'attempt': attempt,
                'max_attempts': max_attempts
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
    def _line_route_points(line) -> list[dict[str, float]]:
        """Returns the selected line direction geometry for the map."""
        if not line.directions:
            return []
        return [
            {
                'latitude': point.latitude,
                'longitude': point.longitude
            }
            for point in line.directions[0].route
        ]

    @staticmethod
    def _line_routes_by_direction(line) -> list[list[dict[str, float]]]:
        """Returns map geometry separately for every displayed direction."""
        return [[
            {
                'latitude': point.latitude,
                'longitude': point.longitude
            }
            for point in direction.route
        ] for direction in line.directions]

    @staticmethod
    def _variant_codes(timetables) -> dict[str, str]:
        """Assigns compact, stable labels to timetable variants."""
        variants: list[str] = []
        for timetable in timetables:
            values = [
                *timetable.variants,
                *(
                    departure.variant
                    for departure in timetable.departures
                    if departure.variant
                )
            ]
            for value in values:
                normalized = str(value).strip()
                if normalized and normalized not in variants:
                    variants.append(normalized)
        return {
            variant: f'W{index}'
            for index, variant in enumerate(variants, start=1)
        }

    @classmethod
    def _stop_line_rows(cls, stop) -> list[dict[str, Any]]:
        """Builds stop-line rows with a separate variant legend per line."""
        return [
            {
                'line': line,
                'timetable': timetable,
                'variant_codes': cls._variant_codes([timetable])
            }
            for line, timetable in stop.lines.items()
        ]

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
                PublicTransportType.METRO,
                PublicTransportType.TRAIN,
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

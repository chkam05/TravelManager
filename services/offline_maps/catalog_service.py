from __future__ import annotations

from datetime import datetime, timezone
import json
import ssl
from threading import Lock, Thread
from typing import Any, Callable
from urllib.parse import urlparse
from urllib.request import Request, urlopen

from models.offline_maps import OfflineMapRegion
from services.offline_maps.catalog_names import display_name
from resources.offline_maps.source_definitions import OfflineMapSources
from storage.offline_maps import OfflineMapCatalogStorage


class OfflineMapCatalogError(RuntimeError):
    """A catalog could not be obtained and no valid cache is available."""


class OfflineMapCatalogService:
    """Downloads, validates and persistently caches the Geofabrik index."""

    def __init__(
        self,
        storage: OfflineMapCatalogStorage,
        opener: Callable[..., Any] = urlopen,
    ):
        self._storage = storage
        self._opener = opener
        self._refresh_lock = Lock()
        self._refreshing = False
        self._last_error = ''

    @property
    def refreshing(self) -> bool:
        with self._refresh_lock:
            return self._refreshing

    @property
    def last_error(self) -> str:
        with self._refresh_lock:
            return self._last_error

    def get(self) -> dict[str, Any]:
        updated_at, regions = self._storage.load()
        if regions:
            return self._result(updated_at, regions, 'cache')
        return self.refresh()

    def refresh(self) -> dict[str, Any]:
        try:
            payload = self._download()
            regions = self.parse(payload)
            if not regions:
                raise OfflineMapCatalogError('Katalog Geofabrik nie zawiera regionów.')
            updated_at = datetime.now(timezone.utc).isoformat()
            self._storage.save(updated_at, regions)
            with self._refresh_lock:
                self._last_error = ''
            return self._result(updated_at, regions, 'current')
        except Exception as error:
            updated_at, regions = self._storage.load()
            if regions:
                with self._refresh_lock:
                    self._last_error = str(error)
                result = self._result(updated_at, regions, 'cache')
                result['warning'] = str(error)
                return result
            if isinstance(error, OfflineMapCatalogError):
                raise
            raise OfflineMapCatalogError(
                f'Nie udało się pobrać katalogu map offline: {error}'
            ) from error

    def refresh_async(self) -> bool:
        """Starts one refresh worker and returns False if one already runs."""
        with self._refresh_lock:
            if self._refreshing:
                return False
            self._refreshing = True
        Thread(target=self._refresh_worker, daemon=True).start()
        return True

    def _refresh_worker(self) -> None:
        try:
            self.refresh()
        except OfflineMapCatalogError as error:
            with self._refresh_lock:
                self._last_error = str(error)
        finally:
            with self._refresh_lock:
                self._refreshing = False

    def _download(self) -> dict[str, Any]:
        request = Request(
            OfflineMapSources.GEOFABRIK_INDEX_URL,
            headers={
                'Accept': 'application/json',
                'User-Agent': OfflineMapSources.USER_AGENT,
            },
        )
        open_options: dict[str, Any] = {'timeout': 30}
        if self._opener is urlopen:
            try:
                import certifi
                open_options['context'] = ssl.create_default_context(
                    cafile=certifi.where()
                )
            except ImportError:
                # Catalog browsing remains available with the platform trust
                # store even before optional map-building dependencies install.
                pass
        with self._opener(request, **open_options) as response:
            content = response.read()
        try:
            value = json.loads(content.decode('utf-8'))
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            raise OfflineMapCatalogError('Nieprawidłowy katalog Geofabrik.') from error
        if not isinstance(value, dict):
            raise OfflineMapCatalogError('Nieprawidłowy katalog Geofabrik.')
        return value

    @classmethod
    def parse(cls, payload: dict[str, Any]) -> list[OfflineMapRegion]:
        features = payload.get('features')
        if payload.get('type') != 'FeatureCollection' or not isinstance(features, list):
            raise OfflineMapCatalogError('Nieprawidłowa struktura katalogu Geofabrik.')

        indexed: dict[str, OfflineMapRegion] = {}
        for feature in features:
            try:
                region = cls._parse_feature(feature)
            except (TypeError, ValueError):
                continue
            if region.id in indexed:
                raise OfflineMapCatalogError(
                    f'Powielony identyfikator regionu Geofabrik: {region.id}'
                )
            indexed[region.id] = region

        for region in indexed.values():
            if region.parent_id in indexed:
                indexed[region.parent_id].children.append(region.id)
        for region in indexed.values():
            region.children.sort()
        return list(indexed.values())

    @classmethod
    def _parse_feature(cls, feature: object) -> OfflineMapRegion:
        if not isinstance(feature, dict):
            raise ValueError('Invalid feature.')
        properties = feature.get('properties')
        if not isinstance(properties, dict):
            raise ValueError('Invalid feature properties.')
        urls = properties.get('urls') or {}
        if not isinstance(urls, dict):
            urls = {}
        pbf_url = str(urls.get('pbf') or '').strip()
        if pbf_url and not cls._trusted_pbf_url(pbf_url):
            raise ValueError('Untrusted PBF URL.')
        return OfflineMapRegion.from_dict({
            'id': properties.get('id'),
            'name': display_name(str(properties.get('name') or '')),
            'parent_id': properties.get('parent') or '',
            'country_codes': cls._string_values(
                properties.get('iso3166-1:alpha2'), upper=True
            ),
            'region_codes': cls._string_values(
                properties.get('iso3166-2'), upper=True
            ),
            'pbf_url': pbf_url,
            'pbf_size': cls._optional_size(properties.get('pbf_size')),
            'source_updated_at': properties.get('timestamp') or '',
            'bounds': None,
            'coverage': feature.get('geometry'),
            'children': [],
        })

    @staticmethod
    def _string_values(value: object, upper: bool = False) -> list[str]:
        values = value if isinstance(value, list) else ([value] if value else [])
        return [
            str(item).strip().upper() if upper else str(item).strip()
            for item in values if str(item).strip()
        ]

    @staticmethod
    def _optional_size(value: object) -> int | None:
        if value is None:
            return None
        return value if type(value) is int and value >= 0 else None

    @staticmethod
    def _trusted_pbf_url(value: str) -> bool:
        parsed = urlparse(value)
        return (
            parsed.scheme == 'https'
            and parsed.hostname == OfflineMapSources.GEOFABRIK_HOST
            and parsed.username is None
            and parsed.password is None
            and parsed.path.endswith('.osm.pbf')
        )

    def _result(
        self, updated_at: str, regions: list[OfflineMapRegion], source: str
    ) -> dict[str, Any]:
        return {
            'updated_at': updated_at,
            'regions': regions,
            'source': source,
            'refreshing': self.refreshing,
        }

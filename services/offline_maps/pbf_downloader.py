from __future__ import annotations

from datetime import datetime, timezone
from email.message import Message
from hashlib import md5
from pathlib import Path
import re
import ssl
from time import sleep
from typing import Any, Callable
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from models.offline_maps import OfflineMapJob, OfflineMapRegion
from resources.offline_maps.source_definitions import OfflineMapSources
from storage.offline_maps import OfflineMapPaths
from services.offline_maps.errors import (
    OfflineMapDownloadCancelled,
    OfflineMapDownloadError,
)
from services.offline_maps.resource_guard import OfflineMapResourceGuard


class OfflineMapPbfDownloader:
    """Downloads only catalogued Geofabrik extracts into resumable files."""

    CHUNK_SIZE = 256 * 1024
    MAX_ATTEMPTS = 3
    REQUEST_TIMEOUT = 90
    _CONTENT_RANGE = re.compile(r'^bytes\s+(\d+)-(\d+)/(\d+|\*)$')

    def __init__(
        self,
        paths: OfflineMapPaths,
        opener: Callable[..., Any] = urlopen,
        sleeper: Callable[[float], None] = sleep,
        checksum_opener: Callable[..., Any] | None = None,
    ):
        self._paths = paths
        self._opener = opener
        self._sleeper = sleeper
        self._checksum_opener = checksum_opener or (
            opener if opener is urlopen else None
        )
        self._resources = OfflineMapResourceGuard(paths.root)

    def download(
        self,
        job: OfflineMapJob,
        cancelled: Callable[[], bool] | None = None,
        progress: Callable[[OfflineMapJob, int, int], None] | None = None,
    ) -> Path:
        """Downloads a job's region and returns the completed source path."""
        region = self._catalog_region(job.region_id)
        if not region.pbf_url:
            raise OfflineMapDownloadError(
                'Wybrany region nie udostępnia pliku OSM PBF.'
            )
        if not OfflineMapSources.GEOFABRIK_HOST == self._hostname(region.pbf_url):
            raise OfflineMapDownloadError('Adres PBF nie pochodzi z Geofabrik.')

        final_path = self._paths.source_path(job.id)
        partial_path = self._paths.source_path(job.id, partial=True)
        if final_path.is_file():
            return final_path
        self._resources.ensure_download(region.pbf_size)

        self._update_job(
            job, status='running', stage='downloading',
            cancel_requested=False, error=''
        )
        last_error: Exception | None = None
        for attempt in range(1, self.MAX_ATTEMPTS + 1):
            try:
                self._attempt(region, job, partial_path, cancelled, progress)
                self._verify_checksum(region, partial_path)
                partial_path.replace(final_path)
                self._update_job(job, stage='analysing')
                return final_path
            except OfflineMapDownloadCancelled:
                self._update_job(
                    job, status='cancelled', stage='cancelled',
                    cancel_requested=True, error=''
                )
                raise
            except Exception as error:
                last_error = error
                if not self._retryable(error) or attempt == self.MAX_ATTEMPTS:
                    break
                self._sleeper(float(2 ** (attempt - 1)))

        message = f'Nie udało się pobrać mapy: {last_error}'
        self._update_job(job, status='failed', stage='failed', error=message)
        raise OfflineMapDownloadError(message) from last_error

    def _attempt(
        self,
        region: OfflineMapRegion,
        job: OfflineMapJob,
        partial_path: Path,
        cancelled: Callable[[], bool] | None,
        progress: Callable[[OfflineMapJob, int, int], None] | None,
    ) -> None:
        existing = partial_path.stat().st_size if partial_path.exists() else 0
        headers = {
            'Accept': 'application/octet-stream,*/*',
            'User-Agent': OfflineMapSources.USER_AGENT,
        }
        if existing:
            headers['Range'] = f'bytes={existing}-'
        request = Request(region.pbf_url, headers=headers)
        options: dict[str, Any] = {'timeout': self.REQUEST_TIMEOUT}
        if self._opener is urlopen:
            try:
                import certifi
                options['context'] = ssl.create_default_context(cafile=certifi.where())
            except ImportError:
                pass

        try:
            response_context = self._opener(request, **options)
        except HTTPError as error:
            if error.code == 416 and self._partial_is_complete(error.headers, existing):
                self._report(job, existing, existing, progress)
                return
            raise

        with response_context as response:
            final_url = response.geturl() if hasattr(response, 'geturl') else region.pbf_url
            if (
                self._hostname(final_url) != OfflineMapSources.GEOFABRIK_HOST
                or not str(final_url).startswith('https://')
            ):
                raise OfflineMapDownloadError(
                    'Pobieranie zostało przekierowane poza zaufane źródło.'
                )
            status = response.getcode()
            resumed = existing > 0 and status == 206
            if resumed and not self._valid_content_range(response.headers, existing):
                raise OfflineMapDownloadError(
                    'Serwer zwrócił nieprawidłowy zakres wznowienia.'
                )
            current = existing if resumed else 0
            length = self._header_integer(response.headers, 'Content-Length')
            total = current + length if length is not None else 0
            mode = 'ab' if resumed else 'wb'
            with partial_path.open(mode) as output:
                while True:
                    if cancelled and cancelled():
                        raise OfflineMapDownloadCancelled(
                            'Pobieranie mapy zostało anulowane.'
                        )
                    chunk = response.read(self.CHUNK_SIZE)
                    if not chunk:
                        break
                    output.write(chunk)
                    current += len(chunk)
                    if current % (16 * 1024 * 1024) < len(chunk):
                        remaining = max(0, (total or current) - current)
                        self._resources.ensure_stage(remaining, 'pobieranie', 1)
                    self._report(job, current, total or current, progress)
            if total and current != total:
                raise URLError(
                    f'Niepełna odpowiedź ({current} z {total} bajtów).'
                )
            self._report(job, current, total or current, progress)

    def _verify_checksum(self, region: OfflineMapRegion, path: Path) -> None:
        if self._checksum_opener is None:
            return
        checksum_url = region.pbf_url + '.md5'
        request = Request(checksum_url, headers={
            'Accept': 'text/plain', 'User-Agent': OfflineMapSources.USER_AGENT,
        })
        try:
            with self._checksum_opener(request, timeout=30) as response:
                final_url = response.geturl() if hasattr(response, 'geturl') else checksum_url
                if (
                    self._hostname(final_url) != OfflineMapSources.GEOFABRIK_HOST
                    or not str(final_url).startswith('https://')
                ):
                    raise OfflineMapDownloadError(
                        'Suma kontrolna pochodzi z niezaufanego źródła.'
                    )
                content = response.read(4097)
        except HTTPError as error:
            if error.code in {404, 410}:
                return
            raise OfflineMapDownloadError(
                f'Nie udało się pobrać sumy kontrolnej: HTTP {error.code}.'
            ) from error
        except (URLError, TimeoutError):
            # The sidecar is optional; the validated PBF remains usable when
            # it cannot be queried independently.
            return
        if len(content) > 4096:
            raise OfflineMapDownloadError('Nieprawidłowy plik sumy kontrolnej.')
        match = re.match(rb'^([0-9a-fA-F]{32})(?:\s|$)', content.strip())
        if not match:
            raise OfflineMapDownloadError('Nieprawidłowa suma kontrolna mapy.')
        expected = match.group(1).decode('ascii').lower()
        digest = md5(usedforsecurity=False)
        with path.open('rb') as source:
            for chunk in iter(lambda: source.read(1024 * 1024), b''):
                digest.update(chunk)
        if digest.hexdigest() != expected:
            raise OfflineMapDownloadError(
                'Pobrany plik mapy nie zgadza się z sumą kontrolną Geofabrik.'
            )

    def _catalog_region(self, region_id: str) -> OfflineMapRegion:
        _, regions = self._paths.catalog.load()
        region = next((item for item in regions if item.id == region_id), None)
        if region is None:
            raise OfflineMapDownloadError(
                'Region nie występuje w zapisanym katalogu Geofabrik.'
            )
        return region

    def _report(
        self,
        job: OfflineMapJob,
        current: int,
        total: int,
        callback: Callable[[OfflineMapJob, int, int], None] | None,
    ) -> None:
        job.downloaded_bytes = current
        job.total_bytes = total
        job.current = current
        job.total = total
        job.updated_at = self._now()
        self._paths.jobs.upsert(job)
        if callback:
            callback(job, current, total)

    def _update_job(self, job: OfflineMapJob, **changes: object) -> None:
        for name, value in changes.items():
            setattr(job, name, value)
        job.updated_at = self._now()
        self._paths.jobs.upsert(job)

    @classmethod
    def _valid_content_range(cls, headers: Message | Any, existing: int) -> bool:
        match = cls._CONTENT_RANGE.fullmatch(str(headers.get('Content-Range') or ''))
        return bool(match and int(match.group(1)) == existing)

    @staticmethod
    def _partial_is_complete(headers: Message | Any, existing: int) -> bool:
        value = str(headers.get('Content-Range') or '')
        match = re.fullmatch(r'bytes\s+\*/(\d+)', value)
        return bool(match and int(match.group(1)) == existing)

    @staticmethod
    def _header_integer(headers: Message | Any, name: str) -> int | None:
        value = headers.get(name)
        try:
            parsed = int(value)
        except (TypeError, ValueError):
            return None
        return parsed if parsed >= 0 else None

    @staticmethod
    def _hostname(url: str) -> str:
        from urllib.parse import urlparse
        return str(urlparse(url).hostname or '')

    @staticmethod
    def _retryable(error: Exception) -> bool:
        if isinstance(error, HTTPError):
            return error.code == 429 or 500 <= error.code < 600
        return isinstance(error, (URLError, TimeoutError, OSError))

    @staticmethod
    def _now() -> str:
        return datetime.now(timezone.utc).isoformat()

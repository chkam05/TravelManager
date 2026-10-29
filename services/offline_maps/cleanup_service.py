from __future__ import annotations

from pathlib import Path
import shutil
from typing import Callable

from models.offline_maps import OfflineMapJob
from models.offline_maps.validation import LOCAL_ID_PATTERN
from storage.offline_maps import OfflineMapPaths


class OfflineMapCleanupService:
    """Removes completed and provably orphaned offline-map work files."""

    def __init__(self, paths: OfflineMapPaths):
        self._paths = paths

    def process(
        self, job: OfflineMapJob, _cancelled: Callable[[], bool]
    ) -> None:
        """Cleans one installed map; installation itself is never rolled back."""
        installed = next(
            (item for item in self._paths.maps.load() if item.id == job.map_id),
            None,
        )
        if installed is None or not self._paths.map_path(installed.file_name).is_file():
            raise RuntimeError('Nie można posprzątać niezainstalowanej mapy.')
        self._paths.clear_job_files(job.id)
        return None

    def cleanup_orphans(self) -> dict[str, int]:
        """Cleans only files with no job owner and leftovers of completed jobs."""
        jobs = {job.id: job for job in self._paths.jobs.load()}
        removed_sources = 0
        removed_work = 0
        removed_feature_indexes = 0

        for path in self._paths.sources_directory.iterdir():
            job_id = self._source_job_id(path)
            if job_id and job_id not in jobs:
                path.unlink()
                removed_sources += 1

        for path in self._paths.work_directory.iterdir():
            if path.name not in jobs and self._safe_local_name(path.name):
                self._remove_work_path(path)
                removed_work += 1

        installed_ids = {item.id for item in self._paths.maps.load()}
        suffix = '.features.sqlite3'
        for path in self._paths.maps_directory.iterdir():
            if not path.name.endswith(suffix):
                continue
            map_id = path.name[:-len(suffix)]
            if map_id not in installed_ids and self._safe_local_name(map_id):
                path.unlink()
                removed_feature_indexes += 1

        for job in jobs.values():
            if job.status != 'completed':
                continue
            source_exists = any(
                self._paths.source_path(job.id, partial=partial).exists()
                for partial in (False, True)
            )
            work = self._paths.job_work_path(job.id, create=False)
            work_exists = work.exists()
            if source_exists or work_exists:
                self._paths.clear_job_files(job.id)
                removed_sources += int(source_exists)
                removed_work += int(work_exists)

        return {
            'sources': removed_sources,
            'work_directories': removed_work,
            'feature_indexes': removed_feature_indexes,
        }

    @staticmethod
    def _source_job_id(path: Path) -> str:
        name = path.name
        for suffix in ('.osm.pbf.part', '.osm.pbf'):
            if name.endswith(suffix):
                candidate = name[:-len(suffix)]
                return candidate if OfflineMapCleanupService._safe_local_name(candidate) else ''
        return ''

    @staticmethod
    def _safe_local_name(value: str) -> bool:
        return bool(LOCAL_ID_PATTERN.fullmatch(value))

    @staticmethod
    def _remove_work_path(path: Path) -> None:
        if path.is_symlink():
            path.unlink()
        elif path.is_dir():
            shutil.rmtree(path)

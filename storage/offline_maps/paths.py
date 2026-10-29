from __future__ import annotations

from pathlib import Path
import re
import shutil

from config import SETTINGS_DIR
from models.offline_maps.offline_map import OfflineMap
from models.offline_maps.validation import local_id
from storage.offline_maps.catalog_storage import OfflineMapCatalogStorage
from storage.offline_maps.job_storage import OfflineMapJobStorage
from storage.offline_maps.map_storage import OfflineMapStorage


class OfflineMapPaths:
    """Owns every filesystem path used by offline maps."""

    DIRECTORY_NAME = 'offline_maps'
    SAFE_FILE_PATTERN = re.compile(r'^[A-Za-z0-9][A-Za-z0-9_.-]{0,179}$')

    def __init__(self, data_directory=SETTINGS_DIR):
        self.root = Path(data_directory) / self.DIRECTORY_NAME
        self.sources_directory = self.root / 'sources'
        self.work_directory = self.root / 'work'
        self.maps_directory = self.root / 'maps'
        for directory in (
            self.root, self.sources_directory, self.work_directory,
            self.maps_directory,
        ):
            directory.mkdir(parents=True, exist_ok=True)
        self.catalog = OfflineMapCatalogStorage(self.root)
        self.maps = OfflineMapStorage(self.root)
        self.jobs = OfflineMapJobStorage(self.root)

    @classmethod
    def _safe_child(cls, directory: Path, file_name: str) -> Path:
        if (
            not isinstance(file_name, str)
            or not cls.SAFE_FILE_PATTERN.fullmatch(file_name)
            or Path(file_name).name != file_name
        ):
            raise ValueError('Invalid offline map file name.')
        directory = directory.resolve()
        candidate = directory / file_name
        # Existing symlinks must not turn a validated name into an escape path.
        if candidate.exists() and candidate.resolve().parent != directory:
            raise ValueError('Offline map path leaves its storage directory.')
        return candidate

    def source_path(self, job_id: str, partial: bool = False) -> Path:
        identifier = local_id(job_id, 'job id')
        suffix = '.osm.pbf.part' if partial else '.osm.pbf'
        return self._safe_child(self.sources_directory, identifier + suffix)

    def job_work_path(self, job_id: str, create: bool = True) -> Path:
        identifier = local_id(job_id, 'job id')
        path = self._safe_child(self.work_directory, identifier)
        if create:
            path.mkdir(parents=False, exist_ok=True)
        if path.resolve().parent != self.work_directory.resolve():
            raise ValueError('Offline map work path leaves its storage directory.')
        return path

    def map_path(self, file_name: str) -> Path:
        if not file_name.endswith('.mbtiles'):
            raise ValueError('Offline map package must use the MBTiles format.')
        return self._safe_child(self.maps_directory, file_name)

    def map_features_path(self, map_id: str) -> Path:
        identifier = local_id(map_id, 'map id')
        return self._safe_child(
            self.maps_directory, f'{identifier}.features.sqlite3'
        )

    def delete_map_file(self, offline_map: OfflineMap) -> bool:
        path = self.map_path(offline_map.file_name)
        try:
            path.unlink()
            return True
        except FileNotFoundError:
            return False

    def delete_map_features(self, map_id: str) -> bool:
        try:
            self.map_features_path(map_id).unlink()
            return True
        except FileNotFoundError:
            return False

    def clear_job_files(self, job_id: str) -> None:
        for partial in (False, True):
            try:
                self.source_path(job_id, partial=partial).unlink()
            except FileNotFoundError:
                pass
        work = self.job_work_path(job_id, create=False)
        if work.exists():
            if work.is_symlink() or work.resolve().parent != self.work_directory.resolve():
                raise ValueError('Invalid offline map work directory.')
            shutil.rmtree(work)

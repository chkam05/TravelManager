from __future__ import annotations

from datetime import datetime

from models.offline_maps import OfflineMap, OfflineMapJob
from storage.offline_maps import OfflineMapPaths


class OfflineMapPackageReuse:
    """Finds installed descendant packages safe to reuse for a parent map."""

    def __init__(self, paths: OfflineMapPaths):
        self._paths = paths

    def covered_maps(self, region_id: str, exclude_map_id: str = '') -> list[OfflineMap]:
        _, regions = self._paths.catalog.load()
        parents = {item.id: item.parent_id for item in regions}
        return [
            item for item in self._paths.maps.load()
            if item.id != exclude_map_id
            and self._is_descendant(item.region_id, region_id, parents)
        ]

    def reusable_maps(self, job: OfflineMapJob) -> list[OfflineMap]:
        _, regions = self._paths.catalog.load()
        target = next((item for item in regions if item.id == job.region_id), None)
        if target is None:
            return []
        result = []
        for item in self.covered_maps(job.region_id, job.map_id):
            if not self._fresh_enough(item.source_updated_at, target.source_updated_at):
                continue
            if not self._paths.map_features_path(item.id).is_file():
                continue
            if not self._paths.map_path(item.file_name).is_file():
                continue
            result.append(item)
        return result

    def coverage_for(self, region_id: str) -> dict | None:
        _, regions = self._paths.catalog.load()
        region = next((item for item in regions if item.id == region_id), None)
        return region.coverage if region else None

    @staticmethod
    def _is_descendant(candidate: str, parent: str, parents: dict[str, str]) -> bool:
        seen = set()
        current = candidate
        while current and current not in seen:
            seen.add(current)
            current = parents.get(current, '')
            if current == parent:
                return True
        return False

    @staticmethod
    def _fresh_enough(candidate: str, target: str) -> bool:
        if not candidate or not target:
            return False
        try:
            return datetime.fromisoformat(candidate) >= datetime.fromisoformat(target)
        except (TypeError, ValueError):
            return False

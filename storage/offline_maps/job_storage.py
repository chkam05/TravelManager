from __future__ import annotations

from core.data.base_json_storage import BaseJsonStorage
from models.offline_maps.offline_map_job import OfflineMapJob


class OfflineMapJobStorage(BaseJsonStorage):
    """Stores resumable offline map job state."""

    def __init__(self, directory):
        super().__init__(directory, 'jobs.json')

    def _initialize_default_data(self):
        return {'jobs': []}

    def load(self) -> list[OfflineMapJob]:
        rows = self._read().get('jobs', [])
        if not isinstance(rows, list):
            return []
        try:
            return OfflineMapJob.from_dict_list(rows)
        except (TypeError, ValueError):
            return []

    def save(self, jobs: list[OfflineMapJob]) -> None:
        validated: list[OfflineMapJob] = []
        identifiers: set[str] = set()
        active_maps: set[str] = set()
        for item in jobs:
            job = OfflineMapJob.from_dict(item.to_dict())
            if job.id in identifiers:
                raise ValueError('Duplicate offline map job id.')
            if job.status in {'queued', 'running'} and job.map_id in active_maps:
                raise ValueError('An active job already exists for this map.')
            identifiers.add(job.id)
            if job.status in {'queued', 'running'}:
                active_maps.add(job.map_id)
            validated.append(job)
        self._write({'jobs': [item.to_dict() for item in validated]})

    def upsert(self, job: OfflineMapJob) -> None:
        """Atomically inserts or replaces one job without losing other jobs."""
        validated = OfflineMapJob.from_dict(job.to_dict())
        with self._lock:
            jobs = [item for item in self.load() if item.id != validated.id]
            self.save([*jobs, validated])

    def find(self, job_id: str) -> OfflineMapJob | None:
        return next((job for job in self.load() if job.id == job_id), None)

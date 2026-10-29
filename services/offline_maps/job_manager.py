from __future__ import annotations

from collections import deque
from datetime import datetime, timezone
from hashlib import sha256
from threading import Condition, Event, Thread
from typing import Callable
from uuid import uuid4

from models.offline_maps import OfflineMapJob
from models.offline_maps.validation import local_id, region_id
from services.offline_maps.errors import OfflineMapProcessingCancelled
from services.offline_maps.pbf_downloader import OfflineMapPbfDownloader
from services.offline_maps.resource_guard import OfflineMapResourceGuard
from storage.offline_maps import (
    OfflineMapFeatureStorage,
    OfflineMapPaths,
    OfflineMapTileStorage,
)


JobProcessor = Callable[[OfflineMapJob, Callable[[], bool]], str | None]


class OfflineMapJobManager:
    """Runs a durable, single-worker offline-map processing queue."""

    ACTIVE_STATUSES = frozenset({'queued', 'running'})

    def __init__(
        self,
        paths: OfflineMapPaths,
        downloader: OfflineMapPbfDownloader | None = None,
    ):
        self._paths = paths
        self._downloader = downloader or OfflineMapPbfDownloader(paths)
        self._resources = OfflineMapResourceGuard(paths.root)
        self._condition = Condition()
        self._queue: deque[str] = deque()
        self._enqueued: set[str] = set()
        self._cancellations: dict[str, Event] = {}
        self._processors: dict[str, JobProcessor] = {}
        self._worker: Thread | None = None
        self._stopping = False

    def start(self) -> None:
        """Starts the worker and recovers processable jobs from storage."""
        with self._condition:
            if self._worker and self._worker.is_alive():
                return
            self._stopping = False
            recovered: list[OfflineMapJob] = []
            for job in self._paths.jobs.load():
                if job.status not in self.ACTIVE_STATUSES:
                    continue
                if job.status == 'running':
                    job.status = 'queued'
                    job.updated_at = self._now()
                    recovered.append(job)
                self._cancellations.setdefault(job.id, Event())
                if job.cancel_requested:
                    self._cancellations[job.id].set()
                if self._can_process(job.stage):
                    self._enqueue_locked(job.id)
            for job in recovered:
                self._paths.jobs.upsert(job)
            self._worker = Thread(
                target=self._work,
                daemon=True,
                name='offline-map-worker',
            )
            self._worker.start()

    def stop(self, timeout: float = 5) -> None:
        """Stops accepting work; active downloads remain resumable on disk."""
        with self._condition:
            self._stopping = True
            self._condition.notify_all()
            worker = self._worker
        if worker and worker.is_alive():
            worker.join(timeout=timeout)

    def register_processor(self, stage: str, processor: JobProcessor) -> None:
        """Adds a later pipeline stage and wakes jobs parked at that stage."""
        if stage in {'preparing', 'downloading'} or not callable(processor):
            raise ValueError('Invalid offline map processor.')
        with self._condition:
            self._processors[stage] = processor
            for job in self._paths.jobs.load():
                if job.status in self.ACTIVE_STATUSES and job.stage == stage:
                    self._enqueue_locked(job.id)
            self._condition.notify_all()

    def create(self, selected_region_id: str, max_zoom: int = 10) -> OfflineMapJob:
        self.start()
        selected_region_id = region_id(selected_region_id)
        if type(max_zoom) is not int or not 0 <= max_zoom <= 22:
            raise ValueError('Nieprawidłowy maksymalny poziom przybliżenia.')
        _, regions = self._paths.catalog.load()
        region = next((row for row in regions if row.id == selected_region_id), None)
        if region is None or not region.pbf_url:
            raise ValueError('Region nie jest dostępny do pobrania.')
        map_id = self.map_id(selected_region_id)
        if any(item.id == map_id for item in self._paths.maps.load()):
            raise ValueError('Mapa tego regionu jest już zainstalowana.')
        if any(
            item.map_id == map_id and item.status in self.ACTIVE_STATUSES
            for item in self._paths.jobs.load()
        ):
            raise ValueError('Zadanie dla tego regionu już istnieje.')

        return self._create_job(selected_region_id, map_id, max_zoom, False)

    def create_update(
        self, selected_map_id: str, max_zoom: int | None = None
    ) -> OfflineMapJob:
        self.start()
        selected_map_id = local_id(selected_map_id, 'map id')
        installed = next(
            (item for item in self._paths.maps.load() if item.id == selected_map_id),
            None,
        )
        if installed is None:
            raise ValueError('Mapa do aktualizacji nie jest zainstalowana.')
        if max_zoom is None:
            max_zoom = installed.max_zoom
        if type(max_zoom) is not int or not 0 <= max_zoom <= 22:
            raise ValueError('Nieprawidłowy maksymalny poziom przybliżenia.')
        if any(
            item.map_id == selected_map_id and item.status in self.ACTIVE_STATUSES
            for item in self._paths.jobs.load()
        ):
            raise ValueError('Zadanie dla tego regionu już istnieje.')
        _, regions = self._paths.catalog.load()
        region = next((item for item in regions if item.id == installed.region_id), None)
        if region is None or not region.pbf_url:
            raise ValueError('Region nie jest dostępny do aktualizacji.')
        return self._create_job(installed.region_id, selected_map_id, max_zoom, True)

    def _create_job(
        self, selected_region_id: str, map_id: str, max_zoom: int,
        is_update: bool,
    ) -> OfflineMapJob:
        _, regions = self._paths.catalog.load()
        region = next((row for row in regions if row.id == selected_region_id), None)
        if region is None or not region.pbf_url:
            raise ValueError('Region nie jest dostępny do pobrania.')
        self._resources.ensure_download(region.pbf_size)
        now = self._now()
        job = OfflineMapJob.from_dict({
            'id': f'job-{uuid4().hex}',
            'region_id': selected_region_id,
            'map_id': map_id,
            'status': 'queued',
            'stage': 'preparing',
            'downloaded_bytes': 0,
            'total_bytes': region.pbf_size or 0,
            'current': 0,
            'total': region.pbf_size or 0,
            'max_zoom': max_zoom,
            'cancel_requested': False,
            'created_at': now,
            'updated_at': now,
            'error': '',
            'is_update': is_update,
        })
        self._paths.jobs.upsert(job)
        with self._condition:
            self._cancellations[job.id] = Event()
            self._enqueue_locked(job.id)
            self._condition.notify_all()
        return job

    def cancel(self, job_id: str) -> OfflineMapJob | None:
        identifier = local_id(job_id, 'job id')
        job = self._paths.jobs.find(identifier)
        if job is None:
            return None
        if job.status not in self.ACTIVE_STATUSES:
            return job
        job.cancel_requested = True
        job.updated_at = self._now()
        self._paths.jobs.upsert(job)
        with self._condition:
            cancellation = self._cancellations.setdefault(identifier, Event())
            cancellation.set()
            self._condition.notify_all()
        return job

    def resume(self, job_id: str) -> OfflineMapJob | None:
        """Requeues a cancelled/failed job from its latest safe artifact."""
        identifier = local_id(job_id, 'job id')
        job = self._paths.jobs.find(identifier)
        if job is None:
            return None
        if job.status not in {'cancelled', 'failed'}:
            raise ValueError('Można wznowić tylko przerwane zadanie mapy.')
        if (
            not job.is_update
            and any(item.id == job.map_id for item in self._paths.maps.load())
        ):
            raise ValueError('Mapa tego zadania jest już zainstalowana.')
        job.stage = self._resume_stage(job)
        job.status = 'queued'
        job.cancel_requested = False
        job.error = ''
        job.updated_at = self._now()
        self._paths.jobs.upsert(job)
        self.start()
        with self._condition:
            self._cancellations[job.id] = Event()
            self._enqueue_locked(job.id)
            self._condition.notify_all()
        return job

    def list(self) -> list[OfflineMapJob]:
        return self._paths.jobs.load()

    def find(self, job_id: str) -> OfflineMapJob | None:
        return self._paths.jobs.find(local_id(job_id, 'job id'))

    @staticmethod
    def map_id(selected_region_id: str) -> str:
        identifier = region_id(selected_region_id)
        readable = ''.join(
            character if character.isalnum() else '-'
            for character in identifier.lower()
        ).strip('-')[:90]
        digest = sha256(identifier.encode('utf-8')).hexdigest()[:12]
        return local_id(f'{readable}-{digest}', 'map id')

    def _work(self) -> None:
        while True:
            with self._condition:
                while not self._queue and not self._stopping:
                    self._condition.wait()
                if self._stopping:
                    return
                job_id = self._queue.popleft()
                self._enqueued.discard(job_id)
            self._run_job(job_id)

    def _run_job(self, job_id: str) -> None:
        job = self._paths.jobs.find(job_id)
        if job is None or job.status not in self.ACTIVE_STATUSES:
            return
        cancellation = self._cancellations.setdefault(job.id, Event())
        if job.cancel_requested:
            cancellation.set()
        try:
            while not cancellation.is_set():
                if job.stage in {'preparing', 'downloading'}:
                    self._downloader.download(
                        job,
                        lambda: cancellation.is_set() or self._is_stopping(),
                    )
                    job = self._paths.jobs.find(job.id) or job
                    continue
                processor = self._processors.get(job.stage)
                if processor is None:
                    # A future implementation stage will register this handler.
                    job.status = 'queued'
                    job.updated_at = self._now()
                    self._paths.jobs.upsert(job)
                    return
                next_stage = processor(job, cancellation.is_set)
                if next_stage is None:
                    job.status = 'completed'
                    job.stage = 'completed'
                    job.current = job.total
                    job.updated_at = self._now()
                    self._paths.jobs.upsert(job)
                    return
                if next_stage not in OfflineMapJob.STAGES:
                    raise ValueError('Procesor zwrócił nieprawidłowy etap zadania.')
                job.stage = next_stage
                job.phase = ''
                job.current = 0
                job.total = 0
                job.status = 'running'
                job.updated_at = self._now()
                self._paths.jobs.upsert(job)
            self._cancel_and_cleanup(job)
        except OfflineMapProcessingCancelled:
            if self._is_stopping() and not cancellation.is_set():
                # Application shutdown is a pause, not a user cancellation.
                job = self._paths.jobs.find(job.id) or job
                job.status = 'queued'
                job.stage = self._resume_stage(job)
                job.cancel_requested = False
                job.updated_at = self._now()
                self._paths.jobs.upsert(job)
            else:
                self._cancel_and_cleanup(job)
        except Exception as error:
            job = self._paths.jobs.find(job.id) or job
            job.status = 'failed'
            job.stage = 'failed'
            job.error = str(error)
            job.updated_at = self._now()
            self._paths.jobs.upsert(job)
        finally:
            with self._condition:
                self._cancellations.pop(job_id, None)

    def _cancel_and_cleanup(self, job: OfflineMapJob) -> None:
        """Marks an explicit user cancellation and removes all job artifacts."""
        cleanup_error = ''
        try:
            self._paths.clear_job_files(job.id)
        except (OSError, ValueError) as error:
            cleanup_error = f'Nie udało się usunąć plików anulowanej mapy: {error}'
        job.status = 'failed' if cleanup_error else 'cancelled'
        job.stage = 'failed' if cleanup_error else 'cancelled'
        job.cancel_requested = True
        job.current = 0
        job.total = 0
        job.downloaded_bytes = 0
        job.total_bytes = 0
        job.phase = ''
        job.error = cleanup_error
        job.updated_at = self._now()
        self._paths.jobs.upsert(job)

    def _can_process(self, stage: str) -> bool:
        return stage in {'preparing', 'downloading'} or stage in self._processors

    def _enqueue_locked(self, job_id: str) -> None:
        if job_id not in self._enqueued:
            self._queue.append(job_id)
            self._enqueued.add(job_id)

    def _is_stopping(self) -> bool:
        with self._condition:
            return self._stopping

    def _resume_stage(self, job: OfflineMapJob) -> str:
        work = self._paths.job_work_path(job.id, create=False)
        features = OfflineMapFeatureStorage(work).path
        if OfflineMapTileStorage(work).is_complete():
            return 'optimising'
        if features.is_file():
            return 'building_tiles'
        if self._paths.source_path(job.id).is_file():
            return 'analysing'
        return 'downloading'

    @staticmethod
    def _now() -> str:
        return datetime.now(timezone.utc).isoformat()

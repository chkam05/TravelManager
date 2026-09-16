from __future__ import annotations

from dataclasses import dataclass
from typing import Any, ClassVar, Dict

from core.data.base_data_model import BaseDataModel
from models.offline_maps.validation import (
    iso_datetime, local_id, non_negative_integer, region_id, optional_text,
)


@dataclass
class OfflineMapJob(BaseDataModel):
    """Persisted state required to resume an offline map operation."""

    STATUSES: ClassVar[frozenset[str]] = frozenset({
        'queued', 'running', 'completed', 'failed', 'cancelled'
    })
    STAGES: ClassVar[frozenset[str]] = frozenset({
        'preparing', 'downloading', 'analysing', 'building_tiles',
        'optimising', 'installing', 'completed', 'failed', 'cancelled'
    })

    FIELD_ID: ClassVar[str] = 'id'
    FIELD_REGION_ID: ClassVar[str] = 'region_id'
    FIELD_MAP_ID: ClassVar[str] = 'map_id'
    FIELD_STATUS: ClassVar[str] = 'status'
    FIELD_STAGE: ClassVar[str] = 'stage'
    FIELD_DOWNLOADED_BYTES: ClassVar[str] = 'downloaded_bytes'
    FIELD_TOTAL_BYTES: ClassVar[str] = 'total_bytes'
    FIELD_CURRENT: ClassVar[str] = 'current'
    FIELD_TOTAL: ClassVar[str] = 'total'
    FIELD_MAX_ZOOM: ClassVar[str] = 'max_zoom'
    FIELD_CANCEL_REQUESTED: ClassVar[str] = 'cancel_requested'
    FIELD_CREATED_AT: ClassVar[str] = 'created_at'
    FIELD_UPDATED_AT: ClassVar[str] = 'updated_at'
    FIELD_ERROR: ClassVar[str] = 'error'
    FIELD_IS_UPDATE: ClassVar[str] = 'is_update'
    FIELD_PHASE: ClassVar[str] = 'phase'

    id: str
    region_id: str
    map_id: str
    status: str
    stage: str
    downloaded_bytes: int
    total_bytes: int
    current: int
    total: int
    max_zoom: int
    cancel_requested: bool
    created_at: str
    updated_at: str
    error: str
    is_update: bool
    phase: str = ''

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> OfflineMapJob:
        if not isinstance(d, dict):
            raise ValueError('Invalid offline map job.')
        status = optional_text(d.get(cls.FIELD_STATUS), 'job status', 32) or 'queued'
        stage = optional_text(d.get(cls.FIELD_STAGE), 'job stage', 32) or 'preparing'
        if status not in cls.STATUSES or stage not in cls.STAGES:
            raise ValueError('Invalid offline map job state.')
        cancel_requested = d.get(cls.FIELD_CANCEL_REQUESTED, False)
        if type(cancel_requested) is not bool:
            raise ValueError('Invalid cancellation state.')
        is_update = d.get(cls.FIELD_IS_UPDATE, False)
        if type(is_update) is not bool:
            raise ValueError('Invalid update state.')
        max_zoom = non_negative_integer(d.get(cls.FIELD_MAX_ZOOM, 14), 'maximum zoom')
        if max_zoom > 22:
            raise ValueError('Invalid maximum zoom.')
        return cls(
            id=local_id(d.get(cls.FIELD_ID), 'job id'),
            region_id=region_id(d.get(cls.FIELD_REGION_ID)),
            map_id=local_id(d.get(cls.FIELD_MAP_ID), 'map id'),
            status=status,
            stage=stage,
            downloaded_bytes=non_negative_integer(d.get(cls.FIELD_DOWNLOADED_BYTES, 0), 'downloaded bytes'),
            total_bytes=non_negative_integer(d.get(cls.FIELD_TOTAL_BYTES, 0), 'total bytes'),
            current=non_negative_integer(d.get(cls.FIELD_CURRENT, 0), 'current progress'),
            total=non_negative_integer(d.get(cls.FIELD_TOTAL, 0), 'total progress'),
            max_zoom=max_zoom,
            cancel_requested=cancel_requested,
            created_at=iso_datetime(d.get(cls.FIELD_CREATED_AT), 'creation date', optional=False),
            updated_at=iso_datetime(d.get(cls.FIELD_UPDATED_AT), 'update date', optional=False),
            error=optional_text(d.get(cls.FIELD_ERROR), 'job error', 2000),
            is_update=is_update,
            phase=optional_text(d.get(cls.FIELD_PHASE), 'job phase', 32),
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            self.FIELD_ID: self.id,
            self.FIELD_REGION_ID: self.region_id,
            self.FIELD_MAP_ID: self.map_id,
            self.FIELD_STATUS: self.status,
            self.FIELD_STAGE: self.stage,
            self.FIELD_DOWNLOADED_BYTES: self.downloaded_bytes,
            self.FIELD_TOTAL_BYTES: self.total_bytes,
            self.FIELD_CURRENT: self.current,
            self.FIELD_TOTAL: self.total,
            self.FIELD_MAX_ZOOM: self.max_zoom,
            self.FIELD_CANCEL_REQUESTED: self.cancel_requested,
            self.FIELD_CREATED_AT: self.created_at,
            self.FIELD_UPDATED_AT: self.updated_at,
            self.FIELD_ERROR: self.error,
            **({self.FIELD_IS_UPDATE: True} if self.is_update else {}),
            **({self.FIELD_PHASE: self.phase} if self.phase else {}),
        }

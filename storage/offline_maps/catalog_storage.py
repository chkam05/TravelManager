from __future__ import annotations

from typing import Any

from core.data.base_json_storage import BaseJsonStorage
from models.offline_maps.offline_map_region import OfflineMapRegion
from models.offline_maps.validation import iso_datetime


class OfflineMapCatalogStorage(BaseJsonStorage):
    """Stores the last valid downloadable-region catalog."""

    def __init__(self, directory):
        super().__init__(directory, 'catalog.json')

    def _initialize_default_data(self):
        return {'updated_at': '', 'regions': []}

    def load(self) -> tuple[str, list[OfflineMapRegion]]:
        data = self._read()
        rows = data.get('regions', [])
        if not isinstance(rows, list):
            return '', []
        try:
            return (
                iso_datetime(data.get('updated_at'), 'catalog update date'),
                OfflineMapRegion.from_dict_list(rows),
            )
        except (TypeError, ValueError):
            return '', []

    def save(self, updated_at: str, regions: list[OfflineMapRegion]) -> None:
        timestamp = iso_datetime(updated_at, 'catalog update date', optional=False)
        self._write({
            'updated_at': timestamp,
            'regions': self._unique_rows(regions),
        })

    @staticmethod
    def _unique_rows(regions: list[OfflineMapRegion]) -> list[dict[str, Any]]:
        result: list[dict[str, Any]] = []
        identifiers: set[str] = set()
        for region in regions:
            validated = OfflineMapRegion.from_dict(region.to_dict())
            if validated.id in identifiers:
                raise ValueError('Duplicate offline map region id.')
            identifiers.add(validated.id)
            result.append(validated.to_dict())
        return result

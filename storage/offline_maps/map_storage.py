from __future__ import annotations

from core.data.base_json_storage import BaseJsonStorage
from models.offline_maps.offline_map import OfflineMap


class OfflineMapStorage(BaseJsonStorage):
    """Stores the registry of completely installed map packages."""

    def __init__(self, directory):
        super().__init__(directory, 'installed_maps.json')

    def _initialize_default_data(self):
        return {'maps': []}

    def load(self) -> list[OfflineMap]:
        rows = self._read().get('maps', [])
        if not isinstance(rows, list):
            return []
        try:
            return OfflineMap.from_dict_list(rows)
        except (TypeError, ValueError):
            return []

    def save(self, maps: list[OfflineMap]) -> None:
        validated: list[OfflineMap] = []
        identifiers: set[str] = set()
        file_names: set[str] = set()
        for item in maps:
            mapped = OfflineMap.from_dict(item.to_dict())
            if mapped.id in identifiers or mapped.file_name in file_names:
                raise ValueError('Duplicate installed offline map.')
            identifiers.add(mapped.id)
            file_names.add(mapped.file_name)
            validated.append(mapped)
        self._write({'maps': self.to_dict_list(validated)})

    def add(self, offline_map: OfflineMap) -> None:
        """Atomically appends one installed package to the registry."""
        validated = OfflineMap.from_dict(offline_map.to_dict())
        with self._lock:
            self.save([*self.load(), validated])

    def upsert(self, offline_map: OfflineMap) -> None:
        """Atomically replaces metadata for one map or appends a new map."""
        validated = OfflineMap.from_dict(offline_map.to_dict())
        with self._lock:
            current = [item for item in self.load() if item.id != validated.id]
            self.save([*current, validated])

    @staticmethod
    def to_dict_list(items: list[OfflineMap]) -> list[dict]:
        return [item.to_dict() for item in items]

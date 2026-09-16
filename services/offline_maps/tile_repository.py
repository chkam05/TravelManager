from __future__ import annotations

from contextlib import closing
from pathlib import Path
import sqlite3

from models.offline_maps import OfflineMap
from models.offline_maps.validation import local_id
from storage.offline_maps import OfflineMapPaths


class OfflineMapTileReadError(RuntimeError):
    pass


class OfflineMapTileRepository:
    """Reads registered MBTiles packages without ever accepting a file path."""

    def __init__(self, paths: OfflineMapPaths):
        self._paths = paths

    def get(self, map_id: str, zoom: int, column: int, row: int) -> bytes | None:
        offline_map = self._registered_map(map_id)
        self._validate_coordinates(offline_map, zoom, column, row)
        path = self._paths.map_path(offline_map.file_name)
        if not path.is_file():
            raise OfflineMapTileReadError('Brak pliku zainstalowanej mapy offline.')
        tms_row = (1 << zoom) - 1 - row
        try:
            uri = path.resolve().as_uri() + '?mode=ro'
            with closing(sqlite3.connect(uri, uri=True)) as connection:
                result = connection.execute('''
                    SELECT tile_data FROM tiles
                    WHERE zoom_level = ? AND tile_column = ? AND tile_row = ?
                ''', (zoom, column, tms_row)).fetchone()
        except sqlite3.Error as error:
            raise OfflineMapTileReadError(
                'Nie udało się odczytać bazy MBTiles.'
            ) from error
        return bytes(result[0]) if result is not None else None

    def _registered_map(self, map_id: str) -> OfflineMap:
        identifier = local_id(map_id, 'map id')
        offline_map = next(
            (item for item in self._paths.maps.load() if item.id == identifier),
            None,
        )
        if offline_map is None:
            raise KeyError('Nie znaleziono mapy offline.')
        return offline_map

    @staticmethod
    def _validate_coordinates(
        offline_map: OfflineMap, zoom: int, column: int, row: int
    ) -> None:
        if type(zoom) is not int or not offline_map.min_zoom <= zoom <= offline_map.max_zoom:
            raise ValueError('Poziom przybliżenia jest poza zakresem mapy.')
        limit = 1 << zoom
        if (
            type(column) is not int or type(row) is not int
            or not 0 <= column < limit or not 0 <= row < limit
        ):
            raise ValueError('Nieprawidłowe współrzędne kafelka.')

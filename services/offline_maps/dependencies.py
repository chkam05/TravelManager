"""Lazy diagnostics for optional, heavyweight OSM processing libraries."""

from __future__ import annotations

from importlib.util import find_spec
from typing import ClassVar


class OfflineMapDependencyError(RuntimeError):
    pass


class OfflineMapDependencies:
    MODULES: ClassVar[dict[str, str]] = {
        'osmium': 'osmium',
        'shapely': 'shapely',
        'mercantile': 'mercantile',
        'mapbox-vector-tile': 'mapbox_vector_tile',
    }

    @classmethod
    def missing(cls) -> list[str]:
        return [
            package for package, module in cls.MODULES.items()
            if find_spec(module) is None
        ]

    @classmethod
    def require(cls) -> None:
        missing = cls.missing()
        if missing:
            raise OfflineMapDependencyError(
                'Brak bibliotek wymaganych do tworzenia map offline: '
                + ', '.join(missing)
                + '. Zainstaluj zależności z pliku requirements.txt.'
            )

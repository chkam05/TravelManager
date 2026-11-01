from __future__ import annotations

from contextlib import closing
import json
from pathlib import Path
import shutil
import sqlite3
from tempfile import TemporaryDirectory
import zipfile

from models.offline_maps import OfflineMap
from storage.offline_maps import OfflineMapPaths


class OfflineMapTransfer:
    """Imports and exports self-contained TravelManager offline map packages."""

    FORMAT_VERSION = 1
    MEMBERS = frozenset({'manifest.json', 'map.mbtiles', 'features.sqlite3'})

    def __init__(self, paths: OfflineMapPaths):
        self._paths = paths

    def export(self, map_id: str, destination: Path) -> None:
        installed = next((item for item in self._paths.maps.load() if item.id == map_id), None)
        if installed is None:
            raise ValueError('Nie znaleziono mapy offline.')
        package = self._paths.map_path(installed.file_name)
        features = self._paths.map_features_path(installed.id)
        if not package.is_file() or not features.is_file():
            raise ValueError('Mapa nie zawiera wszystkich danych potrzebnych do eksportu.')
        with zipfile.ZipFile(destination, 'w', allowZip64=True) as archive:
            archive.writestr('manifest.json', json.dumps({
                'format_version': self.FORMAT_VERSION, 'map': installed.to_dict(),
            }, ensure_ascii=False, indent=2))
            archive.write(package, 'map.mbtiles', compress_type=zipfile.ZIP_STORED)
            archive.write(features, 'features.sqlite3', compress_type=zipfile.ZIP_DEFLATED)

    def import_file(self, source: Path) -> OfflineMap:
        if not source.is_file() or source.suffix.lower() != '.tmmap':
            raise ValueError('Wybierz prawidłowy plik mapy .tmmap.')
        with TemporaryDirectory(dir=self._paths.root) as temporary:
            directory = Path(temporary)
            with zipfile.ZipFile(source) as archive:
                names = {item.filename for item in archive.infolist() if not item.is_dir()}
                if names != self.MEMBERS:
                    raise ValueError('Pakiet mapy ma nieprawidłową strukturę.')
                archive.extractall(directory)
            manifest = json.loads((directory / 'manifest.json').read_text(encoding='utf-8'))
            if manifest.get('format_version') != self.FORMAT_VERSION:
                raise ValueError('Wersja pakietu mapy nie jest obsługiwana.')
            installed = OfflineMap.from_dict(manifest.get('map'))
            if any(item.id == installed.id for item in self._paths.maps.load()):
                raise ValueError('Ta mapa jest już zainstalowana.')
            package, features = directory / 'map.mbtiles', directory / 'features.sqlite3'
            self._validate_sqlite(package, {'metadata', 'tiles'})
            self._validate_sqlite(features, {'features', 'feature_bounds'})
            target_package = self._paths.map_path(installed.file_name)
            target_features = self._paths.map_features_path(installed.id)
            if target_package.exists() or target_features.exists():
                raise ValueError('Pliki tej mapy już istnieją.')
            shutil.copy2(package, target_package)
            try:
                shutil.copy2(features, target_features)
                installed.size = target_package.stat().st_size + target_features.stat().st_size
                self._paths.maps.add(installed)
            except Exception:
                target_package.unlink(missing_ok=True)
                target_features.unlink(missing_ok=True)
                raise
            return installed

    @staticmethod
    def _validate_sqlite(path: Path, required_tables: set[str]) -> None:
        try:
            with closing(sqlite3.connect(f'file:{path}?mode=ro', uri=True, timeout=5)) as connection:
                if connection.execute('PRAGMA quick_check').fetchone() != ('ok',):
                    raise ValueError('Plik bazy mapy jest uszkodzony.')
                tables = {row[0] for row in connection.execute(
                    "SELECT name FROM sqlite_master WHERE type IN ('table', 'view')"
                )}
                if not required_tables <= tables:
                    raise ValueError('Pakiet nie zawiera wymaganych danych mapy.')
        except sqlite3.Error as error:
            raise ValueError('Nie udało się odczytać bazy mapy.') from error

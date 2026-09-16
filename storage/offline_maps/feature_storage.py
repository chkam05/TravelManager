from __future__ import annotations

import json
from pathlib import Path
import sqlite3
from typing import Iterable


class OfflineMapFeatureStorage:
    """Batch-oriented staging database for normalized OSM features."""

    FILE_NAME = 'features.sqlite3'

    def __init__(self, work_directory: Path):
        self.path = Path(work_directory) / self.FILE_NAME
        self._connection: sqlite3.Connection | None = None

    def create(self) -> None:
        self.close()
        try:
            self.path.unlink()
        except FileNotFoundError:
            pass
        self._connection = sqlite3.connect(self.path, timeout=30)
        self._connection.executescript('''
            PRAGMA journal_mode=WAL;
            PRAGMA synchronous=NORMAL;
            PRAGMA cache_size=-32768;
            PRAGMA busy_timeout=30000;
            CREATE TABLE features (
                id INTEGER PRIMARY KEY,
                osm_type TEXT NOT NULL,
                osm_id INTEGER NOT NULL,
                layer TEXT NOT NULL,
                geometry_type TEXT NOT NULL,
                geometry_wkb BLOB NOT NULL,
                min_zoom INTEGER NOT NULL,
                priority INTEGER NOT NULL,
                properties TEXT NOT NULL,
                min_lon REAL NOT NULL,
                min_lat REAL NOT NULL,
                max_lon REAL NOT NULL,
                max_lat REAL NOT NULL
            );
        ''')

    def insert_many(self, rows: Iterable[tuple]) -> None:
        if self._connection is None:
            raise RuntimeError('Feature storage is not open.')
        self._connection.executemany('''
            INSERT INTO features (
                osm_type, osm_id, layer, geometry_type, geometry_wkb,
                min_zoom, priority, properties,
                min_lon, min_lat, max_lon, max_lat
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', rows)
        self._connection.commit()

    def finalize(self) -> None:
        if self._connection is None:
            raise RuntimeError('Feature storage is not open.')
        self._connection.executescript('''
            CREATE INDEX features_layer_zoom
                ON features(layer, min_zoom, priority);
            CREATE INDEX features_bounds
                ON features(min_lon, max_lon, min_lat, max_lat);
            CREATE INDEX features_osm_object
                ON features(osm_type, osm_id);
            ANALYZE;
        ''')
        self._connection.commit()

    def metadata(self, key: str, value: object) -> None:
        if self._connection is None:
            raise RuntimeError('Feature storage is not open.')
        self._connection.execute('''
            CREATE TABLE IF NOT EXISTS metadata (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            )
        ''')
        self._connection.execute(
            'INSERT OR REPLACE INTO metadata(key, value) VALUES (?, ?)',
            (key, json.dumps(value, ensure_ascii=False)),
        )
        self._connection.commit()

    def count(self) -> int:
        if self._connection is not None:
            row = self._connection.execute(
                'SELECT COUNT(*) FROM features'
            ).fetchone()
        else:
            with sqlite3.connect(self.path, timeout=30) as connection:
                row = connection.execute('SELECT COUNT(*) FROM features').fetchone()
        return int(row[0])

    def close(self) -> None:
        if self._connection is not None:
            self._connection.close()
            self._connection = None

    def __enter__(self):
        self.create()
        return self

    def __exit__(self, *_):
        self.close()

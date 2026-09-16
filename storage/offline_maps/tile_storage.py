from __future__ import annotations

from contextlib import closing
import json
from pathlib import Path
import sqlite3


class OfflineMapTileStorage:
    """Temporary, disk-backed tile assignments and encoded MVT output."""

    FILE_NAME = 'tiles.sqlite3'

    def __init__(self, work_directory: Path):
        self.path = Path(work_directory) / self.FILE_NAME
        self.connection: sqlite3.Connection | None = None

    def create(self, feature_database: Path) -> None:
        self.close()
        self.discard()
        self.connection = sqlite3.connect(self.path, timeout=30)
        self.connection.execute('ATTACH DATABASE ? AS source', (str(feature_database),))
        self.connection.executescript('''
            PRAGMA journal_mode=WAL;
            PRAGMA synchronous=NORMAL;
            PRAGMA cache_size=-32768;
            PRAGMA busy_timeout=30000;
            CREATE TABLE tile_features (
                zoom_level INTEGER NOT NULL,
                tile_column INTEGER NOT NULL,
                tile_row INTEGER NOT NULL,
                feature_id INTEGER NOT NULL,
                PRIMARY KEY (zoom_level, tile_column, tile_row, feature_id)
            ) WITHOUT ROWID;
            CREATE INDEX tile_features_by_feature
                ON tile_features(feature_id, zoom_level);
            CREATE TABLE generated_tiles (
                zoom_level INTEGER NOT NULL,
                tile_column INTEGER NOT NULL,
                tile_row INTEGER NOT NULL,
                tile_data BLOB NOT NULL,
                PRIMARY KEY (zoom_level, tile_column, tile_row)
            ) WITHOUT ROWID;
            CREATE TABLE metadata (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            );
        ''')

    def assign(self, rows: list[tuple[int, int, int, int]]) -> None:
        self._require().executemany('''
            INSERT OR IGNORE INTO tile_features(
                zoom_level, tile_column, tile_row, feature_id
            ) VALUES (?, ?, ?, ?)
        ''', rows)
        self._require().commit()

    def tile_coordinates(self):
        cursor = self._require().execute('''
            SELECT zoom_level, tile_column, tile_row
            FROM tile_features
            GROUP BY zoom_level, tile_column, tile_row
            ORDER BY zoom_level, tile_column, tile_row
        ''')
        yield from cursor

    def tile_features(self, zoom: int, column: int, row: int):
        return self._require().execute('''
            SELECT f.osm_id, f.layer, f.geometry_wkb, f.properties,
                   f.priority
            FROM tile_features AS tf
            JOIN source.features AS f ON f.id = tf.feature_id
            WHERE tf.zoom_level = ? AND tf.tile_column = ? AND tf.tile_row = ?
            ORDER BY f.priority, f.id
        ''', (zoom, column, row)).fetchall()

    def save_tile(self, zoom: int, column: int, row: int, data: bytes) -> None:
        self._require().execute('''
            INSERT OR REPLACE INTO generated_tiles(
                zoom_level, tile_column, tile_row, tile_data
            ) VALUES (?, ?, ?, ?)
        ''', (zoom, column, row, data))

    def assignment_count(self) -> int:
        row = self._require().execute('''
            SELECT COUNT(*) FROM (
                SELECT 1 FROM tile_features
                GROUP BY zoom_level, tile_column, tile_row
            )
        ''').fetchone()
        return int(row[0])

    def generated_stats(self) -> tuple[int, int | None, int | None]:
        row = self._require().execute('''
            SELECT COUNT(*), MIN(zoom_level), MAX(zoom_level)
            FROM generated_tiles
        ''').fetchone()
        return int(row[0]), row[1], row[2]

    def is_complete(self) -> bool:
        """Only a finalized tile store may be resumed at MBTiles packaging."""
        if not self.path.is_file():
            return False
        try:
            with closing(sqlite3.connect(f'file:{self.path}?mode=ro', uri=True, timeout=2)) as connection:
                tables = {
                    row[0] for row in connection.execute(
                        "SELECT name FROM sqlite_master WHERE type = 'table'"
                    )
                }
                if 'tile_features' in tables or not {'generated_tiles', 'metadata'} <= tables:
                    return False
                count = connection.execute('SELECT COUNT(*) FROM generated_tiles').fetchone()[0]
                metadata = connection.execute(
                    "SELECT value FROM metadata WHERE key = 'tile_count'"
                ).fetchone()
                return bool(metadata and count > 0 and int(json.loads(metadata[0])) == count)
        except (OSError, sqlite3.Error, ValueError, TypeError):
            return False

    def set_metadata(self, key: str, value: object) -> None:
        self._require().execute(
            'INSERT OR REPLACE INTO metadata(key, value) VALUES (?, ?)',
            (key, json.dumps(value, ensure_ascii=False)),
        )

    def finalize(self) -> None:
        connection = self._require()
        connection.execute('DROP TABLE tile_features')
        connection.commit()

    def commit(self) -> None:
        self._require().commit()

    def close(self) -> None:
        if self.connection is not None:
            self.connection.close()
            self.connection = None

    def discard(self) -> None:
        self.close()
        for suffix in ('', '-wal', '-shm'):
            try:
                Path(str(self.path) + suffix).unlink()
            except FileNotFoundError:
                pass

    def _require(self) -> sqlite3.Connection:
        if self.connection is None:
            raise RuntimeError('Tile storage is not open.')
        return self.connection

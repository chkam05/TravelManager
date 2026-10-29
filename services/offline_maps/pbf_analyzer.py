from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path
import sqlite3
from typing import Callable

from models.offline_maps import OfflineMapJob
from resources.offline_maps import OfflineMapLayers
from services.offline_maps.dependencies import OfflineMapDependencies
from services.offline_maps.errors import (
    OfflineMapAnalysisCancelled,
    OfflineMapAnalysisError,
)
from services.offline_maps.resource_guard import OfflineMapResourceGuard
from services.offline_maps.package_reuse import OfflineMapPackageReuse
from storage.offline_maps import OfflineMapFeatureStorage, OfflineMapPaths


class OfflineMapPbfAnalyzer:
    """Streams OSM objects into a bounded, normalized SQLite staging store."""

    BATCH_SIZE = 500
    PROGRESS_INTERVAL = 5000

    def __init__(self, paths: OfflineMapPaths):
        self._paths = paths
        self._resources = OfflineMapResourceGuard(paths.root)
        self._reuse = OfflineMapPackageReuse(paths)

    def process(
        self,
        job: OfflineMapJob,
        cancelled: Callable[[], bool],
        progress: Callable[[OfflineMapJob, int, int], None] | None = None,
    ) -> str:
        OfflineMapDependencies.require()
        source = self._paths.source_path(job.id)
        if not source.is_file():
            raise OfflineMapAnalysisError('Brak pobranego pliku OSM PBF.')
        self._resources.ensure_stage(source.stat().st_size, 'analiza')
        work = self._paths.job_work_path(job.id)
        index_path = work / 'node-locations.idx'
        self._remove(index_path)
        storage = OfflineMapFeatureStorage(work)
        handler = None
        try:
            storage.create()
            reused_maps = self._reuse.reusable_maps(job)
            reused_features = storage.import_from(
                self._paths.map_features_path(item.id) for item in reused_maps
            )
            handler = self._create_handler(storage, job, cancelled, progress, source)
            handler.apply_file(
                str(source),
                locations=True,
                idx=f'sparse_file_array,{index_path}',
            )
            handler.finish()
            storage.metadata('processed_objects', handler.processed)
            storage.metadata('stored_features', handler.stored)
            storage.metadata('source_size', source.stat().st_size)
            storage.metadata('schema_version', 1)
            storage.metadata('reused_features', reused_features)
            storage.metadata('reused_map_ids', [item.id for item in reused_maps])
            try:
                storage.finalize(cancelled)
            except sqlite3.OperationalError as error:
                if cancelled():
                    raise OfflineMapAnalysisCancelled(
                        'Analizowanie mapy zostało anulowane.'
                    ) from error
                raise
            self._report(job, handler.processed, handler.processed, progress)
            return 'building_tiles'
        except OfflineMapAnalysisCancelled:
            self._discard_database(storage)
            raise
        except Exception as error:
            self._discard_database(storage)
            if isinstance(error, OfflineMapAnalysisError):
                raise
            raise OfflineMapAnalysisError(
                f'Nie udało się przeanalizować danych OSM: {error}'
            ) from error
        finally:
            storage.close()

    def _create_handler(self, storage, job, cancelled, progress, source: Path):
        import osmium
        from shapely import from_wkb, make_valid, to_wkb
        from shapely.ops import unary_union

        owner = self
        factory = osmium.geom.WKBFactory()

        class Handler(osmium.SimpleHandler):
            def __init__(self):
                super().__init__()
                self.rows: list[tuple] = []
                self.processed = 0
                self.stored = 0

            def node(self, node):
                self._tick()
                tags = self._tags(node.tags)
                layers = OfflineMapLayers.matching('node', 'point', tags)
                if not layers or not node.location.valid():
                    return
                self._store('node', node.id, 'point', tags, layers, (
                    lambda: factory.create_point(node)
                ))

            def way(self, way):
                self._tick()
                tags = self._tags(way.tags)
                layers = list(OfflineMapLayers.matching('way', 'line', tags))
                if way.is_closed() and OfflineMapLayers.matching(
                    'way', 'polygon', tags
                ):
                    # Closed area ways are emitted by area(), while genuinely
                    # linear features such as roundabouts remain here.
                    layers = [item for item in layers if item.id in {'roads', 'railways'}]
                if not layers:
                    return
                self._store('way', way.id, 'line', tags, layers, (
                    lambda: factory.create_linestring(way)
                ))

            def relation(self, _relation):
                # Multipolygon and boundary relations are emitted by area().
                self._tick()

            def area(self, area):
                self._tick()
                tags = self._tags(area.tags)
                source_type = 'way' if area.from_way() else 'relation'
                polygon_layers = OfflineMapLayers.matching(
                    source_type, 'polygon', tags
                )
                point_layers = OfflineMapLayers.matching(
                    source_type, 'point', tags
                )
                if not polygon_layers and not point_layers:
                    return
                osm_id = area.orig_id()
                if storage.contains_reused_object(source_type, osm_id):
                    return
                try:
                    raw = factory.create_multipolygon(area)
                    geometry = self._geometry(raw)
                except Exception:
                    return
                if polygon_layers:
                    self._append_geometry(
                        source_type, osm_id, 'polygon', tags,
                        polygon_layers, geometry,
                    )
                if point_layers and not geometry.is_empty:
                    self._append_geometry(
                        source_type, osm_id, 'point', tags,
                        point_layers, geometry.representative_point(),
                    )

            def finish(self):
                self._flush()

            def _tick(self):
                if cancelled():
                    raise OfflineMapAnalysisCancelled(
                        'Analiza mapy została anulowana.'
                    )
                self.processed += 1
                if self.processed % owner.PROGRESS_INTERVAL == 0:
                    owner._resources.ensure_stage(
                        source.stat().st_size, 'analiza'
                    )
                    owner._report(job, self.processed, 0, progress)

            @staticmethod
            def _tags(tag_list):
                required = OfflineMapLayers.required_tags()
                return {
                    tag.k: tag.v for tag in tag_list if tag.k in required
                }

            def _store(
                self, osm_type, osm_id, geometry_type, tags, layers, builder
            ):
                if storage.contains_reused_object(osm_type, osm_id):
                    return
                try:
                    geometry = self._geometry(builder())
                except Exception:
                    return
                self._append_geometry(
                    osm_type, osm_id, geometry_type, tags, layers, geometry
                )

            @staticmethod
            def _geometry(raw):
                data = bytes.fromhex(raw) if isinstance(raw, str) else raw
                geometry = from_wkb(data)
                if not geometry.is_valid:
                    geometry = make_valid(geometry)
                return geometry

            def _append_geometry(
                self, osm_type, osm_id, geometry_type, tags, layers, geometry
            ):
                geometry = self._matching_dimension(geometry, geometry_type)
                if geometry is None or geometry.is_empty:
                    return
                bounds = geometry.bounds
                if (
                    len(bounds) != 4
                    or bounds[0] < -180 or bounds[2] > 180
                    or bounds[1] < -90 or bounds[3] > 90
                ):
                    return
                encoded = to_wkb(geometry)
                for layer in layers:
                    self.rows.append((
                        osm_type, int(osm_id), layer.id, geometry_type, encoded,
                        layer.minimum_zoom(tags), layer.priority,
                        json.dumps(
                            layer.mvt_properties(tags),
                            ensure_ascii=False,
                            separators=(',', ':'),
                            sort_keys=True,
                        ),
                        *bounds,
                    ))
                    self.stored += 1
                    if len(self.rows) >= owner.BATCH_SIZE:
                        self._flush()

            @staticmethod
            def _matching_dimension(geometry, geometry_type):
                accepted = {
                    'point': {'Point', 'MultiPoint'},
                    'line': {'LineString', 'MultiLineString'},
                    'polygon': {'Polygon', 'MultiPolygon'},
                }[geometry_type]
                if geometry.geom_type in accepted:
                    return geometry
                if not hasattr(geometry, 'geoms'):
                    return None
                parts = [
                    part for part in geometry.geoms if part.geom_type in accepted
                ]
                return unary_union(parts) if parts else None

            def _flush(self):
                if self.rows:
                    storage.insert_many(self.rows)
                    self.rows.clear()

        return Handler()

    def _report(self, job, current, total, callback):
        job.status = 'running'
        job.stage = 'analysing'
        job.current = current
        job.total = total
        job.updated_at = datetime.now(timezone.utc).isoformat()
        self._paths.jobs.upsert(job)
        if callback:
            callback(job, current, total)

    @staticmethod
    def _remove(path: Path) -> None:
        try:
            path.unlink()
        except FileNotFoundError:
            pass

    def _discard_database(self, storage: OfflineMapFeatureStorage) -> None:
        storage.close()
        for suffix in ('', '-wal', '-shm'):
            self._remove(Path(str(storage.path) + suffix))

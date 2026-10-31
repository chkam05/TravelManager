from __future__ import annotations

from typing import ClassVar
from contextlib import closing
import json
import sqlite3

from flask import Response, jsonify, request
from hashlib import sha256
import gzip

from core.api.base_controller import BaseController
from services.offline_maps import (
    OfflineMapCatalogError,
    OfflineMapCatalogService,
    OfflineMapJobManager,
    OfflineMapPbfAnalyzer,
    OfflineMapTileGenerator,
    OfflineMapMbtilesBuilder,
    OfflineMapCleanupService,
    OfflineMapTileReadError,
    OfflineMapTileRepository,
    OfflineMapResourceGuard,
    OfflineMapPackageReuse,
)
from services.offline_maps.catalog_localization import localized_catalog
from services.offline_maps.errors import OfflineMapTileGenerationError
from services.offline_maps.pbf_metadata import pbf_metadata
from models.offline_maps.validation import local_id
from storage.offline_maps import OfflineMapPaths
from storage.settings_storage import SettingsStorage


class OfflineMapController(BaseController):
    CONTROLLER_NAME: ClassVar[str] = 'OfflineMapController'

    def __init__(
        self, settings_storage: SettingsStorage, start_manager: bool = False
    ):
        self._settings_storage = settings_storage
        self._paths = OfflineMapPaths(settings_storage.directory)
        self._catalog = OfflineMapCatalogService(self._paths.catalog)
        self._jobs = OfflineMapJobManager(self._paths)
        self._analyser = OfflineMapPbfAnalyzer(self._paths)
        self._tile_generator = OfflineMapTileGenerator(self._paths)
        self._mbtiles_builder = OfflineMapMbtilesBuilder(self._paths)
        self._cleanup = OfflineMapCleanupService(self._paths)
        self._tiles = OfflineMapTileRepository(self._paths)
        self._resources = OfflineMapResourceGuard(self._paths.root)
        self._reuse = OfflineMapPackageReuse(self._paths)
        self._pbf_metadata = pbf_metadata
        self._cleanup.cleanup_orphans()
        self._jobs.register_processor('analysing', self._analyser.process)
        self._jobs.register_processor(
            'building_tiles', self._tile_generator.process
        )
        self._jobs.register_processor(
            'optimising', self._mbtiles_builder.process
        )
        self._jobs.register_processor('installing', self._cleanup.process)
        if start_manager:
            self._jobs.start()
        super().__init__()

    def register_routes(self):
        self.add_url_rule(
            '/api/offline-maps/catalog', view_func=self.catalog, methods=['GET']
        )
        self.add_url_rule(
            '/api/offline-maps/catalog/refresh',
            view_func=self.refresh_catalog,
            methods=['POST'],
        )
        self.add_url_rule(
            '/api/offline-maps', view_func=self.installed_maps, methods=['GET']
        )
        self.add_url_rule(
            '/api/offline-maps/<map_id>/metadata',
            view_func=self.map_metadata,
            methods=['GET'],
        )
        self.add_url_rule(
            '/api/offline-maps/<map_id>/levels',
            view_func=self.map_levels, methods=['GET', 'POST', 'DELETE'],
        )
        self.add_url_rule(
            '/api/offline-maps/<map_id>',
            view_func=self.delete_map,
            methods=['DELETE'],
        )
        self.add_url_rule(
            '/api/offline-maps/<map_id>/update',
            view_func=self.update_map, methods=['POST'],
        )
        self.add_url_rule(
            '/api/offline-maps/<map_id>/continue-generation',
            view_func=self.continue_generation, methods=['POST'],
        )
        self.add_url_rule(
            '/api/offline-maps/<map_id>/generate-next-level',
            view_func=self.generate_next_level, methods=['POST'],
        )
        self.add_url_rule(
            '/api/offline-maps/jobs', view_func=self.map_jobs,
            methods=['GET', 'POST'],
        )
        self.add_url_rule(
            '/api/offline-maps/preflight/<path:region_id>',
            view_func=self.map_preflight, methods=['GET'],
        )
        self.add_url_rule(
            '/api/offline-maps/jobs/<job_id>', view_func=self.map_job,
            methods=['GET'],
        )
        self.add_url_rule(
            '/api/offline-maps/jobs/<job_id>/cancel',
            view_func=self.cancel_map_job,
            methods=['POST'],
        )
        self.add_url_rule(
            '/api/offline-maps/jobs/<job_id>/skip-building',
            view_func=self.skip_map_job_building,
            methods=['POST'],
        )
        self.add_url_rule(
            '/api/offline-maps/jobs/<job_id>/resume',
            view_func=self.resume_map_job,
            methods=['POST'],
        )
        self.add_url_rule(
            '/api/offline-maps/<map_id>/tiles/<int:zoom>/<int:column>/<int:row>.pbf',
            view_func=self.map_tile,
            methods=['GET'],
        )

    def catalog(self):
        try:
            result = self._catalog.get()
        except OfflineMapCatalogError as error:
            return jsonify({'status': 'error', 'message': str(error)}), 503
        return jsonify(self._serialize(result))

    def refresh_catalog(self):
        started = self._catalog.refresh_async()
        return jsonify({
            'status': 'started' if started else 'already_running',
            'refreshing': True,
        }), 202

    def installed_maps(self):
        regions = self._paths.catalog.load()[1]
        localized = {
            item['id']: item['name']
            for item in localized_catalog(regions)
        }
        coverage = {item.id: item.coverage for item in regions}
        return jsonify({
            'maps': [{
                **item.to_dict(),
                'size': self._installed_size(item),
                'display_max_zoom': (
                    self._dynamic_max_zoom()
                    if self._paths.map_features_path(item.id).is_file()
                    else item.max_zoom
                ),
                'region_name': localized.get(item.region_id, item.name),
                'coverage': coverage.get(item.region_id),
                'covered_maps': [
                    {'id': child.id, 'name': child.name}
                    for child in self._reuse.covered_maps(item.region_id, item.id)
                ],
            } for item in self._paths.maps.load()]
        })

    def map_metadata(self, map_id: str):
        identifier, error = self._validated_map_id(map_id)
        if error:
            return error
        installed = self._find_map(identifier)
        if installed is None:
            return jsonify({
                'status': 'error', 'message': 'Nie znaleziono mapy offline.'
            }), 404
        return jsonify({'map': installed.to_dict()})

    def map_levels(self, map_id: str):
        identifier, error = self._validated_map_id(map_id)
        if error:
            return error
        installed = self._find_map(identifier)
        if installed is None:
            return jsonify({'status': 'error', 'message': 'Nie znaleziono mapy offline.'}), 404
        if request.method == 'GET':
            return jsonify({'levels': self._map_level_rows(installed)})
        payload = request.get_json(silent=True)
        levels = payload.get('levels') if isinstance(payload, dict) else None
        if (
            not isinstance(levels, list) or not levels
            or any(type(level) is not int or not 10 <= level <= 19 for level in levels)
        ):
            return jsonify({'status': 'error', 'message': 'Nieprawidłowa lista poziomów.'}), 400
        levels = sorted(set(levels))
        if request.method == 'POST':
            complete = {
                row['zoom'] for row in self._map_level_rows(installed)
                if row['status'] == 'complete'
            }
            pending = [level for level in levels if level not in complete]
            if not pending:
                return jsonify({'status': 'unchanged', 'skipped_levels': levels})
            try:
                job = self._jobs.create_generation(
                    installed.id, max(pending), zoom_levels=pending
                )
            except ValueError as generation_error:
                return jsonify({'status': 'error', 'message': str(generation_error)}), 409
            return jsonify({
                'status': 'queued', 'job': job.to_dict(),
                'skipped_levels': sorted(set(levels) - set(pending)),
            }), 202
        if 10 in levels:
            return jsonify({
                'status': 'error', 'message': 'Poziomu x10 nie można usunąć.'
            }), 400
        if any(
            job.map_id == installed.id and job.status in {'queued', 'running'}
            for job in self._jobs.list()
        ):
            return jsonify({
                'status': 'error', 'message': 'Nie można usuwać poziomów podczas generowania.'
            }), 409
        self._delete_map_levels(installed, levels)
        return jsonify({'status': 'deleted', 'levels': levels})

    def _map_level_rows(self, installed):
        path = self._paths.map_path(installed.file_name)
        with closing(sqlite3.connect(path, timeout=30)) as connection:
            metadata = dict(connection.execute('SELECT name, value FROM metadata'))
            counts = dict(connection.execute('''
                SELECT zoom_level, COUNT(*) FROM tiles
                WHERE zoom_level BETWEEN 10 AND 19 GROUP BY zoom_level
            '''))
        try:
            complete = set(json.loads(metadata.get('travelmanager_complete_zooms', '[]')))
        except (TypeError, ValueError):
            complete = set()
        if not complete:
            try:
                complete = set(range(int(metadata['minzoom']), int(metadata['maxzoom']) + 1))
            except (KeyError, TypeError, ValueError):
                complete = set()
        return [{
            'zoom': zoom,
            'status': 'complete' if zoom in complete else ('partial' if counts.get(zoom, 0) else 'missing'),
            'tile_count': int(counts.get(zoom, 0)),
            'percent': 100 if zoom in complete else None,
            'removable': zoom != 10,
        } for zoom in range(10, 20)]

    def _delete_map_levels(self, installed, levels):
        path = self._paths.map_path(installed.file_name)
        with closing(sqlite3.connect(path, timeout=30)) as connection:
            connection.execute('PRAGMA busy_timeout=30000')
            placeholders = ','.join('?' for _ in levels)
            connection.execute(
                f'DELETE FROM tiles WHERE zoom_level IN ({placeholders})', levels
            )
            metadata = dict(connection.execute('SELECT name, value FROM metadata'))
            try:
                complete = set(json.loads(metadata.get('travelmanager_complete_zooms', '[]')))
            except (TypeError, ValueError):
                complete = set(range(installed.min_zoom, installed.max_zoom + 1))
            complete.difference_update(levels)
            maximum = connection.execute('SELECT MAX(zoom_level) FROM tiles').fetchone()[0]
            maximum = int(maximum if maximum is not None else 10)
            connection.execute(
                "INSERT OR REPLACE INTO metadata(name,value) VALUES('travelmanager_complete_zooms',?)",
                (json.dumps(sorted(complete)),),
            )
            connection.execute(
                "INSERT OR REPLACE INTO metadata(name,value) VALUES('maxzoom',?)",
                (str(maximum),),
            )
            connection.commit()
        installed.max_zoom = maximum
        installed.size = self._installed_size(installed)
        self._paths.maps.upsert(installed)

    def delete_map(self, map_id: str):
        identifier, error = self._validated_map_id(map_id)
        if error:
            return error
        installed = self._find_map(identifier)
        if installed is None:
            return jsonify({
                'status': 'error', 'message': 'Nie znaleziono mapy offline.'
            }), 404
        if any(
            job.map_id == identifier and job.status in {'queued', 'running'}
            for job in self._paths.jobs.load()
        ):
            return jsonify({
                'status': 'error',
                'message': 'Nie można usunąć mapy podczas jej przetwarzania.',
            }), 409

        # Resolve and validate the registered path before modifying the registry.
        package = self._paths.map_path(installed.file_name)
        retained = [
            item for item in self._paths.maps.load() if item.id != identifier
        ]
        self._paths.maps.save(retained)
        try:
            package.unlink()
        except FileNotFoundError:
            pass
        except OSError as error:
            # Restore metadata if the package could not be removed.
            self._paths.maps.save([*retained, installed])
            return jsonify({'status': 'error', 'message': str(error)}), 500
        self._paths.delete_map_features(identifier)
        return jsonify({'status': 'ok', 'deleted_map_id': identifier})

    def map_jobs(self):
        if request.method == 'GET':
            return jsonify({
                'jobs': [job.to_dict() for job in self._jobs.list()]
            })
        payload = request.get_json(silent=True)
        if not isinstance(payload, dict):
            return jsonify({
                'status': 'error', 'message': 'Nieprawidłowe dane zadania.'
            }), 400
        try:
            job = self._jobs.create(
                str(payload.get('region_id') or ''),
                payload.get('max_zoom', 10),
            )
        except (TypeError, ValueError) as error:
            return jsonify({'status': 'error', 'message': str(error)}), 400
        return jsonify({'status': 'queued', 'job': job.to_dict()}), 202

    def update_map(self, map_id: str):
        try:
            payload = request.get_json(silent=True)
            if payload is not None and not isinstance(payload, dict):
                raise ValueError('Nieprawidłowe dane zadania.')
            job = self._jobs.create_update(
                map_id, (payload or {}).get('max_zoom', 10)
            )
        except (TypeError, ValueError) as error:
            return jsonify({'status': 'error', 'message': str(error)}), 400
        return jsonify({'status': 'queued', 'job': job.to_dict()}), 202

    def continue_generation(self, map_id: str):
        installed = self._find_map(map_id)
        if installed is None:
            return jsonify({'status': 'error', 'message': 'Nie znaleziono mapy offline.'}), 404
        targets = [
            job.max_zoom for job in self._jobs.list()
            if job.map_id == installed.id and job.max_zoom > installed.max_zoom
        ]
        if not targets:
            return jsonify({
                'status': 'error',
                'message': 'Ta mapa nie ma pominiętych poziomów do kontynuowania.',
            }), 409
        try:
            job = self._jobs.create_generation(installed.id, min(19, max(targets)))
        except ValueError as error:
            return jsonify({'status': 'error', 'message': str(error)}), 409
        return jsonify({'status': 'queued', 'job': job.to_dict()}), 202

    def generate_next_level(self, map_id: str):
        installed = self._find_map(map_id)
        if installed is None:
            return jsonify({'status': 'error', 'message': 'Nie znaleziono mapy offline.'}), 404
        target = installed.max_zoom + 1
        if target > self._dynamic_max_zoom():
            return jsonify({
                'status': 'error',
                'message': 'Mapa ma już przygotowany maksymalny dozwolony poziom.',
            }), 409
        try:
            job = self._jobs.create_generation(installed.id, target)
        except ValueError as error:
            return jsonify({'status': 'error', 'message': str(error)}), 409
        return jsonify({'status': 'queued', 'job': job.to_dict()}), 202

    def map_preflight(self, region_id: str):
        try:
            selected_region = next(
                (item for item in self._paths.catalog.load()[1]
                 if item.id == region_id), None
        )
        except ValueError as error:
            return jsonify({'status': 'error', 'message': str(error)}), 400
        if selected_region is None or not selected_region.pbf_url:
            return jsonify({
                'status': 'error', 'message': 'Region nie jest dostępny do pobrania.'
            }), 404
        map_id = self._jobs.map_id(region_id)
        metadata = self._pbf_metadata(selected_region.pbf_url)
        source_size = metadata['source_size'] or selected_region.pbf_size
        required_space = self._resources.required_for_download(source_size)
        estimated_map_size = round(source_size * 2.5) if source_size is not None else None
        available_space = self._resources.available()
        return jsonify({
            'status': 'ok',
            'region_id': region_id,
            'map_id': map_id,
            'source_size': source_size,
            'source_modified_at': metadata['source_modified_at'] or selected_region.source_updated_at,
            'estimated_map_size': estimated_map_size,
            'required_space': required_space,
            'available_space': available_space,
            'enough_space': available_space >= required_space,
            'installed': any(item.id == map_id for item in self._paths.maps.load()),
            'active_job': any(
                item.map_id == map_id and item.status in self._jobs.ACTIVE_STATUSES
                for item in self._paths.jobs.load()
            ),
        })

    def map_job(self, job_id: str):
        try:
            job = self._jobs.find(job_id)
        except ValueError as error:
            return jsonify({'status': 'error', 'message': str(error)}), 400
        if job is None:
            return jsonify({
                'status': 'error', 'message': 'Nie znaleziono zadania mapy.'
            }), 404
        return jsonify({'job': job.to_dict()})

    def cancel_map_job(self, job_id: str):
        try:
            job = self._jobs.cancel(job_id)
        except ValueError as error:
            return jsonify({'status': 'error', 'message': str(error)}), 400
        if job is None:
            return jsonify({
                'status': 'error', 'message': 'Nie znaleziono zadania mapy.'
            }), 404
        return jsonify({'status': 'cancelling', 'job': job.to_dict()}), 202

    def skip_map_job_building(self, job_id: str):
        try:
            job = self._jobs.skip_detailed_building(job_id)
        except ValueError as error:
            return jsonify({'status': 'error', 'message': str(error)}), 409
        if job is None:
            return jsonify({
                'status': 'error', 'message': 'Nie znaleziono zadania mapy.'
            }), 404
        return jsonify({'status': 'skipping', 'job': job.to_dict()}), 202

    def resume_map_job(self, job_id: str):
        try:
            job = self._jobs.resume(job_id)
        except ValueError as error:
            return jsonify({'status': 'error', 'message': str(error)}), 400
        if job is None:
            return jsonify({
                'status': 'error', 'message': 'Nie znaleziono zadania mapy.'
            }), 404
        return jsonify({'status': 'queued', 'job': job.to_dict()}), 202

    def map_tile(
        self, map_id: str, zoom: int, column: int, row: int
    ):
        try:
            payload = self._tiles.get(
                map_id, zoom, column, row, self._dynamic_max_zoom()
            )
        except KeyError as error:
            return jsonify({'status': 'error', 'message': str(error.args[0])}), 404
        except ValueError as error:
            return jsonify({'status': 'error', 'message': str(error)}), 400
        except (OfflineMapTileReadError, OfflineMapTileGenerationError) as error:
            return jsonify({'status': 'error', 'message': str(error)}), 500
        if payload is None:
            return Response(status=204)
        try:
            tile = gzip.decompress(payload)
        except (OSError, EOFError) as error:
            return jsonify({
                'status': 'error',
                'message': 'Kafelek mapy offline jest uszkodzony.',
            }), 500
        response = Response(
            tile,
            status=200,
            content_type='application/vnd.mapbox-vector-tile',
        )
        response.headers['Cache-Control'] = 'private, max-age=3600'
        response.set_etag(sha256(payload).hexdigest())
        return response.make_conditional(request)

    def stop(self) -> None:
        self._jobs.stop()

    def _find_map(self, map_id: str):
        return next(
            (item for item in self._paths.maps.load() if item.id == map_id), None
        )

    def _dynamic_max_zoom(self) -> int:
        loader = getattr(self._settings_storage, 'load', None)
        if not callable(loader):
            return 19
        try:
            ui = loader().ui
            return int(ui.offline_map_max_dynamic_zoom) if ui else 19
        except (AttributeError, TypeError, ValueError, OSError):
            return 19

    def _installed_size(self, installed) -> int:
        total = 0
        for path in (
            self._paths.map_path(installed.file_name),
            self._paths.map_features_path(installed.id),
        ):
            try:
                total += path.stat().st_size
            except OSError:
                pass
        return total or installed.size

    @staticmethod
    def _validated_map_id(map_id: str):
        try:
            return local_id(map_id, 'map id'), None
        except ValueError as error:
            return '', (jsonify({'status': 'error', 'message': str(error)}), 400)

    def _serialize(self, result):
        return {
            **{key: value for key, value in result.items() if key != 'regions'},
            'regions': localized_catalog(result['regions']),
            'refreshing': self._catalog.refreshing,
            'last_error': self._catalog.last_error,
        }

"""Repeatable benchmark for full Polish Trains and WKD archives."""
from __future__ import annotations

import argparse
from datetime import date
import json
from pathlib import Path
import resource
import sys
from tempfile import TemporaryDirectory
from time import perf_counter

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from core.gtfs_database import GtfsDatabase
from utils.public_transport.rail_gtfs_repository import RailGtfsRepository


def milliseconds(start: float) -> float:
    return round((perf_counter() - start) * 1000, 2)


def peak_megabytes() -> float:
    value = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    # macOS reports bytes, Linux reports KiB.
    return round(value / (1024 * 1024 if value > 10_000_000 else 1024), 2)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--polish-trains', type=Path, required=True)
    parser.add_argument('--wkd', type=Path, required=True)
    args = parser.parse_args()
    results = {'archives_mb': {}}
    with TemporaryDirectory() as directory:
        databases = {}
        for source_id, archive_path in (
            ('polish_trains', args.polish_trains), ('wkd', args.wkd)
        ):
            payload = archive_path.read_bytes()
            results['archives_mb'][source_id] = round(len(payload) / 1024 / 1024, 2)
            destination = Path(directory) / f'{source_id}.sqlite3'
            started = perf_counter()
            GtfsDatabase.build(destination, {source_id: payload}, coverage_days=62)
            results.setdefault('build_ms', {})[source_id] = milliseconds(started)
            results.setdefault('database_mb', {})[source_id] = round(destination.stat().st_size / 1024 / 1024, 2)
            databases[source_id] = destination

        with GtfsDatabase.connect(databases['polish_trains']) as connection:
            coverage = GtfsDatabase.service_range(connection, 'polish_trains')
        service_date = max(date.today(), coverage[0]) if coverage else date.today()
        repository = RailGtfsRepository(
            'rail_pkp_intercity', databases['polish_trains'], realtime=False
        )
        started = perf_counter()
        stops = repository.download_stops(service_date=service_date)
        results['station_search_ms'] = milliseconds(started)
        results['station_count'] = len(stops)
        platform = next(
            (item for stop in stops for item in stop.platforms if item.url_all), None
        )
        if platform:
            stop_id = repository._query(platform.url_all).get('stop', '')
            started = perf_counter()
            departures = repository.departures(stop_id, service_date)
            results['departures_query_ms'] = milliseconds(started)
            results['sample_departures'] = len(departures)
        results['peak_rss_mb'] = peak_megabytes()
    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()

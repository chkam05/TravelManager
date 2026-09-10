"""Regression tests for railway-specific GTFS structures."""
from datetime import date
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
import sqlite3
from zipfile import ZIP_DEFLATED, ZipFile

from core.gtfs_database import GtfsDatabase


FIXTURE = Path(__file__).parent / 'fixtures' / 'gtfs' / 'rail_representative'


def fixture_payload() -> bytes:
    """Packages the readable fixture files in memory as a GTFS archive."""
    from io import BytesIO

    output = BytesIO()
    with ZipFile(output, 'w', ZIP_DEFLATED) as archive:
        for path in sorted(FIXTURE.glob('*.txt')):
            archive.writestr(path.name, path.read_bytes())
    return output.getvalue()


class RailGtfsFixtureTests(unittest.TestCase):
    def setUp(self):
        self.directory = TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.database_path = Path(self.directory.name) / 'rail.sqlite3'
        GtfsDatabase.build(
            self.database_path,
            {'polish_trains': fixture_payload()},
            coverage_days=32
        )

    def test_extended_time_and_boarding_rules_survive_import(self):
        with GtfsDatabase.connect(self.database_path) as connection:
            rows = connection.execute(
                """
                    SELECT arrival_time, departure_time,
                           pickup_type, drop_off_type, platform, track
                    FROM stop_times
                    WHERE feed_id = ? AND trip_id = ?
                    ORDER BY stop_sequence
                """,
                ('polish_trains', 'NIGHT_401')
            ).fetchall()
        self.assertEqual(rows[1]['arrival_time'], '24:12:00')
        self.assertEqual(rows[0]['drop_off_type'], 1)
        self.assertEqual(rows[1]['pickup_type'], 1)
        self.assertEqual((rows[0]['platform'], rows[0]['track']), ('1', '3'))

    def test_distinct_platforms_keep_parent_and_coordinates(self):
        with GtfsDatabase.connect(self.database_path) as connection:
            rows = connection.execute(
                """
                    SELECT stop_id, parent_station, platform_code,
                           latitude, longitude
                    FROM stops
                    WHERE feed_id = ? AND parent_station = ?
                    ORDER BY platform_code
                """,
                ('polish_trains', 'CENTRAL')
            ).fetchall()
        self.assertEqual(
            [(row['stop_id'], row['platform_code']) for row in rows],
            [('CENTRAL_1', '1'), ('CENTRAL_2', '2')]
        )
        self.assertEqual(
            (rows[0]['latitude'], rows[0]['longitude']),
            (rows[1]['latitude'], rows[1]['longitude'])
        )

    def test_calendar_exceptions_override_regular_weekday(self):
        with GtfsDatabase.connect(self.database_path) as connection:
            services = GtfsDatabase.active_service_ids(
                connection,
                'polish_trains',
                date(2030, 1, 1)
            )
        self.assertNotIn('WEEKDAY', services)
        self.assertIn('SPECIAL', services)

    def test_shape_is_available_for_rail_trip(self):
        with GtfsDatabase.connect(self.database_path) as connection:
            count = connection.execute(
                """
                    SELECT COUNT(*) FROM shapes
                    WHERE feed_id = ? AND shape_id = ?
                """,
                ('polish_trains', 'SHAPE_NIGHT')
            ).fetchone()[0]
        self.assertEqual(count, 3)

    def test_agency_feed_and_train_metadata_survive_import(self):
        with GtfsDatabase.connect(self.database_path) as connection:
            agency = connection.execute(
                'SELECT * FROM agencies WHERE feed_id = ? AND agency_id = ?',
                ('polish_trains', 'IC')
            ).fetchone()
            feed = connection.execute(
                'SELECT * FROM feed_info WHERE feed_id = ?',
                ('polish_trains',)
            ).fetchone()
            trip = connection.execute(
                'SELECT * FROM trips WHERE feed_id = ? AND trip_id = ?',
                ('polish_trains', 'NIGHT_401')
            ).fetchone()
            station = connection.execute(
                'SELECT * FROM stops WHERE feed_id = ? AND stop_id = ?',
                ('polish_trains', 'CENTRAL')
            ).fetchone()
        self.assertEqual(agency['timezone'], 'Europe/Warsaw')
        self.assertEqual(feed['version'], 'synthetic-1')
        self.assertEqual(trip['train_name'], 'TEST EXPRESS')
        self.assertEqual(trip['train_number'], '401')
        self.assertEqual(station['location_type'], 1)

    def test_international_stops_keep_source_country(self):
        with GtfsDatabase.connect(self.database_path) as connection:
            countries = connection.execute(
                "SELECT stop_id, country FROM stops WHERE feed_id = ? AND stop_id IN (?, ?)",
                ('polish_trains', 'CENTRAL', 'TERMINUS')
            ).fetchall()
        self.assertEqual({row['country'] for row in countries}, {'PL', 'DE'})

    def test_agency_and_feed_info_remain_optional_for_city_feeds(self):
        from io import BytesIO

        output = BytesIO()
        with ZipFile(output, 'w', ZIP_DEFLATED) as archive:
            for path in sorted(FIXTURE.glob('*.txt')):
                if path.name not in {'agency.txt', 'feed_info.txt'}:
                    archive.writestr(path.name, path.read_bytes())
        city_path = Path(self.directory.name) / 'city.sqlite3'
        GtfsDatabase.build(city_path, {'city': output.getvalue()})
        with GtfsDatabase.connect(city_path) as connection:
            self.assertEqual(
                connection.execute('SELECT COUNT(*) FROM trips').fetchone()[0],
                6
            )

    def test_existing_city_schema_version_remains_readable(self):
        connection = sqlite3.connect(self.database_path)
        try:
            connection.execute(
                "UPDATE metadata SET value = '3' WHERE key = 'schema_version'"
            )
            connection.commit()
        finally:
            connection.close()
        self.assertTrue(GtfsDatabase.is_valid_cache(self.database_path))


if __name__ == '__main__':
    unittest.main()

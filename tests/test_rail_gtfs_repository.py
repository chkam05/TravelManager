"""Pilot coverage for the shared railway repository."""
from datetime import date
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from core.gtfs_database import GtfsDatabase
from resources.public_transport.public_transport_messages import PublicTransportValueError
from resources.public_transport.public_transport_type import PublicTransportType
from tests.test_rail_gtfs_fixture import fixture_payload
from utils.public_transport.rail_gtfs_repository import RailGtfsRepository


class RailGtfsRepositoryTests(unittest.TestCase):
    SERVICE_DATE = date(2030, 1, 2)

    def setUp(self):
        self.directory = TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        root = Path(self.directory.name)
        self.polish_path = root / 'polish.sqlite3'
        self.wkd_path = root / 'wkd.sqlite3'
        payload = fixture_payload()
        GtfsDatabase.build(
            self.polish_path, {'polish_trains': payload}, coverage_days=32
        )
        GtfsDatabase.build(self.wkd_path, {'wkd': payload}, coverage_days=32)

    def test_pilot_providers_are_filtered_by_source_and_agency(self):
        intercity = RailGtfsRepository(
            'rail_pkp_intercity', self.polish_path
        ).download_lines(service_date=self.SERVICE_DATE)
        polregio = RailGtfsRepository(
            'rail_polregio', self.polish_path
        ).download_lines(service_date=self.SERVICE_DATE)
        wkd = RailGtfsRepository(
            'rail_wkd', self.wkd_path
        ).download_lines(service_date=self.SERVICE_DATE)
        self.assertEqual(
            [line.line for line in intercity],
            ['401 · TEST EXPRESS', '402 · TEST EXPRESS', '403 · TEST EXPRESS']
        )
        self.assertEqual([line.line for line in polregio], ['R'])
        self.assertEqual([line.line for line in wkd], ['WKD'])
        self.assertTrue(all(line.type == PublicTransportType.TRAIN
                            for line in intercity + polregio + wkd))

    def test_platforms_with_same_coordinates_remain_distinct(self):
        repository = RailGtfsRepository(
            'rail_pkp_intercity', self.polish_path
        )
        stops = repository.download_stops(service_date=self.SERVICE_DATE)
        central = next(stop for stop in stops if stop.name == 'Test Central')
        self.assertEqual(
            [platform.name for platform in central.platforms],
            ['1', '2']
        )
        self.assertEqual(
            (central.platforms[0].latitude, central.platforms[0].longitude),
            (central.platforms[1].latitude, central.platforms[1].longitude)
        )
        self.assertEqual(
            [line.line for line in central.platforms[0].lines],
            ['401 · TEST EXPRESS', '403 · TEST EXPRESS']
        )

    def test_overnight_ride_keeps_elapsed_time_and_train_identity(self):
        repository = RailGtfsRepository(
            'rail_pkp_intercity', self.polish_path
        )
        ride = repository.download_ride(repository.ride_url(
            'NIGHT_401', 'CENTRAL_1', self.SERVICE_DATE
        ))
        self.assertEqual(ride.line, '401 · TEST EXPRESS')
        self.assertEqual(ride.departure_time.hour, 23)
        self.assertEqual(ride.next_stops[0].departure_time.hour, 0)
        self.assertEqual(ride.next_stops[0].travel_time, 15)
        self.assertEqual(ride.carrier, 'Test Intercity')

    def test_forged_provider_scope_cannot_open_another_agencys_trip(self):
        intercity = RailGtfsRepository(
            'rail_pkp_intercity', self.polish_path
        )
        polregio = RailGtfsRepository(
            'rail_polregio', self.polish_path
        )
        foreign_url = polregio.ride_url(
            'REGIONAL_101', 'TERMINUS_1', self.SERVICE_DATE
        )
        with self.assertRaises(PublicTransportValueError):
            intercity.download_ride(foreign_url)

    def test_trip_query_still_rejects_foreign_trip_with_valid_scope(self):
        repository = RailGtfsRepository(
            'rail_pkp_intercity', self.polish_path
        )
        forged = repository.ride_url(
            'REGIONAL_101', 'TERMINUS_1', self.SERVICE_DATE
        )
        with self.assertRaises(PublicTransportValueError) as raised:
            repository.download_ride(forged)
        self.assertEqual(
            raised.exception.translation.key,
            'PUBLIC_TRANSPORT_ERROR.GTFS_TRIP_NOT_FOUND'
        )

    def test_departures_keep_train_numbers_and_respect_pickup_rules(self):
        repository = RailGtfsRepository(
            'rail_pkp_intercity', self.polish_path
        )
        departures = repository.departures('CENTRAL_1', self.SERVICE_DATE)
        self.assertEqual(len(departures), 2)
        night = next(item for item in departures if '401' in item.variant)
        self.assertIn('401 · TEST EXPRESS', night.variant)
        self.assertIn('NIGHT_401', night.url)
        self.assertEqual(
            repository.departures('TERMINUS_1', self.SERVICE_DATE),
            []
        )
        central_two = repository.departures('CENTRAL_2', self.SERVICE_DATE)
        self.assertEqual(len(central_two), 1)
        self.assertIn('402', central_two[0].variant)
        self.assertNotEqual(night.variant, central_two[0].variant)

    def test_geometry_uses_shape_and_foreign_trip_is_rejected(self):
        repository = RailGtfsRepository(
            'rail_pkp_intercity', self.polish_path
        )
        route = repository.route_for_trip('NIGHT_401', self.SERVICE_DATE)
        self.assertEqual(len(route), 3)
        self.assertEqual((route[0].latitude, route[0].longitude), (52.0, 21.0))
        with self.assertRaises(PublicTransportValueError):
            repository.route_for_trip('REGIONAL_101', self.SERVICE_DATE)

    def test_long_distance_train_is_a_line_with_relation_not_a_variant(self):
        repository = RailGtfsRepository(
            'rail_pkp_intercity', self.polish_path
        )
        listed_lines = repository.download_lines(service_date=self.SERVICE_DATE)
        self.assertEqual(
            listed_lines[0].direction,
            'Test Central – Test Terminus'
        )
        self.assertEqual(listed_lines[0].sort_name, 'TEST EXPRESS')
        line_url = listed_lines[0].url
        exact = repository.download_line(line_url)
        fallback_url = repository.download_lines(
            service_date=self.SERVICE_DATE
        )[-1].url
        fallback = repository.download_line(fallback_url)
        self.assertEqual(exact.line, '401 · TEST EXPRESS')
        self.assertEqual(exact.route_variants, {})
        self.assertEqual(
            exact.directions[0].name, 'Test Central → Test Terminus'
        )
        self.assertFalse(exact.directions[0].route_is_approximate)
        self.assertTrue(fallback.directions[0].route_is_approximate)
        self.assertEqual(len(fallback.directions[0].route), 2)

    def test_extended_time_uses_feed_timezone_and_next_calendar_day(self):
        repository = RailGtfsRepository(
            'rail_pkp_intercity', self.polish_path
        )
        value = repository.operational_datetime(
            self.SERVICE_DATE, '24:12:00'
        )
        self.assertEqual(value.date(), date(2030, 1, 3))
        self.assertEqual((value.hour, value.minute), (0, 12))
        self.assertEqual(value.tzinfo.key, 'Europe/Warsaw')

    def test_line_stop_timetable_stays_within_selected_route(self):
        repository = RailGtfsRepository(
            'rail_pkp_intercity', self.polish_path
        )
        line_url = repository.download_lines(
            service_date=self.SERVICE_DATE
        )[0].url
        line = repository.download_line(line_url)
        timetable = repository.download_line_stop_timetable(
            line.directions[0].stops[0].url
        )
        self.assertEqual(timetable.line, '401 · TEST EXPRESS')
        self.assertEqual(timetable.platform, '1')
        self.assertIn('rail_view=stop', timetable.stop_lines_url)
        self.assertIn('stop=CENTRAL_1', timetable.stop_lines_url)
        self.assertTrue(timetable.timetable[self.SERVICE_DATE].departures)
        self.assertTrue(all(
            'REGIONAL_101' not in item.url
            for item in timetable.timetable[self.SERVICE_DATE].departures
        ))
        self.assertEqual(
            len(timetable.timetable[self.SERVICE_DATE].departures), 1
        )

    def test_local_line_keeps_designation_and_exposes_both_relations(self):
        repository = RailGtfsRepository('rail_polregio', self.polish_path)
        listed_line = repository.download_lines(service_date=self.SERVICE_DATE)[0]
        self.assertIn('Test Central – Test Terminus', listed_line.direction)
        line_url = listed_line.url
        line = repository.download_line(line_url)
        self.assertEqual(line.line, 'R')
        self.assertEqual(line.route_variants, {})
        self.assertEqual(
            {direction.name for direction in line.directions},
            {
                'Test Terminus → Test Central',
                'Test Central → Test Terminus'
            }
        )

    def test_station_departure_view_contains_only_selected_operator(self):
        repository = RailGtfsRepository(
            'rail_pkp_intercity', self.polish_path
        )
        stops = repository.download_stops(service_date=self.SERVICE_DATE)
        central = next(stop for stop in stops if stop.name == 'Test Central')
        result = repository.download_stop_all(central.platforms[0].url_all)
        self.assertEqual(
            [line.line for line in result.lines],
            ['401 · TEST EXPRESS', '403 · TEST EXPRESS']
        )
        self.assertEqual(
            {timetable.direction_name for timetable in result.lines.values()},
            {'Test Terminus'}
        )
        self.assertTrue(all(
            'REGIONAL_101' not in departure.url
            for timetable in result.lines.values()
            for departure in timetable.departures
        ))

    def test_local_station_departure_view_keeps_line_and_direction(self):
        repository = RailGtfsRepository('rail_polregio', self.polish_path)
        stops = repository.download_stops(service_date=self.SERVICE_DATE)
        central = next(stop for stop in stops if stop.name == 'Test Central')
        platform = next(item for item in central.platforms if item.name == '1')
        result = repository.download_stop_all(platform.url_all)

        self.assertEqual([line.line for line in result.lines], ['R'])
        self.assertEqual(
            [timetable.direction_name for timetable in result.lines.values()],
            ['Test Terminus']
        )


if __name__ == '__main__':
    unittest.main()

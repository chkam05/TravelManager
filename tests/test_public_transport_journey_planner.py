from datetime import date
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
import sqlite3

from core.gtfs_database import GtfsDatabase
from services.public_transport_journey_planner import PublicTransportJourneyPlanner
from tests.test_rail_gtfs_fixture import fixture_payload
from utils.raptor import RaptorJourney, RaptorLeg


class PublicTransportJourneyPlannerTests(unittest.TestCase):
    def test_ranking_rejects_small_time_gain_with_backtracking_and_extra_transfers(self):
        planner = PublicTransportJourneyPlanner(Path('unused'))
        stops = {
            'A': {'latitude': 50.24, 'longitude': 18.99},
            'BACK': {'latitude': 50.23, 'longitude': 18.98},
            'MID': {'latitude': 50.27, 'longitude': 19.00},
            'D': {'latitude': 50.33, 'longitude': 18.94},
        }
        leg = lambda trip, start, end, departure, arrival: RaptorLeg(
            trip, trip, trip, 'bus', '', start, end,
            departure, arrival, 0, 1
        )
        detour = RaptorJourney((
            leg('12', 'A', 'BACK', 100, 280),
            leg('37', 'BACK', 'MID', 400, 800),
            leg('6', 'MID', 'D', 900, 1500),
        ))
        sensible = RaptorJourney((
            leg('12b', 'A', 'MID', 500, 900),
            leg('6b', 'MID', 'D', 1000, 1900),
        ))

        self.assertEqual(
            planner._rank_journeys([detour, sensible], stops, False),
            [sensible]
        )

    def test_catalog_groups_platforms_and_search_returns_display_payload(self):
        with TemporaryDirectory() as directory:
            path = Path(directory) / 'fixture.sqlite3'
            GtfsDatabase.build(path, {'fixture': fixture_payload()})
            with sqlite3.connect(path) as connection:
                connection.execute(
                    """INSERT INTO stops VALUES (
                        'fixture', 'CENTRAL_3', '03', 'Test Central', '',
                        52.0001, 21.0001, '', '3', '', 0, '', 0, 0, 'PL'
                    )"""
                )
                connection.commit()
            planner = PublicTransportJourneyPlanner(path)
            service_date = date(2026, 11, 2)
            catalog = planner.catalog(service_date)
            stops = catalog['cities'][0]['stops']

            self.assertEqual([stop['name'] for stop in stops], ['Test Central', 'Test Terminus'])
            result = planner.search(
                service_date, stops[0]['id'], stops[1]['id'],
                9 * 3600, False, 60
            )

            self.assertTrue(result['journeys'])
            journey = result['journeys'][0]
            self.assertEqual((journey['departure'], journey['arrival']), ('10:00', '10:15'))
            self.assertEqual(journey['legs'][0]['type'], 'train')
            self.assertGreater(journey['distance_km'], 0)
            self.assertGreater(len(journey['legs'][0]['geometry']), 2)

    def test_shape_section_keeps_forward_part_of_looping_shape(self):
        points = [
            [50.0, 19.0], [50.1, 19.1], [50.2, 19.2],
            [50.1, 19.1], [50.3, 19.3]
        ]

        section = PublicTransportJourneyPlanner._shape_section(
            points, [50.19, 19.19], [50.3, 19.3]
        )

        self.assertIn([50.2, 19.2], section)
        self.assertEqual(section[-1], [50.3, 19.3])

    def test_agency_filter_does_not_leak_other_rail_operators(self):
        with TemporaryDirectory() as directory:
            path = Path(directory) / 'fixture.sqlite3'
            GtfsDatabase.build(path, {'fixture': fixture_payload()})
            planner = PublicTransportJourneyPlanner(path, ('IC',))
            service_date = date(2026, 11, 2)
            with GtfsDatabase.connect(path) as connection:
                feeds = planner._active_feeds(connection, service_date)
                _stops, groups = planner._stops(connection, feeds)
                trips = planner._trips(connection, feeds, service_date, groups)

            self.assertTrue(trips)
            self.assertEqual({trip.line for trip in trips}, {'IC'})


if __name__ == '__main__':
    unittest.main()

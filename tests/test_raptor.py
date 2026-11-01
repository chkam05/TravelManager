import unittest

from utils.raptor import Raptor, RaptorFootpath, RaptorStopTime, RaptorTrip


def trip(identifier, line, stops):
    return RaptorTrip(
        identifier, line, line, 'bus', '',
        tuple(RaptorStopTime(stop, arrival, departure, index) for index, (stop, arrival, departure) in enumerate(stops))
    )


class RaptorTests(unittest.TestCase):
    def setUp(self):
        self.router = Raptor([
            trip('slow', '1', [('A', 0, 100), ('D', 1000, 1000)]),
            trip('first', '2', [('A', 0, 120), ('B', 300, 300)]),
            trip('second', '3', [('B', 0, 500), ('D', 700, 700)]),
            trip('too-fast', '4', [('B', 0, 350), ('D', 600, 600)]),
        ])

    def test_depart_after_returns_direct_and_transfer_variants(self):
        journeys = self.router.depart_after('A', 'D', 100, max_transfers=2, minimum_transfer=60)
        self.assertEqual(journeys[0].arrival, 700)
        self.assertEqual([leg.line for leg in journeys[0].legs], ['2', '3'])
        self.assertTrue(any([leg.line for leg in item.legs] == ['1'] for item in journeys))

    def test_arrive_by_finds_latest_valid_departure(self):
        journeys = self.router.arrive_by('A', 'D', 800, max_transfers=2, minimum_transfer=60)
        self.assertEqual(journeys[0].departure, 120)
        self.assertEqual([leg.line for leg in journeys[0].legs], ['2', '3'])

    def test_maximum_transfer_wait_can_reject_connection(self):
        journeys = self.router.depart_after(
            'A', 'D', 100, max_transfers=2, minimum_transfer=60,
            maximum_transfer=100
        )
        self.assertEqual([leg.line for leg in journeys[0].legs], ['1'])

    def test_walking_transfer_connects_nearby_different_stops(self):
        router = Raptor([
            trip('first', '10', [('A', 0, 100), ('B', 300, 300)]),
            trip('second', '20', [('C', 0, 500), ('D', 800, 800)]),
        ], [RaptorFootpath('B', 'C', 90), RaptorFootpath('C', 'B', 90)])

        journey = router.depart_after(
            'A', 'D', 100, max_transfers=2, minimum_transfer=60
        )[0]

        self.assertEqual([leg.mode for leg in journey.legs], ['bus', 'walk', 'bus'])
        self.assertEqual(journey.transfers, 1)

    def test_router_does_not_chain_multiple_walking_transfers(self):
        router = Raptor([
            trip('first', '10', [('A', 0, 100), ('B', 300, 300)]),
        ], [
            RaptorFootpath('B', 'C', 90),
            RaptorFootpath('C', 'D', 90),
        ])

        self.assertEqual(
            router.depart_after('A', 'D', 100, max_transfers=3),
            []
        )


if __name__ == '__main__':
    unittest.main()

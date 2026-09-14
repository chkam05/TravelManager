"""Rail realtime parsing, freshness and conservative matching."""
from datetime import date, datetime, timedelta, timezone
import json
import unittest
from unittest.mock import patch

from google.transit import gtfs_realtime_pb2

from tests.test_rail_gtfs_repository import RailGtfsRepositoryTests
from utils.public_transport.rail_gtfs_repository import RailGtfsRepository
from utils.public_transport.rail_realtime import (
    RailRealtime,
    RailRealtimeSnapshot,
    RailStopUpdate,
    RailTripUpdate,
)


class RailRealtimeTests(unittest.TestCase):
    def test_polish_parser_supports_predictions_and_cancellation_but_ignores_platform(self):
        stamp = datetime.now(timezone.utc)
        payload = json.dumps({
            'timestamp': stamp.isoformat(),
            'trip_updates': [{
                'trip_id': 'TRIP', 'start_date': '2030-01-02',
                'agency_id': 'IC', 'numbers': ['401'], 'cancelled': True,
                'stop_times': [{
                    'stop_sequence': 2,
                    'arrival': '2030-01-02T10:05:00+01:00',
                    'departure': '2030-01-02T10:07:00+01:00',
                    'cancelled': True, 'platform': 'changed', 'track': 'changed'
                }]
            }]
        }).encode()
        snapshot = RailRealtime.parse_polish_trains(payload)
        trip = snapshot.trips[0]
        self.assertTrue(trip.cancelled)
        self.assertTrue(trip.stops[0].cancelled)
        self.assertEqual(trip.stops[0].departure.minute, 7)
        self.assertFalse(hasattr(trip.stops[0], 'platform'))

    def test_expired_snapshot_is_not_matched(self):
        snapshot = RailRealtimeSnapshot(
            'polish_trains',
            datetime.now(timezone.utc) - timedelta(minutes=16),
            (RailTripUpdate('TRIP', date(2030, 1, 2), 'IC'),)
        )
        self.assertIsNone(RailRealtime.match(
            snapshot, 'TRIP', date(2030, 1, 2), ('IC',)
        ))

    def test_number_fallback_rejects_ambiguous_updates(self):
        trip = lambda identifier: RailTripUpdate(
            identifier, date(2030, 1, 2), 'IC', ('401',)
        )
        snapshot = RailRealtimeSnapshot(
            'polish_trains', datetime.now(timezone.utc), (trip('A'), trip('B'))
        )
        self.assertIsNone(RailRealtime.match(
            snapshot, 'UNKNOWN', date(2030, 1, 2), ('IC',), ('401',)
        ))

    def test_stale_cached_snapshot_does_not_claim_freshness_or_use_network(self):
        stale = RailRealtimeSnapshot(
            'polish_trains', datetime.now(timezone.utc) - timedelta(hours=1), (),
            datetime.now(timezone.utc) - timedelta(minutes=2)
        )
        with patch.object(RailRealtime, '_cache', {'polish_trains': stale}), \
                patch.object(RailRealtime, '_download') as download:
            result = RailRealtime.snapshot('polish_trains')
        self.assertIs(result, stale)
        self.assertFalse(result.is_fresh())
        download.assert_not_called()

    def test_exact_match_requires_operational_day_and_operator(self):
        snapshot = RailRealtimeSnapshot(
            'polish_trains', datetime.now(timezone.utc),
            (RailTripUpdate('TRIP', date(2030, 1, 2), 'IC'),)
        )
        self.assertIsNone(RailRealtime.match(
            snapshot, 'TRIP', date(2030, 1, 3), ('IC',)
        ))
        self.assertIsNone(RailRealtime.match(
            snapshot, 'TRIP', date(2030, 1, 2), ('PR',)
        ))

    def test_wkd_gtfs_rt_parser_reads_predicted_departure(self):
        message = gtfs_realtime_pb2.FeedMessage()
        message.header.gtfs_realtime_version = '2.0'
        message.header.timestamp = int(datetime.now(timezone.utc).timestamp())
        entity = message.entity.add()
        entity.id = 'wkd-update'
        update = entity.trip_update
        update.trip.trip_id = '201_3'
        update.trip.start_date = '20300102'
        stop = update.stop_time_update.add()
        stop.stop_id = 'WKD_1'
        stop.stop_sequence = 3
        stop.departure.time = 1893582000
        snapshot = RailRealtime.parse_wkd(message.SerializeToString())
        self.assertEqual(snapshot.trips[0].trip_id, '201_3')
        self.assertEqual(snapshot.trips[0].service_date, date(2030, 1, 2))
        self.assertIsNotNone(snapshot.trips[0].stops[0].departure)

    def test_reading_cached_updates_never_starts_network_io(self):
        with patch.object(RailRealtime, '_cache', {}), \
                patch.object(RailRealtime, '_download') as download:
            self.assertIsNone(RailRealtime.snapshot('polish_trains'))
            self.assertIsNone(RailRealtime.cached_snapshot('polish_trains'))
        download.assert_not_called()


class RailRealtimeRepositoryTests(RailGtfsRepositoryTests):
    """Reuses the representative database with realtime explicitly enabled."""

    def test_fresh_prediction_overlays_schedule_and_keeps_planned_time(self):
        predicted = datetime(2030, 1, 2, 10, 8, tzinfo=timezone(timedelta(hours=1)))
        snapshot = RailRealtimeSnapshot(
            'polish_trains', datetime.now(timezone.utc),
            (RailTripUpdate(
                'DAY_402', self.SERVICE_DATE, 'IC', ('402',), False,
                (RailStopUpdate(0, 'CENTRAL_2', departure=predicted),)
            ),)
        )
        repository = RailGtfsRepository(
            'rail_pkp_intercity', self.polish_path, realtime=True
        )
        with patch.object(RailRealtime, 'cached_snapshot', return_value=snapshot):
            departure = repository.departures('CENTRAL_2', self.SERVICE_DATE)[0]
        self.assertEqual(departure.departure_time.strftime('%H:%M'), '10:08')
        self.assertEqual(departure.scheduled_departure_time.strftime('%H:%M'), '10:00')
        self.assertEqual(departure.delay_minutes, 8)
        self.assertTrue(departure.realtime_updated_at)


if __name__ == '__main__':
    unittest.main()

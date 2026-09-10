"""End-to-end isolation contract for every registered rail operator."""
from datetime import date
from io import BytesIO
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from zipfile import ZIP_DEFLATED, ZipFile

from core.gtfs_database import GtfsDatabase
from resources.public_transport.rail_gtfs_sources import RailGtfsSources
from utils.public_transport.rail_gtfs_repository import RailGtfsRepository


SERVICE_DATE = date.today()


def provider_feed(providers) -> bytes:
    agencies = ['agency_id,agency_name,agency_url,agency_timezone']
    routes = ['route_id,agency_id,route_short_name,route_type']
    trips = ['route_id,service_id,trip_id,trip_headsign,trip_short_name,plk_train_number']
    stop_times = ['trip_id,arrival_time,departure_time,stop_id,stop_sequence']
    for index, provider in enumerate(providers, 1):
        agency = provider.agency_ids[0]
        agencies.append(f'{agency},{provider.display_name},https://example.invalid,Europe/Warsaw')
        routes.append(f'ROUTE_{agency},{agency},{agency},2')
        trips.append(f'ROUTE_{agency},ACTIVE,TRIP_{agency},Destination {agency},{index:03},{index:03}')
        stop_times.append(f'TRIP_{agency},12:00:00,12:00:00,SHARED,0')
        stop_times.append(f'TRIP_{agency},13:00:00,13:00:00,END_{agency},1')
    files = {
        'agency.txt': '\n'.join(agencies) + '\n',
        'routes.txt': '\n'.join(routes) + '\n',
        'trips.txt': '\n'.join(trips) + '\n',
        'stop_times.txt': '\n'.join(stop_times) + '\n',
        'stops.txt': ('stop_id,stop_name,stop_lat,stop_lon\nSHARED,Shared,52,21\n' +
                      ''.join(f'END_{p.agency_ids[0]},End {p.agency_ids[0]},53,22\n' for p in providers)),
        'calendar_dates.txt': (
            f'service_id,date,exception_type\nACTIVE,{SERVICE_DATE.strftime("%Y%m%d")},1\n'
        ),
        'feed_info.txt': ('feed_publisher_name,feed_publisher_url,feed_lang,feed_version,'
                          f'feed_start_date,feed_end_date\nTest,https://example.invalid,pl,all-14,'
                          f'{SERVICE_DATE.strftime("%Y%m%d")},{SERVICE_DATE.strftime("%Y%m%d")}\n')
    }
    output = BytesIO()
    with ZipFile(output, 'w', ZIP_DEFLATED) as archive:
        for name, content in files.items():
            archive.writestr(name, content)
    return output.getvalue()


class RailAllProvidersTests(unittest.TestCase):
    def setUp(self):
        self.directory = TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        root = Path(self.directory.name)
        polish = tuple(p for p in RailGtfsSources.PROVIDERS
                       if p.source_id == RailGtfsSources.POLISH_TRAINS)
        wkd = tuple(p for p in RailGtfsSources.PROVIDERS
                    if p.source_id == RailGtfsSources.WKD)
        self.paths = {
            RailGtfsSources.POLISH_TRAINS: root / 'polish.sqlite3',
            RailGtfsSources.WKD: root / 'wkd.sqlite3'
        }
        GtfsDatabase.build(self.paths[RailGtfsSources.POLISH_TRAINS], {
            RailGtfsSources.POLISH_TRAINS: provider_feed(polish)
        })
        GtfsDatabase.build(self.paths[RailGtfsSources.WKD], {
            RailGtfsSources.WKD: provider_feed(wkd)
        })

    def test_every_provider_returns_only_its_own_routes_and_trips(self):
        for provider in RailGtfsSources.PROVIDERS:
            with self.subTest(provider=provider.provider_id):
                repository = RailGtfsRepository(
                    provider.provider_id, self.paths[provider.source_id]
                )
                agency = provider.agency_ids[0]
                lines = repository.download_lines(service_date=SERVICE_DATE)
                departures = repository.departures('SHARED', SERVICE_DATE)
                expected_line = (
                    f'{RailGtfsSources.PROVIDERS.index(provider) + 1:03}'
                    if provider.provider_id in RailGtfsRepository._LONG_DISTANCE_PROVIDERS
                    else agency
                )
                self.assertEqual([line.line for line in lines], [expected_line])
                self.assertEqual(len(departures), 1)
                self.assertIn(f'TRIP_{agency}', departures[0].url)


if __name__ == '__main__':
    unittest.main()

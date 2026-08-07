from __future__ import annotations
import unicodedata
from typing import Any, ClassVar, Dict, Type
from urllib.parse import urlparse

from utils.public_transport.bialystok_downloader import BialystokDownloader
from utils.public_transport.chojnice_downloader import ChojniceDownloader
from utils.public_transport.czestochowa_downloader import CzestochowaDownloader
from utils.public_transport.elk_downloader import ElkDownloader
from utils.public_transport.gizycko_downloader import GizyckoDownloader
from utils.public_transport.kalisz_downloader import KaliszDownloader
from utils.public_transport.kielce_downloader import KielceDownloader
from utils.public_transport.kutno_downloader import KutnoDownloader
from utils.public_transport.legnica_downloader import LegnicaDownloader
from utils.public_transport.leszno_downloader import LesznoDownloader
from utils.public_transport.lomza_downloader import LomzaDownloader
from utils.public_transport.opole_downloader import OpoleDownloader
from utils.public_transport.przemysl_downloader import PrzemyslDownloader
from utils.public_transport.radom_downloader import RadomDownloader
from utils.public_transport.rybnik_downloader import RybnikDownloader
from utils.public_transport.rzeszow_downloader import RzeszowDownloader
from utils.public_transport.suwalki_downloader import SuwalikiDownloader
from utils.public_transport.swinoujscie_downloader import SwinoujscieDownloader
from utils.public_transport.wejherowo_downloader import WejherowoDownloader
from utils.public_transport.elblag_downloader import ElblagDownloader
from utils.public_transport.gorzow_downloader import GorzowDownloader
from utils.public_transport.grudziadz_downloader import GrudziadzDownloader
from utils.public_transport.gzm_downloader import GzmDownloader
from utils.public_transport.krakow_downloader import KrakowDownloader
from utils.public_transport.lublin_downloader import LublinDownloader
from utils.public_transport.lodz_downloader import LodzDownloader
from utils.public_transport.olsztyn_downloader import OlsztynDownloader
from utils.public_transport.warsaw_downloader import WarsawDownloader
from utils.public_transport.gdansk_downloader import GdanskDownloader
from utils.public_transport.gdynia_downloader import GdyniaDownloader
from utils.public_transport.poznan_downloader import PoznanDownloader
from utils.public_transport.szczecin_downloader import SzczecinDownloader
from utils.public_transport.bydgoszcz_downloader import BydgoszczDownloader
from utils.public_transport.torun_downloader import TorunDownloader
from utils.public_transport.wroclaw_downloader import WroclawDownloader


class PublicTransportProviders:
    """Registers public transport regions and their downloader implementations."""

    BIALYSTOK: ClassVar[str] = 'bialystok'
    CHOJNICE: ClassVar[str] = 'chojnice'
    ELK: ClassVar[str] = 'elk'
    GIZYCKO: ClassVar[str] = 'gizycko'
    KALISZ: ClassVar[str] = 'kalisz'
    KIELCE: ClassVar[str] = 'kielce'
    KUTNO: ClassVar[str] = 'kutno'
    LEGNICA: ClassVar[str] = 'legnica'
    LESZNO: ClassVar[str] = 'leszno'
    LOMZA: ClassVar[str] = 'lomza'
    OPOLE: ClassVar[str] = 'opole'
    PRZEMYSL: ClassVar[str] = 'przemysl'
    RADOM: ClassVar[str] = 'radom'
    RYBNIK: ClassVar[str] = 'rybnik'
    RZESZOW: ClassVar[str] = 'rzeszow'
    SUWALKI: ClassVar[str] = 'suwalki'
    SWINOUJSCIE: ClassVar[str] = 'swinoujscie'
    WEJHEROWO: ClassVar[str] = 'wejherowo'
    GZM: ClassVar[str] = 'gzm'
    CZESTOCHOWA: ClassVar[str] = 'czestochowa'
    KRAKOW: ClassVar[str] = 'krakow'
    WARSAW: ClassVar[str] = 'warsaw'
    GDANSK: ClassVar[str] = 'gdansk'
    GDYNIA: ClassVar[str] = 'gdynia'
    SZCZECIN: ClassVar[str] = 'szczecin'
    POZNAN: ClassVar[str] = 'poznan'
    BYDGOSZCZ: ClassVar[str] = 'bydgoszcz'
    TORUN: ClassVar[str] = 'torun'
    WROCLAW: ClassVar[str] = 'wroclaw'
    ELBLAG: ClassVar[str] = 'elblag'
    GORZOW: ClassVar[str] = 'gorzow'
    GRUDZIADZ: ClassVar[str] = 'grudziadz'
    LUBLIN: ClassVar[str] = 'lublin'
    LODZ: ClassVar[str] = 'lodz'
    OLSZTYN: ClassVar[str] = 'olsztyn'

    FIELD_NAME: ClassVar[str] = 'name'
    FIELD_DESCRIPTION: ClassVar[str] = 'description'
    FIELD_ICON: ClassVar[str] = 'icon'
    FIELD_DOWNLOADER: ClassVar[str] = 'downloader'
    FIELD_CAPABILITIES: ClassVar[str] = 'capabilities'
    FIELD_SETTINGS_CACHE: ClassVar[str] = 'settings_cache'
    FIELD_ATTRIBUTIONS: ClassVar[str] = 'attributions'

    REGIONS: ClassVar[Dict[str, str]] = {
        'bialystok':    'podlaskie',
        'chojnice':     'pomorskie',
        'bydgoszcz':    'kujawsko-pomorskie',
        'czestochowa':  'śląskie',
        'elblag':       'warmińsko-mazurskie',
        'elk':          'warmińsko-mazurskie',
        'gdansk':       'pomorskie',
        'gdynia':       'pomorskie',
        'gizycko':      'warmińsko-mazurskie',
        'gorzow':       'lubuskie',
        'grudziadz':    'kujawsko-pomorskie',
        'gzm':          'śląskie',
        'kalisz':       'wielkopolskie',
        'kielce':       'świętokrzyskie',
        'krakow':       'małopolskie',
        'kutno':        'łódzkie',
        'legnica':      'dolnośląskie',
        'leszno':       'wielkopolskie',
        'lodz':         'łódzkie',
        'lomza':        'podlaskie',
        'lublin':       'lubelskie',
        'olsztyn':      'warmińsko-mazurskie',
        'opole':        'opolskie',
        'poznan':       'wielkopolskie',
        'przemysl':     'podkarpackie',
        'radom':        'mazowieckie',
        'rybnik':       'śląskie',
        'rzeszow':      'podkarpackie',
        'szczecin':     'zachodniopomorskie',
        'suwalki':      'podlaskie',
        'swinoujscie':  'zachodniopomorskie',
        'torun':        'kujawsko-pomorskie',
        'warsaw':       'mazowieckie',
        'wejherowo':    'pomorskie',
        'wroclaw':      'dolnośląskie',
    }

    CAPABILITY_SHOW_PLATFORMS: ClassVar[str] = 'show_platforms'
    CAPABILITY_SHOW_STOP_MAP: ClassVar[str] = 'show_stop_map'
    CAPABILITY_SHOW_RIDE_MAP: ClassVar[str] = 'show_ride_map'
    CAPABILITY_SHOW_RIDE_DISTANCES: ClassVar[str] = 'show_ride_distances'
    CAPABILITY_SHOW_VEHICLE_DETAILS: ClassVar[str] = 'show_vehicle_details'
    CAPABILITY_SHOW_HIGH_FLOOR: ClassVar[str] = 'show_high_floor'
    CAPABILITY_SHOW_STOP_DEPARTURES: ClassVar[str] = 'show_stop_departures'
    CAPABILITY_SHOW_RIDE: ClassVar[str] = 'show_ride'
    CAPABILITY_SHOW_ROUTE_MAP: ClassVar[str] = 'show_route_map'
    CAPABILITY_APPROXIMATE_ROUTE_MAP: ClassVar[str] = 'approximate_route_map'
    CAPABILITY_SHOW_VEHICLE_POSITIONS: ClassVar[str] = (
        'show_vehicle_positions'
    )
    CAPABILITY_CACHE_ANNOUNCEMENTS: ClassVar[str] = 'cache_announcements'
    CAPABILITY_DIRECTION_SELECTOR_LABEL: ClassVar[str] = (
        'direction_selector_label'
    )

    GZM_CAPABILITIES: ClassVar[Dict[str, object]] = {
        CAPABILITY_SHOW_PLATFORMS: True,
        CAPABILITY_SHOW_STOP_MAP: True,
        CAPABILITY_SHOW_RIDE_MAP: True,
        CAPABILITY_SHOW_RIDE_DISTANCES: True,
        CAPABILITY_SHOW_VEHICLE_DETAILS: True,
        CAPABILITY_SHOW_HIGH_FLOOR: True,
        CAPABILITY_SHOW_STOP_DEPARTURES: True,
        CAPABILITY_SHOW_RIDE: True,
        CAPABILITY_SHOW_ROUTE_MAP: True,
        CAPABILITY_SHOW_VEHICLE_POSITIONS: True,
        CAPABILITY_CACHE_ANNOUNCEMENTS: False,
        CAPABILITY_DIRECTION_SELECTOR_LABEL: 'Kierunek'
    }
    CZESTOCHOWA_CAPABILITIES: ClassVar[Dict[str, object]] = {
        CAPABILITY_SHOW_PLATFORMS: False,
        CAPABILITY_SHOW_STOP_MAP: True,
        CAPABILITY_SHOW_RIDE_MAP: True,
        CAPABILITY_SHOW_RIDE_DISTANCES: False,
        CAPABILITY_SHOW_VEHICLE_DETAILS: False,
        CAPABILITY_SHOW_HIGH_FLOOR: False,
        CAPABILITY_SHOW_STOP_DEPARTURES: False,
        CAPABILITY_SHOW_RIDE: True,
        CAPABILITY_SHOW_ROUTE_MAP: False,
        CAPABILITY_SHOW_VEHICLE_POSITIONS: False,
        CAPABILITY_CACHE_ANNOUNCEMENTS: True,
        CAPABILITY_DIRECTION_SELECTOR_LABEL: 'Wariant trasy'
    }
    KRAKOW_CAPABILITIES: ClassVar[Dict[str, object]] = {
        CAPABILITY_SHOW_PLATFORMS: True,
        CAPABILITY_SHOW_STOP_MAP: True,
        CAPABILITY_SHOW_RIDE_MAP: True,
        CAPABILITY_SHOW_RIDE_DISTANCES: False,
        CAPABILITY_SHOW_VEHICLE_DETAILS: False,
        CAPABILITY_SHOW_HIGH_FLOOR: False,
        CAPABILITY_SHOW_STOP_DEPARTURES: True,
        CAPABILITY_SHOW_RIDE: True,
        CAPABILITY_SHOW_ROUTE_MAP: True,
        CAPABILITY_SHOW_VEHICLE_POSITIONS: True,
        CAPABILITY_CACHE_ANNOUNCEMENTS: True,
        CAPABILITY_DIRECTION_SELECTOR_LABEL: 'Wariant trasy'
    }
    WARSAW_CAPABILITIES: ClassVar[Dict[str, object]] = {
        CAPABILITY_SHOW_PLATFORMS: True,
        CAPABILITY_SHOW_STOP_MAP: True,
        CAPABILITY_SHOW_RIDE_MAP: True,
        CAPABILITY_SHOW_RIDE_DISTANCES: False,
        CAPABILITY_SHOW_VEHICLE_DETAILS: False,
        CAPABILITY_SHOW_HIGH_FLOOR: False,
        CAPABILITY_SHOW_STOP_DEPARTURES: True,
        CAPABILITY_SHOW_RIDE: True,
        CAPABILITY_SHOW_ROUTE_MAP: True,
        CAPABILITY_SHOW_VEHICLE_POSITIONS: True,
        CAPABILITY_CACHE_ANNOUNCEMENTS: False,
        CAPABILITY_DIRECTION_SELECTOR_LABEL: 'Wariant trasy'
    }
    GDANSK_CAPABILITIES: ClassVar[Dict[str, object]] = {
        **WARSAW_CAPABILITIES,
        CAPABILITY_SHOW_VEHICLE_POSITIONS: True
    }
    GDYNIA_CAPABILITIES: ClassVar[Dict[str, object]] = {
        **WARSAW_CAPABILITIES,
        CAPABILITY_SHOW_VEHICLE_POSITIONS: False
    }
    SZCZECIN_CAPABILITIES: ClassVar[Dict[str, object]] = {
        **WARSAW_CAPABILITIES,
        CAPABILITY_SHOW_VEHICLE_POSITIONS: True
    }
    POZNAN_CAPABILITIES: ClassVar[Dict[str, object]] = {
        **WARSAW_CAPABILITIES,
        CAPABILITY_SHOW_VEHICLE_POSITIONS: True
    }
    BYDGOSZCZ_CAPABILITIES: ClassVar[Dict[str, object]] = {
        **WARSAW_CAPABILITIES,
        CAPABILITY_SHOW_VEHICLE_POSITIONS: False
    }
    TORUN_CAPABILITIES: ClassVar[Dict[str, object]] = {
        **WARSAW_CAPABILITIES,
        CAPABILITY_SHOW_VEHICLE_POSITIONS: False
    }
    WROCLAW_CAPABILITIES: ClassVar[Dict[str, object]] = {
        **WARSAW_CAPABILITIES,
        CAPABILITY_SHOW_VEHICLE_POSITIONS: True
    }
    ELBLAG_CAPABILITIES: ClassVar[Dict[str, object]] = {
        **WARSAW_CAPABILITIES,
        CAPABILITY_APPROXIMATE_ROUTE_MAP: True,
        CAPABILITY_SHOW_VEHICLE_POSITIONS: False
    }
    GORZOW_CAPABILITIES: ClassVar[Dict[str, object]] = {
        **WARSAW_CAPABILITIES,
        CAPABILITY_SHOW_VEHICLE_POSITIONS: False
    }
    GRUDZIADZ_CAPABILITIES: ClassVar[Dict[str, object]] = {
        **CZESTOCHOWA_CAPABILITIES,
        CAPABILITY_SHOW_ROUTE_MAP: True,
        CAPABILITY_CACHE_ANNOUNCEMENTS: False
    }
    LUBLIN_CAPABILITIES: ClassVar[Dict[str, object]] = {
        **WARSAW_CAPABILITIES,
        CAPABILITY_APPROXIMATE_ROUTE_MAP: True,
        CAPABILITY_SHOW_VEHICLE_POSITIONS: False
    }
    LODZ_CAPABILITIES: ClassVar[Dict[str, object]] = {
        **WARSAW_CAPABILITIES,
        CAPABILITY_SHOW_VEHICLE_POSITIONS: True
    }
    OLSZTYN_CAPABILITIES: ClassVar[Dict[str, object]] = {
        **WARSAW_CAPABILITIES,
        CAPABILITY_APPROXIMATE_ROUTE_MAP: True,
        CAPABILITY_SHOW_VEHICLE_POSITIONS: False
    }
    BIALYSTOK_CAPABILITIES: ClassVar[Dict[str, object]] = {
        **WARSAW_CAPABILITIES,
        CAPABILITY_SHOW_VEHICLE_POSITIONS: False
    }
    CHOJNICE_CAPABILITIES: ClassVar[Dict[str, object]] = {
        **CZESTOCHOWA_CAPABILITIES,
        CAPABILITY_SHOW_ROUTE_MAP: False,
        CAPABILITY_CACHE_ANNOUNCEMENTS: False
    }
    ELK_CAPABILITIES: ClassVar[Dict[str, object]] = {
        **WARSAW_CAPABILITIES,
        CAPABILITY_SHOW_VEHICLE_POSITIONS: True
    }
    GIZYCKO_CAPABILITIES: ClassVar[Dict[str, object]] = {
        **WARSAW_CAPABILITIES,
        CAPABILITY_SHOW_ROUTE_MAP: True,
        CAPABILITY_APPROXIMATE_ROUTE_MAP: True,
        CAPABILITY_SHOW_VEHICLE_POSITIONS: False
    }
    KALISZ_CAPABILITIES: ClassVar[Dict[str, object]] = {
        **WARSAW_CAPABILITIES,
        CAPABILITY_SHOW_VEHICLE_POSITIONS: False
    }
    KIELCE_CAPABILITIES: ClassVar[Dict[str, object]] = {
        **WARSAW_CAPABILITIES,
        CAPABILITY_SHOW_VEHICLE_POSITIONS: True
    }
    KUTNO_CAPABILITIES: ClassVar[Dict[str, object]] = {
        **WARSAW_CAPABILITIES,
        CAPABILITY_SHOW_VEHICLE_POSITIONS: True
    }
    LEGNICA_CAPABILITIES: ClassVar[Dict[str, object]] = {
        **WARSAW_CAPABILITIES,
        CAPABILITY_SHOW_VEHICLE_POSITIONS: True
    }
    LESZNO_CAPABILITIES: ClassVar[Dict[str, object]] = {
        **WARSAW_CAPABILITIES,
        CAPABILITY_SHOW_VEHICLE_POSITIONS: False
    }
    LOMZA_CAPABILITIES: ClassVar[Dict[str, object]] = {
        **WARSAW_CAPABILITIES,
        CAPABILITY_SHOW_ROUTE_MAP: True,
        CAPABILITY_APPROXIMATE_ROUTE_MAP: True,
        CAPABILITY_SHOW_VEHICLE_POSITIONS: False
    }
    OPOLE_CAPABILITIES: ClassVar[Dict[str, object]] = {
        **WARSAW_CAPABILITIES,
        CAPABILITY_SHOW_VEHICLE_POSITIONS: False
    }
    PRZEMYSL_CAPABILITIES: ClassVar[Dict[str, object]] = {
        **WARSAW_CAPABILITIES,
        CAPABILITY_SHOW_VEHICLE_POSITIONS: True
    }
    RADOM_CAPABILITIES: ClassVar[Dict[str, object]] = {
        **WARSAW_CAPABILITIES,
        CAPABILITY_SHOW_VEHICLE_POSITIONS: True
    }
    RYBNIK_CAPABILITIES: ClassVar[Dict[str, object]] = {
        **WARSAW_CAPABILITIES,
        CAPABILITY_SHOW_VEHICLE_POSITIONS: True
    }
    RZESZOW_CAPABILITIES: ClassVar[Dict[str, object]] = {
        **WARSAW_CAPABILITIES,
        CAPABILITY_SHOW_VEHICLE_POSITIONS: False
    }
    SUWALKI_CAPABILITIES: ClassVar[Dict[str, object]] = {
        **WARSAW_CAPABILITIES,
        CAPABILITY_SHOW_VEHICLE_POSITIONS: True
    }
    SWINOUJSCIE_CAPABILITIES: ClassVar[Dict[str, object]] = {
        **WARSAW_CAPABILITIES,
        CAPABILITY_SHOW_ROUTE_MAP: True,
        CAPABILITY_APPROXIMATE_ROUTE_MAP: True,
        CAPABILITY_SHOW_VEHICLE_POSITIONS: False
    }
    WEJHEROWO_CAPABILITIES: ClassVar[Dict[str, object]] = {
        **WARSAW_CAPABILITIES,
        CAPABILITY_SHOW_VEHICLE_POSITIONS: False
    }

    VALUES: ClassVar[Dict[str, Dict[str, object]]] = {
        GZM: {
            FIELD_NAME: 'Górnośląsko-Zagłębiowska Metropolia',
            FIELD_DESCRIPTION: 'Transport GZM (GTFS)',
            FIELD_ICON: 'bus-front',
            FIELD_DOWNLOADER: GzmDownloader,
            FIELD_CAPABILITIES: GZM_CAPABILITIES,
            FIELD_SETTINGS_CACHE: False,
            FIELD_ATTRIBUTIONS: [{
                'name': 'Zarząd Transportu Metropolitalnego / Otwarte Dane GZM',
                'url': (
                    'https://otwartedane.metropoliagzm.pl/dataset/'
                    'rozklady-jazdy-i-lokalizacja-przystankow-gtfs-'
                    'wersja-rozszerzona'
                )
            }]
        },
        CZESTOCHOWA: {
            FIELD_NAME: 'Częstochowa',
            FIELD_DESCRIPTION: 'MPK w Częstochowie',
            FIELD_ICON: 'tram-front',
            FIELD_DOWNLOADER: CzestochowaDownloader,
            FIELD_CAPABILITIES: CZESTOCHOWA_CAPABILITIES,
            FIELD_SETTINGS_CACHE: True,
            FIELD_ATTRIBUTIONS: [{
                'name': 'Miasto Częstochowa / MPK w Częstochowie',
                'url': 'https://www.czestochowa.pl/rozklady-jazdy'
            }]
        },
        CHOJNICE: {
            FIELD_NAME: 'Chojnice',
            FIELD_DESCRIPTION: 'MZK Chojnice',
            FIELD_ICON: 'bus-front',
            FIELD_DOWNLOADER: ChojniceDownloader,
            FIELD_CAPABILITIES: CHOJNICE_CAPABILITIES,
            FIELD_SETTINGS_CACHE: True,
            FIELD_ATTRIBUTIONS: [
                {
                    'name': 'MZK Chojnice',
                    'url': 'https://www.mzkchojnice.pl/'
                },
                {
                    'name': 'Rozkłady: rozklad.com',
                    'url': 'https://rozklad.com/'
                }
            ]
        },
        KRAKOW: {
            FIELD_NAME: 'Kraków',
            FIELD_DESCRIPTION: 'Komunikacja Miejska w Krakowie (GTFS)',
            FIELD_ICON: 'tram-front',
            FIELD_DOWNLOADER: KrakowDownloader,
            FIELD_CAPABILITIES: KRAKOW_CAPABILITIES,
            FIELD_SETTINGS_CACHE: False,
            FIELD_ATTRIBUTIONS: [{
                'name': 'Zarząd Transportu Publicznego w Krakowie',
                'url': 'https://gtfs.ztp.krakow.pl/'
            }]
        },
        WARSAW: {
            FIELD_NAME: 'Warszawa',
            FIELD_DESCRIPTION: 'Warszawski Transport Publiczny (GTFS)',
            FIELD_ICON: 'train-front',
            FIELD_DOWNLOADER: WarsawDownloader,
            FIELD_CAPABILITIES: WARSAW_CAPABILITIES,
            FIELD_SETTINGS_CACHE: False,
            FIELD_ATTRIBUTIONS: [
                {
                    'name': 'Zarząd Transportu Miejskiego w Warszawie',
                    'url': 'https://ztm.waw.pl/'
                },
                {
                    'name': 'GTFS: Mikołaj Kuranowski',
                    'url': 'https://mkuran.pl/gtfs/'
                },
                {
                    'name': 'Geometrie autobusów: © OpenStreetMap',
                    'url': 'https://www.openstreetmap.org/copyright'
                }
            ]
        },
        GDANSK: {
            FIELD_NAME: 'Gdańsk',
            FIELD_DESCRIPTION: 'ZTM Gdańsk (GTFS)',
            FIELD_ICON: 'tram-front',
            FIELD_DOWNLOADER: GdanskDownloader,
            FIELD_CAPABILITIES: GDANSK_CAPABILITIES,
            FIELD_SETTINGS_CACHE: False,
            FIELD_ATTRIBUTIONS: [{
                'name': 'Zarząd Transportu Miejskiego w Gdańsku',
                'url': 'https://ckan.multimediagdansk.pl/tl/dataset/tristar'
            }]
        },
        GDYNIA: {
            FIELD_NAME: 'Gdynia',
            FIELD_DESCRIPTION: 'ZKM Gdynia (GTFS)',
            FIELD_ICON: 'bus-front',
            FIELD_DOWNLOADER: GdyniaDownloader,
            FIELD_CAPABILITIES: GDYNIA_CAPABILITIES,
            FIELD_SETTINGS_CACHE: False,
            FIELD_ATTRIBUTIONS: [{
                'name': 'ZKM Gdynia / Otwarte Dane Gdynia',
                'url': (
                    'https://otwartedane.gdynia.pl/dataset/'
                    'informacje-o-rozkladach-jazdy-i-lokalizacji-przystankow'
                )
            }]
        },
        SZCZECIN: {
            FIELD_NAME: 'Szczecin',
            FIELD_DESCRIPTION: 'ZDiTM Szczecin (GTFS)',
            FIELD_ICON: 'tram-front',
            FIELD_DOWNLOADER: SzczecinDownloader,
            FIELD_CAPABILITIES: SZCZECIN_CAPABILITIES,
            FIELD_SETTINGS_CACHE: False,
            FIELD_ATTRIBUTIONS: [{
                'name': 'Zarząd Dróg i Transportu Miejskiego w Szczecinie',
                'url': (
                    'https://www.zditm.szczecin.pl/pl/zditm/'
                    'dla-programistow/gtfs'
                )
            }]
        },
        POZNAN: {
            FIELD_NAME: 'Poznań',
            FIELD_DESCRIPTION: 'ZTM Poznań (GTFS)',
            FIELD_ICON: 'tram-front',
            FIELD_DOWNLOADER: PoznanDownloader,
            FIELD_CAPABILITIES: POZNAN_CAPABILITIES,
            FIELD_SETTINGS_CACHE: False,
            FIELD_ATTRIBUTIONS: [{
                'name': 'Zarząd Transportu Miejskiego w Poznaniu',
                'url': 'https://www.ztm.poznan.pl/otwarte-dane/gtfsfiles/'
            }]
        },
        BYDGOSZCZ: {
            FIELD_NAME: 'Bydgoszcz',
            FIELD_DESCRIPTION: 'ZDMiKP Bydgoszcz (GTFS)',
            FIELD_ICON: 'tram-front',
            FIELD_DOWNLOADER: BydgoszczDownloader,
            FIELD_CAPABILITIES: BYDGOSZCZ_CAPABILITIES,
            FIELD_SETTINGS_CACHE: False,
            FIELD_ATTRIBUTIONS: [{
                'name': 'ZDMiKP Bydgoszcz',
                'url': 'https://zdmikp.bydgoszcz.pl/rozklady/paczka/linie.htm'
            }]
        },
        TORUN: {
            FIELD_NAME: 'Toruń',
            FIELD_DESCRIPTION: 'MZK Toruń (GTFS)',
            FIELD_ICON: 'tram-front',
            FIELD_DOWNLOADER: TorunDownloader,
            FIELD_CAPABILITIES: TORUN_CAPABILITIES,
            FIELD_SETTINGS_CACHE: False,
            FIELD_ATTRIBUTIONS: [
                {
                    'name': 'Miejski Zakład Komunikacji w Toruniu',
                    'url': 'https://mzk-torun.pl/'
                },
                {
                    'name': 'Konwersja GTFS: Mikołaj Kuranowski (CC0)',
                    'url': 'https://mkuran.pl/gtfs/'
                }
            ]
        },
        WROCLAW: {
            FIELD_NAME: 'Wrocław',
            FIELD_DESCRIPTION: 'Komunikacja miejska we Wrocławiu (GTFS)',
            FIELD_ICON: 'tram-front',
            FIELD_DOWNLOADER: WroclawDownloader,
            FIELD_CAPABILITIES: WROCLAW_CAPABILITIES,
            FIELD_SETTINGS_CACHE: False,
            FIELD_ATTRIBUTIONS: [
                {
                    'name': 'Wrocław Open Data – rozkład jazdy GTFS',
                    'url': 'https://open-data.cui.wroclaw.pl/hdb/ft/6/'
                },
                {
                    'name': 'Wrocław Open Data – pozycje pojazdów',
                    'url': 'https://open-data.cui.wroclaw.pl/hdb/db/14'
                }
            ]
        },
        ELBLAG: {
            FIELD_NAME: 'Elbląg',
            FIELD_DESCRIPTION: 'ZKM Elbląg (GTFS)',
            FIELD_ICON: 'tram-front',
            FIELD_DOWNLOADER: ElblagDownloader,
            FIELD_CAPABILITIES: ELBLAG_CAPABILITIES,
            FIELD_SETTINGS_CACHE: False,
            FIELD_ATTRIBUTIONS: [{
                'name': 'ZKM Elbląg / konwersja GTFS: Mikołaj Kuranowski (CC0)',
                'url': 'https://mkuran.pl/gtfs/'
            }]
        },
        GORZOW: {
            FIELD_NAME: 'Gorzów Wielkopolski',
            FIELD_DESCRIPTION: 'MZK Gorzów Wielkopolski (GTFS)',
            FIELD_ICON: 'tram-front',
            FIELD_DOWNLOADER: GorzowDownloader,
            FIELD_CAPABILITIES: GORZOW_CAPABILITIES,
            FIELD_SETTINGS_CACHE: False,
            FIELD_ATTRIBUTIONS: [{
                'name': 'MZK Gorzów / konwersja GTFS: Mikołaj Kuranowski (CC0)',
                'url': 'https://mkuran.pl/gtfs/'
            }]
        },
        GRUDZIADZ: {
            FIELD_NAME: 'Grudziądz',
            FIELD_DESCRIPTION: 'Komunikacja miejska w Grudziądzu',
            FIELD_ICON: 'tram-front',
            FIELD_DOWNLOADER: GrudziadzDownloader,
            FIELD_CAPABILITIES: GRUDZIADZ_CAPABILITIES,
            FIELD_SETTINGS_CACHE: True,
            FIELD_ATTRIBUTIONS: [
                {
                    'name': 'Wydział Transportu w Grudziądzu',
                    'url': 'https://transport.grudziadz.pl/rozklady-jazdy-2/'
                },
                {
                    'name': 'Dane rozkładowe: Rozkładzik.pl',
                    'url': 'https://www.rozkladzik.pl/grudziadz/'
                }
            ]
        },
        LUBLIN: {
            FIELD_NAME: 'Lublin',
            FIELD_DESCRIPTION: 'ZDiTM Lublin (GTFS)',
            FIELD_ICON: 'bus-front',
            FIELD_DOWNLOADER: LublinDownloader,
            FIELD_CAPABILITIES: LUBLIN_CAPABILITIES,
            FIELD_SETTINGS_CACHE: False,
            FIELD_ATTRIBUTIONS: [{
                'name': 'ZDiTM Lublin / konwersja GTFS: Mikołaj Kuranowski (CC0)',
                'url': 'https://mkuran.pl/gtfs/'
            }]
        },
        LODZ: {
            FIELD_NAME: 'Łódź',
            FIELD_DESCRIPTION: 'MPK-Łódź (GTFS)',
            FIELD_ICON: 'tram-front',
            FIELD_DOWNLOADER: LodzDownloader,
            FIELD_CAPABILITIES: LODZ_CAPABILITIES,
            FIELD_SETTINGS_CACHE: False,
            FIELD_ATTRIBUTIONS: [{
                'name': 'Urząd Miasta Łodzi — Open Data Łódź',
                'url': 'https://otwarte.miasto.lodz.pl/transport_komunikacja/'
            }]
        },
        OLSZTYN: {
            FIELD_NAME: 'Olsztyn',
            FIELD_DESCRIPTION: 'ZDZiT Olsztyn (GTFS)',
            FIELD_ICON: 'tram-front',
            FIELD_DOWNLOADER: OlsztynDownloader,
            FIELD_CAPABILITIES: OLSZTYN_CAPABILITIES,
            FIELD_SETTINGS_CACHE: False,
            FIELD_ATTRIBUTIONS: [{
                'name': 'Zarząd Dróg, Zieleni i Transportu w Olsztynie',
                'url': 'https://zdzit.olsztyn.eu/gtfs/'
            }]
        },
        BIALYSTOK: {
            FIELD_NAME: 'Białystok',
            FIELD_DESCRIPTION: 'BKM Białystok (GTFS)',
            FIELD_ICON: 'bus-front',
            FIELD_DOWNLOADER: BialystokDownloader,
            FIELD_CAPABILITIES: BIALYSTOK_CAPABILITIES,
            FIELD_SETTINGS_CACHE: False,
            FIELD_ATTRIBUTIONS: [{
                'name': 'Białostocka Komunikacja Miejska',
                'url': 'https://komunikacja.bialystok.pl/'
            }]
        },
        ELK: {
            FIELD_NAME: 'Ełk',
            FIELD_DESCRIPTION: 'MZK Ełk (GTFS)',
            FIELD_ICON: 'bus-front',
            FIELD_DOWNLOADER: ElkDownloader,
            FIELD_CAPABILITIES: ELK_CAPABILITIES,
            FIELD_SETTINGS_CACHE: False,
            FIELD_ATTRIBUTIONS: [{
                'name': 'MZK Ełk / konwersja GTFS: Mikołaj Kuranowski (CC0)',
                'url': 'https://mkuran.pl/gtfs/'
            }]
        },
        GIZYCKO: {
            FIELD_NAME: 'Giżycko',
            FIELD_DESCRIPTION: 'GZK Bystry Giżycko (GTFS)',
            FIELD_ICON: 'bus-front',
            FIELD_DOWNLOADER: GizyckoDownloader,
            FIELD_CAPABILITIES: GIZYCKO_CAPABILITIES,
            FIELD_SETTINGS_CACHE: False,
            FIELD_ATTRIBUTIONS: [{
                'name': 'GZK Bystry / konwersja GTFS: Mikołaj Kuranowski (CC0)',
                'url': 'https://mkuran.pl/gtfs/'
            }]
        },
        KALISZ: {
            FIELD_NAME: 'Kalisz',
            FIELD_DESCRIPTION: 'KLA Kalisz (GTFS)',
            FIELD_ICON: 'bus-front',
            FIELD_DOWNLOADER: KaliszDownloader,
            FIELD_CAPABILITIES: KALISZ_CAPABILITIES,
            FIELD_SETTINGS_CACHE: False,
            FIELD_ATTRIBUTIONS: [{
                'name': 'KLA Kalisz / źródło: rj.sdip.kalisz.pl via kasznia.net (CC-BY-4.0)',
                'url': 'https://gtfs.kasznia.net/'
            }]
        },
        KIELCE: {
            FIELD_NAME: 'Kielce',
            FIELD_DESCRIPTION: 'ZTM Kielce (GTFS)',
            FIELD_ICON: 'bus-front',
            FIELD_DOWNLOADER: KielceDownloader,
            FIELD_CAPABILITIES: KIELCE_CAPABILITIES,
            FIELD_SETTINGS_CACHE: False,
            FIELD_ATTRIBUTIONS: [
                {
                    'name': 'Urząd Miasta Kielce – Zarząd Transportu Miejskiego',
                    'url': 'https://ztm.kielce.pl/'
                },
                {
                    'name': 'Konwersja GTFS: Mikołaj Kuranowski',
                    'url': 'https://mkuran.pl/gtfs/'
                }
            ]
        },
        KUTNO: {
            FIELD_NAME: 'Kutno',
            FIELD_DESCRIPTION: 'Komunikacja Miejska Kutno (GTFS)',
            FIELD_ICON: 'bus-front',
            FIELD_DOWNLOADER: KutnoDownloader,
            FIELD_CAPABILITIES: KUTNO_CAPABILITIES,
            FIELD_SETTINGS_CACHE: False,
            FIELD_ATTRIBUTIONS: [{
                'name': 'zbiorkom.live / Komunikacja Miejska Kutno',
                'url': 'https://zbiorkom.live/kutno'
            }]
        },
        LEGNICA: {
            FIELD_NAME: 'Legnica',
            FIELD_DESCRIPTION: 'MPK Legnica (GTFS)',
            FIELD_ICON: 'bus-front',
            FIELD_DOWNLOADER: LegnicaDownloader,
            FIELD_CAPABILITIES: LEGNICA_CAPABILITIES,
            FIELD_SETTINGS_CACHE: False,
            FIELD_ATTRIBUTIONS: [{
                'name': 'MPK Legnica / zbiorkom.live',
                'url': 'https://zbiorkom.live/legnica'
            }]
        },
        LESZNO: {
            FIELD_NAME: 'Leszno',
            FIELD_DESCRIPTION: 'MZK Leszno (GTFS)',
            FIELD_ICON: 'bus-front',
            FIELD_DOWNLOADER: LesznoDownloader,
            FIELD_CAPABILITIES: LESZNO_CAPABILITIES,
            FIELD_SETTINGS_CACHE: False,
            FIELD_ATTRIBUTIONS: [{
                'name': 'MZK Leszno / zbiorkom.live',
                'url': 'https://zbiorkom.live/leszno'
            }]
        },
        LOMZA: {
            FIELD_NAME: 'Łomża',
            FIELD_DESCRIPTION: 'MPK Łomża (GTFS)',
            FIELD_ICON: 'bus-front',
            FIELD_DOWNLOADER: LomzaDownloader,
            FIELD_CAPABILITIES: LOMZA_CAPABILITIES,
            FIELD_SETTINGS_CACHE: False,
            FIELD_ATTRIBUTIONS: [{
                'name': 'MPK ZB w Łomży / konwersja GTFS: Mikołaj Kuranowski (CC0)',
                'url': 'https://mkuran.pl/gtfs/'
            }]
        },
        OPOLE: {
            FIELD_NAME: 'Opole',
            FIELD_DESCRIPTION: 'MZK Opole (GTFS)',
            FIELD_ICON: 'bus-front',
            FIELD_DOWNLOADER: OpoleDownloader,
            FIELD_CAPABILITIES: OPOLE_CAPABILITIES,
            FIELD_SETTINGS_CACHE: False,
            FIELD_ATTRIBUTIONS: [{
                'name': 'MZK Sp. z o.o. Opole / zbiorkom.live',
                'url': 'https://zbiorkom.live/opole'
            }]
        },
        PRZEMYSL: {
            FIELD_NAME: 'Przemyśl',
            FIELD_DESCRIPTION: 'KM Przemyśl (GTFS)',
            FIELD_ICON: 'bus-front',
            FIELD_DOWNLOADER: PrzemyslDownloader,
            FIELD_CAPABILITIES: PRZEMYSL_CAPABILITIES,
            FIELD_SETTINGS_CACHE: False,
            FIELD_ATTRIBUTIONS: [{
                'name': 'Komunikacja Miejska w Przemyślu / zbiorkom.live',
                'url': 'https://zbiorkom.live/przemysl'
            }]
        },
        RADOM: {
            FIELD_NAME: 'Radom',
            FIELD_DESCRIPTION: 'MZDiK Radom (GTFS)',
            FIELD_ICON: 'bus-front',
            FIELD_DOWNLOADER: RadomDownloader,
            FIELD_CAPABILITIES: RADOM_CAPABILITIES,
            FIELD_SETTINGS_CACHE: False,
            FIELD_ATTRIBUTIONS: [{
                'name': 'MZDiK Radom / konwersja GTFS: Mikołaj Kuranowski (CC0)',
                'url': 'https://mkuran.pl/gtfs/'
            }]
        },
        RYBNIK: {
            FIELD_NAME: 'Rybnik',
            FIELD_DESCRIPTION: 'KM Rybnik (GTFS)',
            FIELD_ICON: 'bus-front',
            FIELD_DOWNLOADER: RybnikDownloader,
            FIELD_CAPABILITIES: RYBNIK_CAPABILITIES,
            FIELD_SETTINGS_CACHE: False,
            FIELD_ATTRIBUTIONS: [{
                'name': 'Komunikacja Miejska w Rybniku / zbiorkom.live',
                'url': 'https://zbiorkom.live/rybnik'
            }]
        },
        RZESZOW: {
            FIELD_NAME: 'Rzeszów',
            FIELD_DESCRIPTION: 'RTM Rzeszów (GTFS)',
            FIELD_ICON: 'bus-front',
            FIELD_DOWNLOADER: RzeszowDownloader,
            FIELD_CAPABILITIES: RZESZOW_CAPABILITIES,
            FIELD_SETTINGS_CACHE: False,
            FIELD_ATTRIBUTIONS: [{
                'name': 'Rzeszowski Transport Miejski / Otwarte Dane Rzeszów',
                'url': 'https://otwartedane.erzeszow.pl/dataset/rozklady-jazdy-gtfs'
            }]
        },
        SUWALKI: {
            FIELD_NAME: 'Suwałki',
            FIELD_DESCRIPTION: 'KM Suwałki (GTFS)',
            FIELD_ICON: 'bus-front',
            FIELD_DOWNLOADER: SuwalikiDownloader,
            FIELD_CAPABILITIES: SUWALKI_CAPABILITIES,
            FIELD_SETTINGS_CACHE: False,
            FIELD_ATTRIBUTIONS: [{
                'name': 'Komunikacja Miejska w Suwałkach / zbiorkom.live',
                'url': 'https://zbiorkom.live/suwalki'
            }]
        },
        SWINOUJSCIE: {
            FIELD_NAME: 'Świnoujście',
            FIELD_DESCRIPTION: 'KA Świnoujście (GTFS)',
            FIELD_ICON: 'bus-front',
            FIELD_DOWNLOADER: SwinoujscieDownloader,
            FIELD_CAPABILITIES: SWINOUJSCIE_CAPABILITIES,
            FIELD_SETTINGS_CACHE: False,
            FIELD_ATTRIBUTIONS: [{
                'name': 'KA Świnoujście / konwersja GTFS: Mikołaj Kuranowski (CC0)',
                'url': 'https://mkuran.pl/gtfs/'
            }]
        },
        WEJHEROWO: {
            FIELD_NAME: 'Wejherowo',
            FIELD_DESCRIPTION: 'MZK Wejherowo (GTFS)',
            FIELD_ICON: 'bus-front',
            FIELD_DOWNLOADER: WejherowoDownloader,
            FIELD_CAPABILITIES: WEJHEROWO_CAPABILITIES,
            FIELD_SETTINGS_CACHE: False,
            FIELD_ATTRIBUTIONS: [{
                'name': 'MZK Wejherowo / konwersja GTFS: Mikołaj Kuranowski (CC0)',
                'url': 'https://mkuran.pl/gtfs/'
            }]
        },
    }

    def __new__(cls):
        """Prevents creating instances of this static resource class."""
        raise TypeError(f'{cls.__name__} cannot be instantiated.')

    @classmethod
    def downloader(cls, provider_id: str) -> Type[Any]:
        """Returns the downloader registered for a provider identifier."""
        provider = cls.VALUES.get(provider_id)
        if not provider:
            raise ValueError('Unsupported public transport provider.')
        return provider[cls.FIELD_DOWNLOADER]

    @classmethod
    def capabilities(cls, provider_id: str) -> Dict[str, object]:
        """Returns an immutable copy of provider-specific view capabilities."""
        provider = cls.VALUES.get(provider_id)
        if not provider:
            raise ValueError('Unsupported public transport provider.')
        capabilities = provider.get(cls.FIELD_CAPABILITIES, {})
        return dict(capabilities) if isinstance(capabilities, dict) else {}

    @classmethod
    def uses_settings_cache(cls, provider_id: str) -> bool:
        """Returns whether view data is persisted in settings JSON."""
        provider = cls.VALUES.get(provider_id)
        if not provider:
            raise ValueError('Unsupported public transport provider.')
        return bool(provider.get(cls.FIELD_SETTINGS_CACHE, False))

    @classmethod
    def providers_without_settings_cache(cls) -> list[str]:
        """Returns providers whose persistent cache has a separate backend."""
        return [
            provider_id
            for provider_id in cls.VALUES
            if not cls.uses_settings_cache(provider_id)
        ]

    @classmethod
    def options(cls) -> list[dict[str, Any]]:
        """Returns providers alphabetically for selectors and data sources."""
        options = [
            {
                'id': provider_id,
                'name': str(provider[cls.FIELD_NAME]),
                'description': str(provider[cls.FIELD_DESCRIPTION]),
                'icon': str(provider[cls.FIELD_ICON]),
                'show_route_map': bool(
                    provider.get(cls.FIELD_CAPABILITIES, {}).get(
                        cls.CAPABILITY_SHOW_ROUTE_MAP,
                        False
                    )
                ),
                'approximate_route_map': bool(
                    provider.get(cls.FIELD_CAPABILITIES, {}).get(
                        cls.CAPABILITY_APPROXIMATE_ROUTE_MAP,
                        False
                    )
                ),
                'show_vehicle_positions': bool(
                    provider.get(cls.FIELD_CAPABILITIES, {}).get(
                        cls.CAPABILITY_SHOW_VEHICLE_POSITIONS,
                        False
                    )
                ),
                'region': cls.REGIONS.get(provider_id, ''),
                'attributions': list(provider.get(cls.FIELD_ATTRIBUTIONS, []))
            }
            for provider_id, provider in cls.VALUES.items()
        ]
        _pl = str.maketrans({
            'ą': 'a~', 'ć': 'c~', 'ę': 'e~', 'ł': 'l~',
            'ń': 'n~', 'ó': 'o~', 'ś': 's~', 'ź': 'z~', 'ż': 'z~~'
        })

        def _sort_key(text: str) -> str:
            return text.casefold().translate(_pl)

        return sorted(
            options,
            key=lambda option: (
                _sort_key(option['region']),
                _sort_key(str(option['name']))
            )
        )

    @classmethod
    def options_by_region(cls) -> list[dict]:
        """Returns providers grouped by region, preserving Polish sort order."""
        groups: list[dict] = []
        index: dict[str, int] = {}
        for option in cls.options():
            region = option['region']
            if region not in index:
                index[region] = len(groups)
                groups.append({'region': region, 'providers': []})
            groups[index[region]]['providers'].append(option)
        return groups

    @classmethod
    def validate_url(cls, provider_id: str, url: str) -> str:
        """Validates that a detail URL belongs to the selected provider."""
        downloader = cls.downloader(provider_id)
        parsed = urlparse(url)
        prefixes = getattr(
            downloader,
            'URL_PREFIXES',
            (downloader.BASE_URL,)
        )
        is_allowed = any(
            parsed.scheme == expected.scheme
            and parsed.netloc == expected.netloc
            and parsed.path.startswith(expected.path)
            for expected in map(urlparse, prefixes)
        )
        if not is_allowed:
            raise ValueError('Invalid public transport URL.')
        return url

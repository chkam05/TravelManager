from __future__ import annotations
import unicodedata
from typing import Any, ClassVar, Dict, Type
from urllib.parse import urlparse

from core.language_service import LanguageService
from resources.public_transport.public_transport_messages import PublicTransportValueError
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
from utils.public_transport.rail_downloader import RAIL_DOWNLOADERS
from resources.public_transport.rail_gtfs_sources import RailGtfsSources


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

    NAME_KEYS: ClassVar[Dict[str, str]] = {
        BIALYSTOK: 'RES_PUBLIC_TRANSPORT_PROVIDER.BIALYSTOK_NAME',
        CHOJNICE: 'RES_PUBLIC_TRANSPORT_PROVIDER.CHOJNICE_NAME',
        ELK: 'RES_PUBLIC_TRANSPORT_PROVIDER.ELK_NAME',
        GIZYCKO: 'RES_PUBLIC_TRANSPORT_PROVIDER.GIZYCKO_NAME',
        KALISZ: 'RES_PUBLIC_TRANSPORT_PROVIDER.KALISZ_NAME',
        KIELCE: 'RES_PUBLIC_TRANSPORT_PROVIDER.KIELCE_NAME',
        KUTNO: 'RES_PUBLIC_TRANSPORT_PROVIDER.KUTNO_NAME',
        LEGNICA: 'RES_PUBLIC_TRANSPORT_PROVIDER.LEGNICA_NAME',
        LESZNO: 'RES_PUBLIC_TRANSPORT_PROVIDER.LESZNO_NAME',
        LOMZA: 'RES_PUBLIC_TRANSPORT_PROVIDER.LOMZA_NAME',
        OPOLE: 'RES_PUBLIC_TRANSPORT_PROVIDER.OPOLE_NAME',
        PRZEMYSL: 'RES_PUBLIC_TRANSPORT_PROVIDER.PRZEMYSL_NAME',
        RADOM: 'RES_PUBLIC_TRANSPORT_PROVIDER.RADOM_NAME',
        RYBNIK: 'RES_PUBLIC_TRANSPORT_PROVIDER.RYBNIK_NAME',
        RZESZOW: 'RES_PUBLIC_TRANSPORT_PROVIDER.RZESZOW_NAME',
        SUWALKI: 'RES_PUBLIC_TRANSPORT_PROVIDER.SUWALKI_NAME',
        SWINOUJSCIE: 'RES_PUBLIC_TRANSPORT_PROVIDER.SWINOUJSCIE_NAME',
        WEJHEROWO: 'RES_PUBLIC_TRANSPORT_PROVIDER.WEJHEROWO_NAME',
        GZM: 'RES_PUBLIC_TRANSPORT_PROVIDER.GZM_NAME',
        CZESTOCHOWA: 'RES_PUBLIC_TRANSPORT_PROVIDER.CZESTOCHOWA_NAME',
        KRAKOW: 'RES_PUBLIC_TRANSPORT_PROVIDER.KRAKOW_NAME',
        WARSAW: 'RES_PUBLIC_TRANSPORT_PROVIDER.WARSAW_NAME',
        GDANSK: 'RES_PUBLIC_TRANSPORT_PROVIDER.GDANSK_NAME',
        GDYNIA: 'RES_PUBLIC_TRANSPORT_PROVIDER.GDYNIA_NAME',
        SZCZECIN: 'RES_PUBLIC_TRANSPORT_PROVIDER.SZCZECIN_NAME',
        POZNAN: 'RES_PUBLIC_TRANSPORT_PROVIDER.POZNAN_NAME',
        BYDGOSZCZ: 'RES_PUBLIC_TRANSPORT_PROVIDER.BYDGOSZCZ_NAME',
        TORUN: 'RES_PUBLIC_TRANSPORT_PROVIDER.TORUN_NAME',
        WROCLAW: 'RES_PUBLIC_TRANSPORT_PROVIDER.WROCLAW_NAME',
        ELBLAG: 'RES_PUBLIC_TRANSPORT_PROVIDER.ELBLAG_NAME',
        GORZOW: 'RES_PUBLIC_TRANSPORT_PROVIDER.GORZOW_NAME',
        GRUDZIADZ: 'RES_PUBLIC_TRANSPORT_PROVIDER.GRUDZIADZ_NAME',
        LUBLIN: 'RES_PUBLIC_TRANSPORT_PROVIDER.LUBLIN_NAME',
        LODZ: 'RES_PUBLIC_TRANSPORT_PROVIDER.LODZ_NAME',
        OLSZTYN: 'RES_PUBLIC_TRANSPORT_PROVIDER.OLSZTYN_NAME'
    }
    DESCRIPTION_KEYS: ClassVar[Dict[str, str]] = {
        BIALYSTOK: 'RES_PUBLIC_TRANSPORT_PROVIDER.BIALYSTOK_DESCRIPTION',
        CHOJNICE: 'RES_PUBLIC_TRANSPORT_PROVIDER.CHOJNICE_DESCRIPTION',
        ELK: 'RES_PUBLIC_TRANSPORT_PROVIDER.ELK_DESCRIPTION',
        GIZYCKO: 'RES_PUBLIC_TRANSPORT_PROVIDER.GIZYCKO_DESCRIPTION',
        KALISZ: 'RES_PUBLIC_TRANSPORT_PROVIDER.KALISZ_DESCRIPTION',
        KIELCE: 'RES_PUBLIC_TRANSPORT_PROVIDER.KIELCE_DESCRIPTION',
        KUTNO: 'RES_PUBLIC_TRANSPORT_PROVIDER.KUTNO_DESCRIPTION',
        LEGNICA: 'RES_PUBLIC_TRANSPORT_PROVIDER.LEGNICA_DESCRIPTION',
        LESZNO: 'RES_PUBLIC_TRANSPORT_PROVIDER.LESZNO_DESCRIPTION',
        LOMZA: 'RES_PUBLIC_TRANSPORT_PROVIDER.LOMZA_DESCRIPTION',
        OPOLE: 'RES_PUBLIC_TRANSPORT_PROVIDER.OPOLE_DESCRIPTION',
        PRZEMYSL: 'RES_PUBLIC_TRANSPORT_PROVIDER.PRZEMYSL_DESCRIPTION',
        RADOM: 'RES_PUBLIC_TRANSPORT_PROVIDER.RADOM_DESCRIPTION',
        RYBNIK: 'RES_PUBLIC_TRANSPORT_PROVIDER.RYBNIK_DESCRIPTION',
        RZESZOW: 'RES_PUBLIC_TRANSPORT_PROVIDER.RZESZOW_DESCRIPTION',
        SUWALKI: 'RES_PUBLIC_TRANSPORT_PROVIDER.SUWALKI_DESCRIPTION',
        SWINOUJSCIE: 'RES_PUBLIC_TRANSPORT_PROVIDER.SWINOUJSCIE_DESCRIPTION',
        WEJHEROWO: 'RES_PUBLIC_TRANSPORT_PROVIDER.WEJHEROWO_DESCRIPTION',
        GZM: 'RES_PUBLIC_TRANSPORT_PROVIDER.GZM_DESCRIPTION',
        CZESTOCHOWA: 'RES_PUBLIC_TRANSPORT_PROVIDER.CZESTOCHOWA_DESCRIPTION',
        KRAKOW: 'RES_PUBLIC_TRANSPORT_PROVIDER.KRAKOW_DESCRIPTION',
        WARSAW: 'RES_PUBLIC_TRANSPORT_PROVIDER.WARSAW_DESCRIPTION',
        GDANSK: 'RES_PUBLIC_TRANSPORT_PROVIDER.GDANSK_DESCRIPTION',
        GDYNIA: 'RES_PUBLIC_TRANSPORT_PROVIDER.GDYNIA_DESCRIPTION',
        SZCZECIN: 'RES_PUBLIC_TRANSPORT_PROVIDER.SZCZECIN_DESCRIPTION',
        POZNAN: 'RES_PUBLIC_TRANSPORT_PROVIDER.POZNAN_DESCRIPTION',
        BYDGOSZCZ: 'RES_PUBLIC_TRANSPORT_PROVIDER.BYDGOSZCZ_DESCRIPTION',
        TORUN: 'RES_PUBLIC_TRANSPORT_PROVIDER.TORUN_DESCRIPTION',
        WROCLAW: 'RES_PUBLIC_TRANSPORT_PROVIDER.WROCLAW_DESCRIPTION',
        ELBLAG: 'RES_PUBLIC_TRANSPORT_PROVIDER.ELBLAG_DESCRIPTION',
        GORZOW: 'RES_PUBLIC_TRANSPORT_PROVIDER.GORZOW_DESCRIPTION',
        GRUDZIADZ: 'RES_PUBLIC_TRANSPORT_PROVIDER.GRUDZIADZ_DESCRIPTION',
        LUBLIN: 'RES_PUBLIC_TRANSPORT_PROVIDER.LUBLIN_DESCRIPTION',
        LODZ: 'RES_PUBLIC_TRANSPORT_PROVIDER.LODZ_DESCRIPTION',
        OLSZTYN: 'RES_PUBLIC_TRANSPORT_PROVIDER.OLSZTYN_DESCRIPTION'
    }
    ATTRIBUTION_KEYS: ClassVar[Dict[str, tuple[str, ...]]] = {
        GZM: ('RES_PUBLIC_TRANSPORT_PROVIDER.GZM_ATTRIBUTION_1',),
        CZESTOCHOWA: ('RES_PUBLIC_TRANSPORT_PROVIDER.CZESTOCHOWA_ATTRIBUTION_1',),
        CHOJNICE: (
            'RES_PUBLIC_TRANSPORT_PROVIDER.CHOJNICE_ATTRIBUTION_1',
            'RES_PUBLIC_TRANSPORT_PROVIDER.CHOJNICE_ATTRIBUTION_2'
        ),
        KRAKOW: ('RES_PUBLIC_TRANSPORT_PROVIDER.KRAKOW_ATTRIBUTION_1',),
        WARSAW: (
            'RES_PUBLIC_TRANSPORT_PROVIDER.WARSAW_ATTRIBUTION_1',
            'RES_PUBLIC_TRANSPORT_PROVIDER.WARSAW_ATTRIBUTION_2',
            'RES_PUBLIC_TRANSPORT_PROVIDER.WARSAW_ATTRIBUTION_3'
        ),
        GDANSK: ('RES_PUBLIC_TRANSPORT_PROVIDER.GDANSK_ATTRIBUTION_1',),
        GDYNIA: ('RES_PUBLIC_TRANSPORT_PROVIDER.GDYNIA_ATTRIBUTION_1',),
        SZCZECIN: ('RES_PUBLIC_TRANSPORT_PROVIDER.SZCZECIN_ATTRIBUTION_1',),
        POZNAN: ('RES_PUBLIC_TRANSPORT_PROVIDER.POZNAN_ATTRIBUTION_1',),
        BYDGOSZCZ: ('RES_PUBLIC_TRANSPORT_PROVIDER.BYDGOSZCZ_ATTRIBUTION_1',),
        TORUN: (
            'RES_PUBLIC_TRANSPORT_PROVIDER.TORUN_ATTRIBUTION_1',
            'RES_PUBLIC_TRANSPORT_PROVIDER.TORUN_ATTRIBUTION_2'
        ),
        WROCLAW: (
            'RES_PUBLIC_TRANSPORT_PROVIDER.WROCLAW_ATTRIBUTION_1',
            'RES_PUBLIC_TRANSPORT_PROVIDER.WROCLAW_ATTRIBUTION_2'
        ),
        ELBLAG: ('RES_PUBLIC_TRANSPORT_PROVIDER.ELBLAG_ATTRIBUTION_1',),
        GORZOW: ('RES_PUBLIC_TRANSPORT_PROVIDER.GORZOW_ATTRIBUTION_1',),
        GRUDZIADZ: (
            'RES_PUBLIC_TRANSPORT_PROVIDER.GRUDZIADZ_ATTRIBUTION_1',
            'RES_PUBLIC_TRANSPORT_PROVIDER.GRUDZIADZ_ATTRIBUTION_2'
        ),
        LUBLIN: ('RES_PUBLIC_TRANSPORT_PROVIDER.LUBLIN_ATTRIBUTION_1',),
        LODZ: ('RES_PUBLIC_TRANSPORT_PROVIDER.LODZ_ATTRIBUTION_1',),
        OLSZTYN: ('RES_PUBLIC_TRANSPORT_PROVIDER.OLSZTYN_ATTRIBUTION_1',),
        BIALYSTOK: ('RES_PUBLIC_TRANSPORT_PROVIDER.BIALYSTOK_ATTRIBUTION_1',),
        ELK: ('RES_PUBLIC_TRANSPORT_PROVIDER.ELK_ATTRIBUTION_1',),
        GIZYCKO: ('RES_PUBLIC_TRANSPORT_PROVIDER.GIZYCKO_ATTRIBUTION_1',),
        KALISZ: ('RES_PUBLIC_TRANSPORT_PROVIDER.KALISZ_ATTRIBUTION_1',),
        KIELCE: (
            'RES_PUBLIC_TRANSPORT_PROVIDER.KIELCE_ATTRIBUTION_1',
            'RES_PUBLIC_TRANSPORT_PROVIDER.KIELCE_ATTRIBUTION_2'
        ),
        KUTNO: ('RES_PUBLIC_TRANSPORT_PROVIDER.KUTNO_ATTRIBUTION_1',),
        LEGNICA: ('RES_PUBLIC_TRANSPORT_PROVIDER.LEGNICA_ATTRIBUTION_1',),
        LESZNO: ('RES_PUBLIC_TRANSPORT_PROVIDER.LESZNO_ATTRIBUTION_1',),
        LOMZA: ('RES_PUBLIC_TRANSPORT_PROVIDER.LOMZA_ATTRIBUTION_1',),
        OPOLE: ('RES_PUBLIC_TRANSPORT_PROVIDER.OPOLE_ATTRIBUTION_1',),
        PRZEMYSL: ('RES_PUBLIC_TRANSPORT_PROVIDER.PRZEMYSL_ATTRIBUTION_1',),
        RADOM: ('RES_PUBLIC_TRANSPORT_PROVIDER.RADOM_ATTRIBUTION_1',),
        RYBNIK: ('RES_PUBLIC_TRANSPORT_PROVIDER.RYBNIK_ATTRIBUTION_1',),
        RZESZOW: ('RES_PUBLIC_TRANSPORT_PROVIDER.RZESZOW_ATTRIBUTION_1',),
        SUWALKI: ('RES_PUBLIC_TRANSPORT_PROVIDER.SUWALKI_ATTRIBUTION_1',),
        SWINOUJSCIE: ('RES_PUBLIC_TRANSPORT_PROVIDER.SWINOUJSCIE_ATTRIBUTION_1',),
        WEJHEROWO: ('RES_PUBLIC_TRANSPORT_PROVIDER.WEJHEROWO_ATTRIBUTION_1',)
    }
    REGION_KEYS: ClassVar[Dict[str, str]] = {
        'dolnośląskie': 'RES_PUBLIC_TRANSPORT_REGION.LOWER_SILESIAN',
        'kujawsko-pomorskie': 'RES_PUBLIC_TRANSPORT_REGION.KUYAVIAN_POMERANIAN',
        'lubelskie': 'RES_PUBLIC_TRANSPORT_REGION.LUBLIN',
        'lubuskie': 'RES_PUBLIC_TRANSPORT_REGION.LUBUSZ',
        'mazowieckie': 'RES_PUBLIC_TRANSPORT_REGION.MASOVIAN',
        'małopolskie': 'RES_PUBLIC_TRANSPORT_REGION.LESSER_POLAND',
        'opolskie': 'RES_PUBLIC_TRANSPORT_REGION.OPOLE',
        'podkarpackie': 'RES_PUBLIC_TRANSPORT_REGION.SUBCARPATHIAN',
        'podlaskie': 'RES_PUBLIC_TRANSPORT_REGION.PODLASKIE',
        'pomorskie': 'RES_PUBLIC_TRANSPORT_REGION.POMERANIAN',
        'warmińsko-mazurskie': 'RES_PUBLIC_TRANSPORT_REGION.WARMIAN_MASURIAN',
        'wielkopolskie': 'RES_PUBLIC_TRANSPORT_REGION.GREATER_POLAND',
        'zachodniopomorskie': 'RES_PUBLIC_TRANSPORT_REGION.WEST_POMERANIAN',
        'łódzkie': 'RES_PUBLIC_TRANSPORT_REGION.LODZ',
        'śląskie': 'RES_PUBLIC_TRANSPORT_REGION.SILESIAN',
        'świętokrzyskie': 'RES_PUBLIC_TRANSPORT_REGION.HOLY_CROSS'
    }

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
        CAPABILITY_DIRECTION_SELECTOR_LABEL: 'PUBLIC_TRANSPORT_VIEW.DIRECTION'
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
        CAPABILITY_DIRECTION_SELECTOR_LABEL: 'PUBLIC_TRANSPORT_LINES.ROUTE_VARIANT'
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
        CAPABILITY_DIRECTION_SELECTOR_LABEL: 'PUBLIC_TRANSPORT_LINES.ROUTE_VARIANT'
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
        CAPABILITY_DIRECTION_SELECTOR_LABEL: 'PUBLIC_TRANSPORT_LINES.ROUTE_VARIANT'
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
            raise PublicTransportValueError(
                'PUBLIC_TRANSPORT_ERROR.UNSUPPORTED_PROVIDER'
            )
        return provider[cls.FIELD_DOWNLOADER]

    @classmethod
    def capabilities(cls, provider_id: str) -> Dict[str, object]:
        """Returns an immutable copy of provider-specific view capabilities."""
        provider = cls.VALUES.get(provider_id)
        if not provider:
            raise PublicTransportValueError(
                'PUBLIC_TRANSPORT_ERROR.UNSUPPORTED_PROVIDER'
            )
        capabilities = provider.get(cls.FIELD_CAPABILITIES, {})
        result = dict(capabilities) if isinstance(capabilities, dict) else {}
        direction_key = result.get(cls.CAPABILITY_DIRECTION_SELECTOR_LABEL)
        if isinstance(direction_key, str) and direction_key.startswith('PUBLIC_TRANSPORT_'):
            result[cls.CAPABILITY_DIRECTION_SELECTOR_LABEL] = LanguageService.translate_current(direction_key)
        return result

    @classmethod
    def uses_settings_cache(cls, provider_id: str) -> bool:
        """Returns whether view data is persisted in settings JSON."""
        provider = cls.VALUES.get(provider_id)
        if not provider:
            raise PublicTransportValueError(
                'PUBLIC_TRANSPORT_ERROR.UNSUPPORTED_PROVIDER'
            )
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
                'mode': 'rail' if provider_id.startswith('rail_') else 'city',
                'update_source': next(
                    (
                        mapping.source_id
                        for mapping in RailGtfsSources.PROVIDERS
                        if mapping.provider_id == provider_id
                    ),
                    provider_id
                ),
                'name': LanguageService.translate_current(cls.NAME_KEYS[provider_id]),
                'description': LanguageService.translate_current(cls.DESCRIPTION_KEYS[provider_id]),
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
                'region': LanguageService.translate_current(cls.REGION_KEYS[cls.REGIONS[provider_id]]),
                'attributions': [
                    {
                        **attribution,
                        'name': LanguageService.translate_current(key)
                    }
                    for attribution, key in zip(
                        provider.get(cls.FIELD_ATTRIBUTIONS, []),
                        cls.ATTRIBUTION_KEYS[provider_id]
                    )
                ]
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
                0 if option['id'].startswith('rail_') else 1,
                (
                    next(
                        index
                        for index, mapping in enumerate(RailGtfsSources.PROVIDERS)
                        if mapping.provider_id == option['id']
                    )
                    if option['id'].startswith('rail_')
                    else _sort_key(option['region'])
                ),
                _sort_key(str(option['name']))
            )
        )

    @classmethod
    def options_by_region(cls) -> list[dict]:
        """Returns providers grouped by region in the active locale."""
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
            raise PublicTransportValueError(
                'PUBLIC_TRANSPORT_ERROR.INVALID_URL'
            )
        return url


def _register_rail_providers() -> None:
    """Adds railway providers without disturbing the municipal registry order."""
    registry = PublicTransportProviders
    registry.REGION_KEYS['rail_main'] = 'RES_PUBLIC_TRANSPORT_REGION.RAIL_MAIN'
    rail_regions = {
        'rail_pkp_intercity': 'rail_main',
        'rail_polregio': 'rail_main',
        'rail_regiojet': 'rail_main',
        'rail_leo_express': 'rail_main',
        'rail_arriva': 'kujawsko-pomorskie',
        'rail_kd': 'dolnośląskie',
        'rail_kmal': 'małopolskie',
        'rail_km': 'mazowieckie',
        'rail_skm_warsaw': 'mazowieckie',
        'rail_wkd': 'mazowieckie',
        'rail_ks': 'śląskie',
        'rail_kw': 'wielkopolskie',
        'rail_lka': 'łódzkie',
        'rail_skm_tricity': 'pomorskie'
    }
    capabilities = {
        registry.CAPABILITY_SHOW_PLATFORMS: True,
        registry.CAPABILITY_SHOW_STOP_MAP: True,
        registry.CAPABILITY_SHOW_RIDE_MAP: True,
        registry.CAPABILITY_SHOW_RIDE_DISTANCES: True,
        registry.CAPABILITY_SHOW_VEHICLE_DETAILS: True,
        registry.CAPABILITY_SHOW_HIGH_FLOOR: False,
        registry.CAPABILITY_SHOW_STOP_DEPARTURES: True,
        registry.CAPABILITY_SHOW_RIDE: True,
        registry.CAPABILITY_SHOW_ROUTE_MAP: True,
        registry.CAPABILITY_SHOW_VEHICLE_POSITIONS: False,
        registry.CAPABILITY_CACHE_ANNOUNCEMENTS: False,
        registry.CAPABILITY_DIRECTION_SELECTOR_LABEL: (
            'PUBLIC_TRANSPORT_LINES.ROUTE_VARIANT'
        ),
        'rail_terminology': True
    }
    for mapping in RailGtfsSources.PROVIDERS:
        constant = mapping.provider_id.upper()
        setattr(registry, constant, mapping.provider_id)
        registry.NAME_KEYS[mapping.provider_id] = (
            f'RES_PUBLIC_TRANSPORT_PROVIDER.{constant}_NAME'
        )
        registry.DESCRIPTION_KEYS[mapping.provider_id] = (
            'RES_PUBLIC_TRANSPORT_PROVIDER.RAIL_DESCRIPTION'
        )
        registry.ATTRIBUTION_KEYS[mapping.provider_id] = (
            'RES_PUBLIC_TRANSPORT_PROVIDER.RAIL_ATTRIBUTION_1',
        )
        registry.REGIONS[mapping.provider_id] = rail_regions[mapping.provider_id]
        source = RailGtfsSources.SOURCES[mapping.source_id]
        registry.VALUES[mapping.provider_id] = {
            registry.FIELD_NAME: mapping.display_name,
            registry.FIELD_DESCRIPTION: 'Kolejowy rozkład GTFS',
            registry.FIELD_ICON: 'train-front',
            registry.FIELD_DOWNLOADER: RAIL_DOWNLOADERS[mapping.provider_id],
            registry.FIELD_CAPABILITIES: dict(capabilities),
            registry.FIELD_SETTINGS_CACHE: False,
            registry.FIELD_ATTRIBUTIONS: [{
                'name': 'GTFS: Mikołaj Kuranowski / dane przewoźników',
                'url': source.schedule_url
            }]
        }


_register_rail_providers()

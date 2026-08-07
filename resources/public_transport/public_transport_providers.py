from __future__ import annotations
import unicodedata
from typing import Any, ClassVar, Dict, Type
from urllib.parse import urlparse

from utils.public_transport.czestochowa_downloader import CzestochowaDownloader
from utils.public_transport.elblag_downloader import ElblagDownloader
from utils.public_transport.gorzow_downloader import GorzowDownloader
from utils.public_transport.gzm_downloader import GzmDownloader
from utils.public_transport.krakow_downloader import KrakowDownloader
from utils.public_transport.lublin_downloader import LublinDownloader
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
    LUBLIN: ClassVar[str] = 'lublin'
    OLSZTYN: ClassVar[str] = 'olsztyn'

    FIELD_NAME: ClassVar[str] = 'name'
    FIELD_DESCRIPTION: ClassVar[str] = 'description'
    FIELD_ICON: ClassVar[str] = 'icon'
    FIELD_DOWNLOADER: ClassVar[str] = 'downloader'
    FIELD_CAPABILITIES: ClassVar[str] = 'capabilities'
    FIELD_SETTINGS_CACHE: ClassVar[str] = 'settings_cache'
    FIELD_ATTRIBUTIONS: ClassVar[str] = 'attributions'

    CAPABILITY_SHOW_PLATFORMS: ClassVar[str] = 'show_platforms'
    CAPABILITY_SHOW_STOP_MAP: ClassVar[str] = 'show_stop_map'
    CAPABILITY_SHOW_RIDE_MAP: ClassVar[str] = 'show_ride_map'
    CAPABILITY_SHOW_RIDE_DISTANCES: ClassVar[str] = 'show_ride_distances'
    CAPABILITY_SHOW_VEHICLE_DETAILS: ClassVar[str] = 'show_vehicle_details'
    CAPABILITY_SHOW_HIGH_FLOOR: ClassVar[str] = 'show_high_floor'
    CAPABILITY_SHOW_STOP_DEPARTURES: ClassVar[str] = 'show_stop_departures'
    CAPABILITY_SHOW_RIDE: ClassVar[str] = 'show_ride'
    CAPABILITY_SHOW_ROUTE_MAP: ClassVar[str] = 'show_route_map'
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
        CAPABILITY_SHOW_ROUTE_MAP: True,
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
        CAPABILITY_SHOW_VEHICLE_POSITIONS: False
    }
    GORZOW_CAPABILITIES: ClassVar[Dict[str, object]] = {
        **WARSAW_CAPABILITIES,
        CAPABILITY_SHOW_VEHICLE_POSITIONS: False
    }
    LUBLIN_CAPABILITIES: ClassVar[Dict[str, object]] = {
        **WARSAW_CAPABILITIES,
        CAPABILITY_SHOW_VEHICLE_POSITIONS: False
    }
    OLSZTYN_CAPABILITIES: ClassVar[Dict[str, object]] = {
        **WARSAW_CAPABILITIES,
        CAPABILITY_SHOW_VEHICLE_POSITIONS: False
    }

    VALUES: ClassVar[Dict[str, Dict[str, object]]] = {
        GZM: {
            FIELD_NAME: 'Górnośląsko-Zagłębiowska Metropolia',
            FIELD_DESCRIPTION: 'Transport GZM',
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
        }
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
                'attributions': list(provider.get(cls.FIELD_ATTRIBUTIONS, []))
            }
            for provider_id, provider in cls.VALUES.items()
        ]
        return sorted(
            options,
            key=lambda option: unicodedata.normalize(
                'NFKD',
                str(option['name']).casefold()
            )
        )

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

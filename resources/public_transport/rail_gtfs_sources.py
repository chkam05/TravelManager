"""Stable application identifiers for the Polish railway GTFS feeds.

Source identifiers are deliberately kept separate from provider identifiers.
The former may change when a publisher changes its feed, while the latter are
part of TravelManager settings and UI state.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar


@dataclass(frozen=True)
class RailGtfsSource:
    """One physical GTFS source shared by one or more rail providers."""

    source_id: str
    schedule_url: str
    realtime_url: str


@dataclass(frozen=True)
class RailProviderMapping:
    """Maps a stable application provider to its current source agency."""

    provider_id: str
    display_name: str
    source_id: str
    agency_ids: tuple[str, ...]


class RailGtfsSources:
    """Audited railway sources and agency mappings, in required UI order."""

    POLISH_TRAINS: ClassVar[str] = 'polish_trains'
    WKD: ClassVar[str] = 'wkd'

    SOURCES: ClassVar[dict[str, RailGtfsSource]] = {
        POLISH_TRAINS: RailGtfsSource(
            source_id=POLISH_TRAINS,
            schedule_url='https://mkuran.pl/gtfs/polish_trains.zip',
            realtime_url=(
                'https://mkuran.pl/gtfs/polish_trains/updates.pb'
            )
        ),
        WKD: RailGtfsSource(
            source_id=WKD,
            schedule_url='https://mkuran.pl/gtfs/wkd.zip',
            realtime_url='https://mkuran.pl/gtfs/wkd.pb'
        )
    }

    PROVIDERS: ClassVar[tuple[RailProviderMapping, ...]] = (
        RailProviderMapping(
            'rail_pkp_intercity', 'PKP Intercity', POLISH_TRAINS, ('IC',)
        ),
        RailProviderMapping(
            'rail_polregio', 'POLREGIO', POLISH_TRAINS, ('PR',)
        ),
        RailProviderMapping(
            'rail_arriva', 'Arriva RP', POLISH_TRAINS, ('AR',)
        ),
        RailProviderMapping(
            'rail_kd', 'Koleje Dolnośląskie', POLISH_TRAINS, ('KD',)
        ),
        RailProviderMapping(
            'rail_kmal', 'Koleje Małopolskie', POLISH_TRAINS, ('KML',)
        ),
        RailProviderMapping(
            'rail_km', 'Koleje Mazowieckie', POLISH_TRAINS, ('KM',)
        ),
        RailProviderMapping(
            'rail_ks', 'Koleje Śląskie', POLISH_TRAINS, ('KS',)
        ),
        RailProviderMapping(
            'rail_kw', 'Koleje Wielkopolskie', POLISH_TRAINS, ('KW',)
        ),
        RailProviderMapping(
            'rail_lka', 'Łódzka Kolej Aglomeracyjna',
            POLISH_TRAINS, ('LKA',)
        ),
        RailProviderMapping(
            'rail_skm_tricity', 'PKP SKM w Trójmieście',
            POLISH_TRAINS, ('SKMT',)
        ),
        RailProviderMapping(
            'rail_regiojet', 'RegioJet', POLISH_TRAINS, ('RJ',)
        ),
        RailProviderMapping(
            'rail_leo_express', 'Leo Express', POLISH_TRAINS, ('LEO',)
        ),
        RailProviderMapping(
            'rail_skm_warsaw', 'SKM Warszawa', POLISH_TRAINS, ('SKM',)
        ),
        RailProviderMapping(
            'rail_wkd', 'Warszawska Kolej Dojazdowa', WKD, ('0',)
        )
    )

    @classmethod
    def provider(cls, provider_id: str) -> RailProviderMapping:
        """Returns one mapping without falling back to another operator."""
        for provider in cls.PROVIDERS:
            if provider.provider_id == provider_id:
                return provider
        raise KeyError(provider_id)

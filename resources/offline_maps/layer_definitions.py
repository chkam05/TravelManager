"""Declarative OSM filtering and generalisation rules for offline maps."""

from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar, Mapping


@dataclass(frozen=True)
class OfflineMapTagRule:
    """One AND rule; a layer matches when any of its rules matches."""

    required: tuple[tuple[str, frozenset[str] | None], ...]
    excluded: tuple[tuple[str, frozenset[str]], ...] = ()

    def matches(self, tags: Mapping[str, str]) -> bool:
        for key, values in self.required:
            value = tags.get(key)
            if value is None or (values is not None and value not in values):
                return False
        return not any(tags.get(key) in values for key, values in self.excluded)


@dataclass(frozen=True)
class OfflineMapLayerDefinition:
    """Complete filtering contract consumed by PBF and MVT stages."""

    id: str
    source_types: frozenset[str]
    geometry_types: frozenset[str]
    rules: tuple[OfflineMapTagRule, ...]
    min_zoom: int
    priority: int
    properties: frozenset[str]
    simplification: tuple[tuple[int, float], ...]
    min_zoom_by_tag: tuple[tuple[str, str, int], ...] = ()

    def matches(
        self, source_type: str, geometry_type: str, tags: Mapping[str, str]
    ) -> bool:
        return (
            source_type in self.source_types
            and geometry_type in self.geometry_types
            and any(rule.matches(tags) for rule in self.rules)
        )

    def minimum_zoom(self, tags: Mapping[str, str]) -> int:
        values = [
            zoom for key, value, zoom in self.min_zoom_by_tag
            if tags.get(key) == value
        ]
        return min(values) if values else self.min_zoom

    def simplification_for_zoom(self, zoom: int) -> float:
        """Returns tolerance in Web Mercator metres for the selected zoom."""
        tolerance = 0.0
        for threshold, candidate in self.simplification:
            if zoom >= threshold:
                tolerance = candidate
        return tolerance

    def mvt_properties(self, tags: Mapping[str, str]) -> dict[str, str]:
        """Copies only explicitly approved, non-empty OSM properties."""
        return {
            key: str(tags[key])
            for key in self.properties
            if key in tags and str(tags[key]).strip()
        }


def _values(*items: str) -> frozenset[str]:
    return frozenset(items)


def _rule(
    key: str,
    values: frozenset[str] | None = None,
    *,
    excluded: tuple[tuple[str, frozenset[str]], ...] = (),
) -> OfflineMapTagRule:
    return OfflineMapTagRule(((key, values),), excluded)


class OfflineMapLayers:
    """Audited minimal layer set used by TravelManager offline packages."""

    COMMON_NAMES: ClassVar[frozenset[str]] = frozenset({
        'name', 'name:pl', 'name:en', 'ref',
    })
    LINE_SOURCES: ClassVar[frozenset[str]] = frozenset({'way', 'relation'})
    ALL_SOURCES: ClassVar[frozenset[str]] = frozenset({
        'node', 'way', 'relation'
    })

    DEFINITIONS: ClassVar[tuple[OfflineMapLayerDefinition, ...]] = (
        OfflineMapLayerDefinition(
            id='water',
            source_types=LINE_SOURCES,
            geometry_types=frozenset({'line', 'polygon'}),
            rules=(
                _rule('natural', _values('water', 'bay', 'strait')),
                _rule('waterway', _values('river', 'canal', 'stream', 'riverbank')),
                _rule('landuse', _values('reservoir', 'basin')),
            ),
            min_zoom=5,
            priority=10,
            properties=COMMON_NAMES | frozenset({'natural', 'water', 'waterway'}),
            simplification=((0, 1000), (6, 300), (9, 60), (12, 8), (14, 2)),
        ),
        OfflineMapLayerDefinition(
            id='landuse',
            source_types=LINE_SOURCES,
            geometry_types=frozenset({'polygon'}),
            rules=(
                _rule('landuse', _values(
                    'forest', 'residential', 'industrial', 'commercial',
                    'retail', 'farmland', 'meadow', 'grass', 'cemetery',
                    'recreation_ground',
                )),
                _rule('leisure', _values('park', 'garden', 'pitch', 'golf_course')),
                _rule('natural', _values('wood', 'scrub', 'heath', 'beach', 'sand')),
            ),
            min_zoom=7,
            priority=20,
            properties=COMMON_NAMES | frozenset({'landuse', 'leisure', 'natural'}),
            simplification=((0, 600), (7, 180), (10, 35), (13, 4)),
        ),
        OfflineMapLayerDefinition(
            id='buildings',
            source_types=LINE_SOURCES,
            geometry_types=frozenset({'polygon'}),
            rules=(_rule('building'),),
            min_zoom=13,
            priority=30,
            properties=COMMON_NAMES | frozenset({'building', 'building:levels'}),
            simplification=((0, 12), (13, 2), (15, 0)),
        ),
        OfflineMapLayerDefinition(
            id='roads',
            source_types=frozenset({'way'}),
            geometry_types=frozenset({'line'}),
            rules=(_rule(
                'highway',
                excluded=(('highway', _values('proposed', 'construction', 'abandoned')),),
            ),),
            min_zoom=13,
            priority=50,
            properties=COMMON_NAMES | frozenset({
                'highway', 'surface', 'oneway', 'bridge', 'tunnel', 'access',
            }),
            simplification=((0, 500), (6, 120), (10, 20), (13, 3), (15, 0)),
            min_zoom_by_tag=(
                ('highway', 'motorway', 5), ('highway', 'trunk', 6),
                ('highway', 'primary', 7), ('highway', 'secondary', 9),
                ('highway', 'tertiary', 11),
            ),
        ),
        OfflineMapLayerDefinition(
            id='railways',
            source_types=LINE_SOURCES,
            geometry_types=frozenset({'line'}),
            rules=(_rule(
                'railway',
                _values('rail', 'light_rail', 'subway', 'tram', 'narrow_gauge'),
                excluded=(('service', _values('yard', 'siding', 'spur')),),
            ),),
            min_zoom=8,
            priority=60,
            properties=COMMON_NAMES | frozenset({
                'railway', 'service', 'usage', 'electrified', 'tracks',
            }),
            simplification=((0, 350), (8, 80), (11, 15), (14, 2)),
        ),
        OfflineMapLayerDefinition(
            id='boundaries',
            source_types=frozenset({'relation', 'way'}),
            geometry_types=frozenset({'line', 'polygon'}),
            rules=(OfflineMapTagRule((
                ('boundary', _values('administrative')),
                ('admin_level', _values('2', '4', '6', '8')),
            )),),
            min_zoom=4,
            priority=70,
            properties=COMMON_NAMES | frozenset({'boundary', 'admin_level'}),
            simplification=((0, 1500), (5, 500), (8, 120), (11, 20), (14, 3)),
            min_zoom_by_tag=(
                ('admin_level', '2', 4), ('admin_level', '4', 6),
                ('admin_level', '6', 9), ('admin_level', '8', 11),
            ),
        ),
        OfflineMapLayerDefinition(
            id='places',
            source_types=ALL_SOURCES,
            geometry_types=frozenset({'point'}),
            rules=(_rule('place', _values(
                'country', 'state', 'region', 'city', 'town', 'village',
                'suburb', 'quarter', 'neighbourhood', 'hamlet',
            )),),
            min_zoom=12,
            priority=80,
            properties=COMMON_NAMES | frozenset({'place', 'population', 'capital'}),
            simplification=((0, 0),),
            min_zoom_by_tag=(
                ('place', 'country', 3), ('place', 'state', 5),
                ('place', 'region', 6), ('place', 'city', 7),
                ('place', 'town', 9), ('place', 'village', 11),
            ),
        ),
        OfflineMapLayerDefinition(
            id='pois',
            source_types=ALL_SOURCES,
            geometry_types=frozenset({'point'}),
            rules=(
                _rule('amenity', _values(
                    'hospital', 'clinic', 'pharmacy', 'police', 'fire_station',
                    'fuel', 'charging_station', 'parking', 'bus_station',
                    'school', 'university', 'restaurant', 'cafe', 'toilets',
                )),
                _rule('tourism', _values(
                    'hotel', 'motel', 'hostel', 'camp_site', 'museum',
                    'attraction', 'viewpoint', 'information',
                )),
                _rule('railway', _values('station', 'halt', 'tram_stop')),
                _rule('public_transport', _values('station', 'stop_position')),
            ),
            min_zoom=13,
            priority=90,
            properties=COMMON_NAMES | frozenset({
                'amenity', 'tourism', 'railway', 'public_transport', 'operator',
            }),
            simplification=((0, 0),),
        ),
    )
    BY_ID: ClassVar[dict[str, OfflineMapLayerDefinition]] = {
        definition.id: definition for definition in DEFINITIONS
    }

    @classmethod
    def matching(
        cls,
        source_type: str,
        geometry_type: str,
        tags: Mapping[str, str],
    ) -> tuple[OfflineMapLayerDefinition, ...]:
        return tuple(
            definition for definition in cls.DEFINITIONS
            if definition.matches(source_type, geometry_type, tags)
        )

    @classmethod
    def required_tags(cls) -> frozenset[str]:
        """Returns the tag keys the streaming PBF reader needs to retain."""
        keys: set[str] = set()
        for definition in cls.DEFINITIONS:
            keys.update(definition.properties)
            keys.update(key for rule in definition.rules for key, _ in rule.required)
            keys.update(key for rule in definition.rules for key, _ in rule.excluded)
            keys.update(key for key, _, _ in definition.min_zoom_by_tag)
        return frozenset(keys)

    def __new__(cls, *args, **kwargs):
        raise TypeError(f'{cls.__name__} is a static utility class.')

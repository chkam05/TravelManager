from __future__ import annotations

import unicodedata

from core.language_service import LanguageService
from models.offline_maps import OfflineMapRegion
from resources.countries import Countries
from services.offline_maps.catalog_names import display_name


_POLISH_ORDER = str.maketrans({
    'ą': 'az', 'ć': 'cz', 'ę': 'ez', 'ł': 'lz', 'ń': 'nz',
    'ó': 'oz', 'ś': 'sz', 'ź': 'zx', 'ż': 'zy',
})


def localized_catalog(regions: list[OfflineMapRegion]) -> list[dict[str, object]]:
    locale = LanguageService.current_locale()
    rows = {region.id: _localized_row(region) for region in regions}
    for row in rows.values():
        row['children'].sort(key=lambda item: _sort_key(rows[item]['name'], locale))
    return sorted(
        rows.values(),
        key=lambda row: (
            bool(row['parent_id']), _sort_key(str(row['name']), locale)
        ),
    )


def _localized_row(region: OfflineMapRegion) -> dict[str, object]:
    row = region.to_dict()
    row['source_name'] = region.name
    row['name'] = display_name(region.name)
    # Geofabrik country nodes carry ISO-3166-1, while their subdivisions also
    # carry ISO-3166-2. Only the former should receive a country translation.
    if len(region.country_codes) == 1 and not region.region_codes:
        key = Countries.NAME_KEYS.get(region.country_codes[0])
        if key:
            row['name'] = LanguageService.translate_current(key)
    return row


def _sort_key(value: str, locale: str) -> str:
    text = value.casefold()
    if locale == 'pl_PL':
        text = text.translate(_POLISH_ORDER)
    return unicodedata.normalize('NFKD', text)

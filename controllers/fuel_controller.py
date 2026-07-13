from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timezone
from html import unescape
import json
import re
import ssl
from typing import Any, ClassVar
from urllib.parse import urljoin
from urllib.error import URLError
from urllib.request import Request, urlopen
from zipfile import ZipFile
import xml.etree.ElementTree as ET

from flask import jsonify, request

from core.api.base_controller import BaseController
from models.settings.fuel_cost_cache import FuelCostCache
from resources.country_aliases import CountryAliases
from resources.countries import Countries
from resources.fuel.labels import FuelLabels
from resources.fuel.price_fields import FuelPriceFields
from resources.fuel.sources import FuelSources
from storage.settings_storage import SettingsStorage


@dataclass(frozen=True)
class FuelPrice:
    """Represents a single fuel price loaded from an external source."""

    fuel_type: str
    label: str
    price: float
    source: str
    updated: str | None


class FuelController(BaseController):
    """Controller for external fuel price lookups."""

    CONTROLLER_NAME: ClassVar[str] = 'FuelController'
    _USER_AGENT: ClassVar[str] = 'TravelManager/1.0'

    def register_routes(self):
        self.add_url_rule('/api/fuel-prices/latest', view_func=self.latest, methods=['GET'])
        self.add_url_rule('/api/fuel-costs', view_func=self.costs, methods=['GET'])
        self.add_url_rule('/api/fuel-costs/manual', view_func=self.save_manual_cost, methods=['POST', 'PATCH'])

    #region HTTP

    @classmethod
    def _load_text(cls, url: str, accept: str = 'text/html') -> str:
        """Loads a text document from an external service."""
        req = Request(url, headers={
            'Accept': accept,
            'User-Agent': cls._USER_AGENT
        })

        try:
            return cls._read_text(req)
        except URLError as error:
            if not isinstance(error.reason, ssl.SSLCertVerificationError):
                raise

            context = ssl._create_unverified_context()
            return cls._read_text(req, context)

    @classmethod
    def _load_bytes(cls, url: str, accept: str = '*/*') -> bytes:
        """Loads a binary document from an external service."""
        req = Request(url, headers={
            'Accept': accept,
            'User-Agent': cls._USER_AGENT
        })

        try:
            return cls._read_bytes(req)
        except URLError as error:
            if not isinstance(error.reason, ssl.SSLCertVerificationError):
                raise

            context = ssl._create_unverified_context()
            return cls._read_bytes(req, context)

    @staticmethod
    def _read_text(req: Request, context: ssl.SSLContext | None = None) -> str:
        """Executes a request and decodes the response body."""
        with urlopen(req, timeout=20, context=context) as response:
            charset = response.headers.get_content_charset() or 'utf-8'
            return response.read().decode(charset, errors='replace')

    @staticmethod
    def _read_bytes(req: Request, context: ssl.SSLContext | None = None) -> bytes:
        """Executes a request and returns response bytes."""
        with urlopen(req, timeout=30, context=context) as response:
            return response.read()

    #endregion HTTP

    #region Parsing

    @classmethod
    def _normalize_fuel_type(cls, fuel_type: str) -> str | None:
        """Maps application fuel types to AutoCentrum labels."""
        return FuelLabels.VALUES.get(fuel_type.strip().lower())

    @classmethod
    def _parse_price(cls, html: str, label: str, requested_fuel_type: str) -> FuelPrice | None:
        """Parses a national average fuel price from AutoCentrum HTML."""
        text = unescape(re.sub(r'<[^>]+>', ' ', html))
        text = re.sub(r'\s+', ' ', text).strip()
        label_patterns = {
            '95': r'(?:Pb\s*)?95',
            '98': r'(?:Pb\s*)?98',
            'ON': r'(?:ON|Diesel|Olej\s+napędowy)',
            'LPG': r'(?:LPG|Gaz)'
        }
        label_pattern = label_patterns.get(label, re.escape(label))
        price_pattern = re.compile(
            rf'(?:^|\s){label_pattern}\s+([0-9]+[,.][0-9]{{2}})\s*(?:zł|PLN)?(?:\s|$)',
            re.IGNORECASE
        )
        price_match = price_pattern.search(text)

        if not price_match:
            return None

        updated_match = re.search(
            r'Ostatnia aktualizacja\s*([^\.]+?)(?:\s{2,}|$)',
            text,
            re.IGNORECASE
        )
        price = float(price_match.group(1).replace(',', '.'))

        return FuelPrice(
            fuel_type=requested_fuel_type,
            label=label,
            price=price,
            source=FuelSources.AUTOCENTRUM_URL,
            updated=updated_match.group(1).strip() if updated_match else None
        )

    @classmethod
    def _load_cache(cls) -> dict[str, Any] | None:
        """Loads cached fuel cost data from application settings."""
        settings = SettingsStorage().load()
        cache = settings.fuel_cost_cache.data if settings.fuel_cost_cache else {}

        return cache if isinstance(cache, dict) and cache else None

    @classmethod
    def _save_cache(cls, data: dict[str, Any]) -> None:
        """Persists fuel cost data cache through application settings storage."""
        storage = SettingsStorage()
        settings = storage.load()
        settings.fuel_cost_cache = FuelCostCache.from_dict({'data': data if isinstance(data, dict) else {}})
        storage.save(settings)

    @classmethod
    def _now_iso(cls) -> str:
        """Returns current UTC timestamp."""
        return datetime.now(timezone.utc).isoformat()

    @classmethod
    def _find_latest_taxed_prices_url(cls, html: str) -> str:
        """Finds the latest taxed prices XLSX URL on the Weekly Oil Bulletin page."""
        start = html.lower().find('prices with taxes latest prices')
        search_area = html[start:start + 5000] if start >= 0 else html
        candidates = re.findall(r'href=["\']([^"\']+\.xlsx(?:\?[^"\']*)?)["\']', search_area, re.IGNORECASE)

        if not candidates:
            candidates = re.findall(r'href=["\']([^"\']+)["\']', search_area, re.IGNORECASE)
            candidates = [
                candidate
                for candidate in candidates
                if 'download' in candidate.lower() or 'xlsx' in candidate.lower()
            ]

        if not candidates:
            raise ValueError('Could not find latest taxed prices XLSX link.')

        return urljoin(FuelSources.OIL_BULLETIN_URL, unescape(candidates[0]))

    @staticmethod
    def _xlsx_column_index(cell_ref: str) -> int:
        """Returns zero-based column index from an XLSX cell reference."""
        letters = ''.join(char for char in cell_ref if char.isalpha()).upper()
        index = 0

        for char in letters:
            index = index * 26 + ord(char) - ord('A') + 1

        return max(0, index - 1)

    @classmethod
    def _xlsx_shared_strings(cls, archive: ZipFile) -> list[str]:
        """Loads XLSX shared strings."""
        try:
            xml = archive.read('xl/sharedStrings.xml')
        except KeyError:
            return []

        root = ET.fromstring(xml)
        result: list[str] = []

        for item in root.iter('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}si'):
            texts = [
                node.text or ''
                for node in item.iter('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}t')
            ]
            result.append(''.join(texts))

        return result

    @classmethod
    def _xlsx_rows(cls, content: bytes) -> list[list[Any]]:
        """Reads rows from the first XLSX worksheet using only stdlib XML parsing."""
        from io import BytesIO

        with ZipFile(BytesIO(content)) as archive:
            shared_strings = cls._xlsx_shared_strings(archive)
            sheet_name = 'xl/worksheets/sheet1.xml'

            if sheet_name not in archive.namelist():
                sheet_name = next(
                    name for name in archive.namelist()
                    if name.startswith('xl/worksheets/sheet') and name.endswith('.xml')
                )

            root = ET.fromstring(archive.read(sheet_name))
            ns = '{http://schemas.openxmlformats.org/spreadsheetml/2006/main}'
            rows: list[list[Any]] = []

            for row in root.iter(f'{ns}row'):
                values: list[Any] = []

                for cell in row.iter(f'{ns}c'):
                    index = cls._xlsx_column_index(cell.attrib.get('r', 'A1'))

                    while len(values) <= index:
                        values.append(None)

                    cell_type = cell.attrib.get('t')
                    value_node = cell.find(f'{ns}v')
                    inline_node = cell.find(f'{ns}is/{ns}t')

                    if cell_type == 's' and value_node is not None:
                        value = shared_strings[int(value_node.text or '0')]
                    elif cell_type == 'inlineStr' and inline_node is not None:
                        value = inline_node.text or ''
                    elif value_node is not None:
                        text = value_node.text or ''
                        try:
                            value = float(text)
                        except ValueError:
                            value = text
                    else:
                        value = ''

                    values[index] = value

                rows.append(values)

            return rows

    @staticmethod
    def _cell_text(value: Any) -> str:
        """Converts a spreadsheet cell value to normalized text."""
        return re.sub(r'\s+', ' ', str(value or '')).strip()

    @classmethod
    def _price_from_cell(cls, value: Any) -> float | None:
        """Converts a spreadsheet fuel price to EUR per litre."""
        if value in (None, ''):
            return None

        if isinstance(value, (int, float)):
            number = float(value)
        else:
            match = re.search(r'[0-9]+(?:[,.][0-9]+)?', str(value))

            if not match:
                return None

            number = float(match.group(0).replace(',', '.'))

        if number <= 0:
            return None

        # The Oil Bulletin latest-price tables commonly use EUR / 1000 litres.
        return round(number / 1000, 4) if number > 20 else round(number, 4)

    @classmethod
    def _country_code_from_row(cls, row: list[Any]) -> str | None:
        """Extracts an EU country code from a spreadsheet row."""
        for value in row[:3]:
            text = cls._cell_text(value)
            upper = text.upper()

            if upper in Countries.VALUES:
                return upper

            alias = CountryAliases.VALUES.get(text.lower())

            if alias:
                return alias

        return None

    @classmethod
    def _find_price_columns(cls, rows: list[list[Any]]) -> dict[str, int]:
        """Finds fuel price columns in the Oil Bulletin worksheet."""
        columns: dict[str, int] = {}

        for row in rows[:25]:
            lowered = [cls._cell_text(value).lower() for value in row]
            joined = ' '.join(lowered)

            if not any(term in joined for term in ('euro-super', 'diesel', 'gas oil', 'lpg')):
                continue

            for index, text in enumerate(lowered):
                normalized = text.replace('-', ' ')

                if '95' in normalized and any(term in normalized for term in ('euro super', 'eurosuper', 'gasoline', 'petrol')):
                    columns.setdefault('petrol_95', index)
                elif any(term in normalized for term in ('automotive gas oil', 'diesel', 'gasoil', 'gas oil automobile')):
                    columns.setdefault('diesel', index)
                elif any(term in normalized for term in ('lpg', 'liquefied petroleum')):
                    columns.setdefault('lpg', index)
                elif '98' in normalized and any(term in normalized for term in ('super plus', 'petrol', 'gasoline')):
                    columns.setdefault('petrol_98', index)

        return columns

    @classmethod
    def _parse_oil_bulletin_rows(cls, rows: list[list[Any]]) -> list[dict[str, Any]]:
        """Converts Oil Bulletin worksheet rows to application table rows."""
        columns = cls._find_price_columns(rows)

        if not columns:
            # Fallback for the compact latest-price sheet layout.
            columns = {
                'petrol_95': 1,
                'diesel': 2,
                'lpg': 6
            }

        result: list[dict[str, Any]] = []

        for row in rows:
            country_code = cls._country_code_from_row(row)

            if not country_code:
                continue

            country = Countries.VALUES[country_code]
            item: dict[str, Any] = {
                'country_code': country_code,
                'country': country['country'],
                'currency': country['currency'],
                'source_currency': 'EUR',
                'petrol_95': None,
                'petrol_98': None,
                'diesel': None,
                'lpg': None
            }

            for field, column in columns.items():
                item[field] = cls._price_from_cell(row[column] if column < len(row) else None)

            result.append(item)

        return sorted(result, key=lambda value: value['country'])

    @classmethod
    def _load_autocentrum_poland_prices(cls) -> dict[str, float | None]:
        """Loads Polish national average fuel prices from AutoCentrum."""
        html = cls._load_text(FuelSources.AUTOCENTRUM_URL)

        return {
            'petrol_95': (cls._parse_price(html, '95', '95') or FuelPrice('95', '95', 0, '', None)).price or None,
            'petrol_98': (cls._parse_price(html, '98', '98') or FuelPrice('98', '98', 0, '', None)).price or None,
            'diesel': (cls._parse_price(html, 'ON', 'diesel') or FuelPrice('diesel', 'ON', 0, '', None)).price or None,
            'lpg': (cls._parse_price(html, 'LPG', 'gaz') or FuelPrice('gaz', 'LPG', 0, '', None)).price or None
        }

    @classmethod
    def _apply_poland_autocentrum_prices(cls, rows: list[dict[str, Any]], metadata: dict[str, Any]) -> None:
        """Overrides Poland row with AutoCentrum prices when available."""
        try:
            prices = cls._load_autocentrum_poland_prices()
        except Exception as error:
            metadata['poland_warning'] = f'Nie udało się pobrać cen AutoCentrum: {error}'
            return

        poland = next((row for row in rows if row.get('country_code') == 'PL'), None)

        if not poland:
            return

        for field, price in prices.items():
            if price:
                poland[field] = price

        poland['currency'] = 'PLN'
        poland['source_currency'] = 'PLN'
        poland['source'] = FuelSources.AUTOCENTRUM_URL
        metadata['poland_source'] = FuelSources.AUTOCENTRUM_URL

    @classmethod
    def _extract_updated_date(cls, html: str) -> str | None:
        """Extracts the publication date near the latest taxed price entry."""
        def normalize(value: str) -> str:
            months = {
                'january': '01',
                'february': '02',
                'march': '03',
                'april': '04',
                'may': '05',
                'june': '06',
                'july': '07',
                'august': '08',
                'september': '09',
                'october': '10',
                'november': '11',
                'december': '12'
            }
            match = re.match(r'(\d{1,2})\s+([A-Za-z]+)\s+(\d{4})', value.strip())

            if not match:
                return value

            month = months.get(match.group(2).lower())

            if not month:
                return value

            return f'{match.group(3)}-{month}-{match.group(1).zfill(2)}'

        match = re.search(
            r'(\d{1,2}\s+[A-ZĄĆĘŁŃÓŚŹŻ]+\s+\d{4})\s*</[^>]+>\s*[^<]*Prices with taxes latest prices',
            html,
            re.IGNORECASE
        )

        if match:
            return normalize(match.group(1).title())

        text = unescape(re.sub(r'<[^>]+>', ' ', html))
        match = re.search(r'(\d{1,2}\s+[A-Za-z]+\s+\d{4})\s+Prices with taxes latest prices', text)
        return normalize(match.group(1)) if match else None

    @classmethod
    def _load_exchange_rates(cls) -> dict[str, float]:
        """Loads EUR exchange rates for country conversion."""
        rates = {'EUR': 1.0}

        try:
            data = json.loads(cls._load_text(FuelSources.FRANKFURTER_URL, accept='application/json'))
        except Exception:
            return rates

        if isinstance(data, list):
            for item in data:
                if not isinstance(item, dict):
                    continue

                currency = item.get('quote')
                value = item.get('rate')

                if not currency:
                    continue

                try:
                    rates[str(currency)] = float(value)
                except (TypeError, ValueError):
                    continue
        elif isinstance(data, dict) and isinstance(data.get('rates'), dict):
            for currency, value in data['rates'].items():
                try:
                    rates[str(currency)] = float(value)
                except (TypeError, ValueError):
                    continue

        # Bulgarian lev is pegged to EUR and may be omitted by blended providers.
        rates.setdefault('BGN', 1.95583)

        return rates

    @classmethod
    def _required_currencies(cls, cache: dict[str, Any] | None = None) -> set[str]:
        """Returns currencies needed by the fuel cost view."""
        required = {'EUR', 'PLN'}

        if isinstance(cache, dict):
            rows = cache.get('rows') if isinstance(cache.get('rows'), list) else []

            for row in rows:
                if not isinstance(row, dict):
                    continue

                for field in ('currency', 'source_currency'):
                    currency = str(row.get(field) or '').strip().upper()

                    if currency:
                        required.add(currency)

        return required

    @classmethod
    def _has_required_rates(cls, rates: Any, required: set[str] | None = None) -> bool:
        """Checks if cached exchange rates contain all required currencies."""
        if not isinstance(rates, dict):
            return False

        required = required or cls._required_currencies()

        return all(
            currency in rates and isinstance(rates[currency], (int, float)) and float(rates[currency]) > 0
            for currency in required
        )

    @classmethod
    def _refresh_cache_rates(cls, cache: dict[str, Any], force: bool = False) -> dict[str, Any]:
        """Refreshes missing exchange rates in an existing cache object."""
        required = cls._required_currencies(cache)

        if not force and cls._has_required_rates(cache.get('rates'), required):
            return cache

        rates = cls._load_exchange_rates()

        if cls._has_required_rates(rates, {'EUR', 'PLN'}):
            cache['rates'] = rates
            metadata = dict(cache.get('metadata') or {})
            metadata['currency_source'] = FuelSources.FRANKFURTER_URL
            metadata['currency_loaded_at'] = cls._now_iso()
            missing = sorted(currency for currency in required if currency not in rates)

            if missing:
                metadata['currency_warning'] = f'Brak kursów walut: {", ".join(missing)}'
            else:
                metadata.pop('currency_warning', None)

            cache['metadata'] = metadata
            cls._save_cache(cache)

        return cache

    @classmethod
    def _normalize_cache(cls, cache: dict[str, Any]) -> dict[str, Any]:
        """Normalizes older fuel cost cache schema to the current shape."""
        rows = cache.get('rows') if isinstance(cache.get('rows'), list) else []
        metadata = dict(cache.get('metadata') or {})
        changed = False

        if not cache.get('countries') or len(cache.get('countries') or []) < len(Countries.VALUES):
            cache['countries'] = cls._countries_payload()
            changed = True

        for row in rows:
            if not isinstance(row, dict):
                continue

            for field in ('lng', 'electricity'):
                if field in row:
                    row.pop(field, None)
                    changed = True

            if not row.get('source_currency'):
                row['source_currency'] = 'EUR'
                changed = True

        poland = next((row for row in rows if isinstance(row, dict) and row.get('country_code') == 'PL'), None)

        if poland and not poland.get('manual') and (not metadata.get('poland_source') or not poland.get('petrol_98')):
            cls._apply_poland_autocentrum_prices(rows, metadata)
            changed = True

        if changed:
            cache['rows'] = rows
            cache['metadata'] = metadata
            cls._save_cache(cache)

        return cache

    @classmethod
    def _manual_rows(cls, cache: dict[str, Any] | None) -> dict[str, dict[str, Any]]:
        """Returns manual rows indexed by country code."""
        if not isinstance(cache, dict):
            return {}

        rows = cache.get('rows') if isinstance(cache.get('rows'), list) else []

        return {
            str(row.get('country_code', '')).upper(): dict(row)
            for row in rows
            if isinstance(row, dict) and row.get('manual') and row.get('country_code')
        }

    @classmethod
    def _merge_manual_rows(
        cls,
        rows: list[dict[str, Any]],
        manual_rows: dict[str, dict[str, Any]],
        overwrite_codes: set[str]
    ) -> list[dict[str, Any]]:
        """Keeps manual values unless a country was explicitly selected for overwrite."""
        if not manual_rows:
            return rows

        indexed = {
            str(row.get('country_code', '')).upper(): dict(row)
            for row in rows
            if isinstance(row, dict) and row.get('country_code')
        }

        for code, manual_row in manual_rows.items():
            if code in overwrite_codes and code in indexed:
                indexed[code].pop('manual', None)
                indexed[code].pop('manual_updated_at', None)
                indexed[code].pop('manual_fields', None)
                continue

            item = indexed.get(code, {})
            item.update(manual_row)
            indexed[code] = item

        return sorted(indexed.values(), key=lambda value: str(value.get('country', '')))

    @classmethod
    def _countries_payload(cls) -> list[dict[str, str]]:
        """Returns countries available for fuel costs and manual entries."""
        return [
            {
                'country_code': code,
                'country': data['country'],
                'currency': data['currency']
            }
            for code, data in sorted(Countries.VALUES.items(), key=lambda item: item[1]['country'])
        ]

    @classmethod
    def _to_optional_price(cls, value: Any) -> float | None:
        """Converts a manual price to a nullable non-negative float."""
        if value in (None, ''):
            return None

        try:
            price = float(str(value).replace(',', '.'))
        except (TypeError, ValueError):
            return None

        return round(price, 4) if price > 0 else None

    @classmethod
    def _manual_row_from_payload(cls, payload: dict[str, Any], existing: dict[str, Any] | None = None) -> dict[str, Any]:
        """Builds a manual fuel cost row from request payload."""
        existing = existing or {}
        country_code = str(payload.get('country_code') or existing.get('country_code') or '').strip().upper()
        country = str(payload.get('country') or (existing or {}).get('country') or '').strip()
        currency = str(payload.get('currency') or (existing or {}).get('currency') or '').strip().upper()

        if not country_code or not country or not currency:
            raise ValueError('Country code, country and currency are required.')

        row = dict(existing)
        row.update({
            'country_code': country_code,
            'country': country,
            'currency': currency,
            'source_currency': currency,
            'manual': True,
            'manual_updated_at': cls._now_iso(),
            'manual_fields': list(FuelPriceFields.VALUES),
            'source': 'manual'
        })

        for field in FuelPriceFields.VALUES:
            row[field] = cls._to_optional_price(payload.get(field))

        return row

    @classmethod
    def _build_fuel_cost_cache(cls) -> dict[str, Any]:
        """Downloads source data and builds fresh fuel cost cache."""
        html = cls._load_text(FuelSources.OIL_BULLETIN_URL)
        xlsx_url = cls._find_latest_taxed_prices_url(html)
        xlsx = cls._load_bytes(
            xlsx_url,
            accept='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        rows = cls._parse_oil_bulletin_rows(cls._xlsx_rows(xlsx))

        if not rows:
            raise ValueError('Fuel price rows were not found in the source document.')

        metadata = {
            'source': FuelSources.OIL_BULLETIN_URL,
            'download_url': xlsx_url,
            'currency_source': FuelSources.FRANKFURTER_URL,
            'updated': cls._extract_updated_date(html),
            'loaded_at': cls._now_iso()
        }
        cls._apply_poland_autocentrum_prices(rows, metadata)

        return {
            'metadata': metadata,
            'rows': rows,
            'countries': cls._countries_payload(),
            'rates': cls._load_exchange_rates()
        }

    #endregion Parsing

    #region Endpoints

    def latest(self):
        """Returns the latest known average fuel price for the selected fuel type."""
        fuel_type = request.args.get('fuel_type', '95')
        label = self._normalize_fuel_type(fuel_type)

        if not label:
            return jsonify({
                'status': 'error',
                'message': 'Unsupported fuel type.'
            }), 400

        try:
            html = self._load_text(FuelSources.AUTOCENTRUM_URL)
            price = self._parse_price(html, label, fuel_type)
        except Exception as error:
            return jsonify({
                'status': 'error',
                'message': f'Could not load fuel prices: {error}'
            }), 502

        if not price:
            return jsonify({
                'status': 'error',
                'message': 'Fuel price was not found in the source document.'
            }), 502

        return jsonify({
            'status': 'ok',
            'fuel': {
                'fuel_type': price.fuel_type,
                'label': price.label,
                'price': price.price,
                'source': price.source,
                'updated': price.updated
            }
        })

    def costs(self):
        """Returns cached or freshly downloaded fuel cost table data."""
        force = request.args.get('force', '').strip().lower() in ('1', 'true', 'yes', 'on')
        overwrite_codes = {
            code.strip().upper()
            for code in request.args.get('overwrite_manual', '').split(',')
            if code.strip()
        }
        cache = None if force else self._load_cache()

        if not cache:
            try:
                loaded_cache = self._load_cache() if force else None
                previous_cache = self._normalize_cache(loaded_cache) if loaded_cache else None
                manual_rows = self._manual_rows(previous_cache)
                cache = self._build_fuel_cost_cache()
                cache['rows'] = self._merge_manual_rows(cache.get('rows') or [], manual_rows, overwrite_codes)
                self._save_cache(cache)
            except Exception as error:
                cache = self._load_cache()

                if cache:
                    cache = self._normalize_cache(cache)
                    cache = self._refresh_cache_rates(cache, force=True)
                    metadata = dict(cache.get('metadata') or {})
                    metadata['warning'] = f'Nie udało się odświeżyć danych, pokazuję cache: {error}'
                    cache['metadata'] = metadata
                else:
                    return jsonify({
                        'status': 'error',
                        'message': f'Could not load fuel cost data: {error}'
                    }), 502
        else:
            cache = self._normalize_cache(cache)
            cache = self._refresh_cache_rates(cache)

        return jsonify({
            'status': 'ok',
            'metadata': cache.get('metadata') or {},
            'rows': cache.get('rows') or [],
            'countries': cache.get('countries') or self._countries_payload(),
            'rates': cache.get('rates') or {'EUR': 1.0}
        })

    def save_manual_cost(self):
        """Creates or updates a manual fuel cost row."""
        payload = request.get_json(silent=True) or {}
        loaded_cache = self._load_cache()
        cache = self._normalize_cache(loaded_cache) if loaded_cache else {
            'metadata': {'source': 'manual', 'loaded_at': self._now_iso()},
            'rows': [],
            'countries': self._countries_payload(),
            'rates': self._load_exchange_rates()
        }
        rows = cache.get('rows') if isinstance(cache.get('rows'), list) else []
        country_code = str(payload.get('country_code') or '').strip().upper()
        existing = next((
            row
            for row in rows
            if isinstance(row, dict) and str(row.get('country_code', '')).upper() == country_code
        ), None)

        try:
            row = self._manual_row_from_payload(payload, existing)
        except ValueError as error:
            return jsonify({
                'status': 'error',
                'message': str(error)
            }), 400

        rows = [
            item
            for item in rows
            if not (isinstance(item, dict) and str(item.get('country_code', '')).upper() == row['country_code'])
        ]
        rows.append(row)
        cache['rows'] = sorted(rows, key=lambda value: str(value.get('country', '')))
        cache['countries'] = self._countries_payload()
        cache = self._refresh_cache_rates(cache)
        self._save_cache(cache)

        return jsonify({
            'status': 'ok',
            'row': row,
            'metadata': cache.get('metadata') or {},
            'rows': cache.get('rows') or [],
            'countries': cache.get('countries') or self._countries_payload(),
            'rates': cache.get('rates') or {'EUR': 1.0}
        })

    #endregion Endpoints

from __future__ import annotations
from html import unescape
from io import BytesIO
import re
import ssl
from typing import Any, ClassVar
from urllib.error import URLError
from urllib.parse import urljoin
from urllib.request import Request, urlopen
from zipfile import ZipFile
import xml.etree.ElementTree as ET

from models.fuel_data_model import FuelDataModel
from resources.country_aliases import CountryAliases
from resources.countries import Countries
from resources.fuel.labels import FuelLabels
from resources.fuel.sources import FuelSources


class FuelPriceDownloader:
    """Downloads and parses fuel prices from external sources."""

    _USER_AGENT: ClassVar[str] = 'TravelManager/1.0'

    def __init__(self):
        self.download_url: str | None = None
        self.updated: str | None = None
        self.poland_warning: str | None = None

    def download(self) -> list[FuelDataModel]:
        """Downloads the European fuel price table and applies Polish prices."""
        html = self._load_text(FuelSources.OIL_BULLETIN_URL)
        self.download_url = self._find_latest_taxed_prices_url(html)
        self.updated = self._extract_updated_date(html)
        xlsx = self._load_bytes(
            self.download_url,
            accept='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        models = self._parse_oil_bulletin_rows(self._xlsx_rows(xlsx))

        if not models:
            raise ValueError('Fuel price rows were not found in the source document.')

        self._apply_poland_autocentrum_prices(models)
        return models

    def download_latest(self, fuel_type: str) -> FuelDataModel | None:
        """Downloads the latest Polish price for the selected fuel type."""
        label = FuelLabels.VALUES.get(fuel_type.strip().lower())

        if not label:
            return None

        html = self._load_text(FuelSources.AUTOCENTRUM_URL)
        price, updated = self._parse_price(html, label)

        if price is None:
            return None

        country = Countries.VALUES['PL']
        values = {
            'petrol_95': None,
            'petrol_98': None,
            'diesel': None,
            'lpg': None
        }
        field = {
            '95': 'petrol_95',
            '98': 'petrol_98',
            'ON': 'diesel',
            'LPG': 'lpg'
        }[label]
        values[field] = price

        return FuelDataModel(
            country_code='PL',
            country=country['country'],
            currency='PLN',
            source_currency='PLN',
            source=FuelSources.AUTOCENTRUM_URL,
            updated=updated,
            loaded_at=None,
            manual=False,
            manual_updated_at=None,
            manual_fields=[],
            **values
        )

    @classmethod
    def _load_text(cls, url: str, accept: str = 'text/html') -> str:
        """Loads a text document from an external service."""
        request = Request(url, headers={'Accept': accept, 'User-Agent': cls._USER_AGENT})

        try:
            return cls._read_text(request)
        except URLError as error:
            if not isinstance(error.reason, ssl.SSLCertVerificationError):
                raise

            return cls._read_text(request, ssl._create_unverified_context())

    @classmethod
    def _load_bytes(cls, url: str, accept: str = '*/*') -> bytes:
        """Loads a binary document from an external service."""
        request = Request(url, headers={'Accept': accept, 'User-Agent': cls._USER_AGENT})

        try:
            return cls._read_bytes(request)
        except URLError as error:
            if not isinstance(error.reason, ssl.SSLCertVerificationError):
                raise

            return cls._read_bytes(request, ssl._create_unverified_context())

    @staticmethod
    def _read_text(request: Request, context: ssl.SSLContext | None = None) -> str:
        """Executes a request and decodes its response body."""
        with urlopen(request, timeout=20, context=context) as response:
            charset = response.headers.get_content_charset() or 'utf-8'
            return response.read().decode(charset, errors='replace')

    @staticmethod
    def _read_bytes(request: Request, context: ssl.SSLContext | None = None) -> bytes:
        """Executes a request and returns response bytes."""
        with urlopen(request, timeout=30, context=context) as response:
            return response.read()

    @staticmethod
    def _parse_price(html: str, label: str) -> tuple[float | None, str | None]:
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
        match = re.search(
            rf'(?:^|\s){label_pattern}\s+([0-9]+[,.][0-9]{{2}})\s*(?:zł|PLN)?(?:\s|$)',
            text,
            re.IGNORECASE
        )

        if not match:
            return None, None

        updated_match = re.search(
            r'Ostatnia aktualizacja\s*([^\.]+?)(?:\s{2,}|$)',
            text,
            re.IGNORECASE
        )

        return (
            float(match.group(1).replace(',', '.')),
            updated_match.group(1).strip() if updated_match else None
        )

    @staticmethod
    def _find_latest_taxed_prices_url(html: str) -> str:
        """Finds the latest taxed-prices XLSX URL."""
        start = html.lower().find('prices with taxes latest prices')
        search_area = html[start:start + 5000] if start >= 0 else html
        candidates = re.findall(r'href=["\']([^"\']+\.xlsx(?:\?[^"\']*)?)["\']', search_area, re.IGNORECASE)

        if not candidates:
            links = re.findall(r'href=["\']([^"\']+)["\']', search_area, re.IGNORECASE)
            candidates = [link for link in links if 'download' in link.lower() or 'xlsx' in link.lower()]

        if not candidates:
            raise ValueError('Could not find latest taxed prices XLSX link.')

        return urljoin(FuelSources.OIL_BULLETIN_URL, unescape(candidates[0]))

    @staticmethod
    def _xlsx_column_index(cell_ref: str) -> int:
        """Returns a zero-based XLSX column index."""
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
        namespace = '{http://schemas.openxmlformats.org/spreadsheetml/2006/main}'

        return [
            ''.join(node.text or '' for node in item.iter(f'{namespace}t'))
            for item in root.iter(f'{namespace}si')
        ]

    @classmethod
    def _xlsx_rows(cls, content: bytes) -> list[list[Any]]:
        """Reads rows from the first XLSX worksheet."""
        with ZipFile(BytesIO(content)) as archive:
            shared_strings = cls._xlsx_shared_strings(archive)
            sheet_name = 'xl/worksheets/sheet1.xml'

            if sheet_name not in archive.namelist():
                sheet_name = next(
                    name for name in archive.namelist()
                    if name.startswith('xl/worksheets/sheet') and name.endswith('.xml')
                )

            root = ET.fromstring(archive.read(sheet_name))
            namespace = '{http://schemas.openxmlformats.org/spreadsheetml/2006/main}'
            rows: list[list[Any]] = []

            for row in root.iter(f'{namespace}row'):
                values: list[Any] = []

                for cell in row.iter(f'{namespace}c'):
                    index = cls._xlsx_column_index(cell.attrib.get('r', 'A1'))

                    while len(values) <= index:
                        values.append(None)

                    cell_type = cell.attrib.get('t')
                    value_node = cell.find(f'{namespace}v')
                    inline_node = cell.find(f'{namespace}is/{namespace}t')

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
        """Converts a spreadsheet cell to normalized text."""
        return re.sub(r'\s+', ' ', str(value or '')).strip()

    @classmethod
    def _price_from_cell(cls, value: Any) -> float | None:
        """Converts a spreadsheet price to EUR per litre."""
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

        return round(number / 1000, 4) if number > 20 else round(number, 4)

    @classmethod
    def _country_code_from_row(cls, row: list[Any]) -> str | None:
        """Extracts a country code from an Oil Bulletin row."""
        for value in row[:3]:
            text = cls._cell_text(value)
            upper = text.upper()

            if upper in Countries.VALUES:
                return upper

            if text.lower() in CountryAliases.VALUES:
                return CountryAliases.VALUES[text.lower()]

        return None

    @classmethod
    def _find_price_columns(cls, rows: list[list[Any]]) -> dict[str, int]:
        """Finds fuel price columns in Oil Bulletin rows."""
        columns: dict[str, int] = {}

        for row in rows[:25]:
            lowered = [cls._cell_text(value).lower() for value in row]

            if not any(term in ' '.join(lowered) for term in ('euro-super', 'diesel', 'gas oil', 'lpg')):
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
    def _parse_oil_bulletin_rows(cls, rows: list[list[Any]]) -> list[FuelDataModel]:
        """Converts Oil Bulletin rows to fuel data models."""
        columns = cls._find_price_columns(rows) or {'petrol_95': 1, 'diesel': 2, 'lpg': 6}
        result: list[FuelDataModel] = []

        for row in rows:
            country_code = cls._country_code_from_row(row)
            if not country_code:
                continue

            country = Countries.VALUES[country_code]
            values = {
                field: cls._price_from_cell(row[column] if column < len(row) else None)
                for field, column in columns.items()
            }
            result.append(FuelDataModel(
                country_code=country_code,
                country=country['country'],
                currency=country['currency'],
                source_currency='EUR',
                petrol_95=values.get('petrol_95'),
                petrol_98=values.get('petrol_98'),
                diesel=values.get('diesel'),
                lpg=values.get('lpg'),
                source=FuelSources.OIL_BULLETIN_URL,
                updated=None,
                loaded_at=None,
                manual=False,
                manual_updated_at=None,
                manual_fields=[]
            ))

        return sorted(result, key=lambda item: item.country)

    def _apply_poland_autocentrum_prices(self, models: list[FuelDataModel]) -> None:
        """Overrides the Poland model with AutoCentrum prices."""
        poland = next((model for model in models if model.country_code == 'PL'), None)
        if not poland:
            return

        try:
            html = self._load_text(FuelSources.AUTOCENTRUM_URL)
            prices = {
                'petrol_95': self._parse_price(html, '95')[0],
                'petrol_98': self._parse_price(html, '98')[0],
                'diesel': self._parse_price(html, 'ON')[0],
                'lpg': self._parse_price(html, 'LPG')[0]
            }
        except Exception as error:
            self.poland_warning = f'Nie udało się pobrać cen AutoCentrum: {error}'
            return

        for field, price in prices.items():
            if price:
                setattr(poland, field, price)

        poland.currency = 'PLN'
        poland.source_currency = 'PLN'
        poland.source = FuelSources.AUTOCENTRUM_URL

    @staticmethod
    def _extract_updated_date(html: str) -> str | None:
        """Extracts the publication date of the latest Oil Bulletin."""
        months = {
            'january': '01', 'february': '02', 'march': '03', 'april': '04',
            'may': '05', 'june': '06', 'july': '07', 'august': '08',
            'september': '09', 'october': '10', 'november': '11', 'december': '12'
        }

        def normalize(value: str) -> str:
            match = re.match(r'(\d{1,2})\s+([A-Za-z]+)\s+(\d{4})', value.strip())
            if not match or match.group(2).lower() not in months:
                return value
            return f'{match.group(3)}-{months[match.group(2).lower()]}-{match.group(1).zfill(2)}'

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

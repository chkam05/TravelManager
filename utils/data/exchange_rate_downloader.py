from __future__ import annotations
import json
import ssl
from typing import ClassVar
from urllib.error import URLError
from urllib.request import Request, urlopen

from models.exchange_rate_data_model import ExchangeRateDataModel
from resources.fuel.sources import FuelSources


class ExchangeRateDownloader:
    """Downloads EUR exchange rates from the configured external source."""

    _USER_AGENT: ClassVar[str] = 'TravelManager/1.0'

    @classmethod
    def download(cls) -> list[ExchangeRateDataModel]:
        """Downloads and normalizes exchange rates quoted against EUR."""
        rates: dict[str, float] = {'EUR': 1.0}

        try:
            data = json.loads(cls._load_text(FuelSources.FRANKFURTER_URL))
        except Exception:
            return [ExchangeRateDataModel(
                base_currency='EUR',
                currency='EUR',
                rate=1.0,
                source=FuelSources.FRANKFURTER_URL,
                updated=None
            )]

        if isinstance(data, list):
            for item in data:
                if not isinstance(item, dict):
                    continue

                cls._add_rate(rates, item.get('quote'), item.get('rate'))
        elif isinstance(data, dict) and isinstance(data.get('rates'), dict):
            for currency, value in data['rates'].items():
                cls._add_rate(rates, currency, value)

        # Bulgarian lev is pegged to EUR and may be omitted by blended providers.
        rates.setdefault('BGN', 1.95583)

        return [
            ExchangeRateDataModel(
                base_currency='EUR',
                currency=currency,
                rate=rate,
                source=FuelSources.FRANKFURTER_URL,
                updated=None
            )
            for currency, rate in sorted(rates.items())
        ]

    @staticmethod
    def _add_rate(rates: dict[str, float], currency, value) -> None:
        """Adds a valid positive exchange rate to a rate dictionary."""
        if not currency:
            return

        try:
            rate = float(value)
        except (TypeError, ValueError):
            return

        if rate > 0:
            rates[str(currency).upper()] = rate

    @classmethod
    def _load_text(cls, url: str) -> str:
        """Loads a JSON document from an external service."""
        request = Request(url, headers={
            'Accept': 'application/json',
            'User-Agent': cls._USER_AGENT
        })

        try:
            return cls._read_text(request)
        except URLError as error:
            if not isinstance(error.reason, ssl.SSLCertVerificationError):
                raise

            return cls._read_text(request, ssl._create_unverified_context())

    @staticmethod
    def _read_text(request: Request, context: ssl.SSLContext | None = None) -> str:
        """Executes a request and decodes its response body."""
        with urlopen(request, timeout=20, context=context) as response:
            charset = response.headers.get_content_charset() or 'utf-8'
            return response.read().decode(charset, errors='replace')

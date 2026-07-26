from __future__ import annotations
from datetime import datetime, timezone
from typing import Any, ClassVar

from flask import jsonify, request

from core.api.base_controller import BaseController
from models.exchange_rate_data_model import ExchangeRateDataModel
from models.fuel_data_model import FuelDataModel
from models.settings_data_model import SettingsDataModel
from resources.countries import Countries
from resources.fuel.labels import FuelLabels
from resources.fuel.price_fields import FuelPriceFields
from resources.fuel.sources import FuelSources
from storage.settings_storage import SettingsStorage
from utils.data.exchange_rate_downloader import ExchangeRateDownloader
from utils.data.fuel_price_downloader import FuelPriceDownloader


class FuelController(BaseController):
    """Exposes fuel price endpoints and persists typed fuel data."""

    CONTROLLER_NAME: ClassVar[str] = 'FuelController'

    def register_routes(self):
        self.add_url_rule('/api/fuel-prices/latest', view_func=self.latest, methods=['GET'])
        self.add_url_rule('/api/fuel-costs', view_func=self.costs, methods=['GET'])
        self.add_url_rule(
            '/api/fuel-costs/exchange-rate',
            view_func=self.save_selected_exchange_rate,
            methods=['PATCH']
        )
        self.add_url_rule('/api/fuel-costs/manual', view_func=self.save_manual_cost, methods=['POST', 'PATCH'])

    #region Stored data

    @staticmethod
    def _load_data() -> tuple[list[FuelDataModel], list[ExchangeRateDataModel]]:
        """Loads typed fuel and exchange rate models from settings."""
        settings = SettingsStorage().load()
        return settings.fuel_data, settings.exchange_rates

    @staticmethod
    def _save_data(
        fuel_data: list[FuelDataModel],
        exchange_rates: list[ExchangeRateDataModel]
    ) -> None:
        """Persists typed fuel and exchange rate models in settings."""
        storage = SettingsStorage()
        settings = storage.load()
        settings.fuel_data = fuel_data
        settings.exchange_rates = exchange_rates
        storage.save(settings)

    @staticmethod
    def _now_iso() -> str:
        """Returns the current UTC timestamp."""
        return datetime.now(timezone.utc).isoformat()

    @staticmethod
    def _rate_payload(models: list[ExchangeRateDataModel]) -> dict[str, float]:
        """Converts exchange rate models to the public API shape."""
        return {
            model.currency: model.rate
            for model in models
            if model.currency and model.rate > 0
        }

    @staticmethod
    def _rows_payload(models: list[FuelDataModel]) -> list[dict[str, Any]]:
        """Converts fuel models to the public API shape."""
        rows: list[dict[str, Any]] = []

        for model in models:
            row = model.to_dict()
            row.pop(FuelDataModel.FIELD_LOADED_AT, None)

            if not model.manual:
                row.pop(FuelDataModel.FIELD_MANUAL, None)
                row.pop(FuelDataModel.FIELD_MANUAL_UPDATED_AT, None)
                row.pop(FuelDataModel.FIELD_MANUAL_FIELDS, None)

            if not model.updated:
                row.pop(FuelDataModel.FIELD_UPDATED, None)

            if not model.source:
                row.pop(FuelDataModel.FIELD_SOURCE, None)

            rows.append(row)

        return rows

    @classmethod
    def _required_currencies(cls, fuel_data: list[FuelDataModel]) -> set[str]:
        """Returns currencies needed by the fuel cost view."""
        required = {'EUR', 'PLN'}

        for row in fuel_data:
            if row.currency:
                required.add(row.currency.upper())
            if row.source_currency:
                required.add(row.source_currency.upper())

        return required

    @classmethod
    def _has_required_rates(
        cls,
        rates: list[ExchangeRateDataModel],
        required: set[str]
    ) -> bool:
        """Checks whether modelled rates contain all required currencies."""
        return required.issubset(cls._rate_payload(rates))

    @classmethod
    def _refresh_rates(
        cls,
        fuel_data: list[FuelDataModel],
        rates: list[ExchangeRateDataModel],
        force: bool = False
    ) -> list[ExchangeRateDataModel]:
        """Refreshes incomplete exchange rate models."""
        required = cls._required_currencies(fuel_data)

        if not force and cls._has_required_rates(rates, required):
            return rates

        downloaded = ExchangeRateDownloader.download()

        if cls._has_required_rates(downloaded, {'EUR', 'PLN'}):
            cls._save_data(fuel_data, downloaded)
            return downloaded

        return rates

    @classmethod
    def _download_data(cls) -> tuple[list[FuelDataModel], list[ExchangeRateDataModel]]:
        """Downloads typed fuel and exchange rate models."""
        downloader = FuelPriceDownloader()
        fuel_data = downloader.download()
        loaded_at = cls._now_iso()

        for model in fuel_data:
            model.updated = model.updated or downloader.updated
            model.loaded_at = loaded_at

        return fuel_data, ExchangeRateDownloader.download()

    #endregion Stored data

    #region Manual prices

    @staticmethod
    def _countries_payload() -> list[dict[str, str]]:
        """Returns countries available for fuel costs and manual entries."""
        return [
            {
                'country_code': code,
                'country': data['country'],
                'currency': data['currency']
            }
            for code, data in sorted(Countries.VALUES.items(), key=lambda item: item[1]['country'])
        ]

    @staticmethod
    def _manual_rows(fuel_data: list[FuelDataModel]) -> dict[str, FuelDataModel]:
        """Returns manual fuel models indexed by country code."""
        return {
            row.country_code.upper(): row
            for row in fuel_data
            if row.manual and row.country_code
        }

    @staticmethod
    def _merge_manual_rows(
        fuel_data: list[FuelDataModel],
        manual_rows: dict[str, FuelDataModel],
        overwrite_codes: set[str]
    ) -> list[FuelDataModel]:
        """Keeps manual values unless a country was selected for overwrite."""
        indexed = {row.country_code.upper(): row for row in fuel_data if row.country_code}

        for code, manual_row in manual_rows.items():
            if code not in overwrite_codes or code not in indexed:
                indexed[code] = manual_row

        return sorted(indexed.values(), key=lambda row: row.country)

    @staticmethod
    def _to_optional_price(value: Any) -> float | None:
        """Converts a manual price to a nullable positive float."""
        if value in (None, ''):
            return None

        try:
            price = float(str(value).replace(',', '.'))
        except (TypeError, ValueError):
            return None

        return round(price, 4) if price > 0 else None

    @classmethod
    def _manual_model_from_payload(
        cls,
        payload: dict[str, Any],
        existing: FuelDataModel | None = None
    ) -> FuelDataModel:
        """Builds a typed manual fuel model from a request payload."""
        country_code = str(payload.get('country_code') or (existing.country_code if existing else '')).strip().upper()
        country = str(payload.get('country') or (existing.country if existing else '')).strip()
        currency = str(payload.get('currency') or (existing.currency if existing else '')).strip().upper()

        if not country_code or not country or not currency:
            raise ValueError('Country code, country and currency are required.')

        return FuelDataModel(
            country_code=country_code,
            country=country,
            currency=currency,
            source_currency=currency,
            petrol_95=cls._to_optional_price(payload.get(FuelPriceFields.PETROL_95)),
            petrol_98=cls._to_optional_price(payload.get(FuelPriceFields.PETROL_98)),
            diesel=cls._to_optional_price(payload.get(FuelPriceFields.DIESEL)),
            lpg=cls._to_optional_price(payload.get(FuelPriceFields.LPG)),
            source='manual',
            updated=None,
            loaded_at=cls._now_iso(),
            manual=True,
            manual_updated_at=cls._now_iso(),
            manual_fields=list(FuelPriceFields.VALUES)
        )

    #endregion Manual prices

    #region Responses

    @classmethod
    def _metadata_payload(
        cls,
        fuel_data: list[FuelDataModel],
        warning: str | None = None
    ) -> dict[str, Any]:
        """Derives response metadata from fuel models without storing another model."""
        automatic = [row for row in fuel_data if not row.manual]
        poland = next((row for row in automatic if row.country_code == 'PL'), None)
        updated = next((row.updated for row in automatic if row.updated), None)
        loaded_at = next((row.loaded_at for row in automatic if row.loaded_at), None)

        return {
            'source': FuelSources.OIL_BULLETIN_URL if automatic else 'manual',
            'poland_source': poland.source if poland and poland.source == FuelSources.AUTOCENTRUM_URL else None,
            'updated': updated,
            'loaded_at': loaded_at,
            'warning': warning
        }

    @classmethod
    def _data_response(
        cls,
        fuel_data: list[FuelDataModel],
        exchange_rates: list[ExchangeRateDataModel],
        selected_exchange_rate: str,
        row: FuelDataModel | None = None,
        warning: str | None = None
    ):
        """Builds the stable public response from stored models."""
        payload = {
            'status': 'ok',
            'metadata': cls._metadata_payload(fuel_data, warning),
            'rows': cls._rows_payload(fuel_data),
            'countries': cls._countries_payload(),
            'rates': cls._rate_payload(exchange_rates) or {'EUR': 1.0},
            SettingsDataModel.FIELD_SELECTED_EXCHANGE_RATE: selected_exchange_rate
        }

        if row:
            payload['row'] = cls._rows_payload([row])[0]

        return jsonify(payload)

    #endregion Responses

    #region Endpoints

    def latest(self):
        """Returns the latest known average fuel price for the selected fuel type."""
        fuel_type = request.args.get('fuel_type', '95')
        label = FuelLabels.VALUES.get(fuel_type.strip().lower())

        if not label:
            return jsonify({'status': 'error', 'message': 'Unsupported fuel type.'}), 400

        try:
            model = FuelPriceDownloader().download_latest(fuel_type)
        except Exception as error:
            return jsonify({
                'status': 'error',
                'message': f'Could not load fuel prices: {error}'
            }), 502

        if not model:
            return jsonify({
                'status': 'error',
                'message': 'Fuel price was not found in the source document.'
            }), 502

        price = {
            '95': model.petrol_95,
            '98': model.petrol_98,
            'ON': model.diesel,
            'LPG': model.lpg
        }[label]

        return jsonify({
            'status': 'ok',
            'fuel': {
                'fuel_type': fuel_type,
                'label': label,
                'price': price,
                'source': model.source,
                'updated': model.updated
            }
        })

    def costs(self):
        """Returns stored or freshly downloaded fuel cost data."""
        force = request.args.get('force', '').strip().lower() in ('1', 'true', 'yes', 'on')
        overwrite_codes = {
            code.strip().upper()
            for code in request.args.get('overwrite_manual', '').split(',')
            if code.strip()
        }
        stored_fuel, stored_rates = self._load_data()
        selected_exchange_rate = SettingsStorage().load().selected_exchange_rate

        if force or not stored_fuel:
            try:
                fuel_data, exchange_rates = self._download_data()
                fuel_data = self._merge_manual_rows(
                    fuel_data,
                    self._manual_rows(stored_fuel),
                    overwrite_codes
                )
                self._save_data(fuel_data, exchange_rates)
                return self._data_response(
                    fuel_data,
                    exchange_rates,
                    selected_exchange_rate
                )
            except Exception as error:
                if not stored_fuel:
                    return jsonify({
                        'status': 'error',
                        'message': f'Could not load fuel cost data: {error}'
                    }), 502

                stored_rates = self._refresh_rates(stored_fuel, stored_rates, force=True)
                return self._data_response(
                    stored_fuel,
                    stored_rates,
                    selected_exchange_rate,
                    warning=f'Nie udało się odświeżyć danych, pokazuję cache: {error}'
                )

        stored_rates = self._refresh_rates(stored_fuel, stored_rates)
        return self._data_response(
            stored_fuel,
            stored_rates,
            selected_exchange_rate
        )

    def save_selected_exchange_rate(self):
        """Persists the exchange rate selected in the fuel cost view."""
        payload = request.get_json(silent=True) or {}
        selected_exchange_rate = str(
            payload.get(SettingsDataModel.FIELD_SELECTED_EXCHANGE_RATE) or ''
        ).strip().upper()
        storage = SettingsStorage()
        settings = storage.load()
        available_rates = self._rate_payload(settings.exchange_rates)

        if selected_exchange_rate == 'ORIGINAL':
            selected_exchange_rate = SettingsDataModel.DEFAULT_SELECTED_EXCHANGE_RATE
        elif selected_exchange_rate not in available_rates:
            return jsonify({
                'status': 'error',
                'message': 'Unsupported exchange rate.'
            }), 400

        settings.selected_exchange_rate = selected_exchange_rate
        storage.save(settings)

        return jsonify({
            'status': 'ok',
            SettingsDataModel.FIELD_SELECTED_EXCHANGE_RATE: settings.selected_exchange_rate
        })

    def save_manual_cost(self):
        """Creates or updates a manual fuel cost row."""
        payload = request.get_json(silent=True) or {}
        fuel_data, exchange_rates = self._load_data()
        selected_exchange_rate = SettingsStorage().load().selected_exchange_rate
        country_code = str(payload.get('country_code') or '').strip().upper()
        existing = next((row for row in fuel_data if row.country_code.upper() == country_code), None)

        try:
            row = self._manual_model_from_payload(payload, existing)
        except ValueError as error:
            return jsonify({'status': 'error', 'message': str(error)}), 400

        fuel_data = [
            item for item in fuel_data
            if item.country_code.upper() != row.country_code
        ] + [row]
        fuel_data.sort(key=lambda item: item.country)
        exchange_rates = self._refresh_rates(fuel_data, exchange_rates)
        self._save_data(fuel_data, exchange_rates)

        return self._data_response(
            fuel_data,
            exchange_rates,
            selected_exchange_rate,
            row
        )

    #endregion Endpoints

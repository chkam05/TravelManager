from __future__ import annotations
from dataclasses import dataclass
from typing import Any, ClassVar, Dict, List

from core.data.base_data_model import BaseDataModel
from models.settings.ui_settings import UiSettings
from models.settings.car_profile import CarProfile
from models.settings.favourite_place import FavouritePlace
from models.settings.favourite_tag import FavouriteTag
from models.exchange_rate_data_model import ExchangeRateDataModel
from models.fuel_data_model import FuelDataModel
from models.settings.saved_route import SavedRoute
from models.settings.public_transport_cache import PublicTransportCache
from models.settings.window_settings import WindowSettings


@dataclass
class SettingsDataModel(BaseDataModel):
    """Stores application settings."""

    # Default values
    DEFAULT_SELECTED_EXCHANGE_RATE: ClassVar[str] = 'original'
    LEGACY_FIELD_FUEL_COST_CACHE: ClassVar[str] = 'fuel_cost_cache'

    # Field name declarations
    FIELD_ACTIVE_CAR_PROFILE_ID: ClassVar[str] = 'active_car_profile_id'
    FIELD_CAR_PROFILES: ClassVar[str] = 'car_profiles'
    FIELD_FAVOURITES: ClassVar[str] = 'favourites'
    FIELD_FAVOURITE_TAGS: ClassVar[str] = 'favourite_tags'
    FIELD_FUEL_DATA: ClassVar[str] = 'fuel_data'
    FIELD_EXCHANGE_RATES: ClassVar[str] = 'exchange_rates'
    FIELD_SELECTED_EXCHANGE_RATE: ClassVar[str] = 'selected_exchange_rate'
    FIELD_ROUTES: ClassVar[str] = 'routes'
    FIELD_PUBLIC_TRANSPORT_CACHE: ClassVar[str] = 'public_transport_cache'
    FIELD_SELECTED_PUBLIC_TRANSPORT_PROVIDER: ClassVar[str] = 'selected_public_transport_provider'
    FIELD_UI: ClassVar[str] = 'ui'
    FIELD_WINDOW: ClassVar[str] = 'window'

    # Fields
    active_car_profile_id: str | None
    car_profiles: List[CarProfile]
    favourites: List[FavouritePlace]
    favourite_tags: List[FavouriteTag]
    fuel_data: List[FuelDataModel]
    exchange_rates: List[ExchangeRateDataModel]
    selected_exchange_rate: str
    routes: List[SavedRoute]
    public_transport_cache: Dict[str, PublicTransportCache]
    selected_public_transport_provider: str
    ui: UiSettings | None
    window: WindowSettings | None

    #region Serialization

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> SettingsDataModel:
        """Deserializes data from a dictionary in "attribute:value" format to an object."""
        favourites = d.get(cls.FIELD_FAVOURITES, [])
        car_profiles = d.get(cls.FIELD_CAR_PROFILES, [])
        active_car_profile_id = d.get(cls.FIELD_ACTIVE_CAR_PROFILE_ID, None)
        favourite_tags = d.get(cls.FIELD_FAVOURITE_TAGS, [])
        fuel_data = d.get(cls.FIELD_FUEL_DATA)
        exchange_rates = d.get(cls.FIELD_EXCHANGE_RATES)
        selected_exchange_rate = str(
            d.get(cls.FIELD_SELECTED_EXCHANGE_RATE) or cls.DEFAULT_SELECTED_EXCHANGE_RATE
        ).strip()
        selected_exchange_rate = (
            cls.DEFAULT_SELECTED_EXCHANGE_RATE
            if selected_exchange_rate.lower() == cls.DEFAULT_SELECTED_EXCHANGE_RATE
            else selected_exchange_rate.upper()
        )
        legacy_cache = d.get(cls.LEGACY_FIELD_FUEL_COST_CACHE, {})
        legacy_cache = legacy_cache.get('data', legacy_cache) if isinstance(legacy_cache, dict) else {}

        if not isinstance(fuel_data, list):
            fuel_data = legacy_cache.get('rows', []) if isinstance(legacy_cache, dict) else []

        if not isinstance(exchange_rates, list):
            legacy_rates = legacy_cache.get('rates', []) if isinstance(legacy_cache, dict) else []
            if isinstance(legacy_rates, dict):
                exchange_rates = [
                    {
                        ExchangeRateDataModel.FIELD_BASE_CURRENCY: 'EUR',
                        ExchangeRateDataModel.FIELD_CURRENCY: currency,
                        ExchangeRateDataModel.FIELD_RATE: rate
                    }
                    for currency, rate in legacy_rates.items()
                ]
            else:
                exchange_rates = legacy_rates
        routes = d.get(cls.FIELD_ROUTES, [])
        public_transport_cache = d.get(cls.FIELD_PUBLIC_TRANSPORT_CACHE, {})
        selected_public_transport_provider = str(
            d.get(cls.FIELD_SELECTED_PUBLIC_TRANSPORT_PROVIDER) or ''
        ).strip()
        ui = d.get(cls.FIELD_UI, {})
        window = d.get(cls.FIELD_WINDOW, {})
        tags = FavouriteTag.from_dict_list(favourite_tags if isinstance(favourite_tags, list) else [])
        has_default_tag = any(tag.id == FavouriteTag.DEFAULT_TAG_ID for tag in tags)

        if not has_default_tag:
            tags.insert(0, FavouriteTag.default())
        tag_ids = {tag.id for tag in tags}
        mapped_favourites = FavouritePlace.from_dict_list(favourites if isinstance(favourites, list) else [])
        mapped_car_profiles = CarProfile.from_dict_list(car_profiles if isinstance(car_profiles, list) else [])
        mapped_routes = SavedRoute.from_dict_list(routes if isinstance(routes, list) else [])
        car_profile_ids = {profile.id for profile in mapped_car_profiles}
        active_id = str(active_car_profile_id) if active_car_profile_id else None

        if active_id not in car_profile_ids:
            active_id = None

        for favourite in mapped_favourites:
            if favourite.tag_id not in tag_ids:
                favourite.tag_id = FavouriteTag.DEFAULT_TAG_ID

        return cls(
            active_car_profile_id=active_id,
            car_profiles=mapped_car_profiles,
            favourites=mapped_favourites,
            favourite_tags=tags,
            fuel_data=FuelDataModel.from_dict_list(fuel_data),
            exchange_rates=ExchangeRateDataModel.from_dict_list(
                exchange_rates if isinstance(exchange_rates, list) else []
            ),
            selected_exchange_rate=(
                selected_exchange_rate or cls.DEFAULT_SELECTED_EXCHANGE_RATE
            ),
            routes=mapped_routes,
            public_transport_cache={
                str(carrier): PublicTransportCache.from_dict(value)
                for carrier, value in public_transport_cache.items()
                if isinstance(value, dict)
            } if isinstance(public_transport_cache, dict) else {},
            selected_public_transport_provider=selected_public_transport_provider,
            ui=UiSettings.from_dict(ui),
            window=WindowSettings.from_dict(window)
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Serializes object to a dictionary in the format "attribute:value"."""
        return {
            self.FIELD_ACTIVE_CAR_PROFILE_ID: self.active_car_profile_id,
            self.FIELD_CAR_PROFILES: self.to_dict_list(self.car_profiles),
            self.FIELD_FAVOURITES: self.to_dict_list(self.favourites),
            self.FIELD_FAVOURITE_TAGS: self.to_dict_list(self.favourite_tags),
            self.FIELD_FUEL_DATA: self.to_dict_list(self.fuel_data),
            self.FIELD_EXCHANGE_RATES: self.to_dict_list(self.exchange_rates),
            self.FIELD_SELECTED_EXCHANGE_RATE: self.selected_exchange_rate,
            self.FIELD_ROUTES: self.to_dict_list(self.routes),
            self.FIELD_PUBLIC_TRANSPORT_CACHE: {
                carrier: cache.to_dict()
                for carrier, cache in self.public_transport_cache.items()
            },
            self.FIELD_SELECTED_PUBLIC_TRANSPORT_PROVIDER: self.selected_public_transport_provider,
            self.FIELD_UI: self.ui.to_dict() if self.ui else UiSettings.from_dict({}).to_dict(),
            self.FIELD_WINDOW: self.window.to_dict() if self.window else WindowSettings.from_dict({}).to_dict()
        }

    #endregion Serialization

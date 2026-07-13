from __future__ import annotations
from dataclasses import dataclass
from typing import Any, ClassVar, Dict, List

from core.data.base_data_model import BaseDataModel
from models.settings.ui_settings import UiSettings
from models.settings.car_profile import CarProfile
from models.settings.favourite_place import FavouritePlace
from models.settings.favourite_tag import FavouriteTag
from models.settings.fuel_cost_cache import FuelCostCache
from models.settings.saved_route import SavedRoute
from models.settings.window_settings import WindowSettings


@dataclass
class SettingsDataModel(BaseDataModel):
    """Stores application settings."""

    # Default values

    # Field name declarations
    FIELD_ACTIVE_CAR_PROFILE_ID: ClassVar[str] = 'active_car_profile_id'
    FIELD_CAR_PROFILES: ClassVar[str] = 'car_profiles'
    FIELD_FAVOURITES: ClassVar[str] = 'favourites'
    FIELD_FAVOURITE_TAGS: ClassVar[str] = 'favourite_tags'
    FIELD_FUEL_COST_CACHE: ClassVar[str] = 'fuel_cost_cache'
    FIELD_ROUTES: ClassVar[str] = 'routes'
    FIELD_UI: ClassVar[str] = 'ui'
    FIELD_WINDOW: ClassVar[str] = 'window'

    # Fields
    active_car_profile_id: str | None
    car_profiles: List[CarProfile]
    favourites: List[FavouritePlace]
    favourite_tags: List[FavouriteTag]
    fuel_cost_cache: FuelCostCache | None
    routes: List[SavedRoute]
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
        fuel_cost_cache = d.get(cls.FIELD_FUEL_COST_CACHE, {})
        routes = d.get(cls.FIELD_ROUTES, [])
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
            fuel_cost_cache=FuelCostCache.from_dict(fuel_cost_cache if isinstance(fuel_cost_cache, dict) else {}),
            routes=mapped_routes,
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
            self.FIELD_FUEL_COST_CACHE: self.fuel_cost_cache.to_dict()
                if self.fuel_cost_cache else FuelCostCache.from_dict({}).to_dict(),
            self.FIELD_ROUTES: self.to_dict_list(self.routes),
            self.FIELD_UI: self.ui.to_dict() if self.ui else UiSettings.from_dict({}).to_dict(),
            self.FIELD_WINDOW: self.window.to_dict() if self.window else WindowSettings.from_dict({}).to_dict()
        }

    #endregion Serialization

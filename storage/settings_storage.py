from __future__ import annotations
import json
from typing import Any, ClassVar, Dict, List

from config import SETTINGS_DIR, SETTINGS_FILE_NAME
from core.data.base_data_model import BaseDataModel
from models.settings.favourite_tag import FavouriteTag
from models.settings_transfer.favourites_transfer_data_model import FavouritesTransferDataModel
from models.settings_transfer.fuel_costs_transfer_data_model import FuelCostsTransferDataModel
from models.settings_transfer.routes_transfer_data_model import RoutesTransferDataModel
from models.settings_data_model import SettingsDataModel
from models.settings.public_transport_cache import PublicTransportCache
from models.public_transport.public_transport_announcement import PublicTransportAnnouncement
from models.public_transport.public_transport_base_line import PublicTransportBaseLine
from models.public_transport.public_transport_stop import PublicTransportStop
from core.data.base_json_storage import BaseJsonStorage


class SettingsStorage(BaseJsonStorage):
    """Storage for application settings."""

    _LEGACY_TRANSFER_FIELD_DATA: ClassVar[str] = 'data'

    def __init__(self) -> None:
        super().__init__(SETTINGS_DIR, SETTINGS_FILE_NAME)

    def load(self) -> SettingsDataModel:
        """Loads application settings from JSON."""
        return SettingsDataModel.from_dict(self._read())

    def save(self, model: SettingsDataModel) -> None:
        """Saves application settings to JSON."""
        self._write(model.to_dict())

    #region Public transport cache

    def load_public_transport_cache(
        self,
        carrier: str
    ) -> PublicTransportCache | None:
        """Loads persistent public transport data for one carrier."""
        return self.load().public_transport_cache.get(carrier)

    def save_public_transport_cache(
        self,
        cache: PublicTransportCache
    ) -> None:
        """Saves persistent line and stop lists for one carrier."""
        with self._lock:
            settings = self.load()
            settings.public_transport_cache[cache.carrier] = cache
            self.save(settings)

    def save_public_transport_lines(
        self,
        carrier: str,
        lines: List[PublicTransportBaseLine]
    ) -> None:
        """Updates only the persistent line list for one carrier."""
        with self._lock:
            settings = self.load()
            cache = settings.public_transport_cache.get(carrier)
            settings.public_transport_cache[carrier] = PublicTransportCache(
                carrier=carrier,
                announcements=list(cache.announcements) if cache else [],
                lines=list(lines),
                stops=list(cache.stops) if cache else [],
                stop_locations_initialized=(
                    cache.stop_locations_initialized if cache else False
                )
            )
            self.save(settings)

    def save_public_transport_stops(
        self,
        carrier: str,
        stops: List[PublicTransportStop],
        stop_locations_initialized: bool = True
    ) -> None:
        """Updates only the persistent stop list for one carrier."""
        with self._lock:
            settings = self.load()
            cache = settings.public_transport_cache.get(carrier)
            settings.public_transport_cache[carrier] = PublicTransportCache(
                carrier=carrier,
                announcements=list(cache.announcements) if cache else [],
                lines=list(cache.lines) if cache else [],
                stops=list(stops),
                stop_locations_initialized=stop_locations_initialized
            )
            self.save(settings)

    def save_public_transport_announcements(
        self,
        carrier: str,
        announcements: List[PublicTransportAnnouncement]
    ) -> None:
        """Updates only the persistent announcement list for one carrier."""
        with self._lock:
            settings = self.load()
            cache = settings.public_transport_cache.get(carrier)
            settings.public_transport_cache[carrier] = PublicTransportCache(
                carrier=carrier,
                announcements=list(announcements),
                lines=list(cache.lines) if cache else [],
                stops=list(cache.stops) if cache else [],
                stop_locations_initialized=(
                    cache.stop_locations_initialized if cache else False
                )
            )
            self.save(settings)

    #endregion Public transport cache

    #region Settings transfer

    def export_fuel_costs(self) -> str:
        """Serializes fuel costs and exchange rates to JSON text."""
        settings = self.load()
        model = FuelCostsTransferDataModel(
            fuel_data=list(settings.fuel_data),
            exchange_rates=list(settings.exchange_rates)
        )
        return self._serialize_transfer_model(model)

    def export_routes(self) -> str:
        """Serializes saved routes to JSON text."""
        settings = self.load()
        model = RoutesTransferDataModel(routes=list(settings.routes))
        return self._serialize_transfer_model(model)

    def export_favourites_and_tags(self) -> str:
        """Serializes favourite places and tags to JSON text."""
        settings = self.load()
        model = FavouritesTransferDataModel(
            favourite_tags=list(settings.favourite_tags),
            favourites=list(settings.favourites)
        )
        return self._serialize_transfer_model(model)

    def import_fuel_costs(self, plaintext: str) -> None:
        """Deserializes fuel cost JSON text and updates application settings."""
        data = self._deserialize_transfer_text(plaintext)
        if not isinstance(data, dict):
            raise ValueError('Invalid fuel costs data.')

        if FuelCostsTransferDataModel.FIELD_FUEL_DATA in data:
            transfer = FuelCostsTransferDataModel.from_dict(data)
        else:
            migrated = SettingsDataModel.from_dict({
                SettingsDataModel.LEGACY_FIELD_FUEL_COST_CACHE: data
            })
            transfer = FuelCostsTransferDataModel(
                fuel_data=migrated.fuel_data,
                exchange_rates=migrated.exchange_rates
            )

        settings = self.load()
        settings.fuel_data = transfer.fuel_data
        settings.exchange_rates = transfer.exchange_rates
        self.save(settings)

    def import_routes(self, plaintext: str) -> None:
        """Deserializes saved route JSON text and updates application settings."""
        data = self._deserialize_transfer_text(plaintext)
        if isinstance(data, list):
            data = {RoutesTransferDataModel.FIELD_ROUTES: data}

        if not isinstance(data, dict) or not isinstance(
            data.get(RoutesTransferDataModel.FIELD_ROUTES),
            list
        ):
            raise ValueError('Invalid routes data.')

        transfer = RoutesTransferDataModel.from_dict(data)
        settings = self.load()
        settings.routes = transfer.routes
        self.save(settings)

    def import_favourites_and_tags(self, plaintext: str) -> None:
        """Deserializes favourites JSON text and updates application settings."""
        data = self._deserialize_transfer_text(plaintext)
        if not isinstance(data, dict):
            raise ValueError('Invalid favourites data.')

        transfer = FavouritesTransferDataModel.from_dict(data)
        tags = transfer.favourite_tags

        if not any(tag.id == FavouriteTag.DEFAULT_TAG_ID for tag in tags):
            tags.insert(0, FavouriteTag.default())

        tag_ids = {tag.id for tag in tags}
        for favourite in transfer.favourites:
            if favourite.tag_id not in tag_ids:
                favourite.tag_id = FavouriteTag.DEFAULT_TAG_ID

        settings = self.load()
        settings.favourite_tags = tags
        settings.favourites = transfer.favourites
        self.save(settings)

    @staticmethod
    def _serialize_transfer_model(model: BaseDataModel) -> str:
        """Serializes a transfer data model to formatted JSON text."""
        return json.dumps(model.to_dict(), ensure_ascii=False, indent=2)

    @staticmethod
    def _deserialize_transfer_text(plaintext: str) -> Any:
        """Deserializes JSON text and unwraps the former transfer envelope."""
        if not isinstance(plaintext, str):
            raise ValueError('Settings transfer input must be text.')

        data = json.loads(plaintext)

        if (
            isinstance(data, dict)
            and isinstance(data.get(SettingsStorage._LEGACY_TRANSFER_FIELD_DATA), (dict, list))
        ):
            return data[SettingsStorage._LEGACY_TRANSFER_FIELD_DATA]

        return data

    #endregion Settings transfer

    def _initialize_default_data(self) -> Dict[str, Any]:
        """Return the initial data structure for application settings."""
        return SettingsDataModel.from_dict({}).to_dict()

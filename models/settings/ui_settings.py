from __future__ import annotations
from dataclasses import dataclass
from typing import Any, ClassVar, Dict, List

from core.data.base_data_model import BaseDataModel


@dataclass
class UiSettings(BaseDataModel):
    """Stores persisted user interface state."""

    # Default values
    _DEFAULT_MAP_LATITUDE: ClassVar[float] = 52.2297
    _DEFAULT_MAP_LONGITUDE: ClassVar[float] = 21.0122
    _DEFAULT_MAP_ZOOM: ClassVar[int] = 13
    _DEFAULT_LAYER_DETAILS_PANEL_WIDTH: ClassVar[int] = 320
    _DEFAULT_LEGEND_DETAILS_PANEL_WIDTH: ClassVar[int] = 360
    _DEFAULT_PLACE_DETAILS_PANEL_WIDTH: ClassVar[int] = 320
    _DEFAULT_ROUTE_DETAILS_PANEL_WIDTH: ClassVar[int] = 360
    _DEFAULT_CAR_DETAILS_PANEL_WIDTH: ClassVar[int] = 360
    _DEFAULT_SEARCH_RESULTS_PANEL_WIDTH: ClassVar[int] = 360
    _DEFAULT_LAYER_MAP_NOTES_ENABLED: ClassVar[bool] = False
    _DEFAULT_LAYER_MAP_DATA_ENABLED: ClassVar[bool] = False
    _DEFAULT_LAYER_PUBLIC_GPS_TRACES_ENABLED: ClassVar[bool] = False
    _DEFAULT_LAYER_FAVOURITES_ENABLED: ClassVar[bool] = True
    _DEFAULT_MAP_BASE_LAYER: ClassVar[str] = 'standard'
    _DEFAULT_TRAVEL_FUEL_PRICE: ClassVar[float] = 0.0
    _DEFAULT_TRAVEL_FUEL_PRICES: ClassVar[Dict[str, float]] = {}
    _DEFAULT_TRAVEL_FUEL_TYPE: ClassVar[str] = '95'
    _DEFAULT_TRAVEL_COST_CURRENCY: ClassVar[str] = 'country'
    _DEFAULT_TRAVEL_MIN_CONSUMPTION: ClassVar[float] = 0.0
    _DEFAULT_TRAVEL_MAX_CONSUMPTION: ClassVar[float] = 0.0
    _DEFAULT_ROUTE_FUEL_SEPARATORS_ENABLED: ClassVar[bool] = True
    _DEFAULT_ROUTE_FUEL_SEPARATOR_ECONOMIC_ENABLED: ClassVar[bool] = True
    _DEFAULT_ROUTE_FUEL_SEPARATOR_AVERAGE_ENABLED: ClassVar[bool] = True
    _DEFAULT_ROUTE_FUEL_SEPARATOR_DYNAMIC_ENABLED: ClassVar[bool] = True
    _DEFAULT_ROUTE_FUEL_SEPARATOR_THRESHOLD_PERCENT: ClassVar[float] = 20.0
    _DEFAULT_ROUTE_TOLL_ROADS_ENABLED: ClassVar[bool] = True

    # Field name declarations
    FIELD_LAYER_FAVOURITE_VISIBLE_TAG_IDS: ClassVar[str] = 'layer_favourite_visible_tag_ids'
    FIELD_LAYER_MAP_DATA_ENABLED: ClassVar[str] = 'layer_map_data_enabled'
    FIELD_LAYER_FAVOURITES_ENABLED: ClassVar[str] = 'layer_favourites_enabled'
    FIELD_LAYER_MAP_NOTES_ENABLED: ClassVar[str] = 'layer_map_notes_enabled'
    FIELD_LAYER_PUBLIC_GPS_TRACES_ENABLED: ClassVar[str] = 'layer_public_gps_traces_enabled'
    FIELD_LAYER_DETAILS_PANEL_WIDTH: ClassVar[str] = 'layer_details_panel_width'
    FIELD_MAP_BASE_LAYER: ClassVar[str] = 'map_base_layer'
    FIELD_MAP_LATITUDE: ClassVar[str] = 'map_latitude'
    FIELD_MAP_LONGITUDE: ClassVar[str] = 'map_longitude'
    FIELD_MAP_ZOOM: ClassVar[str] = 'map_zoom'
    FIELD_LEGEND_DETAILS_PANEL_WIDTH: ClassVar[str] = 'legend_details_panel_width'
    FIELD_PLACE_DETAILS_PANEL_WIDTH: ClassVar[str] = 'place_details_panel_width'
    FIELD_ROUTE_DETAILS_PANEL_WIDTH: ClassVar[str] = 'route_details_panel_width'
    FIELD_CAR_DETAILS_PANEL_WIDTH: ClassVar[str] = 'car_details_panel_width'
    FIELD_SEARCH_RESULTS_PANEL_WIDTH: ClassVar[str] = 'search_results_panel_width'
    FIELD_TRAVEL_FUEL_PRICE: ClassVar[str] = 'travel_fuel_price'
    FIELD_TRAVEL_FUEL_PRICES: ClassVar[str] = 'travel_fuel_prices'
    FIELD_TRAVEL_FUEL_TYPE: ClassVar[str] = 'travel_fuel_type'
    FIELD_TRAVEL_COST_CURRENCY: ClassVar[str] = 'travel_cost_currency'
    FIELD_TRAVEL_MIN_CONSUMPTION: ClassVar[str] = 'travel_min_consumption'
    FIELD_TRAVEL_MAX_CONSUMPTION: ClassVar[str] = 'travel_max_consumption'
    FIELD_ROUTE_FUEL_SEPARATORS_ENABLED: ClassVar[str] = 'route_fuel_separators_enabled'
    FIELD_ROUTE_FUEL_SEPARATOR_ECONOMIC_ENABLED: ClassVar[str] = 'route_fuel_separator_economic_enabled'
    FIELD_ROUTE_FUEL_SEPARATOR_AVERAGE_ENABLED: ClassVar[str] = 'route_fuel_separator_average_enabled'
    FIELD_ROUTE_FUEL_SEPARATOR_DYNAMIC_ENABLED: ClassVar[str] = 'route_fuel_separator_dynamic_enabled'
    FIELD_ROUTE_FUEL_SEPARATOR_THRESHOLD_PERCENT: ClassVar[str] = 'route_fuel_separator_threshold_percent'
    FIELD_ROUTE_TOLL_ROADS_ENABLED: ClassVar[str] = 'route_toll_roads_enabled'

    # Fields
    map_latitude: float
    map_longitude: float
    map_zoom: int
    layer_details_panel_width: int
    legend_details_panel_width: int
    place_details_panel_width: int
    route_details_panel_width: int
    car_details_panel_width: int
    search_results_panel_width: int
    layer_favourites_enabled: bool
    layer_favourite_visible_tag_ids: List[str] | None
    layer_map_data_enabled: bool
    layer_map_notes_enabled: bool
    layer_public_gps_traces_enabled: bool
    map_base_layer: str
    travel_fuel_price: float
    travel_fuel_prices: Dict[str, float]
    travel_fuel_type: str
    travel_cost_currency: str
    travel_min_consumption: float
    travel_max_consumption: float
    route_fuel_separators_enabled: bool
    route_fuel_separator_economic_enabled: bool
    route_fuel_separator_average_enabled: bool
    route_fuel_separator_dynamic_enabled: bool
    route_fuel_separator_threshold_percent: float
    route_toll_roads_enabled: bool

    #region Serialization

    @classmethod
    def _to_float(cls, value: Any, default: float) -> float:
        """Converts numeric settings values to float."""
        try:
            return float(value)
        except (TypeError, ValueError):
            return default

    @classmethod
    def _to_int(cls, value: Any, default: int) -> int:
        """Converts numeric settings values to int."""
        try:
            return int(value)
        except (TypeError, ValueError):
            return default

    @classmethod
    def _to_bool(cls, value: Any, default: bool) -> bool:
        """Converts settings values to bool."""
        if isinstance(value, bool):
            return value

        if isinstance(value, str):
            return value.strip().lower() in ('1', 'true', 'yes', 'on')

        if isinstance(value, (int, float)):
            return bool(value)

        return default

    @classmethod
    def _to_string_list(cls, value: Any) -> List[str] | None:
        """Converts settings values to a list of strings or all-items marker."""
        if value is None:
            return None

        if not isinstance(value, list):
            return None

        return [
            str(item)
            for item in value
            if item is not None and str(item).strip()
        ]

    @classmethod
    def _to_float_dict(cls, value: Any) -> Dict[str, float]:
        """Converts settings values to a non-negative float dictionary."""
        if not isinstance(value, dict):
            return {}

        result: Dict[str, float] = {}

        for key, item in value.items():
            name = str(key).strip()

            if not name:
                continue

            result[name] = max(0.0, cls._to_float(item, 0.0))

        return result

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> UiSettings:
        """Deserializes data from a dictionary in "attribute:value" format to an object."""
        return cls(
            map_latitude=cls._to_float(
                d.get(cls.FIELD_MAP_LATITUDE, cls._DEFAULT_MAP_LATITUDE),
                cls._DEFAULT_MAP_LATITUDE
            ),
            map_longitude=cls._to_float(
                d.get(cls.FIELD_MAP_LONGITUDE, cls._DEFAULT_MAP_LONGITUDE),
                cls._DEFAULT_MAP_LONGITUDE
            ),
            map_zoom=cls._to_int(
                d.get(cls.FIELD_MAP_ZOOM, cls._DEFAULT_MAP_ZOOM),
                cls._DEFAULT_MAP_ZOOM
            ),
            layer_details_panel_width=cls._to_int(
                d.get(cls.FIELD_LAYER_DETAILS_PANEL_WIDTH, cls._DEFAULT_LAYER_DETAILS_PANEL_WIDTH),
                cls._DEFAULT_LAYER_DETAILS_PANEL_WIDTH
            ),
            legend_details_panel_width=cls._to_int(
                d.get(cls.FIELD_LEGEND_DETAILS_PANEL_WIDTH, cls._DEFAULT_LEGEND_DETAILS_PANEL_WIDTH),
                cls._DEFAULT_LEGEND_DETAILS_PANEL_WIDTH
            ),
            place_details_panel_width=cls._to_int(
                d.get(cls.FIELD_PLACE_DETAILS_PANEL_WIDTH, cls._DEFAULT_PLACE_DETAILS_PANEL_WIDTH),
                cls._DEFAULT_PLACE_DETAILS_PANEL_WIDTH
            ),
            route_details_panel_width=cls._to_int(
                d.get(cls.FIELD_ROUTE_DETAILS_PANEL_WIDTH, cls._DEFAULT_ROUTE_DETAILS_PANEL_WIDTH),
                cls._DEFAULT_ROUTE_DETAILS_PANEL_WIDTH
            ),
            car_details_panel_width=cls._to_int(
                d.get(cls.FIELD_CAR_DETAILS_PANEL_WIDTH, cls._DEFAULT_CAR_DETAILS_PANEL_WIDTH),
                cls._DEFAULT_CAR_DETAILS_PANEL_WIDTH
            ),
            search_results_panel_width=cls._to_int(
                d.get(cls.FIELD_SEARCH_RESULTS_PANEL_WIDTH, cls._DEFAULT_SEARCH_RESULTS_PANEL_WIDTH),
                cls._DEFAULT_SEARCH_RESULTS_PANEL_WIDTH
            ),
            layer_map_data_enabled=cls._to_bool(
                d.get(cls.FIELD_LAYER_MAP_DATA_ENABLED, cls._DEFAULT_LAYER_MAP_DATA_ENABLED),
                cls._DEFAULT_LAYER_MAP_DATA_ENABLED
            ),
            layer_map_notes_enabled=cls._to_bool(
                d.get(cls.FIELD_LAYER_MAP_NOTES_ENABLED, cls._DEFAULT_LAYER_MAP_NOTES_ENABLED),
                cls._DEFAULT_LAYER_MAP_NOTES_ENABLED
            ),
            layer_public_gps_traces_enabled=cls._to_bool(
                d.get(cls.FIELD_LAYER_PUBLIC_GPS_TRACES_ENABLED, cls._DEFAULT_LAYER_PUBLIC_GPS_TRACES_ENABLED),
                cls._DEFAULT_LAYER_PUBLIC_GPS_TRACES_ENABLED
            ),
            layer_favourites_enabled=cls._to_bool(
                d.get(cls.FIELD_LAYER_FAVOURITES_ENABLED, cls._DEFAULT_LAYER_FAVOURITES_ENABLED),
                cls._DEFAULT_LAYER_FAVOURITES_ENABLED
            ),
            layer_favourite_visible_tag_ids=cls._to_string_list(
                d.get(cls.FIELD_LAYER_FAVOURITE_VISIBLE_TAG_IDS, None)
            ),
            map_base_layer=str(
                d.get(cls.FIELD_MAP_BASE_LAYER, cls._DEFAULT_MAP_BASE_LAYER) or cls._DEFAULT_MAP_BASE_LAYER
            ),
            travel_fuel_price=max(0.0, cls._to_float(
                d.get(cls.FIELD_TRAVEL_FUEL_PRICE, cls._DEFAULT_TRAVEL_FUEL_PRICE),
                cls._DEFAULT_TRAVEL_FUEL_PRICE
            )),
            travel_fuel_prices=cls._to_float_dict(
                d.get(cls.FIELD_TRAVEL_FUEL_PRICES, cls._DEFAULT_TRAVEL_FUEL_PRICES)
            ),
            travel_fuel_type=str(
                d.get(cls.FIELD_TRAVEL_FUEL_TYPE, cls._DEFAULT_TRAVEL_FUEL_TYPE) or cls._DEFAULT_TRAVEL_FUEL_TYPE
            ),
            travel_cost_currency=str(
                d.get(cls.FIELD_TRAVEL_COST_CURRENCY, cls._DEFAULT_TRAVEL_COST_CURRENCY)
                or cls._DEFAULT_TRAVEL_COST_CURRENCY
            ),
            travel_min_consumption=max(0.0, cls._to_float(
                d.get(cls.FIELD_TRAVEL_MIN_CONSUMPTION, cls._DEFAULT_TRAVEL_MIN_CONSUMPTION),
                cls._DEFAULT_TRAVEL_MIN_CONSUMPTION
            )),
            travel_max_consumption=max(0.0, cls._to_float(
                d.get(cls.FIELD_TRAVEL_MAX_CONSUMPTION, cls._DEFAULT_TRAVEL_MAX_CONSUMPTION),
                cls._DEFAULT_TRAVEL_MAX_CONSUMPTION
            )),
            route_fuel_separators_enabled=cls._to_bool(
                d.get(cls.FIELD_ROUTE_FUEL_SEPARATORS_ENABLED, cls._DEFAULT_ROUTE_FUEL_SEPARATORS_ENABLED),
                cls._DEFAULT_ROUTE_FUEL_SEPARATORS_ENABLED
            ),
            route_fuel_separator_economic_enabled=cls._to_bool(
                d.get(
                    cls.FIELD_ROUTE_FUEL_SEPARATOR_ECONOMIC_ENABLED,
                    cls._DEFAULT_ROUTE_FUEL_SEPARATOR_ECONOMIC_ENABLED
                ),
                cls._DEFAULT_ROUTE_FUEL_SEPARATOR_ECONOMIC_ENABLED
            ),
            route_fuel_separator_average_enabled=cls._to_bool(
                d.get(
                    cls.FIELD_ROUTE_FUEL_SEPARATOR_AVERAGE_ENABLED,
                    cls._DEFAULT_ROUTE_FUEL_SEPARATOR_AVERAGE_ENABLED
                ),
                cls._DEFAULT_ROUTE_FUEL_SEPARATOR_AVERAGE_ENABLED
            ),
            route_fuel_separator_dynamic_enabled=cls._to_bool(
                d.get(
                    cls.FIELD_ROUTE_FUEL_SEPARATOR_DYNAMIC_ENABLED,
                    cls._DEFAULT_ROUTE_FUEL_SEPARATOR_DYNAMIC_ENABLED
                ),
                cls._DEFAULT_ROUTE_FUEL_SEPARATOR_DYNAMIC_ENABLED
            ),
            route_fuel_separator_threshold_percent=min(100.0, max(0.0, cls._to_float(
                d.get(
                    cls.FIELD_ROUTE_FUEL_SEPARATOR_THRESHOLD_PERCENT,
                    cls._DEFAULT_ROUTE_FUEL_SEPARATOR_THRESHOLD_PERCENT
                ),
                cls._DEFAULT_ROUTE_FUEL_SEPARATOR_THRESHOLD_PERCENT
            ))),
            route_toll_roads_enabled=cls._to_bool(
                d.get(cls.FIELD_ROUTE_TOLL_ROADS_ENABLED, cls._DEFAULT_ROUTE_TOLL_ROADS_ENABLED),
                cls._DEFAULT_ROUTE_TOLL_ROADS_ENABLED
            )
        )

    def to_dict(self) -> Dict[str, Any]:
        """Serializes object to a dictionary in the format "attribute:value"."""
        return {
            self.FIELD_MAP_LATITUDE: self.map_latitude,
            self.FIELD_MAP_LONGITUDE: self.map_longitude,
            self.FIELD_MAP_ZOOM: self.map_zoom,
            self.FIELD_LAYER_DETAILS_PANEL_WIDTH: self.layer_details_panel_width,
            self.FIELD_LEGEND_DETAILS_PANEL_WIDTH: self.legend_details_panel_width,
            self.FIELD_PLACE_DETAILS_PANEL_WIDTH: self.place_details_panel_width,
            self.FIELD_ROUTE_DETAILS_PANEL_WIDTH: self.route_details_panel_width,
            self.FIELD_CAR_DETAILS_PANEL_WIDTH: self.car_details_panel_width,
            self.FIELD_SEARCH_RESULTS_PANEL_WIDTH: self.search_results_panel_width,
            self.FIELD_LAYER_MAP_DATA_ENABLED: self.layer_map_data_enabled,
            self.FIELD_LAYER_MAP_NOTES_ENABLED: self.layer_map_notes_enabled,
            self.FIELD_LAYER_PUBLIC_GPS_TRACES_ENABLED: self.layer_public_gps_traces_enabled,
            self.FIELD_LAYER_FAVOURITES_ENABLED: self.layer_favourites_enabled,
            self.FIELD_LAYER_FAVOURITE_VISIBLE_TAG_IDS: self.layer_favourite_visible_tag_ids,
            self.FIELD_MAP_BASE_LAYER: self.map_base_layer,
            self.FIELD_TRAVEL_FUEL_PRICE: self.travel_fuel_price,
            self.FIELD_TRAVEL_FUEL_PRICES: self.travel_fuel_prices,
            self.FIELD_TRAVEL_FUEL_TYPE: self.travel_fuel_type,
            self.FIELD_TRAVEL_COST_CURRENCY: self.travel_cost_currency,
            self.FIELD_TRAVEL_MIN_CONSUMPTION: self.travel_min_consumption,
            self.FIELD_TRAVEL_MAX_CONSUMPTION: self.travel_max_consumption,
            self.FIELD_ROUTE_FUEL_SEPARATORS_ENABLED: self.route_fuel_separators_enabled,
            self.FIELD_ROUTE_FUEL_SEPARATOR_ECONOMIC_ENABLED: self.route_fuel_separator_economic_enabled,
            self.FIELD_ROUTE_FUEL_SEPARATOR_AVERAGE_ENABLED: self.route_fuel_separator_average_enabled,
            self.FIELD_ROUTE_FUEL_SEPARATOR_DYNAMIC_ENABLED: self.route_fuel_separator_dynamic_enabled,
            self.FIELD_ROUTE_FUEL_SEPARATOR_THRESHOLD_PERCENT: self.route_fuel_separator_threshold_percent,
            self.FIELD_ROUTE_TOLL_ROADS_ENABLED: self.route_toll_roads_enabled
        }

    #endregion Serialization

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, List

from core.data.base_data_model import BaseDataModel
from models.public_transport.public_transport_city import PublicTransportCity
from models.public_transport.public_transport_coordinate import PublicTransportCoordinate
from models.public_transport.public_transport_direction_stop import PublicTransportDirectionStop


@dataclass
class PublicTransportDirection(BaseDataModel):
    """Stores one travel direction and its ordered stops."""

    # Field name declarations
    FIELD_NAME: ClassVar[str] = 'name'
    FIELD_CITIES: ClassVar[str] = 'cities'
    FIELD_STOPS: ClassVar[str] = 'stops'
    FIELD_ROUTE: ClassVar[str] = 'route'
    FIELD_ROUTE_IS_APPROXIMATE: ClassVar[str] = 'route_is_approximate'

    # Fields
    name: str
    cities: List[PublicTransportCity]
    stops: List[PublicTransportDirectionStop]
    route: List[PublicTransportCoordinate] = field(default_factory=list)
    route_is_approximate: bool = False

    #region Serialization

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> PublicTransportDirection:
        """Deserializes data from a dictionary in "attribute:value" format to an object."""
        cities = d.get(cls.FIELD_CITIES, [])
        stops = d.get(cls.FIELD_STOPS, [])
        route = d.get(cls.FIELD_ROUTE, [])
        return cls(
            name=str(d.get(cls.FIELD_NAME) or ''),
            cities=PublicTransportCity.from_dict_list(cities if isinstance(cities, list) else []),
            stops=PublicTransportDirectionStop.from_dict_list(
                stops if isinstance(stops, list) else []
            ),
            route=PublicTransportCoordinate.from_dict_list(
                route if isinstance(route, list) else []
            ),
            route_is_approximate=bool(
                d.get(cls.FIELD_ROUTE_IS_APPROXIMATE, False)
            )
        )

    def to_dict(self) -> Dict[str, Any]:
        """Serializes object to a dictionary in the format "attribute:value"."""
        return {
            self.FIELD_NAME: self.name,
            self.FIELD_CITIES: self.to_dict_list(self.cities),
            self.FIELD_STOPS: self.to_dict_list(self.stops),
            self.FIELD_ROUTE: self.to_dict_list(self.route),
            self.FIELD_ROUTE_IS_APPROXIMATE: self.route_is_approximate
        }

    #endregion Serialization

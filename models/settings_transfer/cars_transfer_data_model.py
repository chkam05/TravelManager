from __future__ import annotations
from dataclasses import dataclass
from typing import Any, ClassVar, Dict, List

from core.data.base_data_model import BaseDataModel
from models.settings.car_profile import CarProfile


@dataclass
class CarsTransferDataModel(BaseDataModel):
    """Stores the explicit car profiles transfer payload."""

    # Default values

    # Field name declarations
    FIELD_ACTIVE_CAR_PROFILE_ID: ClassVar[str] = 'active_car_profile_id'
    FIELD_CAR_PROFILES: ClassVar[str] = 'car_profiles'

    # Fields
    active_car_profile_id: str | None
    car_profiles: List[CarProfile]

    #region Serialization

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> CarsTransferDataModel:
        """Deserializes data from a dictionary in "attribute:value" format to an object."""
        car_profiles = d.get(cls.FIELD_CAR_PROFILES, [])
        active_car_profile_id = d.get(cls.FIELD_ACTIVE_CAR_PROFILE_ID)
        return cls(
            active_car_profile_id=(
                str(active_car_profile_id) if active_car_profile_id else None
            ),
            car_profiles=CarProfile.from_dict_list(
                car_profiles if isinstance(car_profiles, list) else []
            )
        )

    def to_dict(self) -> Dict[str, Any]:
        """Serializes object to a dictionary in the format "attribute:value"."""
        return {
            self.FIELD_ACTIVE_CAR_PROFILE_ID: self.active_car_profile_id,
            self.FIELD_CAR_PROFILES: self.to_dict_list(self.car_profiles)
        }

    #endregion Serialization

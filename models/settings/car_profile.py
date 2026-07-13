from __future__ import annotations

from dataclasses import dataclass
from typing import Any, ClassVar, Dict, List

from core.data.base_data_model import BaseDataModel
from resources.enums.car_body_type import CarBodyType
from resources.enums.car_drive_type import CarDriveType
from resources.enums.car_transmission_type import CarTransmissionType


@dataclass
class CarProfile(BaseDataModel):
    """Stores a user-defined car profile used for route cost estimates."""

    # Default values
    _HP_PER_KW: ClassVar[float] = 1.359621617

    # Field name declarations
    FIELD_ID: ClassVar[str] = 'id'
    FIELD_NAME: ClassVar[str] = 'name'
    FIELD_BRAND: ClassVar[str] = 'brand'
    FIELD_MODEL: ClassVar[str] = 'model'
    FIELD_VERSION: ClassVar[str] = 'version'
    FIELD_GENERATION: ClassVar[str] = 'generation'
    FIELD_PRODUCTION_YEAR: ClassVar[str] = 'production_year'
    FIELD_BODY_TYPE: ClassVar[str] = 'body_type'
    FIELD_ENGINE_CAPACITY: ClassVar[str] = 'engine_capacity'
    FIELD_POWER_HP: ClassVar[str] = 'power_hp'
    FIELD_POWER_KW: ClassVar[str] = 'power_kw'
    FIELD_MAX_SPEED: ClassVar[str] = 'max_speed'
    FIELD_DRIVE_TYPE: ClassVar[str] = 'drive_type'
    FIELD_TRANSMISSION_TYPE: ClassVar[str] = 'transmission_type'
    FIELD_FUEL_TANK_CAPACITY: ClassVar[str] = 'fuel_tank_capacity'
    FIELD_ODOMETER_ENTRIES: ClassVar[str] = 'odometer_entries'
    FIELD_REGISTRATION_NUMBER: ClassVar[str] = 'registration_number'
    FIELD_FUEL_TYPE: ClassVar[str] = 'fuel_type'
    FIELD_SECONDARY_FUEL_TYPE: ClassVar[str] = 'secondary_fuel_type'
    FIELD_MIN_CONSUMPTION: ClassVar[str] = 'min_consumption'
    FIELD_MAX_CONSUMPTION: ClassVar[str] = 'max_consumption'
    FIELD_IMAGE: ClassVar[str] = 'image'

    # Fields
    id: str
    name: str
    brand: str
    model: str
    version: str
    generation: str
    production_year: int | None
    body_type: str
    engine_capacity: int | None
    power_hp: int | None
    power_kw: float | None
    max_speed: int | None
    drive_type: str
    transmission_type: str
    fuel_tank_capacity: float | None
    odometer_entries: List[Dict[str, Any]]
    registration_number: str
    fuel_type: str
    secondary_fuel_type: str
    min_consumption: float | None
    max_consumption: float | None
    image: str

    #region Serialization

    @classmethod
    def _to_optional_int(cls, value: Any) -> int | None:
        """Converts a value to int or empty value."""
        try:
            result = int(value)
        except (TypeError, ValueError):
            return None

        return result if result >= 0 else None

    @classmethod
    def _to_optional_float(cls, value: Any) -> float | None:
        """Converts a value to float or empty value."""
        try:
            result = float(value)
        except (TypeError, ValueError):
            return None

        return result if result >= 0 else None

    @classmethod
    def _to_odometer_entries(cls, value: Any) -> List[Dict[str, Any]]:
        """Normalizes odometer entries."""
        if not isinstance(value, list):
            return []

        entries: List[Dict[str, Any]] = []

        for item in value:
            if not isinstance(item, dict):
                continue

            distance = cls._to_optional_float(item.get('distance'))
            date = str(item.get('date', '')).strip()

            if distance is None and not date:
                continue

            entries.append({
                'distance': distance or 0.0,
                'date': date
            })

        return entries

    @classmethod
    def _enum_or_text(cls, enum_type, value: Any) -> str:
        """Returns a normalized enum value when possible, otherwise raw text."""
        text = str(value or '').strip()

        if not text:
            return ''

        try:
            return enum_type.from_str(text).value
        except ValueError:
            return text

    @classmethod
    def _resolve_power_hp(cls, hp: int | None, kw: float | None) -> int | None:
        """Returns horsepower, converting from kW when needed."""
        if hp is not None:
            return hp

        if kw is None:
            return None

        return int(round(kw * cls._HP_PER_KW))

    @classmethod
    def _resolve_power_kw(cls, hp: int | None, kw: float | None) -> float | None:
        """Returns kilowatts, converting from horsepower when needed."""
        if kw is not None:
            return round(kw, 2)

        if hp is None:
            return None

        return round(hp / cls._HP_PER_KW, 2)

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> CarProfile:
        """Deserializes car profile data from a dictionary."""
        power_hp = cls._to_optional_int(d.get(cls.FIELD_POWER_HP))
        power_kw = cls._to_optional_float(d.get(cls.FIELD_POWER_KW))

        return cls(
            id=str(d.get(cls.FIELD_ID, '')),
            name=str(d.get(cls.FIELD_NAME, '')),
            brand=str(d.get(cls.FIELD_BRAND, '')),
            model=str(d.get(cls.FIELD_MODEL, '')),
            version=str(d.get(cls.FIELD_VERSION, '')),
            generation=str(d.get(cls.FIELD_GENERATION, '')),
            production_year=cls._to_optional_int(d.get(cls.FIELD_PRODUCTION_YEAR)),
            body_type=cls._enum_or_text(CarBodyType, d.get(cls.FIELD_BODY_TYPE, '')),
            engine_capacity=cls._to_optional_int(d.get(cls.FIELD_ENGINE_CAPACITY)),
            power_hp=cls._resolve_power_hp(power_hp, power_kw),
            power_kw=cls._resolve_power_kw(power_hp, power_kw),
            max_speed=cls._to_optional_int(d.get(cls.FIELD_MAX_SPEED)),
            drive_type=cls._enum_or_text(CarDriveType, d.get(cls.FIELD_DRIVE_TYPE, '')),
            transmission_type=cls._enum_or_text(CarTransmissionType, d.get(cls.FIELD_TRANSMISSION_TYPE, '')),
            fuel_tank_capacity=cls._to_optional_float(d.get(cls.FIELD_FUEL_TANK_CAPACITY)),
            odometer_entries=cls._to_odometer_entries(d.get(cls.FIELD_ODOMETER_ENTRIES)),
            registration_number=str(d.get(cls.FIELD_REGISTRATION_NUMBER, '')),
            fuel_type=str(d.get(cls.FIELD_FUEL_TYPE, '95') or '95'),
            secondary_fuel_type=str(d.get(cls.FIELD_SECONDARY_FUEL_TYPE, '')),
            min_consumption=cls._to_optional_float(d.get(cls.FIELD_MIN_CONSUMPTION)),
            max_consumption=cls._to_optional_float(d.get(cls.FIELD_MAX_CONSUMPTION)),
            image=str(d.get(cls.FIELD_IMAGE, ''))
        )

    def to_dict(self) -> Dict[str, Any]:
        """Serializes car profile data to a dictionary."""
        return {
            self.FIELD_ID: self.id,
            self.FIELD_NAME: self.name,
            self.FIELD_BRAND: self.brand,
            self.FIELD_MODEL: self.model,
            self.FIELD_VERSION: self.version,
            self.FIELD_GENERATION: self.generation,
            self.FIELD_PRODUCTION_YEAR: self.production_year,
            self.FIELD_BODY_TYPE: self.body_type,
            self.FIELD_ENGINE_CAPACITY: self.engine_capacity,
            self.FIELD_POWER_HP: self.power_hp,
            self.FIELD_POWER_KW: self.power_kw,
            self.FIELD_MAX_SPEED: self.max_speed,
            self.FIELD_DRIVE_TYPE: self.drive_type,
            self.FIELD_TRANSMISSION_TYPE: self.transmission_type,
            self.FIELD_FUEL_TANK_CAPACITY: self.fuel_tank_capacity,
            self.FIELD_ODOMETER_ENTRIES: self.odometer_entries,
            self.FIELD_REGISTRATION_NUMBER: self.registration_number,
            self.FIELD_FUEL_TYPE: self.fuel_type,
            self.FIELD_SECONDARY_FUEL_TYPE: self.secondary_fuel_type,
            self.FIELD_MIN_CONSUMPTION: self.min_consumption,
            self.FIELD_MAX_CONSUMPTION: self.max_consumption,
            self.FIELD_IMAGE: self.image
        }

    #endregion Serialization

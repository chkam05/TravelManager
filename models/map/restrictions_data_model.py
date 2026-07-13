from __future__ import annotations
from dataclasses import dataclass
from typing import Any, ClassVar, Dict

from core.data.base_data_model import BaseDataModel


@dataclass
class RestrictionsDataModel(BaseDataModel):
    """Stores OpenStreetMap tag values defined by OpenStreetMap RestrictionsAttr."""

    # Default values
    _DEFAULT_VALUE: ClassVar[Any] = None

    # Field name declarations
    FIELD_ACCESS: ClassVar[str] = 'access'
    FIELD_AGRICULTURAL: ClassVar[str] = 'agricultural'
    FIELD_ATV: ClassVar[str] = 'atv'
    FIELD_BDOUBLE: ClassVar[str] = 'bdouble'
    FIELD_BICYCLE: ClassVar[str] = 'bicycle'
    FIELD_BOAT: ClassVar[str] = 'boat'
    FIELD_BUS: ClassVar[str] = 'bus'
    FIELD_CARRIAGE: ClassVar[str] = 'carriage'
    FIELD_CYCLE_RICKSHAW: ClassVar[str] = 'cycle_rickshaw'
    FIELD_ELECTRIC_BICYCLE: ClassVar[str] = 'electric_bicycle'
    FIELD_EMERGENCY: ClassVar[str] = 'emergency'
    FIELD_FOOT: ClassVar[str] = 'foot'
    FIELD_FORESTRY: ClassVar[str] = 'forestry'
    FIELD_GOLF_CART: ClassVar[str] = 'golf_cart'
    FIELD_GOODS: ClassVar[str] = 'goods'
    FIELD_HAND_CART: ClassVar[str] = 'hand_cart'
    FIELD_HAZMAT: ClassVar[str] = 'hazmat'
    FIELD_HGV: ClassVar[str] = 'hgv'
    FIELD_HORSE: ClassVar[str] = 'horse'
    FIELD_HOV: ClassVar[str] = 'hov'
    FIELD_INLINE_SKATES: ClassVar[str] = 'inline_skates'
    FIELD_LHV: ClassVar[str] = 'lhv'
    FIELD_MOFA: ClassVar[str] = 'mofa'
    FIELD_MOPED: ClassVar[str] = 'moped'
    FIELD_MOTORBOAT: ClassVar[str] = 'motorboat'
    FIELD_MOTORCAR: ClassVar[str] = 'motorcar'
    FIELD_MOTORCYCLE: ClassVar[str] = 'motorcycle'
    FIELD_MOTOR_VEHICLE: ClassVar[str] = 'motor_vehicle'
    FIELD_PSV: ClassVar[str] = 'psv'
    FIELD_ROADTRAIN: ClassVar[str] = 'roadtrain'
    FIELD_SKI: ClassVar[str] = 'ski'
    FIELD_SPEED_PEDELEC: ClassVar[str] = 'speed_pedelec'
    FIELD_TANK: ClassVar[str] = 'tank'
    FIELD_TAXI: ClassVar[str] = 'taxi'
    FIELD_TRAILER: ClassVar[str] = 'trailer'
    FIELD_TOURIST_BUS: ClassVar[str] = 'tourist_bus'
    FIELD_VEHICLE: ClassVar[str] = 'vehicle'
    FIELD_FOUR_WD_ONLY: ClassVar[str] = 'four_wd_only'
    FIELD_ALCOHOL: ClassVar[str] = 'alcohol'
    FIELD_DOG: ClassVar[str] = 'dog'
    FIELD_DRINKING_WATER_LEGAL: ClassVar[str] = 'drinking_water_legal'
    FIELD_FEMALE: ClassVar[str] = 'female'
    FIELD_MALE: ClassVar[str] = 'male'
    FIELD_MAX_AGE: ClassVar[str] = 'max_age'
    FIELD_MAXAXLELOAD: ClassVar[str] = 'maxaxleload'
    FIELD_MAXHEIGHT: ClassVar[str] = 'maxheight'
    FIELD_MAXLENGTH: ClassVar[str] = 'maxlength'
    FIELD_MAXSPEED: ClassVar[str] = 'maxspeed'
    FIELD_MAXSTAY: ClassVar[str] = 'maxstay'
    FIELD_MAXWEIGHT: ClassVar[str] = 'maxweight'
    FIELD_MAXWIDTH: ClassVar[str] = 'maxwidth'
    FIELD_MIN_AGE: ClassVar[str] = 'min_age'
    FIELD_MINSPEED: ClassVar[str] = 'minspeed'
    FIELD_NOEXIT: ClassVar[str] = 'noexit'
    FIELD_ONEWAY: ClassVar[str] = 'oneway'
    FIELD_OPENFIRE: ClassVar[str] = 'openfire'
    FIELD_SMOKING: ClassVar[str] = 'smoking'
    FIELD_TOLL: ClassVar[str] = 'toll'
    FIELD_TRAFFIC_SIGN: ClassVar[str] = 'traffic_sign'
    FIELD_UNISEX: ClassVar[str] = 'unisex'

    # OpenStreetMap tag declarations
    TAG_ACCESS: ClassVar[str] = 'access'
    TAG_AGRICULTURAL: ClassVar[str] = 'agricultural'
    TAG_ATV: ClassVar[str] = 'atv'
    TAG_BDOUBLE: ClassVar[str] = 'bdouble'
    TAG_BICYCLE: ClassVar[str] = 'bicycle'
    TAG_BOAT: ClassVar[str] = 'boat'
    TAG_BUS: ClassVar[str] = 'bus'
    TAG_CARRIAGE: ClassVar[str] = 'carriage'
    TAG_CYCLE_RICKSHAW: ClassVar[str] = 'cycle_rickshaw'
    TAG_ELECTRIC_BICYCLE: ClassVar[str] = 'electric_bicycle'
    TAG_EMERGENCY: ClassVar[str] = 'emergency'
    TAG_FOOT: ClassVar[str] = 'foot'
    TAG_FORESTRY: ClassVar[str] = 'forestry'
    TAG_GOLF_CART: ClassVar[str] = 'golf_cart'
    TAG_GOODS: ClassVar[str] = 'goods'
    TAG_HAND_CART: ClassVar[str] = 'hand_cart'
    TAG_HAZMAT: ClassVar[str] = 'hazmat'
    TAG_HGV: ClassVar[str] = 'hgv'
    TAG_HORSE: ClassVar[str] = 'horse'
    TAG_HOV: ClassVar[str] = 'hov'
    TAG_INLINE_SKATES: ClassVar[str] = 'inline_skates'
    TAG_LHV: ClassVar[str] = 'lhv'
    TAG_MOFA: ClassVar[str] = 'mofa'
    TAG_MOPED: ClassVar[str] = 'moped'
    TAG_MOTORBOAT: ClassVar[str] = 'motorboat'
    TAG_MOTORCAR: ClassVar[str] = 'motorcar'
    TAG_MOTORCYCLE: ClassVar[str] = 'motorcycle'
    TAG_MOTOR_VEHICLE: ClassVar[str] = 'motor_vehicle'
    TAG_PSV: ClassVar[str] = 'psv'
    TAG_ROADTRAIN: ClassVar[str] = 'roadtrain'
    TAG_SKI: ClassVar[str] = 'ski'
    TAG_SPEED_PEDELEC: ClassVar[str] = 'speed_pedelec'
    TAG_TANK: ClassVar[str] = 'tank'
    TAG_TAXI: ClassVar[str] = 'taxi'
    TAG_TRAILER: ClassVar[str] = 'trailer'
    TAG_TOURIST_BUS: ClassVar[str] = 'tourist_bus'
    TAG_VEHICLE: ClassVar[str] = 'vehicle'
    TAG_FOUR_WD_ONLY: ClassVar[str] = '4wd_only'
    TAG_ALCOHOL: ClassVar[str] = 'alcohol'
    TAG_DOG: ClassVar[str] = 'dog'
    TAG_DRINKING_WATER_LEGAL: ClassVar[str] = 'drinking_water:legal'
    TAG_FEMALE: ClassVar[str] = 'female'
    TAG_MALE: ClassVar[str] = 'male'
    TAG_MAX_AGE: ClassVar[str] = 'max_age'
    TAG_MAXAXLELOAD: ClassVar[str] = 'maxaxleload'
    TAG_MAXHEIGHT: ClassVar[str] = 'maxheight'
    TAG_MAXLENGTH: ClassVar[str] = 'maxlength'
    TAG_MAXSPEED: ClassVar[str] = 'maxspeed'
    TAG_MAXSTAY: ClassVar[str] = 'maxstay'
    TAG_MAXWEIGHT: ClassVar[str] = 'maxweight'
    TAG_MAXWIDTH: ClassVar[str] = 'maxwidth'
    TAG_MIN_AGE: ClassVar[str] = 'min_age'
    TAG_MINSPEED: ClassVar[str] = 'minspeed'
    TAG_NOEXIT: ClassVar[str] = 'noexit'
    TAG_ONEWAY: ClassVar[str] = 'oneway'
    TAG_OPENFIRE: ClassVar[str] = 'openfire'
    TAG_SMOKING: ClassVar[str] = 'smoking'
    TAG_TOLL: ClassVar[str] = 'toll'
    TAG_TRAFFIC_SIGN: ClassVar[str] = 'traffic_sign'
    TAG_UNISEX: ClassVar[str] = 'unisex'

    # Fields
    access: Any | None
    agricultural: Any | None
    atv: Any | None
    bdouble: Any | None
    bicycle: Any | None
    boat: Any | None
    bus: Any | None
    carriage: Any | None
    cycle_rickshaw: Any | None
    electric_bicycle: Any | None
    emergency: Any | None
    foot: Any | None
    forestry: Any | None
    golf_cart: Any | None
    goods: Any | None
    hand_cart: Any | None
    hazmat: Any | None
    hgv: Any | None
    horse: Any | None
    hov: Any | None
    inline_skates: Any | None
    lhv: Any | None
    mofa: Any | None
    moped: Any | None
    motorboat: Any | None
    motorcar: Any | None
    motorcycle: Any | None
    motor_vehicle: Any | None
    psv: Any | None
    roadtrain: Any | None
    ski: Any | None
    speed_pedelec: Any | None
    tank: Any | None
    taxi: Any | None
    trailer: Any | None
    tourist_bus: Any | None
    vehicle: Any | None
    four_wd_only: Any | None
    alcohol: Any | None
    dog: Any | None
    drinking_water_legal: Any | None
    female: Any | None
    male: Any | None
    max_age: Any | None
    maxaxleload: Any | None
    maxheight: Any | None
    maxlength: Any | None
    maxspeed: Any | None
    maxstay: Any | None
    maxweight: Any | None
    maxwidth: Any | None
    min_age: Any | None
    minspeed: Any | None
    noexit: Any | None
    oneway: Any | None
    openfire: Any | None
    smoking: Any | None
    toll: Any | None
    traffic_sign: Any | None
    unisex: Any | None

    #region Serialization

    @classmethod
    def _get_value(cls, d: Dict[str, Any], field_name: str, tag_name: str) -> Any:
        """Gets a value by local field name or by the real OpenStreetMap tag key."""
        return d.get(tag_name, d.get(field_name, cls._DEFAULT_VALUE))

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> RestrictionsDataModel:
        """Deserializes data from a dictionary in "attribute:value" format to an object."""
        return cls(
            access=cls._get_value(d, cls.FIELD_ACCESS, cls.TAG_ACCESS),
            agricultural=cls._get_value(d, cls.FIELD_AGRICULTURAL, cls.TAG_AGRICULTURAL),
            atv=cls._get_value(d, cls.FIELD_ATV, cls.TAG_ATV),
            bdouble=cls._get_value(d, cls.FIELD_BDOUBLE, cls.TAG_BDOUBLE),
            bicycle=cls._get_value(d, cls.FIELD_BICYCLE, cls.TAG_BICYCLE),
            boat=cls._get_value(d, cls.FIELD_BOAT, cls.TAG_BOAT),
            bus=cls._get_value(d, cls.FIELD_BUS, cls.TAG_BUS),
            carriage=cls._get_value(d, cls.FIELD_CARRIAGE, cls.TAG_CARRIAGE),
            cycle_rickshaw=cls._get_value(d, cls.FIELD_CYCLE_RICKSHAW, cls.TAG_CYCLE_RICKSHAW),
            electric_bicycle=cls._get_value(d, cls.FIELD_ELECTRIC_BICYCLE, cls.TAG_ELECTRIC_BICYCLE),
            emergency=cls._get_value(d, cls.FIELD_EMERGENCY, cls.TAG_EMERGENCY),
            foot=cls._get_value(d, cls.FIELD_FOOT, cls.TAG_FOOT),
            forestry=cls._get_value(d, cls.FIELD_FORESTRY, cls.TAG_FORESTRY),
            golf_cart=cls._get_value(d, cls.FIELD_GOLF_CART, cls.TAG_GOLF_CART),
            goods=cls._get_value(d, cls.FIELD_GOODS, cls.TAG_GOODS),
            hand_cart=cls._get_value(d, cls.FIELD_HAND_CART, cls.TAG_HAND_CART),
            hazmat=cls._get_value(d, cls.FIELD_HAZMAT, cls.TAG_HAZMAT),
            hgv=cls._get_value(d, cls.FIELD_HGV, cls.TAG_HGV),
            horse=cls._get_value(d, cls.FIELD_HORSE, cls.TAG_HORSE),
            hov=cls._get_value(d, cls.FIELD_HOV, cls.TAG_HOV),
            inline_skates=cls._get_value(d, cls.FIELD_INLINE_SKATES, cls.TAG_INLINE_SKATES),
            lhv=cls._get_value(d, cls.FIELD_LHV, cls.TAG_LHV),
            mofa=cls._get_value(d, cls.FIELD_MOFA, cls.TAG_MOFA),
            moped=cls._get_value(d, cls.FIELD_MOPED, cls.TAG_MOPED),
            motorboat=cls._get_value(d, cls.FIELD_MOTORBOAT, cls.TAG_MOTORBOAT),
            motorcar=cls._get_value(d, cls.FIELD_MOTORCAR, cls.TAG_MOTORCAR),
            motorcycle=cls._get_value(d, cls.FIELD_MOTORCYCLE, cls.TAG_MOTORCYCLE),
            motor_vehicle=cls._get_value(d, cls.FIELD_MOTOR_VEHICLE, cls.TAG_MOTOR_VEHICLE),
            psv=cls._get_value(d, cls.FIELD_PSV, cls.TAG_PSV),
            roadtrain=cls._get_value(d, cls.FIELD_ROADTRAIN, cls.TAG_ROADTRAIN),
            ski=cls._get_value(d, cls.FIELD_SKI, cls.TAG_SKI),
            speed_pedelec=cls._get_value(d, cls.FIELD_SPEED_PEDELEC, cls.TAG_SPEED_PEDELEC),
            tank=cls._get_value(d, cls.FIELD_TANK, cls.TAG_TANK),
            taxi=cls._get_value(d, cls.FIELD_TAXI, cls.TAG_TAXI),
            trailer=cls._get_value(d, cls.FIELD_TRAILER, cls.TAG_TRAILER),
            tourist_bus=cls._get_value(d, cls.FIELD_TOURIST_BUS, cls.TAG_TOURIST_BUS),
            vehicle=cls._get_value(d, cls.FIELD_VEHICLE, cls.TAG_VEHICLE),
            four_wd_only=cls._get_value(d, cls.FIELD_FOUR_WD_ONLY, cls.TAG_FOUR_WD_ONLY),
            alcohol=cls._get_value(d, cls.FIELD_ALCOHOL, cls.TAG_ALCOHOL),
            dog=cls._get_value(d, cls.FIELD_DOG, cls.TAG_DOG),
            drinking_water_legal=cls._get_value(d, cls.FIELD_DRINKING_WATER_LEGAL, cls.TAG_DRINKING_WATER_LEGAL),
            female=cls._get_value(d, cls.FIELD_FEMALE, cls.TAG_FEMALE),
            male=cls._get_value(d, cls.FIELD_MALE, cls.TAG_MALE),
            max_age=cls._get_value(d, cls.FIELD_MAX_AGE, cls.TAG_MAX_AGE),
            maxaxleload=cls._get_value(d, cls.FIELD_MAXAXLELOAD, cls.TAG_MAXAXLELOAD),
            maxheight=cls._get_value(d, cls.FIELD_MAXHEIGHT, cls.TAG_MAXHEIGHT),
            maxlength=cls._get_value(d, cls.FIELD_MAXLENGTH, cls.TAG_MAXLENGTH),
            maxspeed=cls._get_value(d, cls.FIELD_MAXSPEED, cls.TAG_MAXSPEED),
            maxstay=cls._get_value(d, cls.FIELD_MAXSTAY, cls.TAG_MAXSTAY),
            maxweight=cls._get_value(d, cls.FIELD_MAXWEIGHT, cls.TAG_MAXWEIGHT),
            maxwidth=cls._get_value(d, cls.FIELD_MAXWIDTH, cls.TAG_MAXWIDTH),
            min_age=cls._get_value(d, cls.FIELD_MIN_AGE, cls.TAG_MIN_AGE),
            minspeed=cls._get_value(d, cls.FIELD_MINSPEED, cls.TAG_MINSPEED),
            noexit=cls._get_value(d, cls.FIELD_NOEXIT, cls.TAG_NOEXIT),
            oneway=cls._get_value(d, cls.FIELD_ONEWAY, cls.TAG_ONEWAY),
            openfire=cls._get_value(d, cls.FIELD_OPENFIRE, cls.TAG_OPENFIRE),
            smoking=cls._get_value(d, cls.FIELD_SMOKING, cls.TAG_SMOKING),
            toll=cls._get_value(d, cls.FIELD_TOLL, cls.TAG_TOLL),
            traffic_sign=cls._get_value(d, cls.FIELD_TRAFFIC_SIGN, cls.TAG_TRAFFIC_SIGN),
            unisex=cls._get_value(d, cls.FIELD_UNISEX, cls.TAG_UNISEX)
        )

    def to_dict(self) -> Dict[str, Any]:
        """Serializes object to a dictionary in the format "attribute:value"."""
        return {
            self.TAG_ACCESS: self.access,
            self.TAG_AGRICULTURAL: self.agricultural,
            self.TAG_ATV: self.atv,
            self.TAG_BDOUBLE: self.bdouble,
            self.TAG_BICYCLE: self.bicycle,
            self.TAG_BOAT: self.boat,
            self.TAG_BUS: self.bus,
            self.TAG_CARRIAGE: self.carriage,
            self.TAG_CYCLE_RICKSHAW: self.cycle_rickshaw,
            self.TAG_ELECTRIC_BICYCLE: self.electric_bicycle,
            self.TAG_EMERGENCY: self.emergency,
            self.TAG_FOOT: self.foot,
            self.TAG_FORESTRY: self.forestry,
            self.TAG_GOLF_CART: self.golf_cart,
            self.TAG_GOODS: self.goods,
            self.TAG_HAND_CART: self.hand_cart,
            self.TAG_HAZMAT: self.hazmat,
            self.TAG_HGV: self.hgv,
            self.TAG_HORSE: self.horse,
            self.TAG_HOV: self.hov,
            self.TAG_INLINE_SKATES: self.inline_skates,
            self.TAG_LHV: self.lhv,
            self.TAG_MOFA: self.mofa,
            self.TAG_MOPED: self.moped,
            self.TAG_MOTORBOAT: self.motorboat,
            self.TAG_MOTORCAR: self.motorcar,
            self.TAG_MOTORCYCLE: self.motorcycle,
            self.TAG_MOTOR_VEHICLE: self.motor_vehicle,
            self.TAG_PSV: self.psv,
            self.TAG_ROADTRAIN: self.roadtrain,
            self.TAG_SKI: self.ski,
            self.TAG_SPEED_PEDELEC: self.speed_pedelec,
            self.TAG_TANK: self.tank,
            self.TAG_TAXI: self.taxi,
            self.TAG_TRAILER: self.trailer,
            self.TAG_TOURIST_BUS: self.tourist_bus,
            self.TAG_VEHICLE: self.vehicle,
            self.TAG_FOUR_WD_ONLY: self.four_wd_only,
            self.TAG_ALCOHOL: self.alcohol,
            self.TAG_DOG: self.dog,
            self.TAG_DRINKING_WATER_LEGAL: self.drinking_water_legal,
            self.TAG_FEMALE: self.female,
            self.TAG_MALE: self.male,
            self.TAG_MAX_AGE: self.max_age,
            self.TAG_MAXAXLELOAD: self.maxaxleload,
            self.TAG_MAXHEIGHT: self.maxheight,
            self.TAG_MAXLENGTH: self.maxlength,
            self.TAG_MAXSPEED: self.maxspeed,
            self.TAG_MAXSTAY: self.maxstay,
            self.TAG_MAXWEIGHT: self.maxweight,
            self.TAG_MAXWIDTH: self.maxwidth,
            self.TAG_MIN_AGE: self.min_age,
            self.TAG_MINSPEED: self.minspeed,
            self.TAG_NOEXIT: self.noexit,
            self.TAG_ONEWAY: self.oneway,
            self.TAG_OPENFIRE: self.openfire,
            self.TAG_SMOKING: self.smoking,
            self.TAG_TOLL: self.toll,
            self.TAG_TRAFFIC_SIGN: self.traffic_sign,
            self.TAG_UNISEX: self.unisex
        }

    #endregion Serialization

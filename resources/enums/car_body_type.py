from core.enums.enum_str import EnumStr


class CarBodyType(EnumStr):
    # Based on common car body styles: https://en.wikipedia.org/wiki/Car_body_style
    HATCHBACK = 'Hatchback'
    SEDAN = 'Sedan'
    WAGON = 'Kombi'
    COUPE = 'Coupe'
    CONVERTIBLE = 'Kabriolet'
    LIFTBACK = 'Liftback'
    FASTBACK = 'Fastback'
    SUV = 'SUV'
    CROSSOVER = 'Crossover'
    MINIVAN = 'Minivan / MPV'
    ROADSTER = 'Roadster'
    PICKUP = 'Pickup'
    VAN = 'Van'

    @classmethod
    def options(cls) -> tuple[dict[str, str], ...]:
        """Returns stable values with explicit translation keys for presentation."""
        return (
            {'value': cls.HATCHBACK.value, 'name_key': 'RES_ENUM_CAR_BODY_TYPE.HATCHBACK'},
            {'value': cls.SEDAN.value, 'name_key': 'RES_ENUM_CAR_BODY_TYPE.SEDAN'},
            {'value': cls.WAGON.value, 'name_key': 'RES_ENUM_CAR_BODY_TYPE.WAGON'},
            {'value': cls.COUPE.value, 'name_key': 'RES_ENUM_CAR_BODY_TYPE.COUPE'},
            {'value': cls.CONVERTIBLE.value, 'name_key': 'RES_ENUM_CAR_BODY_TYPE.CONVERTIBLE'},
            {'value': cls.LIFTBACK.value, 'name_key': 'RES_ENUM_CAR_BODY_TYPE.LIFTBACK'},
            {'value': cls.FASTBACK.value, 'name_key': 'RES_ENUM_CAR_BODY_TYPE.FASTBACK'},
            {'value': cls.SUV.value, 'name_key': 'RES_ENUM_CAR_BODY_TYPE.SUV'},
            {'value': cls.CROSSOVER.value, 'name_key': 'RES_ENUM_CAR_BODY_TYPE.CROSSOVER'},
            {'value': cls.MINIVAN.value, 'name_key': 'RES_ENUM_CAR_BODY_TYPE.MINIVAN'},
            {'value': cls.ROADSTER.value, 'name_key': 'RES_ENUM_CAR_BODY_TYPE.ROADSTER'},
            {'value': cls.PICKUP.value, 'name_key': 'RES_ENUM_CAR_BODY_TYPE.PICKUP'},
            {'value': cls.VAN.value, 'name_key': 'RES_ENUM_CAR_BODY_TYPE.VAN'}
        )

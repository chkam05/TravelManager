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

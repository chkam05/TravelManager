from core.enums.enum_str import EnumStr


class GeneratorMethod(EnumStr):
    # https://wiki.openstreetmap.org/wiki/Key:generator:method
    ANAEROBIC_DIGESTION = 'anaerobic_digestion'
    BARRAGE = 'barrage'
    COMBUSTION = 'combustion'
    FISSION = 'fission'
    FUSION = 'fusion'
    GASIFICATION = 'gasification'
    PHOTOVOLTAIC = 'photovoltaic'
    RUN_OF_THE_RIVER = 'run-of-the-river'
    STREAM = 'stream'
    THERMAL = 'thermal'
    WATER_PUMPED_STORAGE = 'water-pumped-storage'
    WATER_STORAGE = 'water-storage'
    WIND_TURBINE = 'wind_turbine'

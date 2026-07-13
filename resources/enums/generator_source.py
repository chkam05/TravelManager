from core.enums.enum_str import EnumStr


class GeneratorSource(EnumStr):
    # https://wiki.openstreetmap.org/wiki/Key:generator:source
    BATTERY = 'battery'
    BIOFUEL = 'biofuel'
    BIOGAS = 'biogas'
    BIOMASS = 'biomass'
    COAL = 'coal'
    DIESEL = 'diesel'
    ELECTRICITY = 'electricity'
    GAS = 'gas'
    HYDRO = 'hydro'
    NUCLEAR = 'nuclear'
    OIL = 'oil'
    OSMOTIC = 'osmotic'
    SOLAR = 'solar'
    TIDAL = 'tidal'
    WASTE = 'waste'
    WAVE = 'wave'
    WIND = 'wind'

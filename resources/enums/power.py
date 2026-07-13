from core.enums.enum_str import EnumStr


class Power(EnumStr):
    # https://wiki.openstreetmap.org/wiki/Key:power
    CABLE = 'cable'
    CATENARY_MAST = 'catenary_mast'
    COMPENSATOR = 'compensator'
    CONNECTION = 'connection'
    CONVERTER = 'converter'
    GENERATOR = 'generator'
    HELIOSTAT = 'heliostat'
    INSULATOR = 'insulator'
    INVERTER = 'inverter'
    LINE = 'line'
    MINOR_LINE = 'minor_line'
    PLANT = 'plant'
    POLE = 'pole'
    PORTAL = 'portal'
    SUBSTATION = 'substation'
    SWITCH = 'switch'
    SWITCHGEAR = 'switchgear'
    TERMINAL = 'terminal'
    TOWER = 'tower'
    TRANSFORMER = 'transformer'

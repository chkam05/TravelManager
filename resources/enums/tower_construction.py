from core.enums.enum_str import EnumStr


class TowerConstruction(EnumStr):
    # https://wiki.openstreetmap.org/wiki/Key:tower:construction
    DISH = 'dish'
    DOME = 'dome'
    FREESTANDING = 'freestanding'
    GUYED_LATTICE = 'guyed_lattice'
    GUYED_TUBE = 'guyed_tube'
    LATTICE = 'lattice'

from core.enums.enum_str import EnumStr


class CarDriveType(EnumStr):
    # Based on common powertrain layouts: https://en.wikipedia.org/wiki/Powertrain_layout
    FRONT_WHEEL_DRIVE = 'Przednia oś'
    REAR_WHEEL_DRIVE = 'Tylna oś'
    ALL_WHEEL_DRIVE = 'AWD'
    FOUR_WHEEL_DRIVE = '4x4'

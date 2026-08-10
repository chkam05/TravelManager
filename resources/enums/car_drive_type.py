from core.enums.enum_str import EnumStr


class CarDriveType(EnumStr):
    # Based on common powertrain layouts: https://en.wikipedia.org/wiki/Powertrain_layout
    FRONT_WHEEL_DRIVE = 'Przednia oś'
    REAR_WHEEL_DRIVE = 'Tylna oś'
    ALL_WHEEL_DRIVE = 'AWD'
    FOUR_WHEEL_DRIVE = '4x4'

    @classmethod
    def options(cls) -> tuple[dict[str, str], ...]:
        """Returns stable values with explicit translation keys for presentation."""
        return (
            {'value': cls.FRONT_WHEEL_DRIVE.value, 'name_key': 'RES_ENUM_CAR_DRIVE_TYPE.FRONT_WHEEL_DRIVE'},
            {'value': cls.REAR_WHEEL_DRIVE.value, 'name_key': 'RES_ENUM_CAR_DRIVE_TYPE.REAR_WHEEL_DRIVE'},
            {'value': cls.ALL_WHEEL_DRIVE.value, 'name_key': 'RES_ENUM_CAR_DRIVE_TYPE.ALL_WHEEL_DRIVE'},
            {'value': cls.FOUR_WHEEL_DRIVE.value, 'name_key': 'RES_ENUM_CAR_DRIVE_TYPE.FOUR_WHEEL_DRIVE'}
        )

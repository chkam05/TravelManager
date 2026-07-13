from core.enums.enum_str import EnumStr


class Alcohol(EnumStr):
    # https://wiki.openstreetmap.org/wiki/Key:alcohol
    BRING_YOUR_OWN_BOTTLE = 'bring_your_own_bottle'
    NO = 'no'
    OFF_SITE_ONLY = 'off_site_only'
    ON_SITE_ONLY = 'on_site_only'
    WINE = 'wine'
    YES = 'yes'

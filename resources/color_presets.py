from typing import ClassVar

from models.settings.color_preset import ColorPreset


class ColorPresets:
    """Defines built-in application accent color presets."""

    def __new__(cls, *args, **kwargs):
        raise TypeError(
            f'{cls.__name__} is a static utility class and cannot be instantiated.'
        )

    VALUES: ClassVar[list[ColorPreset]] = [
        ColorPreset('#FFB900', 'Gold Yellow', 'Żółtozłoty'),
        ColorPreset('#FF8C00', 'Gold', 'Złoty'),
        ColorPreset('#F7630C', 'Bright Orange', 'Jasnopomarańczowy'),
        ColorPreset('#C24D0F', 'Dark Orange', 'Ciemnopomarańczowy'),
        ColorPreset('#D53A01', 'Rusty', 'Rdzawy'),
        ColorPreset('#EF6950', 'Pale Rusty', 'Bladordzawy'),
        ColorPreset('#CF3438', 'Brick Red', 'Ceglasty'),
        ColorPreset('#F94141', 'Moderate Red', 'Umiarkowany czerwony'),
        ColorPreset('#E74856', 'Pale Red', 'Bladoczerwony'),
        ColorPreset('#E81123', 'Red', 'Czerwony'),
        ColorPreset('#EA005E', 'Light Pink', 'Jansoróżany'),
        ColorPreset('#BA004E', 'Rose', 'Różany'),
        ColorPreset('#DF0089', 'Light Plum', 'Jasnośliwkowy'),
        ColorPreset('#BA0074', 'Plum', 'Śliwkowy'),
        ColorPreset('#C239B3', 'Lightly Orchid', 'Jasnostorczykowy'),
        ColorPreset('#950084', 'Orchid', 'Storczykowy'),
        ColorPreset('#0078D7', 'Blue', 'Niebieski'),
        ColorPreset('#0063B1', 'Navy', 'Granatowy'),
        ColorPreset('#8785CE', 'Purple Shade', 'Purpurowy cień'),
        ColorPreset('#6B69D6', 'Dark Purple Shade', 'Ciemnopurpurowy cień'),
        ColorPreset('#8562B5', 'Pastel Iris', 'Pastelowy irysowy'),
        ColorPreset('#704BA4', 'Brightly Iridescent', 'Jaskrawoirysowy'),
        ColorPreset('#AD44BD', 'Light Purple Red', 'Jasnofioletowoczerwony'),
        ColorPreset('#881798', 'Purple Red', 'Fioletowoczerwony'),
        ColorPreset('#0099BC', 'Bright Blue', 'Jaskrawojasnoniebieski'),
        ColorPreset('#2D7D9A', 'Light Blue', 'Jasnoniebieski'),
        ColorPreset('#00B7C3', 'Sea Foam', 'Piana morska'),
        ColorPreset('#038387', 'Greeny', 'Zielonomodry'),
        ColorPreset('#00B294', 'Light Mint', 'Jasnomiętowy'),
        ColorPreset('#018170', 'Dark Mint', 'Ciemnomiętowy'),
        ColorPreset('#00CC6A', 'Peaty', 'Torfowy'),
        ColorPreset('#10893E', 'Bright Green', 'Jaskrawozielony'),
        ColorPreset('#746F6E', 'Gray', 'Szary'),
        ColorPreset('#5D5A58', 'Gray Brown', 'Szarobrązowy'),
        ColorPreset('#68768A', 'Steel Blue', 'Stalowoniebieski'),
        ColorPreset('#515C6B', 'Metalic Blue', 'Metalowoniebieski'),
        ColorPreset('#567C73', 'Pale Dark Green', 'Bladociemnozielony'),
        ColorPreset('#47675F', 'Dark Green', 'Ciemnozielony'),
        ColorPreset('#498205', 'Light Green', 'Jasnozielony'),
        ColorPreset('#107C10', 'Green', 'Zielony'),
        ColorPreset('#6B6B6B', 'Cloudy', 'Zachmurzenie'),
        ColorPreset('#4A4846', 'Storm', 'Burza'),
        ColorPreset('#69797E', 'Blue Gray', 'Niebieskoszary'),
        ColorPreset('#464F54', 'Dark Gray', 'Ciemnoszary'),
        ColorPreset('#637B63', 'Shaded Green', 'Cieniowany zielony'),
        ColorPreset('#525E54', 'Sage', 'Szałwiowy'),
        ColorPreset('#847545', 'Desert', 'Pustynia'),
        ColorPreset('#766B59', 'Moro', 'Moro')
    ]

    @classmethod
    def to_dict_list(cls) -> list[dict]:
        """Returns serializable preset definitions for templates and APIs."""
        return ColorPreset.to_dict_list(cls.VALUES)

from typing import ClassVar

from models.settings.color_preset import ColorPreset


class ColorPresets:
    """Defines built-in application accent color presets."""

    def __new__(cls, *args, **kwargs):
        raise TypeError(
            f'{cls.__name__} is a static utility class and cannot be instantiated.'
        )

    VALUES: ClassVar[list[ColorPreset]] = [
        ColorPreset('#FFB900', 'RES_COLOR_PRESET.GOLD_YELLOW'),
        ColorPreset('#FF8C00', 'RES_COLOR_PRESET.GOLD'),
        ColorPreset('#F7630C', 'RES_COLOR_PRESET.BRIGHT_ORANGE'),
        ColorPreset('#C24D0F', 'RES_COLOR_PRESET.DARK_ORANGE'),
        ColorPreset('#D53A01', 'RES_COLOR_PRESET.RUSTY'),
        ColorPreset('#EF6950', 'RES_COLOR_PRESET.PALE_RUSTY'),
        ColorPreset('#CF3438', 'RES_COLOR_PRESET.BRICK_RED'),
        ColorPreset('#F94141', 'RES_COLOR_PRESET.MODERATE_RED'),
        ColorPreset('#E74856', 'RES_COLOR_PRESET.PALE_RED'),
        ColorPreset('#E81123', 'RES_COLOR_PRESET.RED'),
        ColorPreset('#EA005E', 'RES_COLOR_PRESET.LIGHT_PINK'),
        ColorPreset('#BA004E', 'RES_COLOR_PRESET.ROSE'),
        ColorPreset('#DF0089', 'RES_COLOR_PRESET.LIGHT_PLUM'),
        ColorPreset('#BA0074', 'RES_COLOR_PRESET.PLUM'),
        ColorPreset('#C239B3', 'RES_COLOR_PRESET.LIGHT_ORCHID'),
        ColorPreset('#950084', 'RES_COLOR_PRESET.ORCHID'),
        ColorPreset('#0078D7', 'RES_COLOR_PRESET.BLUE'),
        ColorPreset('#0063B1', 'RES_COLOR_PRESET.NAVY'),
        ColorPreset('#8785CE', 'RES_COLOR_PRESET.PURPLE_SHADE'),
        ColorPreset('#6B69D6', 'RES_COLOR_PRESET.DARK_PURPLE_SHADE'),
        ColorPreset('#8562B5', 'RES_COLOR_PRESET.PASTEL_IRIS'),
        ColorPreset('#704BA4', 'RES_COLOR_PRESET.BRIGHT_IRIDESCENT'),
        ColorPreset('#AD44BD', 'RES_COLOR_PRESET.LIGHT_PURPLE_RED'),
        ColorPreset('#881798', 'RES_COLOR_PRESET.PURPLE_RED'),
        ColorPreset('#0099BC', 'RES_COLOR_PRESET.BRIGHT_BLUE'),
        ColorPreset('#2D7D9A', 'RES_COLOR_PRESET.LIGHT_BLUE'),
        ColorPreset('#00B7C3', 'RES_COLOR_PRESET.SEA_FOAM'),
        ColorPreset('#038387', 'RES_COLOR_PRESET.GREEN_BLUE'),
        ColorPreset('#00B294', 'RES_COLOR_PRESET.LIGHT_MINT'),
        ColorPreset('#018170', 'RES_COLOR_PRESET.DARK_MINT'),
        ColorPreset('#00CC6A', 'RES_COLOR_PRESET.PEAT'),
        ColorPreset('#10893E', 'RES_COLOR_PRESET.BRIGHT_GREEN'),
        ColorPreset('#746F6E', 'RES_COLOR_PRESET.GRAY'),
        ColorPreset('#5D5A58', 'RES_COLOR_PRESET.GRAY_BROWN'),
        ColorPreset('#68768A', 'RES_COLOR_PRESET.STEEL_BLUE'),
        ColorPreset('#515C6B', 'RES_COLOR_PRESET.METALLIC_BLUE'),
        ColorPreset('#567C73', 'RES_COLOR_PRESET.PALE_DARK_GREEN'),
        ColorPreset('#47675F', 'RES_COLOR_PRESET.DARK_GREEN'),
        ColorPreset('#498205', 'RES_COLOR_PRESET.LIGHT_GREEN'),
        ColorPreset('#107C10', 'RES_COLOR_PRESET.GREEN'),
        ColorPreset('#6B6B6B', 'RES_COLOR_PRESET.CLOUDY'),
        ColorPreset('#4A4846', 'RES_COLOR_PRESET.STORM'),
        ColorPreset('#69797E', 'RES_COLOR_PRESET.BLUE_GRAY'),
        ColorPreset('#464F54', 'RES_COLOR_PRESET.DARK_GRAY'),
        ColorPreset('#637B63', 'RES_COLOR_PRESET.SHADED_GREEN'),
        ColorPreset('#525E54', 'RES_COLOR_PRESET.SAGE'),
        ColorPreset('#847545', 'RES_COLOR_PRESET.DESERT'),
        ColorPreset('#766B59', 'RES_COLOR_PRESET.CAMOUFLAGE')
    ]

    @classmethod
    def to_dict_list(cls) -> list[dict]:
        """Returns serializable preset definitions for templates and APIs."""
        return ColorPreset.to_dict_list(cls.VALUES)

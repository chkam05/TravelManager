from core.enums.enum_str import EnumStr


class Turn(EnumStr):
    # https://wiki.openstreetmap.org/wiki/Key:turn
    LEFT = 'left'
    MERGE_TO_LEFT = 'merge_to_left'
    MERGE_TO_RIGHT = 'merge_to_right'
    NEXT_LEFT = 'next_left'
    NEXT_RIGHT = 'next_right'
    REVERSE = 'reverse'
    RIGHT = 'right'
    SHARP_LEFT = 'sharp_left'
    SHARP_RIGHT = 'sharp_right'
    SLIDE_LEFT = 'slide_left'
    SLIDE_RIGHT = 'slide_right'
    SLIGHT_LEFT = 'slight_left'
    SLIGHT_RIGHT = 'slight_right'
    THROUGH = 'through'

import re
from typing import Any, ClassVar, Dict, List

from flask import jsonify, request

from core.language_service import LanguageService


class Emojis:
    """Stores grouped emoji presets for favourite tags."""

    # https://www.emotikonyznaczenie.pl/lista-buzki-ludzie

    FIELD_SYMBOL: ClassVar[str] = 'symbol'
    FIELD_SUPPORT_COLOR: ClassVar[str] = 'support_color'
    FIELD_SUPPORT_SEX: ClassVar[str] = 'support_sex'
    GROUP_TRANSLATION_GROUP: ClassVar[str] = 'RES_EMOJI_GROUP'
    EMOJI_TRANSLATION_GROUP: ClassVar[str] = 'RES_EMOJI'

    # Group key declarations
    EMOTIONS: ClassVar[str] = 'emotions'
    HANDS: ClassVar[str] = 'hands'
    FACES: ClassVar[str] = 'faces'
    BODY_PARTS: ClassVar[str] = 'body_parts'
    ACTIVITIES_AND_POSTURES: ClassVar[str] = 'activities_and_postures'
    CLOTHING_AND_ACCESSORIES: ClassVar[str] = 'clothing_and_accessories'
    ANIMALS: ClassVar[str] = 'animals'
    NATURE_AND_PLANTS: ClassVar[str] = 'nature_and_plants'
    UNIVERSE: ClassVar[str] = 'universe'
    WEATHER: ClassVar[str] = 'weather'
    FRUITS_AND_VEGETABLES: ClassVar[str] = 'fruits_and_vegetables'
    FOOD_AND_DRINKS: ClassVar[str] = 'food_and_drinks'
    SPORT: ClassVar[str] = 'sport'
    ART_AND_CULTURE: ClassVar[str] = 'art_and_culture'
    SOUND_AND_MUSIC: ClassVar[str] = 'sound_and_music'
    TRANSPORT: ClassVar[str] = 'transport'
    TRAVEL_AND_PLACES: ClassVar[str] = 'travel_and_places'
    BUILDINGS: ClassVar[str] = 'buildings'
    ENTERTAINMENT: ClassVar[str] = 'entertainment'
    ELECTRONIC_DEVICES: ClassVar[str] = 'electronic_devices'
    CLOCKS_AND_TIME: ClassVar[str] = 'clocks_and_time'
    MONEY_AND_VALUABLES: ClassVar[str] = 'money_and_valuables'
    OBJECTS_AND_TOOLS: ClassVar[str] = 'objects_and_tools'
    SCIENCE_AND_HEALTH: ClassVar[str] = 'science_and_health'
    OFFICE_TOOLS: ClassVar[str] = 'office_tools'
    FLAGS: ClassVar[str] = 'flags'
    SYMBOLS: ClassVar[str] = 'symbols'
    AV_SYMBOLS: ClassVar[str] = 'av_symbols'
    MATHEMATICAL_SYMBOLS: ClassVar[str] = 'mathematical_symbols'
    RELIGIOUS_SYMBOLS: ClassVar[str] = 'religious_symbols'
    OTHER_SYMBOLS: ClassVar[str] = 'other_symbols'
    ZODIAC_SIGNS: ClassVar[str] = 'zodiac_signs'
    WARNING_SIGNS: ClassVar[str] = 'warning_signs'
    ARROW_SIGNS: ClassVar[str] = 'arrow_signs'
    TRANSPORT_SIGNS: ClassVar[str] = 'transport_signs'
    ALPHANUMERIC_SIGNS: ClassVar[str] = 'alphanumeric_signs'
    NUMERIC_SIGNS: ClassVar[str] = 'numeric_signs'
    PUNCTUATION_SIGNS: ClassVar[str] = 'punctuation_signs'
    GEOMETRIC_SIGNS: ClassVar[str] = 'geometric_signs'

    # Emoji declarations
    EMOJIS: ClassVar[Dict[str, Dict[str, Dict[str, Any]]]] = {
        EMOTIONS: {
            'smiling_face': {
                FIELD_SYMBOL: '😀',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'smiling_face_with_open_mouth': {
                FIELD_SYMBOL: '😃',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'smiling_face_with_open_mouth_and_smiling_eyes': {
                FIELD_SYMBOL: '😄',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'smiling_face_with_smiling_eyes': {
                FIELD_SYMBOL: '😁',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'smiling_face_with_open_mouth_and_tightly_closed_eyes': {
                FIELD_SYMBOL: '😆',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'face_holding_back_tears': {
                FIELD_SYMBOL: '🥹',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'smiling_face_with_open_mouth_and_cold_sweat': {
                FIELD_SYMBOL: '😅',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'face_with_tears_of_joy': {
                FIELD_SYMBOL: '😂',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'rolling_on_the_floor_laughing': {
                FIELD_SYMBOL: '🤣',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'smiling_face_with_tear': {
                FIELD_SYMBOL: '🥲',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'white_smiling_face': {
                FIELD_SYMBOL: '☺️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'smiling_face_with_smiling_eyes_2': {
                FIELD_SYMBOL: '😊',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'smiling_face_with_halo': {
                FIELD_SYMBOL: '😇',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'slightly_smiling_face': {
                FIELD_SYMBOL: '🙂',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'upside_down_face': {
                FIELD_SYMBOL: '🙃',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'winking_face': {
                FIELD_SYMBOL: '😉',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'relieved_face': {
                FIELD_SYMBOL: '😌',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'smiling_face_with_heart_shaped_eyes': {
                FIELD_SYMBOL: '😍',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'smiling_face_with_smiling_eyes_and_three_hearts': {
                FIELD_SYMBOL: '🥰',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'face_throwing_a_kiss': {
                FIELD_SYMBOL: '😘',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'kissing_face': {
                FIELD_SYMBOL: '😗',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'kissing_face_with_smiling_eyes': {
                FIELD_SYMBOL: '😙',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'kissing_face_with_closed_eyes': {
                FIELD_SYMBOL: '😚',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'face_savouring_delicious_food': {
                FIELD_SYMBOL: '😋',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'face_with_stuck_out_tongue': {
                FIELD_SYMBOL: '😛',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'face_with_stuck_out_tongue_and_tightly_closed_eyes': {
                FIELD_SYMBOL: '😝',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'face_with_stuck_out_tongue_and_winking_eye': {
                FIELD_SYMBOL: '😜',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'grinning_face_with_one_large_and_one_small_eye': {
                FIELD_SYMBOL: '🤪',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'face_with_one_eyebrow_raised': {
                FIELD_SYMBOL: '🤨',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'face_with_monocle': {
                FIELD_SYMBOL: '🧐',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'nerd_face': {
                FIELD_SYMBOL: '🤓',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'smiling_face_with_sunglasses': {
                FIELD_SYMBOL: '😎',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'disguised_face': {
                FIELD_SYMBOL: '🥸',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'grinning_face_with_star_eyes': {
                FIELD_SYMBOL: '🤩',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'face_with_party_horn_and_party_hat': {
                FIELD_SYMBOL: '🥳',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'slightly_smiling_face_with_up_down_arrow': {
                FIELD_SYMBOL: '🙂‍↕️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'smirking_face': {
                FIELD_SYMBOL: '😏',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'unamused_face': {
                FIELD_SYMBOL: '😒',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'slightly_smiling_face_with_left_right_arrow': {
                FIELD_SYMBOL: '🙂‍↔',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'disappointed_face': {
                FIELD_SYMBOL: '😞',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'pensive_face': {
                FIELD_SYMBOL: '😔',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'worried_face': {
                FIELD_SYMBOL: '😟',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'confused_face': {
                FIELD_SYMBOL: '😕',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'slightly_frowning_face': {
                FIELD_SYMBOL: '🙁',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'white_frowning_face': {
                FIELD_SYMBOL: '☹️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'persevering_face': {
                FIELD_SYMBOL: '😣',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'confounded_face': {
                FIELD_SYMBOL: '😖',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'tired_face': {
                FIELD_SYMBOL: '😫',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'weary_face': {
                FIELD_SYMBOL: '😩',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'face_with_pleading_eyes': {
                FIELD_SYMBOL: '🥺',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'crying_face': {
                FIELD_SYMBOL: '😢',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'loudly_crying_face': {
                FIELD_SYMBOL: '😭',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'face_with_look_of_triumph': {
                FIELD_SYMBOL: '😤',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'angry_face': {
                FIELD_SYMBOL: '😠',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'pouting_face': {
                FIELD_SYMBOL: '😡',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'serious_face_with_symbols_covering_mouth': {
                FIELD_SYMBOL: '🤬',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'shocked_face_with_exploding_head': {
                FIELD_SYMBOL: '🤯',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'flushed_face': {
                FIELD_SYMBOL: '😳',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'overheated_face': {
                FIELD_SYMBOL: '🥵',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'freezing_face': {
                FIELD_SYMBOL: '🥶',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'face_without_mouth_with_fog': {
                FIELD_SYMBOL: '😶‍🌫',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'face_screaming_in_fear': {
                FIELD_SYMBOL: '😱',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'fearful_face': {
                FIELD_SYMBOL: '😨',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'face_with_open_mouth_and_cold_sweat': {
                FIELD_SYMBOL: '😰',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'disappointed_but_relieved_face': {
                FIELD_SYMBOL: '😥',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'face_with_cold_sweat': {
                FIELD_SYMBOL: '😓',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'hugging_face': {
                FIELD_SYMBOL: '🤗',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'thinking_face': {
                FIELD_SYMBOL: '🤔',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'face_with_peeking_eye': {
                FIELD_SYMBOL: '🫣',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'smiling_face_with_smiling_eyes_and_hand_covering_mouth': {
                FIELD_SYMBOL: '🤭',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'face_with_open_eyes_and_hand_over_mouth': {
                FIELD_SYMBOL: '🫢',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'saluting_face': {
                FIELD_SYMBOL: '🫡',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'face_with_finger_covering_closed_lips': {
                FIELD_SYMBOL: '🤫',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'melting_face': {
                FIELD_SYMBOL: '🫠',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'lying_face': {
                FIELD_SYMBOL: '🤥',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'face_without_mouth': {
                FIELD_SYMBOL: '😶',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'dotted_line_face': {
                FIELD_SYMBOL: '🫥',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'neutral_face': {
                FIELD_SYMBOL: '😐',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'face_with_diagonal_mouth': {
                FIELD_SYMBOL: '🫤',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'expressionless_face': {
                FIELD_SYMBOL: '😑',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'shaking_face': {
                FIELD_SYMBOL: '🫨',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'grimacing_face': {
                FIELD_SYMBOL: '😬',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'face_with_rolling_eyes': {
                FIELD_SYMBOL: '🙄',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'hushed_face': {
                FIELD_SYMBOL: '😯',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'frowning_face_with_open_mouth': {
                FIELD_SYMBOL: '😦',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'anguished_face': {
                FIELD_SYMBOL: '😧',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'face_with_open_mouth': {
                FIELD_SYMBOL: '😮',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'astonished_face': {
                FIELD_SYMBOL: '😲',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'yawning_face': {
                FIELD_SYMBOL: '🥱',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'face_with_bags_under_eyes': {
                FIELD_SYMBOL: '🫩',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'distorted_face': {
                FIELD_SYMBOL: '🫪',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'sleeping_face': {
                FIELD_SYMBOL: '😴',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'drooling_face': {
                FIELD_SYMBOL: '🤤',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'sleepy_face': {
                FIELD_SYMBOL: '😪',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'face_with_open_mouth_with_dash_symbol': {
                FIELD_SYMBOL: '😮‍💨',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'dizzy_face': {
                FIELD_SYMBOL: '😵',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'dizzy_face_with_dizzy_symbol': {
                FIELD_SYMBOL: '😵‍💫',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'zipper_mouth_face': {
                FIELD_SYMBOL: '🤐',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'face_with_uneven_eyes_and_wavy_mouth': {
                FIELD_SYMBOL: '🥴',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'nauseated_face': {
                FIELD_SYMBOL: '🤢',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'face_with_open_mouth_vomiting': {
                FIELD_SYMBOL: '🤮',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'sneezing_face': {
                FIELD_SYMBOL: '🤧',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'face_with_medical_mask': {
                FIELD_SYMBOL: '😷',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'face_with_thermometer': {
                FIELD_SYMBOL: '🤒',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'face_with_head_bandage': {
                FIELD_SYMBOL: '🤕',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'money_mouth_face': {
                FIELD_SYMBOL: '🤑',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'face_with_cowboy_hat': {
                FIELD_SYMBOL: '🤠',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'smiling_face_with_horns': {
                FIELD_SYMBOL: '😈',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'imp': {
                FIELD_SYMBOL: '👿',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'japanese_ogre': {
                FIELD_SYMBOL: '👹',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'japanese_goblin': {
                FIELD_SYMBOL: '👺',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'clown_face': {
                FIELD_SYMBOL: '🤡',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'pile_of_poo': {
                FIELD_SYMBOL: '💩',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'ghost': {
                FIELD_SYMBOL: '👻',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'skull': {
                FIELD_SYMBOL: '💀',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'skull_and_crossbones': {
                FIELD_SYMBOL: '☠️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'extraterrestrial_alien': {
                FIELD_SYMBOL: '👽',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'alien_monster': {
                FIELD_SYMBOL: '👾',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'robot_face': {
                FIELD_SYMBOL: '🤖',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'jack_o_lantern': {
                FIELD_SYMBOL: '🎃',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'smiling_cat_face_with_open_mouth': {
                FIELD_SYMBOL: '😺',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'grinning_cat_face_with_smiling_eyes': {
                FIELD_SYMBOL: '😸',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'cat_face_with_tears_of_joy': {
                FIELD_SYMBOL: '😹',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'smiling_cat_face_with_heart_shaped_eyes': {
                FIELD_SYMBOL: '😻',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'cat_face_with_wry_smile': {
                FIELD_SYMBOL: '😼',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'kissing_cat_face_with_closed_eyes': {
                FIELD_SYMBOL: '😽',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'weary_cat_face': {
                FIELD_SYMBOL: '🙀',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'crying_cat_face': {
                FIELD_SYMBOL: '😿',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'pouting_cat_face': {
                FIELD_SYMBOL: '😾',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
        },
        HANDS: {
            'heart_hands': {
                FIELD_SYMBOL: '🫶',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: False
            },
            'palms_up_together': {
                FIELD_SYMBOL: '🤲',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: False
            },
            'open_hands_sign': {
                FIELD_SYMBOL: '👐',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: False
            },
            'person_raising_both_hands_in_celebration': {
                FIELD_SYMBOL: '🙌',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: False
            },
            'clapping_hands_sign': {
                FIELD_SYMBOL: '👏',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: False
            },
            'handshake': {
                FIELD_SYMBOL: '🤝',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'thumbs_up_sign': {
                FIELD_SYMBOL: '👍',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: False
            },
            'thumbs_down_sign': {
                FIELD_SYMBOL: '👎',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: False
            },
            'fisted_hand_sign': {
                FIELD_SYMBOL: '👊',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: False
            },
            'raised_fist': {
                FIELD_SYMBOL: '✊',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: False
            },
            'left_facing_fist': {
                FIELD_SYMBOL: '🤛',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: False
            },
            'right_facing_fist': {
                FIELD_SYMBOL: '🤜',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: False
            },
            'leftwards_pushing_hand': {
                FIELD_SYMBOL: '🫷',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: False
            },
            'rightwards_pushing_hand': {
                FIELD_SYMBOL: '🫸',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: False
            },
            'hand_with_index_and_middle_fingers_crossed': {
                FIELD_SYMBOL: '🤞',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: False
            },
            'victory_hand': {
                FIELD_SYMBOL: '✌️',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: False
            },
            'hand_with_index_finger_and_thumb_crossed': {
                FIELD_SYMBOL: '🫰',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: False
            },
            'i_love_you_hand_sign': {
                FIELD_SYMBOL: '🤟',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: False
            },
            'sign_of_the_horns': {
                FIELD_SYMBOL: '🤘',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'ok_hand_sign': {
                FIELD_SYMBOL: '👌',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: False
            },
            'pinched_fingers': {
                FIELD_SYMBOL: '🤌',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: False
            },
            'pinching_hand': {
                FIELD_SYMBOL: '🤏',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: False
            },
            'palm_down_hand': {
                FIELD_SYMBOL: '🫳',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: False
            },
            'palm_up_hand': {
                FIELD_SYMBOL: '🫴',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: False
            },
            'white_left_pointing_backhand_index': {
                FIELD_SYMBOL: '👈',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'white_right_pointing_backhand_index': {
                FIELD_SYMBOL: '👉',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'white_up_pointing_backhand_index': {
                FIELD_SYMBOL: '👆',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'white_down_pointing_backhand_index': {
                FIELD_SYMBOL: '👇',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'white_up_pointing_index': {
                FIELD_SYMBOL: '☝️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'raised_hand': {
                FIELD_SYMBOL: '✋',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: False
            },
            'raised_back_of_hand': {
                FIELD_SYMBOL: '🤚',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: False
            },
            'raised_hand_with_fingers_splayed': {
                FIELD_SYMBOL: '🖐️',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: False
            },
            'raised_hand_with_part_between_middle_and_ring_fingers': {
                FIELD_SYMBOL: '🖖',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: False
            },
            'waving_hand_sign': {
                FIELD_SYMBOL: '👋',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: False
            },
            'call_me_hand': {
                FIELD_SYMBOL: '🤙',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: False
            },
            'leftwards_hand': {
                FIELD_SYMBOL: '🫲',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: False
            },
            'rightwards_hand': {
                FIELD_SYMBOL: '🫱',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: False
            },
            'reversed_hand_with_middle_finger_extended': {
                FIELD_SYMBOL: '🖕',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: False
            },
            'writing_hand': {
                FIELD_SYMBOL: '✍️',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: False
            },
            'person_with_folded_hands': {
                FIELD_SYMBOL: '🙏',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: False
            },
            'index_pointing_at_the_viewer': {
                FIELD_SYMBOL: '🫵',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
        },
        FACES: {
            'baby': {
                FIELD_SYMBOL: '👶',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: False
            },
            'girl': {
                FIELD_SYMBOL: '👧',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: False
            },
            'child': {
                FIELD_SYMBOL: '🧒',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: False
            },
            'boy': {
                FIELD_SYMBOL: '👦',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: False
            },
            'woman': {
                FIELD_SYMBOL: '👩',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'adult': {
                FIELD_SYMBOL: '🧑',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'man': {
                FIELD_SYMBOL: '👨',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'woman_with_emoji_component_curly_hair': {
                FIELD_SYMBOL: '👩‍🦱',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'adult_with_emoji_component_curly_hair': {
                FIELD_SYMBOL: '🧑‍🦱',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'man_with_emoji_component_curly_hair': {
                FIELD_SYMBOL: '👨‍🦱',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'woman_with_emoji_component_red_hair': {
                FIELD_SYMBOL: '👩‍🦰',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'adult_with_emoji_component_red_hair': {
                FIELD_SYMBOL: '🧑‍🦰',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'man_with_emoji_component_red_hair': {
                FIELD_SYMBOL: '👨‍🦰',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'person_with_blond_hair_with_female_sign': {
                FIELD_SYMBOL: '👱‍♀',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'person_with_blond_hair': {
                FIELD_SYMBOL: '👱',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'person_with_blond_hair_with_male_sign': {
                FIELD_SYMBOL: '👱‍♂️',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'woman_with_emoji_component_white_hair': {
                FIELD_SYMBOL: '👩‍🦳',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'adult_with_emoji_component_white_hair': {
                FIELD_SYMBOL: '🧑‍🦳',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'man_with_emoji_component_white_hair': {
                FIELD_SYMBOL: '👨‍🦳',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'woman_with_emoji_component_bald': {
                FIELD_SYMBOL: '👩‍🦲',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'adult_with_emoji_component_bald': {
                FIELD_SYMBOL: '🧑‍🦲',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'man_with_emoji_component_bald': {
                FIELD_SYMBOL: '👨‍🦲',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'bearded_person_with_female_sign': {
                FIELD_SYMBOL: '🧔‍♀',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'bearded_person': {
                FIELD_SYMBOL: '🧔',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'bearded_person_with_male_sign': {
                FIELD_SYMBOL: '🧔‍♂️',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'older_woman': {
                FIELD_SYMBOL: '👵',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'older_adult': {
                FIELD_SYMBOL: '🧓',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'older_man': {
                FIELD_SYMBOL: '👴',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'man_with_gua_pi_mao': {
                FIELD_SYMBOL: '👲',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'man_with_turban_with_female_sign': {
                FIELD_SYMBOL: '👳‍♀️',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'man_with_turban': {
                FIELD_SYMBOL: '👳',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'man_with_turban_with_male_sign': {
                FIELD_SYMBOL: '👳‍♂️',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'person_with_headscarf': {
                FIELD_SYMBOL: '🧕',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'police_officer_with_female_sign': {
                FIELD_SYMBOL: '👮‍♀️',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'police_officer': {
                FIELD_SYMBOL: '👮',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'police_officer_with_male_sign': {
                FIELD_SYMBOL: '👮‍♂️',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'construction_worker_with_female_sign': {
                FIELD_SYMBOL: '👷‍♀️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: True
            },
            'construction_worker': {
                FIELD_SYMBOL: '👷',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: True
            },
            'construction_worker_with_male_sign': {
                FIELD_SYMBOL: '👷‍♂️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: True
            },
            'guardsman_with_female_sign': {
                FIELD_SYMBOL: '💂‍♀️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: True
            },
            'guardsman': {
                FIELD_SYMBOL: '💂',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'guardsman_with_male_sign': {
                FIELD_SYMBOL: '💂‍♂️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: True
            },
            'sleuth_or_spy_with_female_sign': {
                FIELD_SYMBOL: '🕵️‍♀️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: True
            },
            'sleuth_or_spy': {
                FIELD_SYMBOL: '🕵️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'sleuth_or_spy_with_male_sign': {
                FIELD_SYMBOL: '🕵️‍♂️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: True
            },
            'woman_with_staff_of_aesculapius': {
                FIELD_SYMBOL: '👩‍⚕️',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'adult_with_staff_of_aesculapius': {
                FIELD_SYMBOL: '🧑‍⚕️',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'man_with_staff_of_aesculapius': {
                FIELD_SYMBOL: '👨‍⚕️',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'woman_with_ear_of_rice': {
                FIELD_SYMBOL: '👩‍🌾',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'adult_with_ear_of_rice': {
                FIELD_SYMBOL: '🧑‍🌾',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'man_with_ear_of_rice': {
                FIELD_SYMBOL: '👨‍🌾',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'woman_with_cooking': {
                FIELD_SYMBOL: '👩‍🍳',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'adult_with_cooking': {
                FIELD_SYMBOL: '🧑‍🍳',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'man_with_cooking': {
                FIELD_SYMBOL: '👨‍🍳',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'woman_with_graduation_cap': {
                FIELD_SYMBOL: '👩‍🎓',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'adult_with_graduation_cap': {
                FIELD_SYMBOL: '🧑‍🎓',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'man_with_graduation_cap': {
                FIELD_SYMBOL: '👨‍🎓',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'woman_with_microphone': {
                FIELD_SYMBOL: '👩‍🎤',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'adult_with_microphone': {
                FIELD_SYMBOL: '🧑‍🎤',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'man_with_microphone': {
                FIELD_SYMBOL: '👨‍🎤',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'woman_with_school': {
                FIELD_SYMBOL: '👩‍🏫',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'adult_with_school': {
                FIELD_SYMBOL: '🧑‍🏫',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'man_with_school': {
                FIELD_SYMBOL: '👨‍🏫',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'woman_with_factory': {
                FIELD_SYMBOL: '👩‍🏭',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'adult_with_factory': {
                FIELD_SYMBOL: '🧑‍🏭',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'man_with_factory': {
                FIELD_SYMBOL: '👨‍🏭',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'woman_with_personal_computer': {
                FIELD_SYMBOL: '👩‍💻',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'adult_with_personal_computer': {
                FIELD_SYMBOL: '🧑‍💻',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'man_with_personal_computer': {
                FIELD_SYMBOL: '👨‍💻',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'woman_with_briefcase': {
                FIELD_SYMBOL: '👩‍💼',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'adult_with_briefcase': {
                FIELD_SYMBOL: '🧑‍💼',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'man_with_briefcase': {
                FIELD_SYMBOL: '👨‍💼',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'woman_with_wrench': {
                FIELD_SYMBOL: '👩‍🔧',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'adult_with_wrench': {
                FIELD_SYMBOL: '🧑‍🔧',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'man_with_wrench': {
                FIELD_SYMBOL: '👨‍🔧',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'woman_with_microscope': {
                FIELD_SYMBOL: '👩‍🔬',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'adult_with_microscope': {
                FIELD_SYMBOL: '🧑‍🔬',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'man_with_microscope': {
                FIELD_SYMBOL: '👨‍🔬',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'woman_with_artist_palette': {
                FIELD_SYMBOL: '👩‍🎨',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'adult_with_artist_palette': {
                FIELD_SYMBOL: '🧑‍🎨',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'man_with_artist_palette': {
                FIELD_SYMBOL: '👨‍🎨',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'woman_with_fire_engine': {
                FIELD_SYMBOL: '👩‍🚒',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'adult_with_fire_engine': {
                FIELD_SYMBOL: '🧑‍🚒',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'man_with_fire_engine': {
                FIELD_SYMBOL: '👨‍🚒',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'woman_with_airplane': {
                FIELD_SYMBOL: '👩‍✈️',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'adult_with_airplane': {
                FIELD_SYMBOL: '🧑‍✈️',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'man_with_airplane': {
                FIELD_SYMBOL: '👨‍✈️',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'woman_with_rocket': {
                FIELD_SYMBOL: '👩‍🚀',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'adult_with_rocket': {
                FIELD_SYMBOL: '🧑‍🚀',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'man_with_rocket': {
                FIELD_SYMBOL: '👨‍🚀',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'woman_with_scales': {
                FIELD_SYMBOL: '👩‍⚖️',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'adult_with_scales': {
                FIELD_SYMBOL: '🧑‍⚖️',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'man_with_scales': {
                FIELD_SYMBOL: '👨‍⚖️',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'bride_with_veil_with_female_sign': {
                FIELD_SYMBOL: '👰‍♀️',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'bride_with_veil': {
                FIELD_SYMBOL: '👰',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'bride_with_veil_with_male_sign': {
                FIELD_SYMBOL: '👰‍♂️',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'man_in_tuxedo_with_female_sign': {
                FIELD_SYMBOL: '🤵‍♀️',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'man_in_tuxedo': {
                FIELD_SYMBOL: '🤵',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'man_in_tuxedo_with_male_sign': {
                FIELD_SYMBOL: '🤵‍♂️',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'princess': {
                FIELD_SYMBOL: '👸',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'person_with_crown': {
                FIELD_SYMBOL: '🫅',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'prince': {
                FIELD_SYMBOL: '🤴',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'ninja': {
                FIELD_SYMBOL: '🥷',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'superhero_with_female_sign': {
                FIELD_SYMBOL: '🦸‍♀️',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'superhero': {
                FIELD_SYMBOL: '🦸',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'superhero_with_male_sign': {
                FIELD_SYMBOL: '🦸‍♂️',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'supervillain_with_female_sign': {
                FIELD_SYMBOL: '🦹‍♀️',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'supervillain': {
                FIELD_SYMBOL: '🦹',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'supervillain_with_male_sign': {
                FIELD_SYMBOL: '🦹‍♂️',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'mother_christmas': {
                FIELD_SYMBOL: '🤶',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'adult_with_christmas_tree': {
                FIELD_SYMBOL: '🧑‍🎄',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'father_christmas': {
                FIELD_SYMBOL: '🎅',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'mage_with_female_sign': {
                FIELD_SYMBOL: '🧙‍♀️',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'mage': {
                FIELD_SYMBOL: '🧙',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'mage_with_male_sign': {
                FIELD_SYMBOL: '🧙‍♂️',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'elf_with_female_sign': {
                FIELD_SYMBOL: '🧝‍♀️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: True
            },
            'elf': {
                FIELD_SYMBOL: '🧝',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'elf_with_male_sign': {
                FIELD_SYMBOL: '🧝‍♂️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: True
            },
            'troll': {
                FIELD_SYMBOL: '🧌',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'vampire_with_female_sign': {
                FIELD_SYMBOL: '🧛‍♀️',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'vampire': {
                FIELD_SYMBOL: '🧛',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'vampire_with_male_sign': {
                FIELD_SYMBOL: '🧛‍♂️',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'zombie_with_female_sign': {
                FIELD_SYMBOL: '🧟‍♀️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: True
            },
            'zombie': {
                FIELD_SYMBOL: '🧟',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: True
            },
            'zombie_with_male_sign': {
                FIELD_SYMBOL: '🧟‍♂️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: True
            },
            'genie_with_female_sign': {
                FIELD_SYMBOL: '🧞‍♀️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: True
            },
            'genie': {
                FIELD_SYMBOL: '🧞',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: True
            },
            'genie_with_male_sign': {
                FIELD_SYMBOL: '🧞‍♂️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: True
            },
            'merperson_with_female_sign': {
                FIELD_SYMBOL: '🧜‍♀️',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'merperson': {
                FIELD_SYMBOL: '🧜',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'merperson_with_male_sign': {
                FIELD_SYMBOL: '🧜‍♂️',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'fairy_with_female_sign': {
                FIELD_SYMBOL: '🧚‍♀️',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'fairy': {
                FIELD_SYMBOL: '🧚',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'fairy_with_male_sign': {
                FIELD_SYMBOL: '🧚‍♂️',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'baby_angel': {
                FIELD_SYMBOL: '👼',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: False
            },
            'pregnant_woman': {
                FIELD_SYMBOL: '🤰',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'pregnant_person': {
                FIELD_SYMBOL: '🫄',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'pregnant_man': {
                FIELD_SYMBOL: '🫃',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'breast_feeding': {
                FIELD_SYMBOL: '🤱',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'woman_with_baby_bottle': {
                FIELD_SYMBOL: '👩‍🍼',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'adult_with_baby_bottle': {
                FIELD_SYMBOL: '🧑‍🍼',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'man_with_baby_bottle': {
                FIELD_SYMBOL: '👨‍🍼',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'person_bowing_deeply_with_female_sign': {
                FIELD_SYMBOL: '🙇‍♀️',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'person_bowing_deeply': {
                FIELD_SYMBOL: '🙇',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'person_bowing_deeply_with_male_sign': {
                FIELD_SYMBOL: '🙇‍♂',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'information_desk_person_with_female_sign': {
                FIELD_SYMBOL: '💁‍♀️',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'information_desk_person': {
                FIELD_SYMBOL: '💁',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'information_desk_person_with_male_sign': {
                FIELD_SYMBOL: '💁‍♂',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'face_with_no_good_gesture_with_female_sign': {
                FIELD_SYMBOL: '🙅‍♀',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: True
            },
            'face_with_no_good_gesture': {
                FIELD_SYMBOL: '🙅',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'face_with_no_good_gesture_with_male_sign': {
                FIELD_SYMBOL: '🙅‍♂',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: True
            },
            'face_with_ok_gesture_with_female_sign': {
                FIELD_SYMBOL: '🙆‍♀',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: True
            },
            'face_with_ok_gesture': {
                FIELD_SYMBOL: '🙆',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'face_with_ok_gesture_with_male_sign': {
                FIELD_SYMBOL: '🙆‍♂️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: True
            },
            'happy_person_raising_one_hand_with_female_sign': {
                FIELD_SYMBOL: '🙋‍♀️',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'happy_person_raising_one_hand': {
                FIELD_SYMBOL: '🙋',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'happy_person_raising_one_hand_2': {
                FIELD_SYMBOL: '🙋‍️',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'deaf_person_with_female_sign': {
                FIELD_SYMBOL: '🧏‍♀️',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'deaf_person': {
                FIELD_SYMBOL: '🧏',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'deaf_person_with_male_sign': {
                FIELD_SYMBOL: '🧏‍♂️',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'face_palm_with_female_sign': {
                FIELD_SYMBOL: '🤦‍♀️',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'face_palm': {
                FIELD_SYMBOL: '🤦',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: False
            },
            'face_palm_with_male_sign': {
                FIELD_SYMBOL: '🤦‍♂️',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'shrug_with_female_sign': {
                FIELD_SYMBOL: '🤷‍♀️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: True
            },
            'shrug': {
                FIELD_SYMBOL: '🤷',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'shrug_2': {
                FIELD_SYMBOL: '🤷🏻‍️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'person_with_pouting_face_with_female_sign': {
                FIELD_SYMBOL: '🙎‍♀️',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'person_with_pouting_face': {
                FIELD_SYMBOL: '🙎',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'person_with_pouting_face_with_male_sign': {
                FIELD_SYMBOL: '🙎‍♂️',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'person_frowning_with_female_sign': {
                FIELD_SYMBOL: '🙍‍♀️',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'person_frowning': {
                FIELD_SYMBOL: '🙍',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'person_frowning_with_male_sign': {
                FIELD_SYMBOL: '🙍‍♂️',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'haircut_with_female_sign': {
                FIELD_SYMBOL: '💇‍♀️',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'haircut': {
                FIELD_SYMBOL: '💇',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'haircut_with_male_sign': {
                FIELD_SYMBOL: '💇‍♂️',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'face_massage_with_female_sign': {
                FIELD_SYMBOL: '💆‍♀️',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'face_massage': {
                FIELD_SYMBOL: '💆',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'face_massage_with_male_sign': {
                FIELD_SYMBOL: '💆‍♂️',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'person_in_steamy_room_with_female_sign': {
                FIELD_SYMBOL: '🧖‍♀️',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'person_in_steamy_room': {
                FIELD_SYMBOL: '🧖',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'person_in_steamy_room_with_male_sign': {
                FIELD_SYMBOL: '🧖‍♂️',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'woman_with_heavy_black_heart_with_man': {
                FIELD_SYMBOL: '👩‍❤️‍👨',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'woman_with_heavy_black_heart_with_woman': {
                FIELD_SYMBOL: '👩‍❤️‍👩',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'adult_with_heavy_black_heart_with_adult': {
                FIELD_SYMBOL: '🧑‍❤️‍🧑',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'man_with_heavy_black_heart_with_man': {
                FIELD_SYMBOL: '👨‍❤️‍👨',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'woman_with_heavy_black_heart_with_kiss_mark_with_man': {
                FIELD_SYMBOL: '👩‍❤️‍💋‍👨',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'woman_with_heavy_black_heart_with_kiss_mark_with_woman': {
                FIELD_SYMBOL: '👩‍❤️‍💋‍👩',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'adult_with_heavy_black_heart_with_kiss_mark_with_adult': {
                FIELD_SYMBOL: '🧑‍❤️‍💋‍🧑',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'man_with_heavy_black_heart_with_kiss_mark_with_man': {
                FIELD_SYMBOL: '👨‍❤️‍💋‍👨',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
        },
        BODY_PARTS: {
            'flexed_biceps': {
                FIELD_SYMBOL: '💪',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: False
            },
            'mechanical_arm': {
                FIELD_SYMBOL: '🦾',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'foot': {
                FIELD_SYMBOL: '🦶',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: False
            },
            'leg': {
                FIELD_SYMBOL: '🦵',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: False
            },
            'mechanical_leg': {
                FIELD_SYMBOL: '🦿',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: False
            },
            'kiss_mark': {
                FIELD_SYMBOL: '💋',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'mouth': {
                FIELD_SYMBOL: '👄',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'biting_lip': {
                FIELD_SYMBOL: '🫦',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'tooth': {
                FIELD_SYMBOL: '🦷',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'tongue': {
                FIELD_SYMBOL: '👅',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'ear': {
                FIELD_SYMBOL: '👂',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: False
            },
            'ear_with_hearing_aid': {
                FIELD_SYMBOL: '🦻',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: False
            },
            'nose': {
                FIELD_SYMBOL: '👃',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: False
            },
            'eye': {
                FIELD_SYMBOL: '👁',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'eyes': {
                FIELD_SYMBOL: '️👀',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'anatomical_heart': {
                FIELD_SYMBOL: '🫀',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'lungs': {
                FIELD_SYMBOL: '🫁',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'brain': {
                FIELD_SYMBOL: '🧠',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
        },
        ACTIVITIES_AND_POSTURES: {
            'dancer': {
                FIELD_SYMBOL: '💃',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'man_dancing': {
                FIELD_SYMBOL: '🕺',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'adult_with_ballet_shoes': {
                FIELD_SYMBOL: '🧑‍🩰',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'woman_with_bunny_ears_with_female_sign': {
                FIELD_SYMBOL: '👯‍♀️',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'woman_with_bunny_ears': {
                FIELD_SYMBOL: '👯',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'woman_with_bunny_ears_with_male_sign': {
                FIELD_SYMBOL: '👯‍♂️',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'man_in_business_suit_levitating': {
                FIELD_SYMBOL: '🕴️',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'woman_with_manual_wheelchair': {
                FIELD_SYMBOL: '👩‍🦽',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'adult_with_manual_wheelchair': {
                FIELD_SYMBOL: '🧑‍🦽',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'man_with_manual_wheelchair': {
                FIELD_SYMBOL: '👨‍🦽',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'woman_with_manual_wheelchair_with_black_rightwards_arrow': {
                FIELD_SYMBOL: '👩‍🦽‍➡️',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'adult_with_manual_wheelchair_with_black_rightwards_arrow': {
                FIELD_SYMBOL: '🧑‍🦽‍➡️',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'man_with_manual_wheelchair_with_black_rightwards_arrow': {
                FIELD_SYMBOL: '👨‍🦽‍➡️',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'woman_with_motorized_wheelchair': {
                FIELD_SYMBOL: '👩‍🦼',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'adult_with_motorized_wheelchair': {
                FIELD_SYMBOL: '🧑‍🦼',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'man_with_motorized_wheelchair': {
                FIELD_SYMBOL: '👨‍🦼',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'woman_with_motorized_wheelchair_with_black_rightwards_arrow': {
                FIELD_SYMBOL: '👩‍🦼‍➡️',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'adult_with_motorized_wheelchair_with_black_rightwards_arrow': {
                FIELD_SYMBOL: '🧑‍🦼‍➡️',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'man_with_motorized_wheelchair_with_black_rightwards_arrow': {
                FIELD_SYMBOL: '👨‍🦼‍➡️',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'pedestrian_with_female_sign': {
                FIELD_SYMBOL: '🚶‍♀️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: True
            },
            'pedestrian': {
                FIELD_SYMBOL: '🚶',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'pedestrian_with_male_sign': {
                FIELD_SYMBOL: '🚶‍♂️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: True
            },
            'pedestrian_with_female_sign_with_black_rightwards_arrow': {
                FIELD_SYMBOL: '🚶‍♀️‍➡️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: True
            },
            'pedestrian_with_black_rightwards_arrow': {
                FIELD_SYMBOL: '🚶‍➡️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'pedestrian_with_male_sign_with_black_rightwards_arrow': {
                FIELD_SYMBOL: '🚶‍♂️‍➡️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: True
            },
            'woman_with_probing_cane': {
                FIELD_SYMBOL: '👩‍🦯',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'adult_with_probing_cane': {
                FIELD_SYMBOL: '🧑‍🦯',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'man_with_probing_cane': {
                FIELD_SYMBOL: '👨‍🦯',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'woman_with_probing_cane_with_black_rightwards_arrow': {
                FIELD_SYMBOL: '👩‍🦯‍➡️',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'adult_with_probing_cane_with_black_rightwards_arrow': {
                FIELD_SYMBOL: '🧑‍🦯‍➡️',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'man_with_probing_cane_with_black_rightwards_arrow': {
                FIELD_SYMBOL: '👨‍🦯‍➡️',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'kneeling_person_with_female_sign': {
                FIELD_SYMBOL: '🧎‍♀️',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'kneeling_person': {
                FIELD_SYMBOL: '🧎',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'kneeling_person_with_male_sign': {
                FIELD_SYMBOL: '🧎‍♂️',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'runner_with_female_sign': {
                FIELD_SYMBOL: '🏃‍♀️',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'runner': {
                FIELD_SYMBOL: '🏃',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'runner_with_male_sign': {
                FIELD_SYMBOL: '🏃‍♂️',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'runner_with_female_sign_with_black_rightwards_arrow': {
                FIELD_SYMBOL: '🏃‍♀️‍➡️',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'runner_with_black_rightwards_arrow': {
                FIELD_SYMBOL: '🏃‍➡️',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'runner_with_male_sign_with_black_rightwards_arrow': {
                FIELD_SYMBOL: '🏃‍♂️‍➡️',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'kneeling_person_with_female_sign_with_black_rightwards_arrow': {
                FIELD_SYMBOL: '🧎‍♀️‍➡️',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'kneeling_person_with_black_rightwards_arrow': {
                FIELD_SYMBOL: '🧎‍➡️',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'kneeling_person_with_male_sign_with_black_rightwards_arrow': {
                FIELD_SYMBOL: '🧎‍♂️‍➡️',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'standing_person_with_female_sign': {
                FIELD_SYMBOL: '🧍‍♀️',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'standing_person': {
                FIELD_SYMBOL: '🧍',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'standing_person_with_male_sign': {
                FIELD_SYMBOL: '🧍‍♂️',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'man_and_woman_holding_hands': {
                FIELD_SYMBOL: '👫',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'two_women_holding_hands': {
                FIELD_SYMBOL: '👭',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: False
            },
            'two_men_holding_hands': {
                FIELD_SYMBOL: '👬',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: False
            },
            'skier': {
                FIELD_SYMBOL: '⛷️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'snowboarder': {
                FIELD_SYMBOL: '🏂',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'parachute': {
                FIELD_SYMBOL: '🪂',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'weight_lifter_with_female_sign': {
                FIELD_SYMBOL: '🏋️‍♀️',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'weight_lifter': {
                FIELD_SYMBOL: '🏋️',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: False
            },
            'weight_lifter_with_male_sign': {
                FIELD_SYMBOL: '🏋️‍♂️',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'wrestlers_with_female_sign': {
                FIELD_SYMBOL: '🤼‍♀️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: True
            },
            'wrestlers': {
                FIELD_SYMBOL: '🤼',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: True
            },
            'wrestlers_with_male_sign': {
                FIELD_SYMBOL: '🤼‍♂️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: True
            },
            'person_doing_cartwheel_with_female_sign': {
                FIELD_SYMBOL: '🤸‍♀️',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'person_doing_cartwheel': {
                FIELD_SYMBOL: '🤸',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'person_doing_cartwheel_with_male_sign': {
                FIELD_SYMBOL: '🤸‍♂️',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'person_with_ball_with_female_sign': {
                FIELD_SYMBOL: '⛹️‍♀️',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'person_with_ball': {
                FIELD_SYMBOL: '⛹️',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'person_with_ball_with_male_sign': {
                FIELD_SYMBOL: '⛹️‍♂️',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'fencer': {
                FIELD_SYMBOL: '🤺',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'handball_with_female_sign': {
                FIELD_SYMBOL: '🤾‍♀️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: True
            },
            'handball': {
                FIELD_SYMBOL: '🤾',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: True
            },
            'handball_with_male_sign': {
                FIELD_SYMBOL: '🤾‍♂️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: True
            },
            'golfer_with_female_sign': {
                FIELD_SYMBOL: '🏌️‍♀️',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'golfer': {
                FIELD_SYMBOL: '🏌️',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'golfer_with_male_sign': {
                FIELD_SYMBOL: '🏌️‍♂️',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'horse_racing': {
                FIELD_SYMBOL: '🏇',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'person_in_lotus_position_with_female_sign': {
                FIELD_SYMBOL: '🧘‍♀️',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'person_in_lotus_position': {
                FIELD_SYMBOL: '🧘',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'person_in_lotus_position_with_male_sign': {
                FIELD_SYMBOL: '🧘‍♂️',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'surfer_with_female_sign': {
                FIELD_SYMBOL: '🏄‍♀️',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'surfer': {
                FIELD_SYMBOL: '🏄',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'surfer_with_male_sign': {
                FIELD_SYMBOL: '🏄‍♂️',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'swimmer_with_female_sign': {
                FIELD_SYMBOL: '🏊‍♀️',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'swimmer': {
                FIELD_SYMBOL: '🏊',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'swimmer_with_male_sign': {
                FIELD_SYMBOL: '🏊‍♂️',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'water_polo_with_female_sign': {
                FIELD_SYMBOL: '🤽‍♀️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: True
            },
            'water_polo': {
                FIELD_SYMBOL: '🤽',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'water_polo_with_male_sign': {
                FIELD_SYMBOL: '🤽‍♂️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: True
            },
            'rowboat_with_female_sign': {
                FIELD_SYMBOL: '🚣‍♀️',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'rowboat': {
                FIELD_SYMBOL: '🚣',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'rowboat_with_male_sign': {
                FIELD_SYMBOL: '🚣‍♂️',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'person_climbing_with_female_sign': {
                FIELD_SYMBOL: '🧗‍♀️',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'person_climbing': {
                FIELD_SYMBOL: '🧗',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'person_climbing_with_male_sign': {
                FIELD_SYMBOL: '🧗‍♂️',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'mountain_bicyclist_with_female_sign': {
                FIELD_SYMBOL: '🚵‍♀️',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'mountain_bicyclist': {
                FIELD_SYMBOL: '🚵',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'mountain_bicyclist_with_male_sign': {
                FIELD_SYMBOL: '🚵‍♂️',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'bicyclist_with_female_sign': {
                FIELD_SYMBOL: '🚴‍♀️',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'bicyclist': {
                FIELD_SYMBOL: '🚴',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'bicyclist_with_male_sign': {
                FIELD_SYMBOL: '🚴‍♂️',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'juggling_with_female_sign': {
                FIELD_SYMBOL: '🤹‍♀️',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'juggling': {
                FIELD_SYMBOL: '🤹',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'juggling_with_male_sign': {
                FIELD_SYMBOL: '🤹‍♂️',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'speaking_head_in_silhouette': {
                FIELD_SYMBOL: '🗣️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'bust_in_silhouette': {
                FIELD_SYMBOL: '👤',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'busts_in_silhouette': {
                FIELD_SYMBOL: '👥',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'people_hugging': {
                FIELD_SYMBOL: '🫂',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
        },
        CLOTHING_AND_ACCESSORIES: {
            'lipstick': {
                FIELD_SYMBOL: '💄',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'nail_polish': {
                FIELD_SYMBOL: '💅',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'selfie': {
                FIELD_SYMBOL: '🤳',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'knot': {
                FIELD_SYMBOL: '🪢',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'ball_of_yarn': {
                FIELD_SYMBOL: '🧶',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'spool_of_thread': {
                FIELD_SYMBOL: '🧵',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'sewing_needle': {
                FIELD_SYMBOL: '🪡',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'coat': {
                FIELD_SYMBOL: '🧥',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'lab_coat': {
                FIELD_SYMBOL: '🥼',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'safety_vest': {
                FIELD_SYMBOL: '🦺',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'womans_clothes': {
                FIELD_SYMBOL: '👚',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            't_shirt': {
                FIELD_SYMBOL: '👕',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'jeans': {
                FIELD_SYMBOL: '👖',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'briefs': {
                FIELD_SYMBOL: '🩲',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'shorts': {
                FIELD_SYMBOL: '🩳',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'necktie': {
                FIELD_SYMBOL: '👔',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'dress': {
                FIELD_SYMBOL: '👗',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'bikini': {
                FIELD_SYMBOL: '👙',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'one_piece_swimsuit': {
                FIELD_SYMBOL: '🩱',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'kimono': {
                FIELD_SYMBOL: '👘',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'sari': {
                FIELD_SYMBOL: '🥻',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'thong_sandal': {
                FIELD_SYMBOL: '🩴',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'flat_shoe': {
                FIELD_SYMBOL: '🥿',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'high_heeled_shoe': {
                FIELD_SYMBOL: '👠',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'womans_sandal': {
                FIELD_SYMBOL: '👡',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'womans_boots': {
                FIELD_SYMBOL: '👢',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'mans_shoe': {
                FIELD_SYMBOL: '👞',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'athletic_shoe': {
                FIELD_SYMBOL: '👟',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'hiking_boot': {
                FIELD_SYMBOL: '🥾',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'socks': {
                FIELD_SYMBOL: '🧦',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'gloves': {
                FIELD_SYMBOL: '🧤',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'scarf': {
                FIELD_SYMBOL: '🧣',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'top_hat': {
                FIELD_SYMBOL: '🎩',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'billed_cap': {
                FIELD_SYMBOL: '🧢',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'womans_hat': {
                FIELD_SYMBOL: '👒',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'graduation_cap': {
                FIELD_SYMBOL: '🎓',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'helmet_with_white_cross': {
                FIELD_SYMBOL: '⛑️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'military_helmet': {
                FIELD_SYMBOL: '🪖',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'crown': {
                FIELD_SYMBOL: '👑',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'ring': {
                FIELD_SYMBOL: '💍',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'pouch': {
                FIELD_SYMBOL: '👝',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'purse': {
                FIELD_SYMBOL: '👛',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'handbag': {
                FIELD_SYMBOL: '👜',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'briefcase': {
                FIELD_SYMBOL: '💼',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'school_satchel': {
                FIELD_SYMBOL: '🎒',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'luggage': {
                FIELD_SYMBOL: '🧳',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'eyeglasses': {
                FIELD_SYMBOL: '👓',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'dark_sunglasses': {
                FIELD_SYMBOL: '🕶️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'goggles': {
                FIELD_SYMBOL: '🥽',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'closed_umbrella': {
                FIELD_SYMBOL: '🌂',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'probing_cane': {
                FIELD_SYMBOL: '🦯',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'manual_wheelchair': {
                FIELD_SYMBOL: '🦽',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'motorized_wheelchair': {
                FIELD_SYMBOL: '🦼',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'crutch': {
                FIELD_SYMBOL: '🩼',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
        },
        ANIMALS: {
            'dog_face': {
                FIELD_SYMBOL: '🐶',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'cat_face': {
                FIELD_SYMBOL: '🐱',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'mouse_face': {
                FIELD_SYMBOL: '🐭',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'hamster_face': {
                FIELD_SYMBOL: '🐹',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'rabbit_face': {
                FIELD_SYMBOL: '🐰',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'fox_face': {
                FIELD_SYMBOL: '🦊',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'bear_face': {
                FIELD_SYMBOL: '🐻',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'panda_face': {
                FIELD_SYMBOL: '🐼',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'bear_face_with_snowflake': {
                FIELD_SYMBOL: '🐻‍❄️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'koala': {
                FIELD_SYMBOL: '🐨',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'tiger_face': {
                FIELD_SYMBOL: '🐯',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'lion_face': {
                FIELD_SYMBOL: '🦁',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'cow_face': {
                FIELD_SYMBOL: '🐮',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'pig_face': {
                FIELD_SYMBOL: '🐷',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'pig_nose': {
                FIELD_SYMBOL: '🐽',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'frog_face': {
                FIELD_SYMBOL: '🐸',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'monkey_face': {
                FIELD_SYMBOL: '🐵',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'see_no_evil_monkey': {
                FIELD_SYMBOL: '🙈',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'hear_no_evil_monkey': {
                FIELD_SYMBOL: '🙉',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'speak_no_evil_monkey': {
                FIELD_SYMBOL: '🙊',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'monkey': {
                FIELD_SYMBOL: '🐒',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'chicken': {
                FIELD_SYMBOL: '🐔',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'penguin': {
                FIELD_SYMBOL: '🐧',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'bird': {
                FIELD_SYMBOL: '🐦',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'baby_chick': {
                FIELD_SYMBOL: '🐤',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'hatching_chick': {
                FIELD_SYMBOL: '🐣',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'front_facing_baby_chick': {
                FIELD_SYMBOL: '🐥',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'goose': {
                FIELD_SYMBOL: '🪿',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'duck': {
                FIELD_SYMBOL: '🦆',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'bird_with_black_large_square': {
                FIELD_SYMBOL: '🐦‍⬛',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'eagle': {
                FIELD_SYMBOL: '🦅',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'owl': {
                FIELD_SYMBOL: '🦉',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'bat': {
                FIELD_SYMBOL: '🦇',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'wolf_face': {
                FIELD_SYMBOL: '🐺',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'boar': {
                FIELD_SYMBOL: '🐗',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'horse_face': {
                FIELD_SYMBOL: '🐴',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'unicorn_face': {
                FIELD_SYMBOL: '🦄',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'moose': {
                FIELD_SYMBOL: '🫎',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'honeybee': {
                FIELD_SYMBOL: '🐝',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'worm': {
                FIELD_SYMBOL: '🪱',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'bug': {
                FIELD_SYMBOL: '🐛',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'butterfly': {
                FIELD_SYMBOL: '🦋',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'snail': {
                FIELD_SYMBOL: '🐌',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'lady_beetle': {
                FIELD_SYMBOL: '🐞',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'ant': {
                FIELD_SYMBOL: '🐜',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'fly': {
                FIELD_SYMBOL: '🪰',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'beetle': {
                FIELD_SYMBOL: '🪲',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'cockroach': {
                FIELD_SYMBOL: '🪳',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'mosquito': {
                FIELD_SYMBOL: '🦟',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'cricket': {
                FIELD_SYMBOL: '🦗',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'spider': {
                FIELD_SYMBOL: '🕷️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'spider_web': {
                FIELD_SYMBOL: '🕸️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'scorpion': {
                FIELD_SYMBOL: '🦂',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'turtle': {
                FIELD_SYMBOL: '🐢',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'snake': {
                FIELD_SYMBOL: '🐍',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'lizard': {
                FIELD_SYMBOL: '🦎',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            't_rex': {
                FIELD_SYMBOL: '🦖',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'sauropod': {
                FIELD_SYMBOL: '🦕',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'octopus': {
                FIELD_SYMBOL: '🐙',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'squid': {
                FIELD_SYMBOL: '🦑',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'jellyfish': {
                FIELD_SYMBOL: '🪼',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'shrimp': {
                FIELD_SYMBOL: '🦐',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'lobster': {
                FIELD_SYMBOL: '🦞',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'crab': {
                FIELD_SYMBOL: '🦀',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'blowfish': {
                FIELD_SYMBOL: '🐡',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'tropical_fish': {
                FIELD_SYMBOL: '🐠',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'fish': {
                FIELD_SYMBOL: '🐟',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'dolphin': {
                FIELD_SYMBOL: '🐬',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'spouting_whale': {
                FIELD_SYMBOL: '🐳',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'whale': {
                FIELD_SYMBOL: '🐋',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'orca': {
                FIELD_SYMBOL: '🫍',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'shark': {
                FIELD_SYMBOL: '🦈',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'seal': {
                FIELD_SYMBOL: '🦭',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'crocodile': {
                FIELD_SYMBOL: '🐊',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'tiger': {
                FIELD_SYMBOL: '🐅',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'leopard': {
                FIELD_SYMBOL: '🐆',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'zebra_face': {
                FIELD_SYMBOL: '🦓',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'gorilla': {
                FIELD_SYMBOL: '🦍',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'orangutan': {
                FIELD_SYMBOL: '🦧',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'bigfoot': {
                FIELD_SYMBOL: '🫈',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'mammoth': {
                FIELD_SYMBOL: '🦣',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'elephant': {
                FIELD_SYMBOL: '🐘',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'hippopotamus': {
                FIELD_SYMBOL: '🦛',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'rhinoceros': {
                FIELD_SYMBOL: '🦏',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'dromedary_camel': {
                FIELD_SYMBOL: '🐪',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'bactrian_camel': {
                FIELD_SYMBOL: '🐫',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'giraffe_face': {
                FIELD_SYMBOL: '🦒',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'kangaroo': {
                FIELD_SYMBOL: '🦘',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'bison': {
                FIELD_SYMBOL: '🦬',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'water_buffalo': {
                FIELD_SYMBOL: '🐃',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'ox': {
                FIELD_SYMBOL: '🐂',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'cow': {
                FIELD_SYMBOL: '🐄',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'donkey': {
                FIELD_SYMBOL: '🫏',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'horse': {
                FIELD_SYMBOL: '🐎',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'pig': {
                FIELD_SYMBOL: '🐖',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'ram': {
                FIELD_SYMBOL: '🐏',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'sheep': {
                FIELD_SYMBOL: '🐑',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'llama': {
                FIELD_SYMBOL: '🦙',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'goat': {
                FIELD_SYMBOL: '🐐',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'deer': {
                FIELD_SYMBOL: '🦌',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'dog': {
                FIELD_SYMBOL: '🐕',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'poodle': {
                FIELD_SYMBOL: '🐩',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'guide_dog': {
                FIELD_SYMBOL: '🦮',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'dog_with_safety_vest': {
                FIELD_SYMBOL: '🐕‍🦺',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'cat': {
                FIELD_SYMBOL: '🐈',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'cat_with_black_large_square': {
                FIELD_SYMBOL: '🐈‍⬛',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'feather': {
                FIELD_SYMBOL: '🪶',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'wing': {
                FIELD_SYMBOL: '🪽',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'rooster': {
                FIELD_SYMBOL: '🐓',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'turkey': {
                FIELD_SYMBOL: '🦃',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'dodo': {
                FIELD_SYMBOL: '🦤',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'peacock': {
                FIELD_SYMBOL: '🦚',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'parrot': {
                FIELD_SYMBOL: '🦜',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'swan': {
                FIELD_SYMBOL: '🦢',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'flamingo': {
                FIELD_SYMBOL: '🦩',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'dove_of_peace': {
                FIELD_SYMBOL: '🕊️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'rabbit': {
                FIELD_SYMBOL: '🐇',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'raccoon': {
                FIELD_SYMBOL: '🦝',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'skunk': {
                FIELD_SYMBOL: '🦨',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'badger': {
                FIELD_SYMBOL: '🦡',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'beaver': {
                FIELD_SYMBOL: '🦫',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'otter': {
                FIELD_SYMBOL: '🦦',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'sloth': {
                FIELD_SYMBOL: '🦥',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'mouse': {
                FIELD_SYMBOL: '🐁',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'rat': {
                FIELD_SYMBOL: '🐀',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'chipmunk': {
                FIELD_SYMBOL: '🐿️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'hedgehog': {
                FIELD_SYMBOL: '🦔',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'paw_prints': {
                FIELD_SYMBOL: '🐾',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'dragon': {
                FIELD_SYMBOL: '🐉',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'dragon_face': {
                FIELD_SYMBOL: '🐲',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'bird_with_fire': {
                FIELD_SYMBOL: '🐦‍🔥',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'nest_with_eggs': {
                FIELD_SYMBOL: '🪺',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'empty_nest': {
                FIELD_SYMBOL: '🪹',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'spiral_shell': {
                FIELD_SYMBOL: '🐚',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
        },
        NATURE_AND_PLANTS: {
            'cactus': {
                FIELD_SYMBOL: '🌵',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'christmas_tree': {
                FIELD_SYMBOL: '🎄',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'evergreen_tree': {
                FIELD_SYMBOL: '🌲',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'deciduous_tree': {
                FIELD_SYMBOL: '🌳',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'palm_tree': {
                FIELD_SYMBOL: '🌴',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'leafless_tree': {
                FIELD_SYMBOL: '🪾',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'wood': {
                FIELD_SYMBOL: '🪵',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'seedling': {
                FIELD_SYMBOL: '🌱',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'herb': {
                FIELD_SYMBOL: '🌿',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'shamrock': {
                FIELD_SYMBOL: '☘️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'four_leaf_clover': {
                FIELD_SYMBOL: '🍀',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'pine_decoration': {
                FIELD_SYMBOL: '🎍',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'potted_plant': {
                FIELD_SYMBOL: '🪴',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'tanabata_tree': {
                FIELD_SYMBOL: '🎋',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'leaf_fluttering_in_wind': {
                FIELD_SYMBOL: '🍃',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'fallen_leaf': {
                FIELD_SYMBOL: '🍂',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'maple_leaf': {
                FIELD_SYMBOL: '🍁',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'mushroom': {
                FIELD_SYMBOL: '🍄',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'mushroom_with_large_brown_square': {
                FIELD_SYMBOL: '🍄‍🟫',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'coral': {
                FIELD_SYMBOL: '🪸',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'rock': {
                FIELD_SYMBOL: '🪨',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'landslide': {
                FIELD_SYMBOL: '🛘',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'ear_of_rice': {
                FIELD_SYMBOL: '🌾',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'bouquet': {
                FIELD_SYMBOL: '💐',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'tulip': {
                FIELD_SYMBOL: '🌷',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'rose': {
                FIELD_SYMBOL: '🌹',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'wilted_flower': {
                FIELD_SYMBOL: '🥀',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'hyacinth': {
                FIELD_SYMBOL: '🪻',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'lotus': {
                FIELD_SYMBOL: '🪷',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'hibiscus': {
                FIELD_SYMBOL: '🌺',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'cherry_blossom': {
                FIELD_SYMBOL: '🌸',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'blossom': {
                FIELD_SYMBOL: '🌼',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'sunflower': {
                FIELD_SYMBOL: '🌻',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'high_voltage_sign': {
                FIELD_SYMBOL: '⚡️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'fire': {
                FIELD_SYMBOL: '🔥',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'fight_cloud': {
                FIELD_SYMBOL: '🫯',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'water_wave': {
                FIELD_SYMBOL: '🌊',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'bubbles': {
                FIELD_SYMBOL: '🫧',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
        },
        UNIVERSE: {
            'sun_with_face': {
                FIELD_SYMBOL: '🌞',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'full_moon_with_face': {
                FIELD_SYMBOL: '🌝',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'first_quarter_moon_with_face': {
                FIELD_SYMBOL: '🌛',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'last_quarter_moon_with_face': {
                FIELD_SYMBOL: '🌜',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'new_moon_with_face': {
                FIELD_SYMBOL: '🌚',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'full_moon_symbol': {
                FIELD_SYMBOL: '🌕',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'waning_gibbous_moon_symbol': {
                FIELD_SYMBOL: '🌖',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'last_quarter_moon_symbol': {
                FIELD_SYMBOL: '🌗',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'waning_crescent_moon_symbol': {
                FIELD_SYMBOL: '🌘',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'new_moon_symbol': {
                FIELD_SYMBOL: '🌑',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'waxing_crescent_moon_symbol': {
                FIELD_SYMBOL: '🌒',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'first_quarter_moon_symbol': {
                FIELD_SYMBOL: '🌓',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'waxing_gibbous_moon_symbol': {
                FIELD_SYMBOL: '🌔',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'crescent_moon': {
                FIELD_SYMBOL: '🌙',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'earth_globe_americas': {
                FIELD_SYMBOL: '🌎',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'earth_globe_europe_africa': {
                FIELD_SYMBOL: '🌍',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'earth_globe_asia_australia': {
                FIELD_SYMBOL: '🌏',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'ringed_planet': {
                FIELD_SYMBOL: '🪐',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'dizzy_symbol': {
                FIELD_SYMBOL: '💫',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'white_medium_star': {
                FIELD_SYMBOL: '⭐️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'glowing_star': {
                FIELD_SYMBOL: '🌟',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'sparkles': {
                FIELD_SYMBOL: '✨',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'comet': {
                FIELD_SYMBOL: '☄️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'collision_symbol': {
                FIELD_SYMBOL: '💥',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'satellite': {
                FIELD_SYMBOL: '🛰️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'rocket': {
                FIELD_SYMBOL: '🚀',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'flying_saucer': {
                FIELD_SYMBOL: '🛸',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'coin': {
                FIELD_SYMBOL: '🪙',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'telescope': {
                FIELD_SYMBOL: '🔭',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
        },
        WEATHER: {
            'cloud_with_tornado': {
                FIELD_SYMBOL: '🌪️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'rainbow': {
                FIELD_SYMBOL: '🌈',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'black_sun_with_rays': {
                FIELD_SYMBOL: '☀️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'white_sun_with_small_cloud': {
                FIELD_SYMBOL: '🌤️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'sun_behind_cloud': {
                FIELD_SYMBOL: '⛅️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'white_sun_behind_cloud': {
                FIELD_SYMBOL: '🌥️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'cloud': {
                FIELD_SYMBOL: '☁️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'white_sun_behind_cloud_with_rain': {
                FIELD_SYMBOL: '🌦️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'cloud_with_rain': {
                FIELD_SYMBOL: '🌧️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'thunder_cloud_and_rain': {
                FIELD_SYMBOL: '⛈️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'cloud_with_lightning': {
                FIELD_SYMBOL: '🌩️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'cloud_with_snow': {
                FIELD_SYMBOL: '🌨️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'snowflake': {
                FIELD_SYMBOL: '❄️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'snowman': {
                FIELD_SYMBOL: '☃️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'snowman_without_snow': {
                FIELD_SYMBOL: '⛄️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'wind_blowing_face': {
                FIELD_SYMBOL: '🌬️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'dash_symbol': {
                FIELD_SYMBOL: '💨',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'droplet': {
                FIELD_SYMBOL: '💧',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'splashing_sweat_symbol': {
                FIELD_SYMBOL: '💦',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'umbrella_with_rain_drops': {
                FIELD_SYMBOL: '☔️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'umbrella': {
                FIELD_SYMBOL: '☂️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'fog': {
                FIELD_SYMBOL: '🌫️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
        },
        FRUITS_AND_VEGETABLES: {
            'green_apple': {
                FIELD_SYMBOL: '🍏',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'red_apple': {
                FIELD_SYMBOL: '🍎',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'pear': {
                FIELD_SYMBOL: '🍐',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'tangerine': {
                FIELD_SYMBOL: '🍊',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'lemon': {
                FIELD_SYMBOL: '🍋',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'lemon_with_large_green_square': {
                FIELD_SYMBOL: '🍋‍🟩',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'banana': {
                FIELD_SYMBOL: '🍌',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'watermelon': {
                FIELD_SYMBOL: '🍉',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'grapes': {
                FIELD_SYMBOL: '🍇',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'strawberry': {
                FIELD_SYMBOL: '🍓',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'blueberries': {
                FIELD_SYMBOL: '🫐',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'melon': {
                FIELD_SYMBOL: '🍈',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'cherries': {
                FIELD_SYMBOL: '🍒',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'peach': {
                FIELD_SYMBOL: '🍑',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'mango': {
                FIELD_SYMBOL: '🥭',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'pineapple': {
                FIELD_SYMBOL: '🍍',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'coconut': {
                FIELD_SYMBOL: '🥥',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'kiwifruit': {
                FIELD_SYMBOL: '🥝',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'tomato': {
                FIELD_SYMBOL: '🍅',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'aubergine': {
                FIELD_SYMBOL: '🍆',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'avocado': {
                FIELD_SYMBOL: '🥑',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'pea_pod': {
                FIELD_SYMBOL: '🫛',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'broccoli': {
                FIELD_SYMBOL: '🥦',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'leafy_green': {
                FIELD_SYMBOL: '🥬',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'cucumber': {
                FIELD_SYMBOL: '🥒',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'hot_pepper': {
                FIELD_SYMBOL: '🌶️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'bell_pepper': {
                FIELD_SYMBOL: '🫑',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'ear_of_maize': {
                FIELD_SYMBOL: '🌽',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'carrot': {
                FIELD_SYMBOL: '🥕',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'olive': {
                FIELD_SYMBOL: '🫒',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'garlic': {
                FIELD_SYMBOL: '🧄',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'onion': {
                FIELD_SYMBOL: '🧅',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'potato': {
                FIELD_SYMBOL: '🥔',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'root_vegetable': {
                FIELD_SYMBOL: '🫜',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'roasted_sweet_potato': {
                FIELD_SYMBOL: '🍠',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'ginger_root': {
                FIELD_SYMBOL: '🫚',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
        },
        FOOD_AND_DRINKS: {
            'croissant': {
                FIELD_SYMBOL: '🥐',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'bagel': {
                FIELD_SYMBOL: '🥯',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'bread': {
                FIELD_SYMBOL: '🍞',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'baguette_bread': {
                FIELD_SYMBOL: '🥖',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'pretzel': {
                FIELD_SYMBOL: '🥨',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'cheese_wedge': {
                FIELD_SYMBOL: '🧀',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'egg': {
                FIELD_SYMBOL: '🥚',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'cooking': {
                FIELD_SYMBOL: '🍳',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'butter': {
                FIELD_SYMBOL: '🧈',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'pancakes': {
                FIELD_SYMBOL: '🥞',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'waffle': {
                FIELD_SYMBOL: '🧇',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'bacon': {
                FIELD_SYMBOL: '🥓',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'cut_of_meat': {
                FIELD_SYMBOL: '🥩',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'poultry_leg': {
                FIELD_SYMBOL: '🍗',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'meat_on_bone': {
                FIELD_SYMBOL: '🍖',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'bone': {
                FIELD_SYMBOL: '🦴',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'hot_dog': {
                FIELD_SYMBOL: '🌭',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'hamburger': {
                FIELD_SYMBOL: '🍔',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'french_fries': {
                FIELD_SYMBOL: '🍟',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'slice_of_pizza': {
                FIELD_SYMBOL: '🍕',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'flatbread': {
                FIELD_SYMBOL: '🫓',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'sandwich': {
                FIELD_SYMBOL: '🥪',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'stuffed_flatbread': {
                FIELD_SYMBOL: '🥙',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'falafel': {
                FIELD_SYMBOL: '🧆',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'taco': {
                FIELD_SYMBOL: '🌮',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'burrito': {
                FIELD_SYMBOL: '🌯',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'tamale': {
                FIELD_SYMBOL: '🫔',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'green_salad': {
                FIELD_SYMBOL: '🥗',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'shallow_pan_of_food': {
                FIELD_SYMBOL: '🥘',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'fondue': {
                FIELD_SYMBOL: '🫕',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'canned_food': {
                FIELD_SYMBOL: '🥫',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'jar': {
                FIELD_SYMBOL: '🫙',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'spaghetti': {
                FIELD_SYMBOL: '🍝',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'steaming_bowl': {
                FIELD_SYMBOL: '🍜',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'pot_of_food': {
                FIELD_SYMBOL: '🍲',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'curry_and_rice': {
                FIELD_SYMBOL: '🍛',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'sushi': {
                FIELD_SYMBOL: '🍣',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'bento_box': {
                FIELD_SYMBOL: '🍱',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'dumpling': {
                FIELD_SYMBOL: '🥟',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'oyster': {
                FIELD_SYMBOL: '🦪',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'fried_shrimp': {
                FIELD_SYMBOL: '🍤',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'rice_ball': {
                FIELD_SYMBOL: '🍙',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'cooked_rice': {
                FIELD_SYMBOL: '🍚',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'rice_cracker': {
                FIELD_SYMBOL: '🍘',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'fish_cake_with_swirl_design': {
                FIELD_SYMBOL: '🍥',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'fortune_cookie': {
                FIELD_SYMBOL: '🥠',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'moon_cake': {
                FIELD_SYMBOL: '🥮',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'oden': {
                FIELD_SYMBOL: '🍢',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'dango': {
                FIELD_SYMBOL: '🍡',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'shaved_ice': {
                FIELD_SYMBOL: '🍧',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'ice_cream': {
                FIELD_SYMBOL: '🍨',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'soft_ice_cream': {
                FIELD_SYMBOL: '🍦',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'pie': {
                FIELD_SYMBOL: '🥧',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'cupcake': {
                FIELD_SYMBOL: '🧁',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'shortcake': {
                FIELD_SYMBOL: '🍰',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'birthday_cake': {
                FIELD_SYMBOL: '🎂',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'custard': {
                FIELD_SYMBOL: '🍮',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'lollipop': {
                FIELD_SYMBOL: '🍭',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'candy': {
                FIELD_SYMBOL: '🍬',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'chocolate_bar': {
                FIELD_SYMBOL: '🍫',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'popcorn': {
                FIELD_SYMBOL: '🍿',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'doughnut': {
                FIELD_SYMBOL: '🍩',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'cookie': {
                FIELD_SYMBOL: '🍪',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'chestnut': {
                FIELD_SYMBOL: '🌰',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'peanuts': {
                FIELD_SYMBOL: '🥜',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'beans': {
                FIELD_SYMBOL: '🫘',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'honey_pot': {
                FIELD_SYMBOL: '🍯',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'glass_of_milk': {
                FIELD_SYMBOL: '🥛',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'pouring_liquid': {
                FIELD_SYMBOL: '🫗',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'baby_bottle': {
                FIELD_SYMBOL: '🍼',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'teapot': {
                FIELD_SYMBOL: '🫖',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'hot_beverage': {
                FIELD_SYMBOL: '☕️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'teacup_without_handle': {
                FIELD_SYMBOL: '🍵',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'beverage_box': {
                FIELD_SYMBOL: '🧃',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'cup_with_straw': {
                FIELD_SYMBOL: '🥤',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'bubble_tea': {
                FIELD_SYMBOL: '🧋',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'sake_bottle_and_cup': {
                FIELD_SYMBOL: '🍶',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'beer_mug': {
                FIELD_SYMBOL: '🍺',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'clinking_beer_mugs': {
                FIELD_SYMBOL: '🍻',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'clinking_glasses': {
                FIELD_SYMBOL: '🥂',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'wine_glass': {
                FIELD_SYMBOL: '🍷',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'tumbler_glass': {
                FIELD_SYMBOL: '🥃',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'cocktail_glass': {
                FIELD_SYMBOL: '🍸',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'tropical_drink': {
                FIELD_SYMBOL: '🍹',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'mate_drink': {
                FIELD_SYMBOL: '🧉',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'bottle_with_popping_cork': {
                FIELD_SYMBOL: '🍾',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'ice_cube': {
                FIELD_SYMBOL: '🧊',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'spoon': {
                FIELD_SYMBOL: '🥄',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'fork_and_knife': {
                FIELD_SYMBOL: '🍴',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'fork_and_knife_with_plate': {
                FIELD_SYMBOL: '🍽️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'bowl_with_spoon': {
                FIELD_SYMBOL: '🥣',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'takeout_box': {
                FIELD_SYMBOL: '🥡',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'chopsticks': {
                FIELD_SYMBOL: '🥢',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'salt_shaker': {
                FIELD_SYMBOL: '🧂',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
        },
        SPORT: {
            'soccer_ball': {
                FIELD_SYMBOL: '⚽️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'basketball_and_hoop': {
                FIELD_SYMBOL: '🏀',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'american_football': {
                FIELD_SYMBOL: '🏈',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'baseball': {
                FIELD_SYMBOL: '⚾️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'softball': {
                FIELD_SYMBOL: '🥎',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'tennis_racquet_and_ball': {
                FIELD_SYMBOL: '🎾',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'volleyball': {
                FIELD_SYMBOL: '🏐',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'rugby_football': {
                FIELD_SYMBOL: '🏉',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'flying_disc': {
                FIELD_SYMBOL: '🥏',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'billiards': {
                FIELD_SYMBOL: '🎱',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'yo_yo': {
                FIELD_SYMBOL: '🪀',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'table_tennis_paddle_and_ball': {
                FIELD_SYMBOL: '🏓',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'badminton_racquet_and_shuttlecock': {
                FIELD_SYMBOL: '🏸',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'ice_hockey_stick_and_puck': {
                FIELD_SYMBOL: '🏒',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'field_hockey_stick_and_ball': {
                FIELD_SYMBOL: '🏑',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'lacrosse_stick_and_ball': {
                FIELD_SYMBOL: '🥍',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'cricket_bat_and_ball': {
                FIELD_SYMBOL: '🏏',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'boomerang': {
                FIELD_SYMBOL: '🪃',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'goal_net': {
                FIELD_SYMBOL: '🥅',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'flag_in_hole': {
                FIELD_SYMBOL: '⛳️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'kite': {
                FIELD_SYMBOL: '🪁',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'playground_slide': {
                FIELD_SYMBOL: '🛝',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'bow_and_arrow': {
                FIELD_SYMBOL: '🏹',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'fishing_pole_and_fish': {
                FIELD_SYMBOL: '🎣',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'diving_mask': {
                FIELD_SYMBOL: '🤿',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'boxing_glove': {
                FIELD_SYMBOL: '🥊',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'martial_arts_uniform': {
                FIELD_SYMBOL: '🥋',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'running_shirt_with_sash': {
                FIELD_SYMBOL: '🎽',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'skateboard': {
                FIELD_SYMBOL: '🛹',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'roller_skate': {
                FIELD_SYMBOL: '🛼',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'sled': {
                FIELD_SYMBOL: '🛷',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'ice_skate': {
                FIELD_SYMBOL: '⛸️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'curling_stone': {
                FIELD_SYMBOL: '🥌',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'ski_and_ski_boot': {
                FIELD_SYMBOL: '🎿',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'trophy': {
                FIELD_SYMBOL: '🏆',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'first_place_medal': {
                FIELD_SYMBOL: '🥇',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'second_place_medal': {
                FIELD_SYMBOL: '🥈',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'third_place_medal': {
                FIELD_SYMBOL: '🥉',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'sports_medal': {
                FIELD_SYMBOL: '🏅',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'military_medal': {
                FIELD_SYMBOL: '🎖️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'rosette': {
                FIELD_SYMBOL: '🏵️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'canoe': {
                FIELD_SYMBOL: '🛶',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'sailboat': {
                FIELD_SYMBOL: '⛵️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
        },
        ART_AND_CULTURE: {
            'reminder_ribbon': {
                FIELD_SYMBOL: '🎗️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'ticket': {
                FIELD_SYMBOL: '🎫',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'admission_tickets': {
                FIELD_SYMBOL: '🎟️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'circus_tent': {
                FIELD_SYMBOL: '🎪',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'performing_arts': {
                FIELD_SYMBOL: '🎭',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'ballet_shoes': {
                FIELD_SYMBOL: '🩰',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'artist_palette': {
                FIELD_SYMBOL: '🎨',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'splatter': {
                FIELD_SYMBOL: '🫟',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'clapper_board': {
                FIELD_SYMBOL: '🎬',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'fountain': {
                FIELD_SYMBOL: '⛲',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'film_frames': {
                FIELD_SYMBOL: '🎞️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
        },
        SOUND_AND_MUSIC: {
            'microphone': {
                FIELD_SYMBOL: '🎤',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'headphone': {
                FIELD_SYMBOL: '🎧',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'musical_score': {
                FIELD_SYMBOL: '🎼',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'musical_keyboard': {
                FIELD_SYMBOL: '🎹',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'maracas': {
                FIELD_SYMBOL: '🪇',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'drum_with_drumsticks': {
                FIELD_SYMBOL: '🥁',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'long_drum': {
                FIELD_SYMBOL: '🪘',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'saxophone': {
                FIELD_SYMBOL: '🎷',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'trumpet': {
                FIELD_SYMBOL: '🎺',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'trombone': {
                FIELD_SYMBOL: '🪊',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'accordion': {
                FIELD_SYMBOL: '🪗',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'guitar': {
                FIELD_SYMBOL: '🎸',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'banjo': {
                FIELD_SYMBOL: '🪕',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'harp': {
                FIELD_SYMBOL: '🪉',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'violin': {
                FIELD_SYMBOL: '🎻',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'flute': {
                FIELD_SYMBOL: '🪈',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'musical_note': {
                FIELD_SYMBOL: '🎵',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'multiple_musical_notes': {
                FIELD_SYMBOL: '🎶',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'speaker': {
                FIELD_SYMBOL: '🔈',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'speaker_with_cancellation_stroke': {
                FIELD_SYMBOL: '🔇',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'speaker_with_one_sound_wave': {
                FIELD_SYMBOL: '🔉',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'speaker_with_three_sound_waves': {
                FIELD_SYMBOL: '🔊',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'bell': {
                FIELD_SYMBOL: '🔔',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'bell_with_cancellation_stroke': {
                FIELD_SYMBOL: '🔕',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'cheering_megaphone': {
                FIELD_SYMBOL: '📣',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'public_address_loudspeaker': {
                FIELD_SYMBOL: '📢',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
        },
        TRANSPORT: {
            'automobile': {
                FIELD_SYMBOL: '🚗',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'taxi': {
                FIELD_SYMBOL: '🚕',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'recreational_vehicle': {
                FIELD_SYMBOL: '🚙',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'bus': {
                FIELD_SYMBOL: '🚌',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'trolleybus': {
                FIELD_SYMBOL: '🚎',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'racing_car': {
                FIELD_SYMBOL: '🏎️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'police_car': {
                FIELD_SYMBOL: '🚓',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'ambulance': {
                FIELD_SYMBOL: '🚑',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'fire_engine': {
                FIELD_SYMBOL: '🚒',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'minibus': {
                FIELD_SYMBOL: '🚐',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'pickup_truck': {
                FIELD_SYMBOL: '🛻',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'delivery_truck': {
                FIELD_SYMBOL: '🚚',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'articulated_lorry': {
                FIELD_SYMBOL: '🚛',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'tractor': {
                FIELD_SYMBOL: '🚜',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'scooter': {
                FIELD_SYMBOL: '🛴',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'bicycle': {
                FIELD_SYMBOL: '🚲',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'motor_scooter': {
                FIELD_SYMBOL: '🛵',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'racing_motorcycle': {
                FIELD_SYMBOL: '🏍️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'auto_rickshaw': {
                FIELD_SYMBOL: '🛺',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'wheel': {
                FIELD_SYMBOL: '🛞',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'police_cars_revolving_light': {
                FIELD_SYMBOL: '🚨',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'oncoming_police_car': {
                FIELD_SYMBOL: '🚔',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'oncoming_bus': {
                FIELD_SYMBOL: '🚍',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'oncoming_automobile': {
                FIELD_SYMBOL: '🚘',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'oncoming_taxi': {
                FIELD_SYMBOL: '🚖',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'aerial_tramway': {
                FIELD_SYMBOL: '🚡',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'mountain_cableway': {
                FIELD_SYMBOL: '🚠',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'suspension_railway': {
                FIELD_SYMBOL: '🚟',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'railway_car': {
                FIELD_SYMBOL: '🚃',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'tram_car': {
                FIELD_SYMBOL: '🚋',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'mountain_railway': {
                FIELD_SYMBOL: '🚞',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'monorail': {
                FIELD_SYMBOL: '🚝',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'high_speed_train': {
                FIELD_SYMBOL: '🚄',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'high_speed_train_with_bullet_nose': {
                FIELD_SYMBOL: '🚅',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'light_rail': {
                FIELD_SYMBOL: '🚈',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'steam_locomotive': {
                FIELD_SYMBOL: '🚂',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'train': {
                FIELD_SYMBOL: '🚆',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'metro': {
                FIELD_SYMBOL: '🚇',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'tram': {
                FIELD_SYMBOL: '🚊',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'station': {
                FIELD_SYMBOL: '🚉',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'airplane': {
                FIELD_SYMBOL: '✈️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'airplane_departure': {
                FIELD_SYMBOL: '🛫',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'airplane_arriving': {
                FIELD_SYMBOL: '🛬',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'small_airplane': {
                FIELD_SYMBOL: '🛩️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'seat': {
                FIELD_SYMBOL: '💺',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'helicopter': {
                FIELD_SYMBOL: '🚁',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'speedboat': {
                FIELD_SYMBOL: '🚤',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'motor_boat': {
                FIELD_SYMBOL: '🛥️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'passenger_ship': {
                FIELD_SYMBOL: '🛳️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'ferry': {
                FIELD_SYMBOL: '⛴️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'ship': {
                FIELD_SYMBOL: '🚢',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'ring_buoy': {
                FIELD_SYMBOL: '🛟',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'anchor': {
                FIELD_SYMBOL: '⚓️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'hook': {
                FIELD_SYMBOL: '🪝',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'fuel_pump': {
                FIELD_SYMBOL: '⛽️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'construction_sign': {
                FIELD_SYMBOL: '🚧',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'vertical_traffic_light': {
                FIELD_SYMBOL: '🚦',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'horizontal_traffic_light': {
                FIELD_SYMBOL: '🚥',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'bus_stop': {
                FIELD_SYMBOL: '🚏',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'world_map': {
                FIELD_SYMBOL: '🗺️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'railway_track': {
                FIELD_SYMBOL: '🛤️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'motorway': {
                FIELD_SYMBOL: '🛣️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
        },
        TRAVEL_AND_PLACES: {
            'compass': {
                FIELD_SYMBOL: '🧭',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'moyai': {
                FIELD_SYMBOL: '🗿',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'statue_of_liberty': {
                FIELD_SYMBOL: '🗽',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'tokyo_tower': {
                FIELD_SYMBOL: '🗼',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'european_castle': {
                FIELD_SYMBOL: '🏰',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'japanese_castle': {
                FIELD_SYMBOL: '🏯️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'umbrella_on_ground': {
                FIELD_SYMBOL: '⛱️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'beach_with_umbrella': {
                FIELD_SYMBOL: '🏖️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'desert_island': {
                FIELD_SYMBOL: '🏝️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'desert': {
                FIELD_SYMBOL: '🏜️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'volcano': {
                FIELD_SYMBOL: '🌋',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'mountain': {
                FIELD_SYMBOL: '⛰️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'snow_capped_mountain': {
                FIELD_SYMBOL: '🏔️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'mount_fuji': {
                FIELD_SYMBOL: '🗻',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'camping': {
                FIELD_SYMBOL: '🏕️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'tent': {
                FIELD_SYMBOL: '⛺️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'silhouette_of_japan': {
                FIELD_SYMBOL: '🗾',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'moon_viewing_ceremony': {
                FIELD_SYMBOL: '🎑',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'national_park': {
                FIELD_SYMBOL: '🏞️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'sunrise': {
                FIELD_SYMBOL: '🌅',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'sunrise_over_mountains': {
                FIELD_SYMBOL: '🌄',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'shooting_star': {
                FIELD_SYMBOL: '🌠',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'firework_sparkler': {
                FIELD_SYMBOL: '🎇',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'fireworks': {
                FIELD_SYMBOL: '🎆',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'sunset_over_buildings': {
                FIELD_SYMBOL: '🌇',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'cityscape_at_dusk': {
                FIELD_SYMBOL: '🌆',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'cityscape': {
                FIELD_SYMBOL: '🏙️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'night_with_stars': {
                FIELD_SYMBOL: '🌃',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'milky_way': {
                FIELD_SYMBOL: '🌌',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'bridge_at_night': {
                FIELD_SYMBOL: '🌉',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'foggy': {
                FIELD_SYMBOL: '🌁',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
        },
        BUILDINGS: {
            'hut': {
                FIELD_SYMBOL: '🛖',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'house_building': {
                FIELD_SYMBOL: '🏠',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'house_with_garden': {
                FIELD_SYMBOL: '🏡',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'house_buildings': {
                FIELD_SYMBOL: '🏘️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'derelict_house_building': {
                FIELD_SYMBOL: '🏚️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'building_construction': {
                FIELD_SYMBOL: '🏗️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'factory': {
                FIELD_SYMBOL: '🏭',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'office_building': {
                FIELD_SYMBOL: '🏢',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'department_store': {
                FIELD_SYMBOL: '🏬',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'japanese_post_office': {
                FIELD_SYMBOL: '🏣',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'european_post_office': {
                FIELD_SYMBOL: '🏤',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'hospital': {
                FIELD_SYMBOL: '🏥',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'bank': {
                FIELD_SYMBOL: '🏦',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'hotel': {
                FIELD_SYMBOL: '🏨',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'convenience_store': {
                FIELD_SYMBOL: '🏪',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'school': {
                FIELD_SYMBOL: '🏫',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'love_hotel': {
                FIELD_SYMBOL: '🏩',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'wedding': {
                FIELD_SYMBOL: '💒',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'classical_building': {
                FIELD_SYMBOL: '🏛️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'church': {
                FIELD_SYMBOL: '⛪️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'mosque': {
                FIELD_SYMBOL: '🕌',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'synagogue': {
                FIELD_SYMBOL: '🕍',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'hindu_temple': {
                FIELD_SYMBOL: '🛕',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'kaaba': {
                FIELD_SYMBOL: '🕋',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'shinto_shrine': {
                FIELD_SYMBOL: '⛩️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
        },
        ENTERTAINMENT: {
            'game_die': {
                FIELD_SYMBOL: '🎲',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'black_chess_pawn': {
                FIELD_SYMBOL: '♟️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'direct_hit': {
                FIELD_SYMBOL: '🎯',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'bowling': {
                FIELD_SYMBOL: '🎳',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'video_game': {
                FIELD_SYMBOL: '🎮',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'slot_machine': {
                FIELD_SYMBOL: '🎰',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'jigsaw_puzzle_piece': {
                FIELD_SYMBOL: '🧩',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'stadium': {
                FIELD_SYMBOL: '🏟️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'ferris_wheel': {
                FIELD_SYMBOL: '🎡',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'roller_coaster': {
                FIELD_SYMBOL: '🎢',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'carousel_horse': {
                FIELD_SYMBOL: '🎠',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'black_spade_suit': {
                FIELD_SYMBOL: '♠️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'black_club_suit': {
                FIELD_SYMBOL: '♣️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'black_heart_suit': {
                FIELD_SYMBOL: '♥️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'black_diamond_suit': {
                FIELD_SYMBOL: '♦️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'playing_card_black_joker': {
                FIELD_SYMBOL: '🃏',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'flower_playing_cards': {
                FIELD_SYMBOL: '🎴',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'mahjong_tile_red_dragon': {
                FIELD_SYMBOL: '🀄️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
        },
        ELECTRONIC_DEVICES: {
            'watch': {
                FIELD_SYMBOL: '⌚️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'mobile_phone': {
                FIELD_SYMBOL: '📱',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'mobile_phone_with_rightwards_arrow_at_left': {
                FIELD_SYMBOL: '📲',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'personal_computer': {
                FIELD_SYMBOL: '💻',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'keyboard': {
                FIELD_SYMBOL: '⌨️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'desktop_computer': {
                FIELD_SYMBOL: '🖥️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'printer': {
                FIELD_SYMBOL: '🖨️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'three_button_mouse': {
                FIELD_SYMBOL: '🖱️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'trackball': {
                FIELD_SYMBOL: '🖲️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'joystick': {
                FIELD_SYMBOL: '🕹️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'minidisc': {
                FIELD_SYMBOL: '💽',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'floppy_disk': {
                FIELD_SYMBOL: '💾',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'optical_disc': {
                FIELD_SYMBOL: '💿',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'dvd': {
                FIELD_SYMBOL: '📀',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'videocassette': {
                FIELD_SYMBOL: '📼',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'camera': {
                FIELD_SYMBOL: '📷',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'camera_with_flash': {
                FIELD_SYMBOL: '📸',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'video_camera': {
                FIELD_SYMBOL: '📹',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'movie_camera': {
                FIELD_SYMBOL: '🎥',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'film_projector': {
                FIELD_SYMBOL: '📽️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'telephone_receiver': {
                FIELD_SYMBOL: '📞',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'black_telephone': {
                FIELD_SYMBOL: '☎️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'pager': {
                FIELD_SYMBOL: '📟',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'fax_machine': {
                FIELD_SYMBOL: '📠',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'television': {
                FIELD_SYMBOL: '📺',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'radio': {
                FIELD_SYMBOL: '📻',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'studio_microphone': {
                FIELD_SYMBOL: '🎙️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'level_slider': {
                FIELD_SYMBOL: '🎚️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'control_knobs': {
                FIELD_SYMBOL: '🎛️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'satellite_antenna': {
                FIELD_SYMBOL: '📡',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'battery': {
                FIELD_SYMBOL: '🔋',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'low_battery': {
                FIELD_SYMBOL: '🪫',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'electric_plug': {
                FIELD_SYMBOL: '🔌',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'electric_light_bulb': {
                FIELD_SYMBOL: '💡',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'electric_torch': {
                FIELD_SYMBOL: '🔦',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
        },
        CLOCKS_AND_TIME: {
            'stopwatch': {
                FIELD_SYMBOL: '⏱️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'timer_clock': {
                FIELD_SYMBOL: '⏲️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'alarm_clock': {
                FIELD_SYMBOL: '⏰',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'mantelpiece_clock': {
                FIELD_SYMBOL: '🕰️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'hourglass': {
                FIELD_SYMBOL: '⌛️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'hourglass_with_flowing_sand': {
                FIELD_SYMBOL: '⏳',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'clock_face_one_oclock': {
                FIELD_SYMBOL: '🕐',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'clock_face_two_oclock': {
                FIELD_SYMBOL: '🕑',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'clock_face_three_oclock': {
                FIELD_SYMBOL: '🕒',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'clock_face_four_oclock': {
                FIELD_SYMBOL: '🕓',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'clock_face_five_oclock': {
                FIELD_SYMBOL: '🕔',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'clock_face_six_oclock': {
                FIELD_SYMBOL: '🕕',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'clock_face_seven_oclock': {
                FIELD_SYMBOL: '🕖',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'clock_face_eight_oclock': {
                FIELD_SYMBOL: '🕗',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'clock_face_nine_oclock': {
                FIELD_SYMBOL: '🕘',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'clock_face_ten_oclock': {
                FIELD_SYMBOL: '🕙',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'clock_face_eleven_oclock': {
                FIELD_SYMBOL: '🕚',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'clock_face_twelve_oclock': {
                FIELD_SYMBOL: '🕛',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'clock_face_one_thirty': {
                FIELD_SYMBOL: '🕜',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'clock_face_two_thirty': {
                FIELD_SYMBOL: '🕝',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'clock_face_three_thirty': {
                FIELD_SYMBOL: '🕞',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'clock_face_four_thirty': {
                FIELD_SYMBOL: '🕟',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'clock_face_five_thirty': {
                FIELD_SYMBOL: '🕠',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'clock_face_six_thirty': {
                FIELD_SYMBOL: '🕡',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'clock_face_seven_thirty': {
                FIELD_SYMBOL: '🕢',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'clock_face_eight_thirty': {
                FIELD_SYMBOL: '🕣',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'clock_face_nine_thirty': {
                FIELD_SYMBOL: '🕤',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'clock_face_ten_thirty': {
                FIELD_SYMBOL: '🕥',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'clock_face_eleven_thirty': {
                FIELD_SYMBOL: '🕦',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'clock_face_twelve_thirty': {
                FIELD_SYMBOL: '🕧',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
        },
        MONEY_AND_VALUABLES: {
            'money_with_wings': {
                FIELD_SYMBOL: '💸',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'banknote_with_dollar_sign': {
                FIELD_SYMBOL: '💵',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'banknote_with_yen_sign': {
                FIELD_SYMBOL: '💴',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'banknote_with_euro_sign': {
                FIELD_SYMBOL: '💶',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'banknote_with_pound_sign': {
                FIELD_SYMBOL: '💷',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'money_bag': {
                FIELD_SYMBOL: '💰',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'credit_card': {
                FIELD_SYMBOL: '💳',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'gem_stone': {
                FIELD_SYMBOL: '💎',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'treasure_chest': {
                FIELD_SYMBOL: '🪎',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'heavy_dollar_sign': {
                FIELD_SYMBOL: '💲',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'currency_exchange': {
                FIELD_SYMBOL: '💱',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'chart_with_upwards_trend_and_yen_sign': {
                FIELD_SYMBOL: '💹',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
        },
        OBJECTS_AND_TOOLS: {
            'fingerprint': {
                FIELD_SYMBOL: '🫆',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'identification_card': {
                FIELD_SYMBOL: '🪪',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'compression': {
                FIELD_SYMBOL: '🗜️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'candle': {
                FIELD_SYMBOL: '🕯️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'diya_lamp': {
                FIELD_SYMBOL: '🪔',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'fire_extinguisher': {
                FIELD_SYMBOL: '🧯',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'oil_drum': {
                FIELD_SYMBOL: '🛢️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'scales': {
                FIELD_SYMBOL: '⚖️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'ladder': {
                FIELD_SYMBOL: '🪜',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'toolbox': {
                FIELD_SYMBOL: '🧰',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'screwdriver': {
                FIELD_SYMBOL: '🪛',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'wrench': {
                FIELD_SYMBOL: '🔧',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'hammer': {
                FIELD_SYMBOL: '🔨',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'hammer_and_pick': {
                FIELD_SYMBOL: '⚒️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'hammer_and_wrench': {
                FIELD_SYMBOL: '🛠️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'pick': {
                FIELD_SYMBOL: '⛏️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'shovel': {
                FIELD_SYMBOL: '🪏',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'carpentry_saw': {
                FIELD_SYMBOL: '🪚',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'nut_and_bolt': {
                FIELD_SYMBOL: '🔩',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'gear': {
                FIELD_SYMBOL: '⚙️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'mouse_trap': {
                FIELD_SYMBOL: '🪤',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'brick': {
                FIELD_SYMBOL: '🧱',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'chains': {
                FIELD_SYMBOL: '⛓️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'chains_with_collision_symbol': {
                FIELD_SYMBOL: '⛓️‍💥',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'magnet': {
                FIELD_SYMBOL: '🧲',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'pistol': {
                FIELD_SYMBOL: '🔫',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'bomb': {
                FIELD_SYMBOL: '💣',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'firecracker': {
                FIELD_SYMBOL: '🧨',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'axe': {
                FIELD_SYMBOL: '🪓',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'hocho': {
                FIELD_SYMBOL: '🔪',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'dagger_knife': {
                FIELD_SYMBOL: '🗡️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'crossed_swords': {
                FIELD_SYMBOL: '⚔️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'shield': {
                FIELD_SYMBOL: '🛡️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'smoking_symbol': {
                FIELD_SYMBOL: '🚬',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'coffin': {
                FIELD_SYMBOL: '⚰️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'headstone': {
                FIELD_SYMBOL: '🪦',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'funeral_urn': {
                FIELD_SYMBOL: '⚱️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'amphora': {
                FIELD_SYMBOL: '🏺',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'crystal_ball': {
                FIELD_SYMBOL: '🔮',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'prayer_beads': {
                FIELD_SYMBOL: '📿',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'nazar_amulet': {
                FIELD_SYMBOL: '🧿',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'hamsa': {
                FIELD_SYMBOL: '🪬',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'barber_pole': {
                FIELD_SYMBOL: '💈',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'broom': {
                FIELD_SYMBOL: '🧹',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'plunger': {
                FIELD_SYMBOL: '🪠',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'basket': {
                FIELD_SYMBOL: '🧺',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'roll_of_paper': {
                FIELD_SYMBOL: '🧻',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'toilet': {
                FIELD_SYMBOL: '🚽',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'potable_water_symbol': {
                FIELD_SYMBOL: '🚰',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'shower': {
                FIELD_SYMBOL: '🚿',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'bathtub': {
                FIELD_SYMBOL: '🛁',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'bath': {
                FIELD_SYMBOL: '🛀',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'bar_of_soap': {
                FIELD_SYMBOL: '🧼',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'toothbrush': {
                FIELD_SYMBOL: '🪥',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'razor': {
                FIELD_SYMBOL: '🪒',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'hair_pick': {
                FIELD_SYMBOL: '🪮',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'sponge': {
                FIELD_SYMBOL: '🧽',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'bucket': {
                FIELD_SYMBOL: '🪣',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'lotion_bottle': {
                FIELD_SYMBOL: '🧴',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'bellhop_bell': {
                FIELD_SYMBOL: '🛎️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'key': {
                FIELD_SYMBOL: '🔑',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'old_key': {
                FIELD_SYMBOL: '🗝️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'door': {
                FIELD_SYMBOL: '🚪',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'chair': {
                FIELD_SYMBOL: '🪑',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'couch_and_lamp': {
                FIELD_SYMBOL: '🛋️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'bed': {
                FIELD_SYMBOL: '🛏️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'sleeping_accommodation': {
                FIELD_SYMBOL: '🛌',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'teddy_bear': {
                FIELD_SYMBOL: '🧸',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'nesting_dolls': {
                FIELD_SYMBOL: '🪆',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'frame_with_picture': {
                FIELD_SYMBOL: '🖼️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'mirror': {
                FIELD_SYMBOL: '🪞',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'window': {
                FIELD_SYMBOL: '🪟',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'shopping_bags': {
                FIELD_SYMBOL: '🛍️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'shopping_trolley': {
                FIELD_SYMBOL: '🛒',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'wrapped_present': {
                FIELD_SYMBOL: '🎁',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'balloon': {
                FIELD_SYMBOL: '🎈',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'carp_streamer': {
                FIELD_SYMBOL: '🎏',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'ribbon': {
                FIELD_SYMBOL: '🎀',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'magic_wand': {
                FIELD_SYMBOL: '🪄',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'pinata': {
                FIELD_SYMBOL: '🪅',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'confetti_ball': {
                FIELD_SYMBOL: '🎊',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'party_popper': {
                FIELD_SYMBOL: '🎉',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'japanese_dolls': {
                FIELD_SYMBOL: '🎎',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'folding_hand_fan': {
                FIELD_SYMBOL: '🪭',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'izakaya_lantern': {
                FIELD_SYMBOL: '🏮',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'wind_chime': {
                FIELD_SYMBOL: '🎐',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'mirror_ball': {
                FIELD_SYMBOL: '🪩',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'red_gift_envelope': {
                FIELD_SYMBOL: '🧧',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'link_symbol': {
                FIELD_SYMBOL: '🔗',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'lock_with_ink_pen': {
                FIELD_SYMBOL: '🔏',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'closed_lock_with_key': {
                FIELD_SYMBOL: '🔐',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'lock': {
                FIELD_SYMBOL: '🔒',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'open_lock': {
                FIELD_SYMBOL: '🔓',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
        },
        SCIENCE_AND_HEALTH: {
            'alembic': {
                FIELD_SYMBOL: '⚗️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'microscope': {
                FIELD_SYMBOL: '🔬',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'hole': {
                FIELD_SYMBOL: '🕳️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'x_ray': {
                FIELD_SYMBOL: '🩻',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'adhesive_bandage': {
                FIELD_SYMBOL: '🩹',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'stethoscope': {
                FIELD_SYMBOL: '🩺',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'pill': {
                FIELD_SYMBOL: '💊',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'syringe': {
                FIELD_SYMBOL: '💉',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'drop_of_blood': {
                FIELD_SYMBOL: '🩸',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'dna_double_helix': {
                FIELD_SYMBOL: '🧬',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'microbe': {
                FIELD_SYMBOL: '🦠',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'petri_dish': {
                FIELD_SYMBOL: '🧫',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'test_tube': {
                FIELD_SYMBOL: '🧪',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'thermometer': {
                FIELD_SYMBOL: '🌡️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
        },
        OFFICE_TOOLS: {
            'envelope': {
                FIELD_SYMBOL: '✉️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'envelope_with_downwards_arrow_above': {
                FIELD_SYMBOL: '📩',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'incoming_envelope': {
                FIELD_SYMBOL: '📨',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'e_mail_symbol': {
                FIELD_SYMBOL: '📧',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'love_letter': {
                FIELD_SYMBOL: '💌',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'inbox_tray': {
                FIELD_SYMBOL: '📥',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'outbox_tray': {
                FIELD_SYMBOL: '📤',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'package': {
                FIELD_SYMBOL: '📦',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'label': {
                FIELD_SYMBOL: '🏷️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'placard': {
                FIELD_SYMBOL: '🪧',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'closed_mailbox_with_lowered_flag': {
                FIELD_SYMBOL: '📪',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'closed_mailbox_with_raised_flag': {
                FIELD_SYMBOL: '📫',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'open_mailbox_with_raised_flag': {
                FIELD_SYMBOL: '📬',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'open_mailbox_with_lowered_flag': {
                FIELD_SYMBOL: '📭',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'postbox': {
                FIELD_SYMBOL: '📮',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'postal_horn': {
                FIELD_SYMBOL: '📯',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'scroll': {
                FIELD_SYMBOL: '📜',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'page_with_curl': {
                FIELD_SYMBOL: '📃',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'page_facing_up': {
                FIELD_SYMBOL: '📄',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'bookmark_tabs': {
                FIELD_SYMBOL: '📑',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'receipt': {
                FIELD_SYMBOL: '🧾',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'bar_chart': {
                FIELD_SYMBOL: '📊',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'chart_with_upwards_trend': {
                FIELD_SYMBOL: '📈',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'chart_with_downwards_trend': {
                FIELD_SYMBOL: '📉',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'spiral_note_pad': {
                FIELD_SYMBOL: '🗒️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'spiral_calendar_pad': {
                FIELD_SYMBOL: '🗓️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'tear_off_calendar': {
                FIELD_SYMBOL: '📆',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'calendar': {
                FIELD_SYMBOL: '📅',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'wastebasket': {
                FIELD_SYMBOL: '🗑️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'card_index': {
                FIELD_SYMBOL: '📇',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'card_file_box': {
                FIELD_SYMBOL: '🗃️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'ballot_box_with_ballot': {
                FIELD_SYMBOL: '🗳️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'file_cabinet': {
                FIELD_SYMBOL: '🗄️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'clipboard': {
                FIELD_SYMBOL: '📋',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'file_folder': {
                FIELD_SYMBOL: '📁',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'open_file_folder': {
                FIELD_SYMBOL: '📂',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'card_index_dividers': {
                FIELD_SYMBOL: '🗂️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'rolled_up_newspaper': {
                FIELD_SYMBOL: '🗞️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'newspaper': {
                FIELD_SYMBOL: '📰',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'notebook': {
                FIELD_SYMBOL: '📓',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'notebook_with_decorative_cover': {
                FIELD_SYMBOL: '📔',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'ledger': {
                FIELD_SYMBOL: '📒',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'closed_book': {
                FIELD_SYMBOL: '📕',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'green_book': {
                FIELD_SYMBOL: '📗',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'blue_book': {
                FIELD_SYMBOL: '📘',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'orange_book': {
                FIELD_SYMBOL: '📙',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'books': {
                FIELD_SYMBOL: '📚',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'open_book': {
                FIELD_SYMBOL: '📖',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'bookmark': {
                FIELD_SYMBOL: '🔖',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'safety_pin': {
                FIELD_SYMBOL: '🧷',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'paperclip': {
                FIELD_SYMBOL: '📎',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'linked_paperclips': {
                FIELD_SYMBOL: '🖇️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'triangular_ruler': {
                FIELD_SYMBOL: '📐',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'straight_ruler': {
                FIELD_SYMBOL: '📏',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'abacus': {
                FIELD_SYMBOL: '🧮',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'pushpin': {
                FIELD_SYMBOL: '📌',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'round_pushpin': {
                FIELD_SYMBOL: '📍',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'black_scissors': {
                FIELD_SYMBOL: '✂️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'lower_left_ballpoint_pen': {
                FIELD_SYMBOL: '🖊️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'lower_left_fountain_pen': {
                FIELD_SYMBOL: '🖋️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'black_nib': {
                FIELD_SYMBOL: '✒️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'lower_left_paintbrush': {
                FIELD_SYMBOL: '🖌️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'lower_left_crayon': {
                FIELD_SYMBOL: '🖍️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'memo': {
                FIELD_SYMBOL: '📝',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'pencil': {
                FIELD_SYMBOL: '✏️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'left_pointing_magnifying_glass': {
                FIELD_SYMBOL: '🔍',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'right_pointing_magnifying_glass': {
                FIELD_SYMBOL: '🔎',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
        },
        FLAGS: {
            'waving_white_flag': {
                FIELD_SYMBOL: '🏳️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'waving_black_flag': {
                FIELD_SYMBOL: '🏴',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'waving_black_flag_with_skull_and_crossbones': {
                FIELD_SYMBOL: '🏴‍☠️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'chequered_flag': {
                FIELD_SYMBOL: '🏁',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'triangular_flag_on_post': {
                FIELD_SYMBOL: '🚩',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'waving_white_flag_with_rainbow': {
                FIELD_SYMBOL: '🏳️‍🌈',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'waving_white_flag_with_male_with_stroke_and_male_and_female_sign': {
                FIELD_SYMBOL: '🏳️‍⚧️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_u_with_regional_indicator_symbol_letter_n': {
                FIELD_SYMBOL: '🇺🇳',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_a_with_regional_indicator_symbol_letter_f': {
                FIELD_SYMBOL: '🇦🇫',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_a_with_regional_indicator_symbol_letter_l': {
                FIELD_SYMBOL: '🇦🇱',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_d_with_regional_indicator_symbol_letter_z': {
                FIELD_SYMBOL: '🇩🇿',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_a_with_regional_indicator_symbol_letter_d': {
                FIELD_SYMBOL: '🇦🇩',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_a_with_regional_indicator_symbol_letter_o': {
                FIELD_SYMBOL: '🇦🇴',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_a_with_regional_indicator_symbol_letter_i': {
                FIELD_SYMBOL: '🇦🇮',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_a_with_regional_indicator_symbol_letter_q': {
                FIELD_SYMBOL: '🇦🇶',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_a_with_regional_indicator_symbol_letter_g': {
                FIELD_SYMBOL: '🇦🇬',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_s_with_regional_indicator_symbol_letter_a': {
                FIELD_SYMBOL: '🇸🇦',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_a_with_regional_indicator_symbol_letter_r': {
                FIELD_SYMBOL: '🇦🇷',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_a_with_regional_indicator_symbol_letter_m': {
                FIELD_SYMBOL: '🇦🇲',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_a_with_regional_indicator_symbol_letter_w': {
                FIELD_SYMBOL: '🇦🇼',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_a_with_regional_indicator_symbol_letter_u': {
                FIELD_SYMBOL: '🇦🇺',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_a_with_regional_indicator_symbol_letter_t': {
                FIELD_SYMBOL: '🇦🇹',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_a_with_regional_indicator_symbol_letter_z': {
                FIELD_SYMBOL: '🇦🇿',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_b_with_regional_indicator_symbol_letter_s': {
                FIELD_SYMBOL: '🇧🇸',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_b_with_regional_indicator_symbol_letter_h': {
                FIELD_SYMBOL: '🇧🇭',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_b_with_regional_indicator_symbol_letter_d': {
                FIELD_SYMBOL: '🇧🇩',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_b_with_regional_indicator_symbol_letter_b': {
                FIELD_SYMBOL: '🇧🇧',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_b_with_regional_indicator_symbol_letter_e': {
                FIELD_SYMBOL: '🇧🇪',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_b_with_regional_indicator_symbol_letter_z': {
                FIELD_SYMBOL: '🇧🇿',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_b_with_regional_indicator_symbol_letter_j': {
                FIELD_SYMBOL: '🇧🇯',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_b_with_regional_indicator_symbol_letter_m': {
                FIELD_SYMBOL: '🇧🇲',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_b_with_regional_indicator_symbol_letter_t': {
                FIELD_SYMBOL: '🇧🇹',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_b_with_regional_indicator_symbol_letter_y': {
                FIELD_SYMBOL: '🇧🇾',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_b_with_regional_indicator_symbol_letter_o': {
                FIELD_SYMBOL: '🇧🇴',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_b_with_regional_indicator_symbol_letter_a': {
                FIELD_SYMBOL: '🇧🇦',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_b_with_regional_indicator_symbol_letter_w': {
                FIELD_SYMBOL: '🇧🇼',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_b_with_regional_indicator_symbol_letter_r': {
                FIELD_SYMBOL: '🇧🇷',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_b_with_regional_indicator_symbol_letter_n': {
                FIELD_SYMBOL: '🇧🇳',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_v_with_regional_indicator_symbol_letter_g': {
                FIELD_SYMBOL: '🇻🇬',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_b_with_regional_indicator_symbol_letter_g': {
                FIELD_SYMBOL: '🇧🇬',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_b_with_regional_indicator_symbol_letter_f': {
                FIELD_SYMBOL: '🇧🇫',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_b_with_regional_indicator_symbol_letter_i': {
                FIELD_SYMBOL: '🇧🇮',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_c_with_regional_indicator_symbol_letter_l': {
                FIELD_SYMBOL: '🇨🇱',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_c_with_regional_indicator_symbol_letter_n': {
                FIELD_SYMBOL: '🇨🇳',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_h_with_regional_indicator_symbol_letter_r': {
                FIELD_SYMBOL: '🇭🇷',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_c_with_regional_indicator_symbol_letter_i': {
                FIELD_SYMBOL: '🇨🇮',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_c_with_regional_indicator_symbol_letter_w': {
                FIELD_SYMBOL: '🇨🇼',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_c_with_regional_indicator_symbol_letter_y': {
                FIELD_SYMBOL: '🇨🇾',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_t_with_regional_indicator_symbol_letter_d': {
                FIELD_SYMBOL: '🇹🇩',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_i_with_regional_indicator_symbol_letter_o': {
                FIELD_SYMBOL: '🇮🇴',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_m_with_regional_indicator_symbol_letter_e': {
                FIELD_SYMBOL: '🇲🇪',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_c_with_regional_indicator_symbol_letter_z': {
                FIELD_SYMBOL: '🇨🇿',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_d_with_regional_indicator_symbol_letter_k': {
                FIELD_SYMBOL: '🇩🇰',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_c_with_regional_indicator_symbol_letter_d': {
                FIELD_SYMBOL: '🇨🇩',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_d_with_regional_indicator_symbol_letter_m': {
                FIELD_SYMBOL: '🇩🇲',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_d_with_regional_indicator_symbol_letter_o': {
                FIELD_SYMBOL: '🇩🇴',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_d_with_regional_indicator_symbol_letter_j': {
                FIELD_SYMBOL: '🇩🇯',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_e_with_regional_indicator_symbol_letter_g': {
                FIELD_SYMBOL: '🇪🇬',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_e_with_regional_indicator_symbol_letter_c': {
                FIELD_SYMBOL: '🇪🇨',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_e_with_regional_indicator_symbol_letter_r': {
                FIELD_SYMBOL: '🇪🇷',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_e_with_regional_indicator_symbol_letter_e': {
                FIELD_SYMBOL: '🇪🇪',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_s_with_regional_indicator_symbol_letter_z': {
                FIELD_SYMBOL: '🇸🇿',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_e_with_regional_indicator_symbol_letter_t': {
                FIELD_SYMBOL: '🇪🇹',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_f_with_regional_indicator_symbol_letter_k': {
                FIELD_SYMBOL: '🇫🇰',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_f_with_regional_indicator_symbol_letter_j': {
                FIELD_SYMBOL: '🇫🇯',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_p_with_regional_indicator_symbol_letter_h': {
                FIELD_SYMBOL: '🇵🇭',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_f_with_regional_indicator_symbol_letter_i': {
                FIELD_SYMBOL: '🇫🇮',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_f_with_regional_indicator_symbol_letter_r': {
                FIELD_SYMBOL: '🇫🇷',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_t_with_regional_indicator_symbol_letter_f': {
                FIELD_SYMBOL: '🇹🇫',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_g_with_regional_indicator_symbol_letter_a': {
                FIELD_SYMBOL: '🇬🇦',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_g_with_regional_indicator_symbol_letter_m': {
                FIELD_SYMBOL: '🇬🇲',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_g_with_regional_indicator_symbol_letter_s': {
                FIELD_SYMBOL: '🇬🇸',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_g_with_regional_indicator_symbol_letter_h': {
                FIELD_SYMBOL: '🇬🇭',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_g_with_regional_indicator_symbol_letter_i': {
                FIELD_SYMBOL: '🇬🇮',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_g_with_regional_indicator_symbol_letter_r': {
                FIELD_SYMBOL: '🇬🇷',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_g_with_regional_indicator_symbol_letter_d': {
                FIELD_SYMBOL: '🇬🇩',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_g_with_regional_indicator_symbol_letter_l': {
                FIELD_SYMBOL: '🇬🇱',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_g_with_regional_indicator_symbol_letter_e': {
                FIELD_SYMBOL: '🇬🇪',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_g_with_regional_indicator_symbol_letter_u': {
                FIELD_SYMBOL: '🇬🇺',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_g_with_regional_indicator_symbol_letter_g': {
                FIELD_SYMBOL: '🇬🇬',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_g_with_regional_indicator_symbol_letter_y': {
                FIELD_SYMBOL: '🇬🇾',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_g_with_regional_indicator_symbol_letter_f': {
                FIELD_SYMBOL: '🇬🇫',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_g_with_regional_indicator_symbol_letter_p': {
                FIELD_SYMBOL: '🇬🇵',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_g_with_regional_indicator_symbol_letter_t': {
                FIELD_SYMBOL: '🇬🇹',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_g_with_regional_indicator_symbol_letter_n': {
                FIELD_SYMBOL: '🇬🇳',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_g_with_regional_indicator_symbol_letter_w': {
                FIELD_SYMBOL: '🇬🇼',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_g_with_regional_indicator_symbol_letter_q': {
                FIELD_SYMBOL: '🇬🇶',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_h_with_regional_indicator_symbol_letter_t': {
                FIELD_SYMBOL: '🇭🇹',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_e_with_regional_indicator_symbol_letter_s': {
                FIELD_SYMBOL: '🇪🇸',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_n_with_regional_indicator_symbol_letter_l': {
                FIELD_SYMBOL: '🇳🇱',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_h_with_regional_indicator_symbol_letter_n': {
                FIELD_SYMBOL: '🇭🇳',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_h_with_regional_indicator_symbol_letter_k': {
                FIELD_SYMBOL: '🇭🇰',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_i_with_regional_indicator_symbol_letter_n': {
                FIELD_SYMBOL: '🇮🇳',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_i_with_regional_indicator_symbol_letter_d': {
                FIELD_SYMBOL: '🇮🇩',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_i_with_regional_indicator_symbol_letter_q': {
                FIELD_SYMBOL: '🇮🇶',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_i_with_regional_indicator_symbol_letter_r': {
                FIELD_SYMBOL: '🇮🇷',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_i_with_regional_indicator_symbol_letter_e': {
                FIELD_SYMBOL: '🇮🇪',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_i_with_regional_indicator_symbol_letter_s': {
                FIELD_SYMBOL: '🇮🇸',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_i_with_regional_indicator_symbol_letter_l': {
                FIELD_SYMBOL: '🇮🇱',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_j_with_regional_indicator_symbol_letter_m': {
                FIELD_SYMBOL: '🇯🇲',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_j_with_regional_indicator_symbol_letter_p': {
                FIELD_SYMBOL: '🇯🇵',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'crossed_flags': {
                FIELD_SYMBOL: '🎌',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_y_with_regional_indicator_symbol_letter_e': {
                FIELD_SYMBOL: '🇾🇪',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_j_with_regional_indicator_symbol_letter_e': {
                FIELD_SYMBOL: '🇯🇪',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_j_with_regional_indicator_symbol_letter_o': {
                FIELD_SYMBOL: '🇯🇴',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_k_with_regional_indicator_symbol_letter_y': {
                FIELD_SYMBOL: '🇰🇾',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_k_with_regional_indicator_symbol_letter_h': {
                FIELD_SYMBOL: '🇰🇭',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_c_with_regional_indicator_symbol_letter_m': {
                FIELD_SYMBOL: '🇨🇲',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_c_with_regional_indicator_symbol_letter_a': {
                FIELD_SYMBOL: '🇨🇦',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_q_with_regional_indicator_symbol_letter_a': {
                FIELD_SYMBOL: '🇶🇦',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_k_with_regional_indicator_symbol_letter_z': {
                FIELD_SYMBOL: '🇰🇿',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_k_with_regional_indicator_symbol_letter_e': {
                FIELD_SYMBOL: '🇰🇪',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_k_with_regional_indicator_symbol_letter_g': {
                FIELD_SYMBOL: '🇰🇬',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_k_with_regional_indicator_symbol_letter_i': {
                FIELD_SYMBOL: '🇰🇮',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_c_with_regional_indicator_symbol_letter_o': {
                FIELD_SYMBOL: '🇨🇴',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_k_with_regional_indicator_symbol_letter_m': {
                FIELD_SYMBOL: '🇰🇲',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_c_with_regional_indicator_symbol_letter_g': {
                FIELD_SYMBOL: '🇨🇬',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_k_with_regional_indicator_symbol_letter_r': {
                FIELD_SYMBOL: '🇰🇷',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_k_with_regional_indicator_symbol_letter_p': {
                FIELD_SYMBOL: '🇰🇵',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_x_with_regional_indicator_symbol_letter_k': {
                FIELD_SYMBOL: '🇽🇰',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_c_with_regional_indicator_symbol_letter_r': {
                FIELD_SYMBOL: '🇨🇷',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_c_with_regional_indicator_symbol_letter_u': {
                FIELD_SYMBOL: '🇨🇺',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_k_with_regional_indicator_symbol_letter_w': {
                FIELD_SYMBOL: '🇰🇼',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_l_with_regional_indicator_symbol_letter_a': {
                FIELD_SYMBOL: '🇱🇦',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_l_with_regional_indicator_symbol_letter_s': {
                FIELD_SYMBOL: '🇱🇸',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_l_with_regional_indicator_symbol_letter_b': {
                FIELD_SYMBOL: '🇱🇧',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_l_with_regional_indicator_symbol_letter_r': {
                FIELD_SYMBOL: '🇱🇷',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_l_with_regional_indicator_symbol_letter_y': {
                FIELD_SYMBOL: '🇱🇾',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_l_with_regional_indicator_symbol_letter_i': {
                FIELD_SYMBOL: '🇱🇮',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_l_with_regional_indicator_symbol_letter_t': {
                FIELD_SYMBOL: '🇱🇹',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_l_with_regional_indicator_symbol_letter_u': {
                FIELD_SYMBOL: '🇱🇺',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_l_with_regional_indicator_symbol_letter_v': {
                FIELD_SYMBOL: '🇱🇻',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_m_with_regional_indicator_symbol_letter_k': {
                FIELD_SYMBOL: '🇲🇰',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_m_with_regional_indicator_symbol_letter_g': {
                FIELD_SYMBOL: '🇲🇬',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_y_with_regional_indicator_symbol_letter_t': {
                FIELD_SYMBOL: '🇾🇹',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_m_with_regional_indicator_symbol_letter_o': {
                FIELD_SYMBOL: '🇲🇴',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_m_with_regional_indicator_symbol_letter_w': {
                FIELD_SYMBOL: '🇲🇼',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_m_with_regional_indicator_symbol_letter_v': {
                FIELD_SYMBOL: '🇲🇻',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_m_with_regional_indicator_symbol_letter_y': {
                FIELD_SYMBOL: '🇲🇾',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_m_with_regional_indicator_symbol_letter_l': {
                FIELD_SYMBOL: '🇲🇱',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_m_with_regional_indicator_symbol_letter_t': {
                FIELD_SYMBOL: '🇲🇹',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_m_with_regional_indicator_symbol_letter_p': {
                FIELD_SYMBOL: '🇲🇵',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_m_with_regional_indicator_symbol_letter_a': {
                FIELD_SYMBOL: '🇲🇦',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_m_with_regional_indicator_symbol_letter_q': {
                FIELD_SYMBOL: '🇲🇶',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_m_with_regional_indicator_symbol_letter_r': {
                FIELD_SYMBOL: '🇲🇷',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_m_with_regional_indicator_symbol_letter_u': {
                FIELD_SYMBOL: '🇲🇺',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_m_with_regional_indicator_symbol_letter_x': {
                FIELD_SYMBOL: '🇲🇽',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_f_with_regional_indicator_symbol_letter_m': {
                FIELD_SYMBOL: '🇫🇲',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_m_with_regional_indicator_symbol_letter_m': {
                FIELD_SYMBOL: '🇲🇲',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_m_with_regional_indicator_symbol_letter_d': {
                FIELD_SYMBOL: '🇲🇩',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_m_with_regional_indicator_symbol_letter_c': {
                FIELD_SYMBOL: '🇲🇨',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_m_with_regional_indicator_symbol_letter_n': {
                FIELD_SYMBOL: '🇲🇳',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_m_with_regional_indicator_symbol_letter_s': {
                FIELD_SYMBOL: '🇲🇸',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_m_with_regional_indicator_symbol_letter_z': {
                FIELD_SYMBOL: '🇲🇿',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_n_with_regional_indicator_symbol_letter_a': {
                FIELD_SYMBOL: '🇳🇦',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_n_with_regional_indicator_symbol_letter_r': {
                FIELD_SYMBOL: '🇳🇷',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_n_with_regional_indicator_symbol_letter_p': {
                FIELD_SYMBOL: '🇳🇵',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_b_with_regional_indicator_symbol_letter_q': {
                FIELD_SYMBOL: '🇧🇶',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_d_with_regional_indicator_symbol_letter_e': {
                FIELD_SYMBOL: '🇩🇪',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_n_with_regional_indicator_symbol_letter_e': {
                FIELD_SYMBOL: '🇳🇪',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_n_with_regional_indicator_symbol_letter_g': {
                FIELD_SYMBOL: '🇳🇬',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_n_with_regional_indicator_symbol_letter_i': {
                FIELD_SYMBOL: '🇳🇮',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_n_with_regional_indicator_symbol_letter_u': {
                FIELD_SYMBOL: '🇳🇺',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_n_with_regional_indicator_symbol_letter_f': {
                FIELD_SYMBOL: '🇳🇫',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_n_with_regional_indicator_symbol_letter_o': {
                FIELD_SYMBOL: '🇳🇴',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_n_with_regional_indicator_symbol_letter_c': {
                FIELD_SYMBOL: '🇳🇨',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_n_with_regional_indicator_symbol_letter_z': {
                FIELD_SYMBOL: '🇳🇿',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_o_with_regional_indicator_symbol_letter_m': {
                FIELD_SYMBOL: '🇴🇲',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_p_with_regional_indicator_symbol_letter_k': {
                FIELD_SYMBOL: '🇵🇰',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_p_with_regional_indicator_symbol_letter_w': {
                FIELD_SYMBOL: '🇵🇼',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_p_with_regional_indicator_symbol_letter_a': {
                FIELD_SYMBOL: '🇵🇦',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_p_with_regional_indicator_symbol_letter_g': {
                FIELD_SYMBOL: '🇵🇬',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_p_with_regional_indicator_symbol_letter_y': {
                FIELD_SYMBOL: '🇵🇾',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_p_with_regional_indicator_symbol_letter_e': {
                FIELD_SYMBOL: '🇵🇪',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_p_with_regional_indicator_symbol_letter_n': {
                FIELD_SYMBOL: '🇵🇳',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_p_with_regional_indicator_symbol_letter_f': {
                FIELD_SYMBOL: '🇵🇫',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_p_with_regional_indicator_symbol_letter_l': {
                FIELD_SYMBOL: '🇵🇱',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_p_with_regional_indicator_symbol_letter_r': {
                FIELD_SYMBOL: '🇵🇷',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_p_with_regional_indicator_symbol_letter_t': {
                FIELD_SYMBOL: '🇵🇹',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_z_with_regional_indicator_symbol_letter_a': {
                FIELD_SYMBOL: '🇿🇦',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_c_with_regional_indicator_symbol_letter_f': {
                FIELD_SYMBOL: '🇨🇫',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_c_with_regional_indicator_symbol_letter_v': {
                FIELD_SYMBOL: '🇨🇻',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_r_with_regional_indicator_symbol_letter_e': {
                FIELD_SYMBOL: '🇷🇪',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_r_with_regional_indicator_symbol_letter_u': {
                FIELD_SYMBOL: '🇷🇺',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_r_with_regional_indicator_symbol_letter_o': {
                FIELD_SYMBOL: '🇷🇴',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_r_with_regional_indicator_symbol_letter_w': {
                FIELD_SYMBOL: '🇷🇼',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_e_with_regional_indicator_symbol_letter_h': {
                FIELD_SYMBOL: '🇪🇭',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_k_with_regional_indicator_symbol_letter_n': {
                FIELD_SYMBOL: '🇰🇳',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_l_with_regional_indicator_symbol_letter_c': {
                FIELD_SYMBOL: '🇱🇨',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_v_with_regional_indicator_symbol_letter_c': {
                FIELD_SYMBOL: '🇻🇨',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_b_with_regional_indicator_symbol_letter_l': {
                FIELD_SYMBOL: '🇧🇱',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_p_with_regional_indicator_symbol_letter_m': {
                FIELD_SYMBOL: '🇵🇲',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_s_with_regional_indicator_symbol_letter_v': {
                FIELD_SYMBOL: '🇸🇻',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_w_with_regional_indicator_symbol_letter_s': {
                FIELD_SYMBOL: '🇼🇸',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_a_with_regional_indicator_symbol_letter_s': {
                FIELD_SYMBOL: '🇦🇸',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_s_with_regional_indicator_symbol_letter_m': {
                FIELD_SYMBOL: '🇸🇲',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_c_with_regional_indicator_symbol_letter_q': {
                FIELD_SYMBOL: '🇨🇶',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_s_with_regional_indicator_symbol_letter_n': {
                FIELD_SYMBOL: '🇸🇳',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_r_with_regional_indicator_symbol_letter_s': {
                FIELD_SYMBOL: '🇷🇸',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_s_with_regional_indicator_symbol_letter_c': {
                FIELD_SYMBOL: '🇸🇨',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_s_with_regional_indicator_symbol_letter_l': {
                FIELD_SYMBOL: '🇸🇱',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_s_with_regional_indicator_symbol_letter_g': {
                FIELD_SYMBOL: '🇸🇬',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_s_with_regional_indicator_symbol_letter_x': {
                FIELD_SYMBOL: '🇸🇽',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_s_with_regional_indicator_symbol_letter_k': {
                FIELD_SYMBOL: '🇸🇰',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_s_with_regional_indicator_symbol_letter_i': {
                FIELD_SYMBOL: '🇸🇮',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_s_with_regional_indicator_symbol_letter_o': {
                FIELD_SYMBOL: '🇸🇴',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_l_with_regional_indicator_symbol_letter_k': {
                FIELD_SYMBOL: '🇱🇰',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_u_with_regional_indicator_symbol_letter_s': {
                FIELD_SYMBOL: '🇺🇸',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_s_with_regional_indicator_symbol_letter_d': {
                FIELD_SYMBOL: '🇸🇩',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_s_with_regional_indicator_symbol_letter_s': {
                FIELD_SYMBOL: '🇸🇸',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_s_with_regional_indicator_symbol_letter_r': {
                FIELD_SYMBOL: '🇸🇷',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_s_with_regional_indicator_symbol_letter_y': {
                FIELD_SYMBOL: '🇸🇾',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_c_with_regional_indicator_symbol_letter_h': {
                FIELD_SYMBOL: '🇨🇭',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_s_with_regional_indicator_symbol_letter_e': {
                FIELD_SYMBOL: '🇸🇪',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_t_with_regional_indicator_symbol_letter_j': {
                FIELD_SYMBOL: '🇹🇯',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_t_with_regional_indicator_symbol_letter_h': {
                FIELD_SYMBOL: '🇹🇭',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_t_with_regional_indicator_symbol_letter_w': {
                FIELD_SYMBOL: '🇹🇼',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_t_with_regional_indicator_symbol_letter_z': {
                FIELD_SYMBOL: '🇹🇿',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_p_with_regional_indicator_symbol_letter_s': {
                FIELD_SYMBOL: '🇵🇸',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_t_with_regional_indicator_symbol_letter_l': {
                FIELD_SYMBOL: '🇹🇱',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_t_with_regional_indicator_symbol_letter_g': {
                FIELD_SYMBOL: '🇹🇬',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_t_with_regional_indicator_symbol_letter_k': {
                FIELD_SYMBOL: '🇹🇰',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_t_with_regional_indicator_symbol_letter_o': {
                FIELD_SYMBOL: '🇹🇴',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_t_with_regional_indicator_symbol_letter_t': {
                FIELD_SYMBOL: '🇹🇹',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_t_with_regional_indicator_symbol_letter_n': {
                FIELD_SYMBOL: '🇹🇳',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_t_with_regional_indicator_symbol_letter_r': {
                FIELD_SYMBOL: '🇹🇷',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_t_with_regional_indicator_symbol_letter_m': {
                FIELD_SYMBOL: '🇹🇲',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_t_with_regional_indicator_symbol_letter_c': {
                FIELD_SYMBOL: '🇹🇨',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_t_with_regional_indicator_symbol_letter_v': {
                FIELD_SYMBOL: '🇹🇻',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_u_with_regional_indicator_symbol_letter_g': {
                FIELD_SYMBOL: '🇺🇬',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_u_with_regional_indicator_symbol_letter_a': {
                FIELD_SYMBOL: '🇺🇦',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_e_with_regional_indicator_symbol_letter_u': {
                FIELD_SYMBOL: '🇪🇺',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_u_with_regional_indicator_symbol_letter_y': {
                FIELD_SYMBOL: '🇺🇾',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_u_with_regional_indicator_symbol_letter_z': {
                FIELD_SYMBOL: '🇺🇿',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_v_with_regional_indicator_symbol_letter_u': {
                FIELD_SYMBOL: '🇻🇺',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_w_with_regional_indicator_symbol_letter_f': {
                FIELD_SYMBOL: '🇼🇫',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_v_with_regional_indicator_symbol_letter_a': {
                FIELD_SYMBOL: '🇻🇦',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_v_with_regional_indicator_symbol_letter_e': {
                FIELD_SYMBOL: '🇻🇪',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_h_with_regional_indicator_symbol_letter_u': {
                FIELD_SYMBOL: '🇭🇺',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_g_with_regional_indicator_symbol_letter_b': {
                FIELD_SYMBOL: '🇬🇧',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'waving_black_flag_with_tag_latin_small_letter_g_with_tag_latin_small_letter_b_with_tag_latin_small_letter_e_with_tag_latin_small_letter_n_with_tag_latin_small_letter_g_with_cancel_tag': {
                FIELD_SYMBOL: '🏴󠁧󠁢󠁥󠁮󠁧󠁿',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'waving_black_flag_with_tag_latin_small_letter_g_with_tag_latin_small_letter_b_with_tag_latin_small_letter_s_with_tag_latin_small_letter_c_with_tag_latin_small_letter_t_with_cancel_tag': {
                FIELD_SYMBOL: '🏴󠁧󠁢󠁳󠁣󠁴󠁿',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'waving_black_flag_with_tag_latin_small_letter_g_with_tag_latin_small_letter_b_with_tag_latin_small_letter_w_with_tag_latin_small_letter_l_with_tag_latin_small_letter_s_with_cancel_tag': {
                FIELD_SYMBOL: '🏴󠁧󠁢󠁷󠁬󠁳󠁿',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_v_with_regional_indicator_symbol_letter_n': {
                FIELD_SYMBOL: '🇻🇳',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_i_with_regional_indicator_symbol_letter_t': {
                FIELD_SYMBOL: '🇮🇹',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_c_with_regional_indicator_symbol_letter_x': {
                FIELD_SYMBOL: '🇨🇽',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_i_with_regional_indicator_symbol_letter_m': {
                FIELD_SYMBOL: '🇮🇲',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_s_with_regional_indicator_symbol_letter_h': {
                FIELD_SYMBOL: '🇸🇭',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_a_with_regional_indicator_symbol_letter_x': {
                FIELD_SYMBOL: '🇦🇽',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_c_with_regional_indicator_symbol_letter_k': {
                FIELD_SYMBOL: '🇨🇰',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_v_with_regional_indicator_symbol_letter_i': {
                FIELD_SYMBOL: '🇻🇮',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_i_with_regional_indicator_symbol_letter_c': {
                FIELD_SYMBOL: '🇮🇨',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_c_with_regional_indicator_symbol_letter_c': {
                FIELD_SYMBOL: '🇨🇨',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_m_with_regional_indicator_symbol_letter_h': {
                FIELD_SYMBOL: '🇲🇭',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_f_with_regional_indicator_symbol_letter_o': {
                FIELD_SYMBOL: '🇫🇴',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_s_with_regional_indicator_symbol_letter_b': {
                FIELD_SYMBOL: '🇸🇧',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_s_with_regional_indicator_symbol_letter_t': {
                FIELD_SYMBOL: '🇸🇹',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_z_with_regional_indicator_symbol_letter_m': {
                FIELD_SYMBOL: '🇿🇲',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_z_with_regional_indicator_symbol_letter_w': {
                FIELD_SYMBOL: '🇿🇼',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_a_with_regional_indicator_symbol_letter_e': {
                FIELD_SYMBOL: '🇦🇪',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
        },
        SYMBOLS: {
            'pink_heart': {
                FIELD_SYMBOL: '🩷',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'heavy_black_heart': {
                FIELD_SYMBOL: '❤️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'orange_heart': {
                FIELD_SYMBOL: '🧡',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'yellow_heart': {
                FIELD_SYMBOL: '💛',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'green_heart': {
                FIELD_SYMBOL: '💚',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'light_blue_heart': {
                FIELD_SYMBOL: '🩵',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'blue_heart': {
                FIELD_SYMBOL: '💙',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'purple_heart': {
                FIELD_SYMBOL: '💜',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'black_heart': {
                FIELD_SYMBOL: '🖤',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'grey_heart': {
                FIELD_SYMBOL: '🩶',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'white_heart': {
                FIELD_SYMBOL: '🤍',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'brown_heart': {
                FIELD_SYMBOL: '🤎',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'broken_heart': {
                FIELD_SYMBOL: '💔',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'heavy_black_heart_with_fire': {
                FIELD_SYMBOL: '❤️‍🔥',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'heavy_black_heart_with_adhesive_bandage': {
                FIELD_SYMBOL: '❤️‍🩹',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'heavy_heart_exclamation_mark_ornament': {
                FIELD_SYMBOL: '❣️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'two_hearts': {
                FIELD_SYMBOL: '💕',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'revolving_hearts': {
                FIELD_SYMBOL: '💞',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'beating_heart': {
                FIELD_SYMBOL: '💓',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'growing_heart': {
                FIELD_SYMBOL: '💗',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'sparkling_heart': {
                FIELD_SYMBOL: '💖',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'heart_with_arrow': {
                FIELD_SYMBOL: '💘',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'heart_with_ribbon': {
                FIELD_SYMBOL: '💝',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
        },
        AV_SYMBOLS: {
            'mobile_phone_off': {
                FIELD_SYMBOL: '📴',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'vibration_mode': {
                FIELD_SYMBOL: '📳',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'low_brightness_symbol': {
                FIELD_SYMBOL: '🔅',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'high_brightness_symbol': {
                FIELD_SYMBOL: '🔆',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'wireless': {
                FIELD_SYMBOL: '🛜',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'cinema': {
                FIELD_SYMBOL: '🎦',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'antenna_with_bars': {
                FIELD_SYMBOL: '📶',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'eject_symbol': {
                FIELD_SYMBOL: '⏏️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'black_right_pointing_triangle': {
                FIELD_SYMBOL: '▶️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'double_vertical_bar': {
                FIELD_SYMBOL: '⏸️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'black_right_pointing_triangle_with_double_vertical_bar': {
                FIELD_SYMBOL: '⏯️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'black_square_for_stop': {
                FIELD_SYMBOL: '⏹️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'black_circle_for_record': {
                FIELD_SYMBOL: '⏺️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'black_right_pointing_double_triangle_with_vertical_bar': {
                FIELD_SYMBOL: '⏭️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'black_left_pointing_double_triangle_with_vertical_bar': {
                FIELD_SYMBOL: '⏮️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'black_right_pointing_double_triangle': {
                FIELD_SYMBOL: '⏩️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'black_left_pointing_double_triangle': {
                FIELD_SYMBOL: '⏪️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'black_up_pointing_double_triangle': {
                FIELD_SYMBOL: '⏫️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'black_down_pointing_double_triangle': {
                FIELD_SYMBOL: '⏬️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'black_left_pointing_triangle': {
                FIELD_SYMBOL: '◀️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'up_pointing_small_red_triangle': {
                FIELD_SYMBOL: '🔼',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'down_pointing_small_red_triangle': {
                FIELD_SYMBOL: '🔽',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'twisted_rightwards_arrows': {
                FIELD_SYMBOL: '🔀',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'clockwise_rightwards_and_leftwards_open_circle_arrows': {
                FIELD_SYMBOL: '🔁',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'clockwise_rightwards_and_leftwards_open_circle_arrows_with_circled_one_overlay': {
                FIELD_SYMBOL: '🔂',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
        },
        MATHEMATICAL_SYMBOLS: {
            'heavy_plus_sign': {
                FIELD_SYMBOL: '➕',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'heavy_minus_sign': {
                FIELD_SYMBOL: '➖',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'heavy_division_sign': {
                FIELD_SYMBOL: '➗',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'heavy_multiplication_x': {
                FIELD_SYMBOL: '✖️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'heavy_equals_sign': {
                FIELD_SYMBOL: '🟰',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'permanent_paper_sign': {
                FIELD_SYMBOL: '♾️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
        },
        RELIGIOUS_SYMBOLS: {
            'peace_symbol': {
                FIELD_SYMBOL: '☮️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'latin_cross': {
                FIELD_SYMBOL: '✝️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'star_and_crescent': {
                FIELD_SYMBOL: '☪️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'om_symbol': {
                FIELD_SYMBOL: '🕉️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'wheel_of_dharma': {
                FIELD_SYMBOL: '☸️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'khanda': {
                FIELD_SYMBOL: '🪯',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'star_of_david': {
                FIELD_SYMBOL: '✡️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'six_pointed_star_with_middle_dot': {
                FIELD_SYMBOL: '🔯',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'menorah_with_nine_branches': {
                FIELD_SYMBOL: '🕎',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'yin_yang': {
                FIELD_SYMBOL: '☯️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'orthodox_cross': {
                FIELD_SYMBOL: '☦️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'place_of_worship': {
                FIELD_SYMBOL: '🛐',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
        },
        OTHER_SYMBOLS: {
            'heart_decoration': {
                FIELD_SYMBOL: '💟',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'ophiuchus': {
                FIELD_SYMBOL: '⛎',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'atom_symbol': {
                FIELD_SYMBOL: '⚛️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'eight_pointed_black_star': {
                FIELD_SYMBOL: '✴️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'white_flower': {
                FIELD_SYMBOL: '💮',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'cross_mark': {
                FIELD_SYMBOL: '❌',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'heavy_large_circle': {
                FIELD_SYMBOL: '⭕️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'octagonal_sign': {
                FIELD_SYMBOL: '🛑️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'name_badge': {
                FIELD_SYMBOL: '📛',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'hundred_points_symbol': {
                FIELD_SYMBOL: '💯',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'anger_symbol': {
                FIELD_SYMBOL: '💢',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'hot_springs': {
                FIELD_SYMBOL: '♨️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'part_alternation_mark': {
                FIELD_SYMBOL: '〽️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'children_crossing': {
                FIELD_SYMBOL: '🚸',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'trident_emblem': {
                FIELD_SYMBOL: '🔱',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'fleur_de_lis': {
                FIELD_SYMBOL: '⚜️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'japanese_symbol_for_beginner': {
                FIELD_SYMBOL: '🔰',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'black_universal_recycling_symbol': {
                FIELD_SYMBOL: '♻️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'white_heavy_check_mark': {
                FIELD_SYMBOL: '✅',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'sparkle': {
                FIELD_SYMBOL: '❇️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'eight_spoked_asterisk': {
                FIELD_SYMBOL: '✳️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'negative_squared_cross_mark': {
                FIELD_SYMBOL: '❎',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'globe_with_meridians': {
                FIELD_SYMBOL: '🌐',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'diamond_shape_with_a_dot_inside': {
                FIELD_SYMBOL: '💠',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'cyclone': {
                FIELD_SYMBOL: '🌀',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'sleeping_symbol': {
                FIELD_SYMBOL: '💤️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'elevator': {
                FIELD_SYMBOL: '🛗',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'adult_with_adult_with_child': {
                FIELD_SYMBOL: '🧑‍🧑‍🧒',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'adult_with_adult_with_child_with_child': {
                FIELD_SYMBOL: '🧑‍🧑‍🧒‍🧒',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'adult_with_child': {
                FIELD_SYMBOL: '🧑‍🧒',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'adult_with_child_with_child': {
                FIELD_SYMBOL: '🧑‍🧒‍🧒',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'male_with_stroke_and_male_and_female_sign': {
                FIELD_SYMBOL: '⚧️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'squared_katakana_koko': {
                FIELD_SYMBOL: '🈁',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'eye_with_left_speech_bubble': {
                FIELD_SYMBOL: '👁️‍🗨️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'wavy_dash': {
                FIELD_SYMBOL: '〰️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'curly_loop': {
                FIELD_SYMBOL: '➰',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'double_curly_loop': {
                FIELD_SYMBOL: '➿',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'heavy_check_mark': {
                FIELD_SYMBOL: '✔️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'ballot_box_with_check': {
                FIELD_SYMBOL: '☑️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'radio_button': {
                FIELD_SYMBOL: '🔘',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'speech_balloon': {
                FIELD_SYMBOL: '💬',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'thought_balloon': {
                FIELD_SYMBOL: '💭',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'right_anger_bubble': {
                FIELD_SYMBOL: '🗯️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
        },
        ZODIAC_SIGNS: {
            'aries': {
                FIELD_SYMBOL: '♈️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'taurus': {
                FIELD_SYMBOL: '♉️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'gemini': {
                FIELD_SYMBOL: '♊️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'cancer': {
                FIELD_SYMBOL: '♋️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'leo': {
                FIELD_SYMBOL: '♌️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'virgo': {
                FIELD_SYMBOL: '♍️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'libra': {
                FIELD_SYMBOL: '♎️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'scorpius': {
                FIELD_SYMBOL: '♏️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'sagittarius': {
                FIELD_SYMBOL: '♐️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'capricorn': {
                FIELD_SYMBOL: '♑️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'aquarius': {
                FIELD_SYMBOL: '♒️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'pisces': {
                FIELD_SYMBOL: '♓️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
        },
        WARNING_SIGNS: {
            'radioactive_sign': {
                FIELD_SYMBOL: '☢️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'biohazard_sign': {
                FIELD_SYMBOL: '☣️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'warning_sign': {
                FIELD_SYMBOL: '⚠️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'no_entry': {
                FIELD_SYMBOL: '⛔',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'no_entry_sign': {
                FIELD_SYMBOL: '🚫',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'no_pedestrians': {
                FIELD_SYMBOL: '🚷',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'do_not_litter_symbol': {
                FIELD_SYMBOL: '🚯',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'no_bicycles': {
                FIELD_SYMBOL: '🚳',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'non_potable_water_symbol': {
                FIELD_SYMBOL: '🚱',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'no_one_under_eighteen_symbol': {
                FIELD_SYMBOL: '🔞',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'no_mobile_phones': {
                FIELD_SYMBOL: '📵',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'no_smoking_symbol': {
                FIELD_SYMBOL: '🚭',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
        },
        ARROW_SIGNS: {
            'black_rightwards_arrow': {
                FIELD_SYMBOL: '➡️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'leftwards_black_arrow': {
                FIELD_SYMBOL: '⬅️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'upwards_black_arrow': {
                FIELD_SYMBOL: '⬆️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'downwards_black_arrow': {
                FIELD_SYMBOL: '⬇️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'north_east_arrow': {
                FIELD_SYMBOL: '↗️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'south_east_arrow': {
                FIELD_SYMBOL: '↘️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'south_west_arrow': {
                FIELD_SYMBOL: '↙️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'north_west_arrow': {
                FIELD_SYMBOL: '↖️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'up_down_arrow': {
                FIELD_SYMBOL: '↕️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'left_right_arrow': {
                FIELD_SYMBOL: '↔️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'rightwards_arrow_with_hook': {
                FIELD_SYMBOL: '↪️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'leftwards_arrow_with_hook': {
                FIELD_SYMBOL: '↩️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'arrow_pointing_rightwards_then_curving_upwards': {
                FIELD_SYMBOL: '⤴️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'arrow_pointing_rightwards_then_curving_downwards': {
                FIELD_SYMBOL: '⤵️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'anticlockwise_downwards_and_upwards_open_circle_arrows': {
                FIELD_SYMBOL: '🔄',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'clockwise_downwards_and_upwards_open_circle_arrows': {
                FIELD_SYMBOL: '🔃',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'end_with_leftwards_arrow_above': {
                FIELD_SYMBOL: '🔚',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'back_with_leftwards_arrow_above': {
                FIELD_SYMBOL: '🔙',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'on_with_exclamation_mark_with_left_right_arrow_above': {
                FIELD_SYMBOL: '🔛',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'top_with_upwards_arrow_above': {
                FIELD_SYMBOL: '🔝',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'soon_with_rightwards_arrow_above': {
                FIELD_SYMBOL: '🔜',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
        },
        TRANSPORT_SIGNS: {
            'automated_teller_machine': {
                FIELD_SYMBOL: '🏧',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'baby_symbol': {
                FIELD_SYMBOL: '🚼',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'restroom': {
                FIELD_SYMBOL: '🚻',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'mens_symbol': {
                FIELD_SYMBOL: '🚹',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'womens_symbol': {
                FIELD_SYMBOL: '🚺',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'put_litter_in_its_place_symbol': {
                FIELD_SYMBOL: '🚮',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'left_luggage': {
                FIELD_SYMBOL: '🛅',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'baggage_claim': {
                FIELD_SYMBOL: '🛄',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'passport_control': {
                FIELD_SYMBOL: '🛂',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'customs': {
                FIELD_SYMBOL: '🛃',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'water_closet': {
                FIELD_SYMBOL: '🚾',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'wheelchair_symbol': {
                FIELD_SYMBOL: '♿',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
        },
        ALPHANUMERIC_SIGNS: {
            'squared_id': {
                FIELD_SYMBOL: '🆔',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'circled_ideograph_accept': {
                FIELD_SYMBOL: '🉑',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'squared_cjk_unified_ideograph_6709': {
                FIELD_SYMBOL: '🈶',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'squared_cjk_unified_ideograph_7121': {
                FIELD_SYMBOL: '🈚️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'squared_cjk_unified_ideograph_7533': {
                FIELD_SYMBOL: '🈸',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'squared_cjk_unified_ideograph_55b6': {
                FIELD_SYMBOL: '🈺',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'squared_cjk_unified_ideograph_6708': {
                FIELD_SYMBOL: '🈷️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'squared_vs': {
                FIELD_SYMBOL: '🆚',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'circled_ideograph_advantage': {
                FIELD_SYMBOL: '🉐',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'circled_ideograph_secret': {
                FIELD_SYMBOL: '㊙️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'circled_ideograph_congratulation': {
                FIELD_SYMBOL: '㊗️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'squared_cjk_unified_ideograph_5408': {
                FIELD_SYMBOL: '🈴',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'squared_cjk_unified_ideograph_6e80': {
                FIELD_SYMBOL: '🈵',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'squared_cjk_unified_ideograph_5272': {
                FIELD_SYMBOL: '🈹',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'squared_cjk_unified_ideograph_7981': {
                FIELD_SYMBOL: '🈲',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'negative_squared_latin_capital_letter_a': {
                FIELD_SYMBOL: '🅰️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'negative_squared_latin_capital_letter_b': {
                FIELD_SYMBOL: '🅱️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'negative_squared_ab': {
                FIELD_SYMBOL: '🆎',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'squared_cl': {
                FIELD_SYMBOL: '🆑',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'negative_squared_latin_capital_letter_o': {
                FIELD_SYMBOL: '🅾️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'squared_sos': {
                FIELD_SYMBOL: '🆘',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'squared_cjk_unified_ideograph_6307': {
                FIELD_SYMBOL: '🈯️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'circled_latin_capital_letter_m': {
                FIELD_SYMBOL: 'Ⓜ️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'negative_squared_latin_capital_letter_p': {
                FIELD_SYMBOL: '🅿️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'squared_cjk_unified_ideograph_7a7a': {
                FIELD_SYMBOL: '🈳',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'squared_katakana_sa': {
                FIELD_SYMBOL: '🈂️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'input_symbol_for_symbols': {
                FIELD_SYMBOL: '🔣',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'information_source': {
                FIELD_SYMBOL: 'ℹ️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'input_symbol_for_latin_letters': {
                FIELD_SYMBOL: '🔤',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'input_symbol_for_latin_small_letters': {
                FIELD_SYMBOL: '🔡',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'input_symbol_for_latin_capital_letters': {
                FIELD_SYMBOL: '🔠',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'squared_ng': {
                FIELD_SYMBOL: '🆖',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'squared_ok': {
                FIELD_SYMBOL: '🆗',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'squared_up_with_exclamation_mark': {
                FIELD_SYMBOL: '🆙',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'squared_cool': {
                FIELD_SYMBOL: '🆒',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'squared_new': {
                FIELD_SYMBOL: '🆕',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'squared_free': {
                FIELD_SYMBOL: '🆓',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'trade_mark_sign': {
                FIELD_SYMBOL: '™️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'copyright_sign': {
                FIELD_SYMBOL: '©️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'registered_sign': {
                FIELD_SYMBOL: '®️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
        },
        NUMERIC_SIGNS: {
            'digit_zero_with_combining_enclosing_keycap': {
                FIELD_SYMBOL: '0️⃣',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'digit_one_with_combining_enclosing_keycap': {
                FIELD_SYMBOL: '1️⃣',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'digit_two_with_combining_enclosing_keycap': {
                FIELD_SYMBOL: '2️⃣',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'digit_three_with_combining_enclosing_keycap': {
                FIELD_SYMBOL: '3️⃣',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'digit_four_with_combining_enclosing_keycap': {
                FIELD_SYMBOL: '4️⃣',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'digit_five_with_combining_enclosing_keycap': {
                FIELD_SYMBOL: '5️⃣',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'digit_six_with_combining_enclosing_keycap': {
                FIELD_SYMBOL: '6️⃣',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'digit_seven_with_combining_enclosing_keycap': {
                FIELD_SYMBOL: '7️⃣',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'digit_eight_with_combining_enclosing_keycap': {
                FIELD_SYMBOL: '8️⃣',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'digit_nine_with_combining_enclosing_keycap': {
                FIELD_SYMBOL: '9️⃣',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'keycap_ten': {
                FIELD_SYMBOL: '🔟',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'input_symbol_for_numbers': {
                FIELD_SYMBOL: '🔢',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'number_sign_with_combining_enclosing_keycap': {
                FIELD_SYMBOL: '#️⃣',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'asterisk_with_combining_enclosing_keycap': {
                FIELD_SYMBOL: '*️⃣',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
        },
        PUNCTUATION_SIGNS: {
            'heavy_exclamation_mark_symbol': {
                FIELD_SYMBOL: '❗️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'white_exclamation_mark_ornament': {
                FIELD_SYMBOL: '❕',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'black_question_mark_ornament': {
                FIELD_SYMBOL: '❓',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'white_question_mark_ornament': {
                FIELD_SYMBOL: '❔',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'double_exclamation_mark': {
                FIELD_SYMBOL: '‼️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'exclamation_question_mark': {
                FIELD_SYMBOL: '⁉️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
        },
        GEOMETRIC_SIGNS: {
            'large_red_circle': {
                FIELD_SYMBOL: '🔴',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'large_orange_circle': {
                FIELD_SYMBOL: '🟠',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'large_yellow_circle': {
                FIELD_SYMBOL: '🟡',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'large_green_circle': {
                FIELD_SYMBOL: '🟢',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'large_blue_circle': {
                FIELD_SYMBOL: '🔵',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'large_purple_circle': {
                FIELD_SYMBOL: '🟣',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'medium_black_circle': {
                FIELD_SYMBOL: '⚫️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'medium_white_circle': {
                FIELD_SYMBOL: '⚪️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'large_brown_circle': {
                FIELD_SYMBOL: '🟤',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'up_pointing_red_triangle': {
                FIELD_SYMBOL: '🔺',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'down_pointing_red_triangle': {
                FIELD_SYMBOL: '🔻',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'small_orange_diamond': {
                FIELD_SYMBOL: '🔸',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'small_blue_diamond': {
                FIELD_SYMBOL: '🔹',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'large_orange_diamond': {
                FIELD_SYMBOL: '🔶',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'large_blue_diamond': {
                FIELD_SYMBOL: '🔷',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'white_square_button': {
                FIELD_SYMBOL: '🔳',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'black_square_button': {
                FIELD_SYMBOL: '🔲',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'black_small_square': {
                FIELD_SYMBOL: '▪️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'white_small_square': {
                FIELD_SYMBOL: '▫️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'black_medium_small_square': {
                FIELD_SYMBOL: '◾️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'white_medium_small_square': {
                FIELD_SYMBOL: '◽️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'black_medium_square': {
                FIELD_SYMBOL: '◼️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'white_medium_square': {
                FIELD_SYMBOL: '◻️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'large_red_square': {
                FIELD_SYMBOL: '🟥',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'large_orange_square': {
                FIELD_SYMBOL: '🟧',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'large_yellow_square': {
                FIELD_SYMBOL: '🟨',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'large_green_square': {
                FIELD_SYMBOL: '🟩',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'large_blue_square': {
                FIELD_SYMBOL: '🟦',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'large_purple_square': {
                FIELD_SYMBOL: '🟪',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'black_large_square': {
                FIELD_SYMBOL: '⬛️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'white_large_square': {
                FIELD_SYMBOL: '⬜️',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'large_brown_square': {
                FIELD_SYMBOL: '🟫',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
        },
    }

    #region Queries

    @classmethod
    def groups(cls) -> List[str]:
        """Returns available emoji group keys."""
        return list(cls.EMOJIS.keys())

    @staticmethod
    def translation_member(identifier: str) -> str:
        """Converts an English resource identifier to a catalogue-safe key."""
        member = re.sub(r'[^A-Z0-9]+', '_', identifier.upper()).strip('_')
        return f'NUMBER_{member}' if member[:1].isdigit() else member

    @classmethod
    def group_translation_key(cls, group_key: str) -> str:
        """Returns the stable translation key for an emoji group."""
        return f'{cls.GROUP_TRANSLATION_GROUP}.{cls.translation_member(group_key)}'

    @classmethod
    def emoji_translation_key(cls, emoji_key: str) -> str:
        """Returns the stable translation key for one emoji name."""
        return f'{cls.EMOJI_TRANSLATION_GROUP}.{cls.translation_member(emoji_key)}'

    @classmethod
    def get_group_name(cls, group_key: str) -> str:
        """Returns translated group name for display."""
        return (
            LanguageService.translate_current(cls.group_translation_key(group_key))
            if group_key in cls.EMOJIS
            else group_key
        )

    @classmethod
    def get_emoji_name(cls, emoji_key: str) -> str:
        """Returns a translated emoji name for API presentation."""
        return LanguageService.translate_current(cls.emoji_translation_key(emoji_key))

    @classmethod
    def get_group(cls, group_key: str) -> Dict[str, Dict[str, Any]]:
        """Returns emoji presets for the selected group."""
        return cls.EMOJIS.get(group_key, {})

    @classmethod
    def get_group_first_symbol(cls, group_key: str) -> str:
        """Returns the first emoji symbol from the selected group."""
        first = next(iter(cls.get_group(group_key).values()), {})

        return str(first.get(cls.FIELD_SYMBOL, ''))

    @classmethod
    def supports_color(cls, group_key: str) -> bool:
        """Returns whether group contains emoji that support skin color modifiers."""
        return any(
            bool(data.get(cls.FIELD_SUPPORT_COLOR))
            for data in cls.get_group(group_key).values()
        )

    @classmethod
    def supports_sex(cls, group_key: str) -> bool:
        """Returns whether group contains emoji that support sex variants."""
        return any(
            bool(data.get(cls.FIELD_SUPPORT_SEX))
            for data in cls.get_group(group_key).values()
        )

    #endregion Queries

    #region Endpoints

    @classmethod
    def emoji_groups(cls):
        """Returns emoji group metadata for the emoji picker."""
        response = jsonify({
            'status': 'ok',
            'groups': [
                {
                    'key': group_key,
                    'name': cls.get_group_name(group_key),
                    'label': cls.get_group_name(group_key),
                    'emoji': cls.get_group_first_symbol(group_key),
                    'support_color': cls.supports_color(group_key),
                    'support_sex': cls.supports_sex(group_key)
                }
                for group_key in cls.groups()
            ]
        })
        response.headers['Cache-Control'] = 'no-store'

        return response

    @classmethod
    def emojis(cls):
        """Returns emoji presets for the requested group."""
        groups = cls.groups()
        group_key = request.args.get('group', groups[0] if groups else '')
        group_name = cls.get_group_name(group_key)
        response = jsonify({
            'status': 'ok',
            'group': {
                'key': group_key,
                'name': group_name,
                'label': group_name,
                'support_color': cls.supports_color(group_key),
                'support_sex': cls.supports_sex(group_key)
            },
            'emojis': [
                {
                    'key': key,
                    'name': cls.get_emoji_name(key),
                    'label': cls.get_emoji_name(key),
                    'emoji': data.get(cls.FIELD_SYMBOL, ''),
                    'support_color': bool(data.get(cls.FIELD_SUPPORT_COLOR)),
                    'support_sex': bool(data.get(cls.FIELD_SUPPORT_SEX)),
                    'supports_skin_tone': bool(data.get(cls.FIELD_SUPPORT_COLOR)),
                    'supports_gender': bool(data.get(cls.FIELD_SUPPORT_SEX))
                }
                for key, data in cls.get_group(group_key).items()
            ]
        })
        response.headers['Cache-Control'] = 'no-store'

        return response

    #endregion Endpoints

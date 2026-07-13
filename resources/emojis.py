from typing import Any, ClassVar, Dict, List


class Emojis:
    """Stores grouped emoji presets for favourite tags."""

    # https://www.emotikonyznaczenie.pl/lista-buzki-ludzie

    FIELD_SYMBOL: ClassVar[str] = 'symbol'
    FIELD_NAME: ClassVar[str] = 'name'
    FIELD_SUPPORT_COLOR: ClassVar[str] = 'support_color'
    FIELD_SUPPORT_SEX: ClassVar[str] = 'support_sex'

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

    # Group translations
    GROUP_TRANSLATIONS: ClassVar[Dict[str, str]] = {
        EMOTIONS: 'Emocje',
        HANDS: 'Dłonie',
        FACES: 'Twarze',
        BODY_PARTS: 'Części Ciała',
        ACTIVITIES_AND_POSTURES: 'Aktywności i postury',
        CLOTHING_AND_ACCESSORIES: 'Ubrania i akcesoria',
        ANIMALS: 'Zwierzęta',
        NATURE_AND_PLANTS: 'Natura i Rośliny',
        UNIVERSE: 'Wszechświat',
        WEATHER: 'Pogoda',
        FRUITS_AND_VEGETABLES: 'Owoce i Warzywa',
        FOOD_AND_DRINKS: 'Jedzenie i napoje',
        SPORT: 'Sport',
        ART_AND_CULTURE: 'Sztuka i Kultura',
        SOUND_AND_MUSIC: 'Dźwięk i Muzyka',
        TRANSPORT: 'Transport',
        TRAVEL_AND_PLACES: 'Podróże i Miejsca',
        BUILDINGS: 'Budowle',
        ENTERTAINMENT: 'Rozrywka',
        ELECTRONIC_DEVICES: 'Urządzenia Elektroniczne',
        CLOCKS_AND_TIME: 'Zegary i czas',
        MONEY_AND_VALUABLES: 'Pieniądze i kosztowności',
        OBJECTS_AND_TOOLS: 'Przedmioty i Narzędzia',
        SCIENCE_AND_HEALTH: 'Nauka i Zdrowie',
        OFFICE_TOOLS: 'Narzędzia Biurowe',
        FLAGS: 'Flagi',
        SYMBOLS: 'Symbole',
        AV_SYMBOLS: 'Symbole AV',
        MATHEMATICAL_SYMBOLS: 'Symbole Matematyczne',
        RELIGIOUS_SYMBOLS: 'Symbole Religijne',
        OTHER_SYMBOLS: 'Inne Symbole',
        ZODIAC_SIGNS: 'Znaki Zodiaku',
        WARNING_SIGNS: 'Znaki Ostrzegawcze',
        ARROW_SIGNS: 'Znaki Strzałki',
        TRANSPORT_SIGNS: 'Znaki Transportu',
        ALPHANUMERIC_SIGNS: 'Znaki Alfanumeryczne',
        NUMERIC_SIGNS: 'Znaki Liczbowe',
        PUNCTUATION_SIGNS: 'Znaki Interpunkcyjne',
        GEOMETRIC_SIGNS: 'Znaki Geometryczne',
    }

    # Emoji declarations
    EMOJIS: ClassVar[Dict[str, Dict[str, Dict[str, Any]]]] = {
        EMOTIONS: {
            'smiling_face': {
                FIELD_SYMBOL: '😀',
                FIELD_NAME: 'Szeroko uśmiechnięta twarz',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'smiling_face_with_open_mouth': {
                FIELD_SYMBOL: '😃',
                FIELD_NAME: 'Uśmiechnięta twarz z otwartymi ustami',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'smiling_face_with_open_mouth_and_smiling_eyes': {
                FIELD_SYMBOL: '😄',
                FIELD_NAME: 'Uśmiechnięta twarz z otwartymi ustami i roześmianymi oczami',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'smiling_face_with_smiling_eyes': {
                FIELD_SYMBOL: '😁',
                FIELD_NAME: 'Szeroko uśmiechnięta twarz o roześmianych oczach',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'smiling_face_with_open_mouth_and_tightly_closed_eyes': {
                FIELD_SYMBOL: '😆',
                FIELD_NAME: 'Uśmiechnięta twarz z przymrużonymi oczami',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'face_holding_back_tears': {
                FIELD_SYMBOL: '🥹',
                FIELD_NAME: 'Twarz powstrzymująca łzy',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'smiling_face_with_open_mouth_and_cold_sweat': {
                FIELD_SYMBOL: '😅',
                FIELD_NAME: 'Uśmiechnięta twarz z otwartymi ustami, oblana zimnym potem',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'face_with_tears_of_joy': {
                FIELD_SYMBOL: '😂',
                FIELD_NAME: 'Twarz ze łzami radości',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'rolling_on_the_floor_laughing': {
                FIELD_SYMBOL: '🤣',
                FIELD_NAME: 'Tarza się ze śmiechu',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'smiling_face_with_tear': {
                FIELD_SYMBOL: '🥲',
                FIELD_NAME: 'Uśmiechnięta buźka ze łzą',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'white_smiling_face': {
                FIELD_SYMBOL: '☺️',
                FIELD_NAME: 'Uśmiechnięta twarz',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'smiling_face_with_smiling_eyes_2': {
                FIELD_SYMBOL: '😊',
                FIELD_NAME: 'Uśmiechnięta twarz o roześmianych oczach',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'smiling_face_with_halo': {
                FIELD_SYMBOL: '😇',
                FIELD_NAME: 'Uśmiechnięta twarz z aureolą',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'slightly_smiling_face': {
                FIELD_SYMBOL: '🙂',
                FIELD_NAME: 'Lekko uśmiechnięta twarz',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'upside_down_face': {
                FIELD_SYMBOL: '🙃',
                FIELD_NAME: 'Odwrócona twarz',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'winking_face': {
                FIELD_SYMBOL: '😉',
                FIELD_NAME: 'Twarz puszczająca oko',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'relieved_face': {
                FIELD_SYMBOL: '😌',
                FIELD_NAME: 'Twarz z wyrazem ulgi',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'smiling_face_with_heart_shaped_eyes': {
                FIELD_SYMBOL: '😍',
                FIELD_NAME: 'Uśmiechnięta twarz z oczami w kształcie serca',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'smiling_face_with_smiling_eyes_and_three_hearts': {
                FIELD_SYMBOL: '🥰',
                FIELD_NAME: 'Uśmiechnięta buźka z sercami',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'face_throwing_a_kiss': {
                FIELD_SYMBOL: '😘',
                FIELD_NAME: 'Twarz przesyłająca całusa',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'kissing_face': {
                FIELD_SYMBOL: '😗',
                FIELD_NAME: 'Całująca twarz',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'kissing_face_with_smiling_eyes': {
                FIELD_SYMBOL: '😙',
                FIELD_NAME: 'Całująca twarz o roześmianych oczach',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'kissing_face_with_closed_eyes': {
                FIELD_SYMBOL: '😚',
                FIELD_NAME: 'Całująca twarz z zamkniętymi oczami',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'face_savouring_delicious_food': {
                FIELD_SYMBOL: '😋',
                FIELD_NAME: 'Twarz delektująca się pysznym jedzeniem',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'face_with_stuck_out_tongue': {
                FIELD_SYMBOL: '😛',
                FIELD_NAME: 'Twarz wystawiająca język',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'face_with_stuck_out_tongue_and_tightly_closed_eyes': {
                FIELD_SYMBOL: '😝',
                FIELD_NAME: 'Twarz ze zmrużonymi oczami wystawiająca język',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'face_with_stuck_out_tongue_and_winking_eye': {
                FIELD_SYMBOL: '😜',
                FIELD_NAME: 'Twarz wystawiająca język i puszczająca oko',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'grinning_face_with_one_large_and_one_small_eye': {
                FIELD_SYMBOL: '🤪',
                FIELD_NAME: 'Szalona twarz',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'face_with_one_eyebrow_raised': {
                FIELD_SYMBOL: '🤨',
                FIELD_NAME: 'Twarz z podniesioną brwią',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'face_with_monocle': {
                FIELD_SYMBOL: '🧐',
                FIELD_NAME: 'Twarz z monoklem',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'nerd_face': {
                FIELD_SYMBOL: '🤓',
                FIELD_NAME: 'Kujon',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'smiling_face_with_sunglasses': {
                FIELD_SYMBOL: '😎',
                FIELD_NAME: 'Uśmiechnięta twarz w okularach przeciwsłonecznych',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'disguised_face': {
                FIELD_SYMBOL: '🥸',
                FIELD_NAME: 'Buźka w przebraniu',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'grinning_face_with_star_eyes': {
                FIELD_SYMBOL: '🤩',
                FIELD_NAME: 'Zafascynowany',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'face_with_party_horn_and_party_hat': {
                FIELD_SYMBOL: '🥳',
                FIELD_NAME: 'Świętująca twarz',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'slightly_smiling_face_with_up_down_arrow': {
                FIELD_SYMBOL: '🙂‍↕️',
                FIELD_NAME: 'Głowa kiwająca się pionowo',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'smirking_face': {
                FIELD_SYMBOL: '😏',
                FIELD_NAME: 'Twarz z uśmieszkiem',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'unamused_face': {
                FIELD_SYMBOL: '😒',
                FIELD_NAME: 'Niezadowolona twarz',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'slightly_smiling_face_with_left_right_arrow': {
                FIELD_SYMBOL: '🙂‍↔',
                FIELD_NAME: 'Głowa kręcąca się poziomo',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'disappointed_face': {
                FIELD_SYMBOL: '😞',
                FIELD_NAME: 'Rozczarowana twarz',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'pensive_face': {
                FIELD_SYMBOL: '😔',
                FIELD_NAME: 'Zamyślona twarz',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'worried_face': {
                FIELD_SYMBOL: '😟',
                FIELD_NAME: 'Zmartwiona twarz',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'confused_face': {
                FIELD_SYMBOL: '😕',
                FIELD_NAME: 'Zdezorientowana twarz',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'slightly_frowning_face': {
                FIELD_SYMBOL: '🙁',
                FIELD_NAME: 'Lekko zachmurzona twarz',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'white_frowning_face': {
                FIELD_SYMBOL: '☹️',
                FIELD_NAME: 'Zachmurzona twarz',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'persevering_face': {
                FIELD_SYMBOL: '😣',
                FIELD_NAME: 'Uparta twarz',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'confounded_face': {
                FIELD_SYMBOL: '😖',
                FIELD_NAME: 'Zakłopotana twarz',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'tired_face': {
                FIELD_SYMBOL: '😫',
                FIELD_NAME: 'Zmęczona twarz',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'weary_face': {
                FIELD_SYMBOL: '😩',
                FIELD_NAME: 'Znużona twarz',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'face_with_pleading_eyes': {
                FIELD_SYMBOL: '🥺',
                FIELD_NAME: 'Błagająca twarz',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'crying_face': {
                FIELD_SYMBOL: '😢',
                FIELD_NAME: 'Płacząca twarz',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'loudly_crying_face': {
                FIELD_SYMBOL: '😭',
                FIELD_NAME: 'Głośno płacząca twarz',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'face_with_look_of_triumph': {
                FIELD_SYMBOL: '😤',
                FIELD_NAME: 'Prychająca twarz',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'angry_face': {
                FIELD_SYMBOL: '😠',
                FIELD_NAME: 'Zagniewana twarz',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'pouting_face': {
                FIELD_SYMBOL: '😡',
                FIELD_NAME: 'Nadąsana twarz',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'serious_face_with_symbols_covering_mouth': {
                FIELD_SYMBOL: '🤬',
                FIELD_NAME: 'Twarz z symbolami na ustach',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'shocked_face_with_exploding_head': {
                FIELD_SYMBOL: '🤯',
                FIELD_NAME: 'Eksplodująca głowa',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'flushed_face': {
                FIELD_SYMBOL: '😳',
                FIELD_NAME: 'Twarz z rumieńcami',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'overheated_face': {
                FIELD_SYMBOL: '🥵',
                FIELD_NAME: 'Rozgrzana twarz',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'freezing_face': {
                FIELD_SYMBOL: '🥶',
                FIELD_NAME: 'Zmarznięta twarz',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'face_without_mouth_with_fog': {
                FIELD_SYMBOL: '😶‍🌫',
                FIELD_NAME: 'Twarz w chmurach',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'face_screaming_in_fear': {
                FIELD_SYMBOL: '😱',
                FIELD_NAME: 'Twarz krzycząca ze strachu',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'fearful_face': {
                FIELD_SYMBOL: '😨',
                FIELD_NAME: 'Przestraszona twarz',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'face_with_open_mouth_and_cold_sweat': {
                FIELD_SYMBOL: '😰',
                FIELD_NAME: 'Zaniepokojona twarz oblana potem',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'disappointed_but_relieved_face': {
                FIELD_SYMBOL: '😥',
                FIELD_NAME: 'Smutna twarz z wyrazem ulgi',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'face_with_cold_sweat': {
                FIELD_SYMBOL: '😓',
                FIELD_NAME: 'Twarz ze spuszczonymi oczami oblana potem',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'hugging_face': {
                FIELD_SYMBOL: '🤗',
                FIELD_NAME: 'Twarz z gestem przytulania',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'thinking_face': {
                FIELD_SYMBOL: '🤔',
                FIELD_NAME: 'Myśląca twarz',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'face_with_peeking_eye': {
                FIELD_SYMBOL: '🫣',
                FIELD_NAME: 'Twarz z podglądającym okiem',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'smiling_face_with_smiling_eyes_and_hand_covering_mouth': {
                FIELD_SYMBOL: '🤭',
                FIELD_NAME: 'Twarz z ręką na ustach',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'face_with_open_eyes_and_hand_over_mouth': {
                FIELD_SYMBOL: '🫢',
                FIELD_NAME: 'Twarz z otwartymi oczami i ręką na ustach',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'saluting_face': {
                FIELD_SYMBOL: '🫡',
                FIELD_NAME: 'Salutująca twarz',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'face_with_finger_covering_closed_lips': {
                FIELD_SYMBOL: '🤫',
                FIELD_NAME: 'Uciszająca twarz',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'melting_face': {
                FIELD_SYMBOL: '🫠',
                FIELD_NAME: 'Roztapiająca się twarz',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'lying_face': {
                FIELD_SYMBOL: '🤥',
                FIELD_NAME: 'Twarz kłamcy',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'face_without_mouth': {
                FIELD_SYMBOL: '😶',
                FIELD_NAME: 'Twarz bez ust',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'dotted_line_face': {
                FIELD_SYMBOL: '🫥',
                FIELD_NAME: 'Twarz otoczona linią przerywaną',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'neutral_face': {
                FIELD_SYMBOL: '😐',
                FIELD_NAME: 'Neutralna twarz',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'face_with_diagonal_mouth': {
                FIELD_SYMBOL: '🫤',
                FIELD_NAME: 'Twarz z ukośnymi ustami',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'expressionless_face': {
                FIELD_SYMBOL: '😑',
                FIELD_NAME: 'Twarz bez wyrazu',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'shaking_face': {
                FIELD_SYMBOL: '🫨',
                FIELD_NAME: 'Wstrząśnięta twarz',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'grimacing_face': {
                FIELD_SYMBOL: '😬',
                FIELD_NAME: 'Twarz z grymasem',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'face_with_rolling_eyes': {
                FIELD_SYMBOL: '🙄',
                FIELD_NAME: 'Twarz przewracająca oczami',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'hushed_face': {
                FIELD_SYMBOL: '😯',
                FIELD_NAME: 'Zdumiona twarz',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'frowning_face_with_open_mouth': {
                FIELD_SYMBOL: '😦',
                FIELD_NAME: 'Zachmurzona twarz z otwartymi ustami',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'anguished_face': {
                FIELD_SYMBOL: '😧',
                FIELD_NAME: 'Udręczona twarz',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'face_with_open_mouth': {
                FIELD_SYMBOL: '😮',
                FIELD_NAME: 'Twarz z otwartymi ustami',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'astonished_face': {
                FIELD_SYMBOL: '😲',
                FIELD_NAME: 'Zadziwiona twarz',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'yawning_face': {
                FIELD_SYMBOL: '🥱',
                FIELD_NAME: 'Ziewająca twarz',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'emoji': {
                FIELD_SYMBOL: '🫩',
                FIELD_NAME: 'Twarz z workami pod oczami',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'emoji_2': {
                FIELD_SYMBOL: '🫪',
                FIELD_NAME: 'Wykrzywiona twarz',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'sleeping_face': {
                FIELD_SYMBOL: '😴',
                FIELD_NAME: 'Śpiąca twarz',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'drooling_face': {
                FIELD_SYMBOL: '🤤',
                FIELD_NAME: 'Śliniąca się twarz',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'sleepy_face': {
                FIELD_SYMBOL: '😪',
                FIELD_NAME: 'Senna twarz',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'face_with_open_mouth_with_dash_symbol': {
                FIELD_SYMBOL: '😮‍💨',
                FIELD_NAME: 'Twarz wypuszczająca powietrze',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'dizzy_face': {
                FIELD_SYMBOL: '😵',
                FIELD_NAME: 'Oszołomiona twarz',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'dizzy_face_with_dizzy_symbol': {
                FIELD_SYMBOL: '😵‍💫',
                FIELD_NAME: 'Twarz ze spiralnymi oczami',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'zipper_mouth_face': {
                FIELD_SYMBOL: '🤐',
                FIELD_NAME: 'Twarz z zamkiem błyskawicznym na ustach',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'face_with_uneven_eyes_and_wavy_mouth': {
                FIELD_SYMBOL: '🥴',
                FIELD_NAME: 'Zamroczona twarz',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'nauseated_face': {
                FIELD_SYMBOL: '🤢',
                FIELD_NAME: 'Twarz z mdłościami',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'face_with_open_mouth_vomiting': {
                FIELD_SYMBOL: '🤮',
                FIELD_NAME: 'Wymiotująca twarz',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'sneezing_face': {
                FIELD_SYMBOL: '🤧',
                FIELD_NAME: 'Kichająca twarz',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'face_with_medical_mask': {
                FIELD_SYMBOL: '😷',
                FIELD_NAME: 'Twarz w masce medycznej',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'face_with_thermometer': {
                FIELD_SYMBOL: '🤒',
                FIELD_NAME: 'Twarz z termometrem',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'face_with_head_bandage': {
                FIELD_SYMBOL: '🤕',
                FIELD_NAME: 'Twarz z bandażem',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'money_mouth_face': {
                FIELD_SYMBOL: '🤑',
                FIELD_NAME: 'Twarz z pieniędzmi na ustach',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'face_with_cowboy_hat': {
                FIELD_SYMBOL: '🤠',
                FIELD_NAME: 'Głowa w kapeluszu kowbojskim',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'smiling_face_with_horns': {
                FIELD_SYMBOL: '😈',
                FIELD_NAME: 'Uśmiechnięta twarz z rogami',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'imp': {
                FIELD_SYMBOL: '👿',
                FIELD_NAME: 'Zagniewana twarz z rogami',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'japanese_ogre': {
                FIELD_SYMBOL: '👹',
                FIELD_NAME: 'Ogr',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'japanese_goblin': {
                FIELD_SYMBOL: '👺',
                FIELD_NAME: 'Goblin',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'clown_face': {
                FIELD_SYMBOL: '🤡',
                FIELD_NAME: 'Twarz klauna',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'pile_of_poo': {
                FIELD_SYMBOL: '💩',
                FIELD_NAME: 'Kupa',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'ghost': {
                FIELD_SYMBOL: '👻',
                FIELD_NAME: 'Duch',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'skull': {
                FIELD_SYMBOL: '💀',
                FIELD_NAME: 'Czaszka',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'skull_and_crossbones': {
                FIELD_SYMBOL: '☠️',
                FIELD_NAME: 'Czaszka z piszczelami',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'extraterrestrial_alien': {
                FIELD_SYMBOL: '👽',
                FIELD_NAME: 'Ufoludek',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'alien_monster': {
                FIELD_SYMBOL: '👾',
                FIELD_NAME: 'Kosmiczny potwór',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'robot_face': {
                FIELD_SYMBOL: '🤖',
                FIELD_NAME: 'Głowa robota',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'jack_o_lantern': {
                FIELD_SYMBOL: '🎃',
                FIELD_NAME: 'Dynia na halloween',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'smiling_cat_face_with_open_mouth': {
                FIELD_SYMBOL: '😺',
                FIELD_NAME: 'Uśmiechnięty kot',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'grinning_cat_face_with_smiling_eyes': {
                FIELD_SYMBOL: '😸',
                FIELD_NAME: 'Uśmiechnięty kot o wesołych oczach',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'cat_face_with_tears_of_joy': {
                FIELD_SYMBOL: '😹',
                FIELD_NAME: 'Kot ze łzami radości',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'smiling_cat_face_with_heart_shaped_eyes': {
                FIELD_SYMBOL: '😻',
                FIELD_NAME: 'Uśmiechnięty kot z oczami w kształcie serca',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'cat_face_with_wry_smile': {
                FIELD_SYMBOL: '😼',
                FIELD_NAME: 'Kot z drwiącym uśmiechem',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'kissing_cat_face_with_closed_eyes': {
                FIELD_SYMBOL: '😽',
                FIELD_NAME: 'Kot przesyłający całusa',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'weary_cat_face': {
                FIELD_SYMBOL: '🙀',
                FIELD_NAME: 'Przestraszony kot',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'crying_cat_face': {
                FIELD_SYMBOL: '😿',
                FIELD_NAME: 'Płaczący kot',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'pouting_cat_face': {
                FIELD_SYMBOL: '😾',
                FIELD_NAME: 'Nadąsany kot',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
        },
        HANDS: {
            'heart_hands': {
                FIELD_SYMBOL: '🫶',
                FIELD_NAME: 'Dłonie tworzące serce',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: False
            },
            'palms_up_together': {
                FIELD_SYMBOL: '🤲',
                FIELD_NAME: 'Dłonie do góry razem',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: False
            },
            'open_hands_sign': {
                FIELD_SYMBOL: '👐',
                FIELD_NAME: 'Otwarte dłonie',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: False
            },
            'person_raising_both_hands_in_celebration': {
                FIELD_SYMBOL: '🙌',
                FIELD_NAME: 'Wzniesione ręce',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: False
            },
            'clapping_hands_sign': {
                FIELD_SYMBOL: '👏',
                FIELD_NAME: 'Klaskanie',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: False
            },
            'handshake': {
                FIELD_SYMBOL: '🤝',
                FIELD_NAME: 'Uścisk dłoni',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'thumbs_up_sign': {
                FIELD_SYMBOL: '👍',
                FIELD_NAME: 'Kciuk w górę',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: False
            },
            'thumbs_down_sign': {
                FIELD_SYMBOL: '👎',
                FIELD_NAME: 'Kciuk w dół',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: False
            },
            'fisted_hand_sign': {
                FIELD_SYMBOL: '👊',
                FIELD_NAME: 'Pięść od przodu',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: False
            },
            'raised_fist': {
                FIELD_SYMBOL: '✊',
                FIELD_NAME: 'Wzniesiona pięść',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: False
            },
            'left_facing_fist': {
                FIELD_SYMBOL: '🤛',
                FIELD_NAME: 'Pięść skierowana w lewo',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: False
            },
            'right_facing_fist': {
                FIELD_SYMBOL: '🤜',
                FIELD_NAME: 'Pięść skierowana w prawo',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: False
            },
            'leftwards_pushing_hand': {
                FIELD_SYMBOL: '🫷',
                FIELD_NAME: 'Dłoń pchająca w lewo',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: False
            },
            'rightwards_pushing_hand': {
                FIELD_SYMBOL: '🫸',
                FIELD_NAME: 'Dłoń pchająca w prawo',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: False
            },
            'hand_with_index_and_middle_fingers_crossed': {
                FIELD_SYMBOL: '🤞',
                FIELD_NAME: 'Skrzyżowane palce',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: False
            },
            'victory_hand': {
                FIELD_SYMBOL: '✌️',
                FIELD_NAME: 'Gest V',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: False
            },
            'hand_with_index_finger_and_thumb_crossed': {
                FIELD_SYMBOL: '🫰',
                FIELD_NAME: 'Dłoń ze skrzyżowanym palcem wskazującym i kciukiem',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: False
            },
            'i_love_you_hand_sign': {
                FIELD_SYMBOL: '🤟',
                FIELD_NAME: 'Gest Kocham cię',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: False
            },
            'sign_of_the_horns': {
                FIELD_SYMBOL: '🤘',
                FIELD_NAME: 'Gest rogów',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'ok_hand_sign': {
                FIELD_SYMBOL: '👌',
                FIELD_NAME: 'Dłoń z gestem OK',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: False
            },
            'pinched_fingers': {
                FIELD_SYMBOL: '🤌',
                FIELD_NAME: 'Złączone palce',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: False
            },
            'pinching_hand': {
                FIELD_SYMBOL: '🤏',
                FIELD_NAME: 'Dłoń z gestem „trochę”',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: False
            },
            'palm_down_hand': {
                FIELD_SYMBOL: '🫳',
                FIELD_NAME: 'Dłoń skierowana w dół',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: False
            },
            'palm_up_hand': {
                FIELD_SYMBOL: '🫴',
                FIELD_NAME: 'Dłoń skierowana w górę',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: False
            },
            'white_left_pointing_backhand_index': {
                FIELD_SYMBOL: '👈',
                FIELD_NAME: 'Dłoń z palcem wskazującym w lewo',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'white_right_pointing_backhand_index': {
                FIELD_SYMBOL: '👉',
                FIELD_NAME: 'Dłoń z palcem wskazującym w prawo',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'white_up_pointing_backhand_index': {
                FIELD_SYMBOL: '👆',
                FIELD_NAME: 'Dłoń z palcem wskazującym w górę',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'white_down_pointing_backhand_index': {
                FIELD_SYMBOL: '👇',
                FIELD_NAME: 'Dłoń z palcem wskazującym w dół',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'white_up_pointing_index': {
                FIELD_SYMBOL: '☝️',
                FIELD_NAME: 'Palec wskazujący w górę',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'raised_hand': {
                FIELD_SYMBOL: '✋',
                FIELD_NAME: 'Wzniesiona dłoń',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: False
            },
            'raised_back_of_hand': {
                FIELD_SYMBOL: '🤚',
                FIELD_NAME: 'Wzniesiony grzbiet dłoni',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: False
            },
            'raised_hand_with_fingers_splayed': {
                FIELD_SYMBOL: '🖐️',
                FIELD_NAME: 'Uniesiona otwarta dłoń',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: False
            },
            'raised_hand_with_part_between_middle_and_ring_fingers': {
                FIELD_SYMBOL: '🖖',
                FIELD_NAME: 'Salut wolkański',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: False
            },
            'waving_hand_sign': {
                FIELD_SYMBOL: '👋',
                FIELD_NAME: 'Machająca dłoń',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: False
            },
            'call_me_hand': {
                FIELD_SYMBOL: '🤙',
                FIELD_NAME: 'Dłoń w geście „Zadzwoń do mnie”',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: False
            },
            'leftwards_hand': {
                FIELD_SYMBOL: '🫲',
                FIELD_NAME: 'Dłoń skierowana w lewo',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: False
            },
            'rightwards_hand': {
                FIELD_SYMBOL: '🫱',
                FIELD_NAME: 'Dłoń skierowana w prawo',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: False
            },
            'reversed_hand_with_middle_finger_extended': {
                FIELD_SYMBOL: '🖕',
                FIELD_NAME: 'Środkowy palec',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: False
            },
            'writing_hand': {
                FIELD_SYMBOL: '✍️',
                FIELD_NAME: 'Pisząca dłoń',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: False
            },
            'person_with_folded_hands': {
                FIELD_SYMBOL: '🙏',
                FIELD_NAME: 'Złożone ręce',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: False
            },
            'index_pointing_at_the_viewer': {
                FIELD_SYMBOL: '🫵',
                FIELD_NAME: 'Palec wskazujący skierowany na patrzącego',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
        },
        FACES: {
            'baby': {
                FIELD_SYMBOL: '👶',
                FIELD_NAME: 'Niemowlę',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: False
            },
            'girl': {
                FIELD_SYMBOL: '👧',
                FIELD_NAME: 'Dziewczynka',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: False
            },
            'child': {
                FIELD_SYMBOL: '🧒',
                FIELD_NAME: 'Dziecko',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: False
            },
            'boy': {
                FIELD_SYMBOL: '👦',
                FIELD_NAME: 'Chłopak',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: False
            },
            'woman': {
                FIELD_SYMBOL: '👩',
                FIELD_NAME: 'Kobieta',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'adult': {
                FIELD_SYMBOL: '🧑',
                FIELD_NAME: 'Dorosły',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'man': {
                FIELD_SYMBOL: '👨',
                FIELD_NAME: 'Mężczyzna',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'woman_with_emoji_component_curly_hair': {
                FIELD_SYMBOL: '👩\u200d🦱',
                FIELD_NAME: 'Woman z emoji component curly hair',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'adult_with_emoji_component_curly_hair': {
                FIELD_SYMBOL: '🧑\u200d🦱',
                FIELD_NAME: 'Adult z emoji component curly hair',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'man_with_emoji_component_curly_hair': {
                FIELD_SYMBOL: '👨\u200d🦱',
                FIELD_NAME: 'Man z emoji component curly hair',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'woman_with_emoji_component_red_hair': {
                FIELD_SYMBOL: '👩\u200d🦰',
                FIELD_NAME: 'Woman z emoji component czerwony hair',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'adult_with_emoji_component_red_hair': {
                FIELD_SYMBOL: '🧑\u200d🦰',
                FIELD_NAME: 'Adult z emoji component czerwony hair',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'man_with_emoji_component_red_hair': {
                FIELD_SYMBOL: '👨\u200d🦰',
                FIELD_NAME: 'Man z emoji component czerwony hair',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'person_with_blond_hair_with_female_sign': {
                FIELD_SYMBOL: '👱\u200d♀',
                FIELD_NAME: 'Person z blond hair z female sign',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'person_with_blond_hair': {
                FIELD_SYMBOL: '👱',
                FIELD_NAME: 'Osoba o blond włosach',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'person_with_blond_hair_with_male_sign': {
                FIELD_SYMBOL: '👱\u200d♂️',
                FIELD_NAME: 'Person z blond hair z male sign',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'woman_with_emoji_component_white_hair': {
                FIELD_SYMBOL: '👩\u200d🦳',
                FIELD_NAME: 'Woman z emoji component biały hair',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'adult_with_emoji_component_white_hair': {
                FIELD_SYMBOL: '🧑\u200d🦳',
                FIELD_NAME: 'Adult z emoji component biały hair',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'man_with_emoji_component_white_hair': {
                FIELD_SYMBOL: '👨\u200d🦳',
                FIELD_NAME: 'Man z emoji component biały hair',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'woman_with_emoji_component_bald': {
                FIELD_SYMBOL: '👩\u200d🦲',
                FIELD_NAME: 'Woman z emoji component bald',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'adult_with_emoji_component_bald': {
                FIELD_SYMBOL: '🧑\u200d🦲',
                FIELD_NAME: 'Adult z emoji component bald',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'man_with_emoji_component_bald': {
                FIELD_SYMBOL: '👨\u200d🦲',
                FIELD_NAME: 'Man z emoji component bald',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'bearded_person_with_female_sign': {
                FIELD_SYMBOL: '🧔\u200d♀',
                FIELD_NAME: 'Bearded person z female sign',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'bearded_person': {
                FIELD_SYMBOL: '🧔',
                FIELD_NAME: 'Brodata osoba',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'bearded_person_with_male_sign': {
                FIELD_SYMBOL: '🧔\u200d♂️',
                FIELD_NAME: 'Bearded person z male sign',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'older_woman': {
                FIELD_SYMBOL: '👵',
                FIELD_NAME: 'Starsza kobieta',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'older_adult': {
                FIELD_SYMBOL: '🧓',
                FIELD_NAME: 'Starszy dorosły',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'older_man': {
                FIELD_SYMBOL: '👴',
                FIELD_NAME: 'Starszy człowiek',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'man_with_gua_pi_mao': {
                FIELD_SYMBOL: '👲',
                FIELD_NAME: 'Człowiek z Gua Pi Mao',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'man_with_turban_with_female_sign': {
                FIELD_SYMBOL: '👳\u200d♀️',
                FIELD_NAME: 'Man z turban z female sign',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'man_with_turban': {
                FIELD_SYMBOL: '👳',
                FIELD_NAME: 'Człowiek z Turbanem',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'man_with_turban_with_male_sign': {
                FIELD_SYMBOL: '👳\u200d♂️',
                FIELD_NAME: 'Man z turban z male sign',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'person_with_headscarf': {
                FIELD_SYMBOL: '🧕',
                FIELD_NAME: 'Osoba Z Chustka Na Głowę',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'police_officer_with_female_sign': {
                FIELD_SYMBOL: '👮\u200d♀️',
                FIELD_NAME: 'Police officer z female sign',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'police_officer': {
                FIELD_SYMBOL: '👮',
                FIELD_NAME: 'Policjant',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'police_officer_with_male_sign': {
                FIELD_SYMBOL: '👮\u200d♂️',
                FIELD_NAME: 'Police officer z male sign',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'construction_worker_with_female_sign': {
                FIELD_SYMBOL: '👷\u200d♀️',
                FIELD_NAME: 'Construction worker z female sign',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: True
            },
            'construction_worker': {
                FIELD_SYMBOL: '👷',
                FIELD_NAME: 'Pracownik budowlany',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: True
            },
            'construction_worker_with_male_sign': {
                FIELD_SYMBOL: '👷\u200d♂️',
                FIELD_NAME: 'Construction worker z male sign',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: True
            },
            'guardsman_with_female_sign': {
                FIELD_SYMBOL: '💂\u200d♀️',
                FIELD_NAME: 'Guardsman z female sign',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: True
            },
            'guardsman': {
                FIELD_SYMBOL: '💂',
                FIELD_NAME: 'Gwardzista',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'guardsman_with_male_sign': {
                FIELD_SYMBOL: '💂\u200d♂️',
                FIELD_NAME: 'Guardsman z male sign',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: True
            },
            'sleuth_or_spy_with_female_sign': {
                FIELD_SYMBOL: '🕵️\u200d♀️',
                FIELD_NAME: 'Sleuth or spy z female sign',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: True
            },
            'sleuth_or_spy': {
                FIELD_SYMBOL: '🕵️',
                FIELD_NAME: 'Sleuth or Spy',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'sleuth_or_spy_with_male_sign': {
                FIELD_SYMBOL: '🕵️\u200d♂️',
                FIELD_NAME: 'Sleuth or spy z male sign',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: True
            },
            'woman_with_staff_of_aesculapius': {
                FIELD_SYMBOL: '👩\u200d⚕️',
                FIELD_NAME: 'Woman z staff of aesculapius',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'adult_with_staff_of_aesculapius': {
                FIELD_SYMBOL: '🧑\u200d⚕️',
                FIELD_NAME: 'Adult z staff of aesculapius',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'man_with_staff_of_aesculapius': {
                FIELD_SYMBOL: '👨\u200d⚕️',
                FIELD_NAME: 'Man z staff of aesculapius',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'woman_with_ear_of_rice': {
                FIELD_SYMBOL: '👩\u200d🌾',
                FIELD_NAME: 'Woman z ear of rice',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'adult_with_ear_of_rice': {
                FIELD_SYMBOL: '🧑\u200d🌾',
                FIELD_NAME: 'Adult z ear of rice',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'man_with_ear_of_rice': {
                FIELD_SYMBOL: '👨\u200d🌾',
                FIELD_NAME: 'Man z ear of rice',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'woman_with_cooking': {
                FIELD_SYMBOL: '👩\u200d🍳',
                FIELD_NAME: 'Woman z cooking',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'adult_with_cooking': {
                FIELD_SYMBOL: '🧑\u200d🍳',
                FIELD_NAME: 'Adult z cooking',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'man_with_cooking': {
                FIELD_SYMBOL: '👨\u200d🍳',
                FIELD_NAME: 'Man z cooking',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'woman_with_graduation_cap': {
                FIELD_SYMBOL: '👩\u200d🎓',
                FIELD_NAME: 'Woman z graduation cap',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'adult_with_graduation_cap': {
                FIELD_SYMBOL: '🧑\u200d🎓',
                FIELD_NAME: 'Adult z graduation cap',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'man_with_graduation_cap': {
                FIELD_SYMBOL: '👨\u200d🎓',
                FIELD_NAME: 'Man z graduation cap',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'woman_with_microphone': {
                FIELD_SYMBOL: '👩\u200d🎤',
                FIELD_NAME: 'Woman z microphone',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'adult_with_microphone': {
                FIELD_SYMBOL: '🧑\u200d🎤',
                FIELD_NAME: 'Adult z microphone',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'man_with_microphone': {
                FIELD_SYMBOL: '👨\u200d🎤',
                FIELD_NAME: 'Man z microphone',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'woman_with_school': {
                FIELD_SYMBOL: '👩\u200d🏫',
                FIELD_NAME: 'Woman z szkoła',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'adult_with_school': {
                FIELD_SYMBOL: '🧑\u200d🏫',
                FIELD_NAME: 'Adult z szkoła',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'man_with_school': {
                FIELD_SYMBOL: '👨\u200d🏫',
                FIELD_NAME: 'Man z szkoła',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'woman_with_factory': {
                FIELD_SYMBOL: '👩\u200d🏭',
                FIELD_NAME: 'Woman z factory',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'adult_with_factory': {
                FIELD_SYMBOL: '🧑\u200d🏭',
                FIELD_NAME: 'Adult z factory',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'man_with_factory': {
                FIELD_SYMBOL: '👨\u200d🏭',
                FIELD_NAME: 'Man z factory',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'woman_with_personal_computer': {
                FIELD_SYMBOL: '👩\u200d💻',
                FIELD_NAME: 'Woman z personal computer',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'adult_with_personal_computer': {
                FIELD_SYMBOL: '🧑\u200d💻',
                FIELD_NAME: 'Adult z personal computer',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'man_with_personal_computer': {
                FIELD_SYMBOL: '👨\u200d💻',
                FIELD_NAME: 'Man z personal computer',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'woman_with_briefcase': {
                FIELD_SYMBOL: '👩\u200d💼',
                FIELD_NAME: 'Woman z briefcase',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'adult_with_briefcase': {
                FIELD_SYMBOL: '🧑\u200d💼',
                FIELD_NAME: 'Adult z briefcase',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'man_with_briefcase': {
                FIELD_SYMBOL: '👨\u200d💼',
                FIELD_NAME: 'Man z briefcase',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'woman_with_wrench': {
                FIELD_SYMBOL: '👩\u200d🔧',
                FIELD_NAME: 'Woman z wrench',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'adult_with_wrench': {
                FIELD_SYMBOL: '🧑\u200d🔧',
                FIELD_NAME: 'Adult z wrench',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'man_with_wrench': {
                FIELD_SYMBOL: '👨\u200d🔧',
                FIELD_NAME: 'Man z wrench',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'woman_with_microscope': {
                FIELD_SYMBOL: '👩\u200d🔬',
                FIELD_NAME: 'Woman z microscope',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'adult_with_microscope': {
                FIELD_SYMBOL: '🧑\u200d🔬',
                FIELD_NAME: 'Adult z microscope',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'man_with_microscope': {
                FIELD_SYMBOL: '👨\u200d🔬',
                FIELD_NAME: 'Man z microscope',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'woman_with_artist_palette': {
                FIELD_SYMBOL: '👩\u200d🎨',
                FIELD_NAME: 'Woman z artist palette',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'adult_with_artist_palette': {
                FIELD_SYMBOL: '🧑\u200d🎨',
                FIELD_NAME: 'Adult z artist palette',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'man_with_artist_palette': {
                FIELD_SYMBOL: '👨\u200d🎨',
                FIELD_NAME: 'Man z artist palette',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'woman_with_fire_engine': {
                FIELD_SYMBOL: '👩\u200d🚒',
                FIELD_NAME: 'Woman z fire engine',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'adult_with_fire_engine': {
                FIELD_SYMBOL: '🧑\u200d🚒',
                FIELD_NAME: 'Adult z fire engine',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'man_with_fire_engine': {
                FIELD_SYMBOL: '👨\u200d🚒',
                FIELD_NAME: 'Man z fire engine',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'woman_with_airplane': {
                FIELD_SYMBOL: '👩\u200d✈️',
                FIELD_NAME: 'Woman z samolot',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'adult_with_airplane': {
                FIELD_SYMBOL: '🧑\u200d✈️',
                FIELD_NAME: 'Adult z samolot',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'man_with_airplane': {
                FIELD_SYMBOL: '👨\u200d✈️',
                FIELD_NAME: 'Man z samolot',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'woman_with_rocket': {
                FIELD_SYMBOL: '👩\u200d🚀',
                FIELD_NAME: 'Woman z rocket',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'adult_with_rocket': {
                FIELD_SYMBOL: '🧑\u200d🚀',
                FIELD_NAME: 'Adult z rocket',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'man_with_rocket': {
                FIELD_SYMBOL: '👨\u200d🚀',
                FIELD_NAME: 'Man z rocket',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'woman_with_scales': {
                FIELD_SYMBOL: '👩\u200d⚖️',
                FIELD_NAME: 'Woman z scales',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'adult_with_scales': {
                FIELD_SYMBOL: '🧑\u200d⚖️',
                FIELD_NAME: 'Adult z scales',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'man_with_scales': {
                FIELD_SYMBOL: '👨\u200d⚖️',
                FIELD_NAME: 'Man z scales',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'bride_with_veil_with_female_sign': {
                FIELD_SYMBOL: '👰\u200d♀️',
                FIELD_NAME: 'Bride z veil z female sign',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'bride_with_veil': {
                FIELD_SYMBOL: '👰',
                FIELD_NAME: 'Panna młoda z welonem',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'bride_with_veil_with_male_sign': {
                FIELD_SYMBOL: '👰\u200d♂️',
                FIELD_NAME: 'Bride z veil z male sign',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'man_in_tuxedo_with_female_sign': {
                FIELD_SYMBOL: '🤵\u200d♀️',
                FIELD_NAME: 'Man in tuxedo z female sign',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'man_in_tuxedo': {
                FIELD_SYMBOL: '🤵',
                FIELD_NAME: 'Mężczyzna W Smokingu',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'man_in_tuxedo_with_male_sign': {
                FIELD_SYMBOL: '🤵\u200d♂️',
                FIELD_NAME: 'Man in tuxedo z male sign',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'princess': {
                FIELD_SYMBOL: '👸',
                FIELD_NAME: 'Księżniczka',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'person_with_crown': {
                FIELD_SYMBOL: '🫅',
                FIELD_NAME: 'Osoba W Koronie',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'prince': {
                FIELD_SYMBOL: '🤴',
                FIELD_NAME: 'Książę',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'ninja': {
                FIELD_SYMBOL: '🥷',
                FIELD_NAME: 'Ninja',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'superhero_with_female_sign': {
                FIELD_SYMBOL: '🦸\u200d♀️',
                FIELD_NAME: 'Superhero z female sign',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'superhero': {
                FIELD_SYMBOL: '🦸',
                FIELD_NAME: 'Superbohatera',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'superhero_with_male_sign': {
                FIELD_SYMBOL: '🦸\u200d♂️',
                FIELD_NAME: 'Superhero z male sign',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'supervillain_with_female_sign': {
                FIELD_SYMBOL: '🦹\u200d♀️',
                FIELD_NAME: 'Supervillain z female sign',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'supervillain': {
                FIELD_SYMBOL: '🦹',
                FIELD_NAME: 'Supervillain',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'supervillain_with_male_sign': {
                FIELD_SYMBOL: '🦹\u200d♂️',
                FIELD_NAME: 'Supervillain z male sign',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'mother_christmas': {
                FIELD_SYMBOL: '🤶',
                FIELD_NAME: 'Matka Boże Narodzenie',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'adult_with_christmas_tree': {
                FIELD_SYMBOL: '🧑\u200d🎄',
                FIELD_NAME: 'Adult z christmas tree',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'father_christmas': {
                FIELD_SYMBOL: '🎅',
                FIELD_NAME: 'Mikolaj',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'mage_with_female_sign': {
                FIELD_SYMBOL: '🧙\u200d♀️',
                FIELD_NAME: 'Mage z female sign',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'mage': {
                FIELD_SYMBOL: '🧙',
                FIELD_NAME: 'Mag',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'mage_with_male_sign': {
                FIELD_SYMBOL: '🧙\u200d♂️',
                FIELD_NAME: 'Mage z male sign',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'elf_with_female_sign': {
                FIELD_SYMBOL: '🧝\u200d♀️',
                FIELD_NAME: 'Elf z female sign',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: True
            },
            'elf': {
                FIELD_SYMBOL: '🧝',
                FIELD_NAME: 'Elf',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'elf_with_male_sign': {
                FIELD_SYMBOL: '🧝\u200d♂️',
                FIELD_NAME: 'Elf z male sign',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: True
            },
            'troll': {
                FIELD_SYMBOL: '🧌',
                FIELD_NAME: 'Troll',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'vampire_with_female_sign': {
                FIELD_SYMBOL: '🧛\u200d♀️',
                FIELD_NAME: 'Vampire z female sign',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'vampire': {
                FIELD_SYMBOL: '🧛',
                FIELD_NAME: 'Wampir',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'vampire_with_male_sign': {
                FIELD_SYMBOL: '🧛\u200d♂️',
                FIELD_NAME: 'Vampire z male sign',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'zombie_with_female_sign': {
                FIELD_SYMBOL: '🧟\u200d♀️',
                FIELD_NAME: 'Zombie z female sign',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: True
            },
            'zombie': {
                FIELD_SYMBOL: '🧟',
                FIELD_NAME: 'Zambi',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: True
            },
            'zombie_with_male_sign': {
                FIELD_SYMBOL: '🧟\u200d♂️',
                FIELD_NAME: 'Zombie z male sign',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: True
            },
            'genie_with_female_sign': {
                FIELD_SYMBOL: '🧞\u200d♀️',
                FIELD_NAME: 'Genie z female sign',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: True
            },
            'genie': {
                FIELD_SYMBOL: '🧞',
                FIELD_NAME: 'dżin',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: True
            },
            'genie_with_male_sign': {
                FIELD_SYMBOL: '🧞\u200d♂️',
                FIELD_NAME: 'Genie z male sign',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: True
            },
            'merperson_with_female_sign': {
                FIELD_SYMBOL: '🧜\u200d♀️',
                FIELD_NAME: 'Merperson z female sign',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'merperson': {
                FIELD_SYMBOL: '🧜',
                FIELD_NAME: 'Merperson',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'merperson_with_male_sign': {
                FIELD_SYMBOL: '🧜\u200d♂️',
                FIELD_NAME: 'Merperson z male sign',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'fairy_with_female_sign': {
                FIELD_SYMBOL: '🧚\u200d♀️',
                FIELD_NAME: 'Fairy z female sign',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'fairy': {
                FIELD_SYMBOL: '🧚',
                FIELD_NAME: 'Wróżka',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'fairy_with_male_sign': {
                FIELD_SYMBOL: '🧚\u200d♂️',
                FIELD_NAME: 'Fairy z male sign',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'baby_angel': {
                FIELD_SYMBOL: '👼',
                FIELD_NAME: 'Aniołek',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: False
            },
            'pregnant_woman': {
                FIELD_SYMBOL: '🤰',
                FIELD_NAME: 'Kobieta w ciąży',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'pregnant_person': {
                FIELD_SYMBOL: '🫄',
                FIELD_NAME: 'Osoba W Ciąży',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'pregnant_man': {
                FIELD_SYMBOL: '🫃',
                FIELD_NAME: 'Mężczyzna W Ciąży',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'breast_feeding': {
                FIELD_SYMBOL: '🤱',
                FIELD_NAME: 'Karmienie piersią',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'woman_with_baby_bottle': {
                FIELD_SYMBOL: '👩\u200d🍼',
                FIELD_NAME: 'Woman z baby bottle',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'adult_with_baby_bottle': {
                FIELD_SYMBOL: '🧑\u200d🍼',
                FIELD_NAME: 'Adult z baby bottle',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'man_with_baby_bottle': {
                FIELD_SYMBOL: '👨\u200d🍼',
                FIELD_NAME: 'Man z baby bottle',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'person_bowing_deeply_with_female_sign': {
                FIELD_SYMBOL: '🙇\u200d♀️',
                FIELD_NAME: 'Person bowing deeply z female sign',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'person_bowing_deeply': {
                FIELD_SYMBOL: '🙇',
                FIELD_NAME: 'Osoba kłaniająca się głęboko',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'person_bowing_deeply_with_male_sign': {
                FIELD_SYMBOL: '🙇\u200d♂',
                FIELD_NAME: 'Person bowing deeply z male sign',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'information_desk_person_with_female_sign': {
                FIELD_SYMBOL: '💁\u200d♀️',
                FIELD_NAME: 'Information desk person z female sign',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'information_desk_person': {
                FIELD_SYMBOL: '💁',
                FIELD_NAME: 'Osoba informacyjna',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'information_desk_person_with_male_sign': {
                FIELD_SYMBOL: '💁\u200d♂',
                FIELD_NAME: 'Information desk person z male sign',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'face_with_no_good_gesture_with_female_sign': {
                FIELD_SYMBOL: '🙅\u200d♀',
                FIELD_NAME: 'Twarz z no good gesture z female sign',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: True
            },
            'face_with_no_good_gesture': {
                FIELD_SYMBOL: '🙅',
                FIELD_NAME: 'Twarz bez dobrego gestu',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'face_with_no_good_gesture_with_male_sign': {
                FIELD_SYMBOL: '🙅\u200d♂',
                FIELD_NAME: 'Twarz z no good gesture z male sign',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: True
            },
            'face_with_ok_gesture_with_female_sign': {
                FIELD_SYMBOL: '🙆\u200d♀',
                FIELD_NAME: 'Twarz z ok gesture z female sign',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: True
            },
            'face_with_ok_gesture': {
                FIELD_SYMBOL: '🙆',
                FIELD_NAME: 'Twarz Z Ok Gestem',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'face_with_ok_gesture_with_male_sign': {
                FIELD_SYMBOL: '🙆\u200d♂️',
                FIELD_NAME: 'Twarz z ok gesture z male sign',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: True
            },
            'happy_person_raising_one_hand_with_female_sign': {
                FIELD_SYMBOL: '🙋\u200d♀️',
                FIELD_NAME: 'Happy person raising one hand z female sign',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'happy_person_raising_one_hand': {
                FIELD_SYMBOL: '🙋',
                FIELD_NAME: 'Szczęśliwa osoba podnosi jedną rękę',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'happy_person_raising_one_hand_2': {
                FIELD_SYMBOL: '🙋\u200d️',
                FIELD_NAME: 'Happy person raising one hand 2',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'deaf_person_with_female_sign': {
                FIELD_SYMBOL: '🧏\u200d♀️',
                FIELD_NAME: 'Deaf person z female sign',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'deaf_person': {
                FIELD_SYMBOL: '🧏',
                FIELD_NAME: 'Głucha osoba',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'deaf_person_with_male_sign': {
                FIELD_SYMBOL: '🧏\u200d♂️',
                FIELD_NAME: 'Deaf person z male sign',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'face_palm_with_female_sign': {
                FIELD_SYMBOL: '🤦\u200d♀️',
                FIELD_NAME: 'Twarz palm z female sign',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'face_palm': {
                FIELD_SYMBOL: '🤦',
                FIELD_NAME: 'Twarz dłoni',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: False
            },
            'face_palm_with_male_sign': {
                FIELD_SYMBOL: '🤦\u200d♂️',
                FIELD_NAME: 'Twarz palm z male sign',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'shrug_with_female_sign': {
                FIELD_SYMBOL: '🤷\u200d♀️',
                FIELD_NAME: 'Shrug z female sign',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: True
            },
            'shrug': {
                FIELD_SYMBOL: '🤷',
                FIELD_NAME: 'Wzruszać ramionami',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'shrug_2': {
                FIELD_SYMBOL: '🤷🏻\u200d️',
                FIELD_NAME: 'Shrug 2',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'person_with_pouting_face_with_female_sign': {
                FIELD_SYMBOL: '🙎\u200d♀️',
                FIELD_NAME: 'Person z pouting twarz z female sign',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'person_with_pouting_face': {
                FIELD_SYMBOL: '🙎',
                FIELD_NAME: 'Osoba z Pouting Face',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'person_with_pouting_face_with_male_sign': {
                FIELD_SYMBOL: '🙎\u200d♂️',
                FIELD_NAME: 'Person z pouting twarz z male sign',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'person_frowning_with_female_sign': {
                FIELD_SYMBOL: '🙍\u200d♀️',
                FIELD_NAME: 'Person frowning z female sign',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'person_frowning': {
                FIELD_SYMBOL: '🙍',
                FIELD_NAME: 'Osoba marszcząca brwi',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'person_frowning_with_male_sign': {
                FIELD_SYMBOL: '🙍\u200d♂️',
                FIELD_NAME: 'Person frowning z male sign',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'haircut_with_female_sign': {
                FIELD_SYMBOL: '💇\u200d♀️',
                FIELD_NAME: 'Haircut z female sign',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'haircut': {
                FIELD_SYMBOL: '💇',
                FIELD_NAME: 'Ostrzyżenie',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'haircut_with_male_sign': {
                FIELD_SYMBOL: '💇\u200d♂️',
                FIELD_NAME: 'Haircut z male sign',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'face_massage_with_female_sign': {
                FIELD_SYMBOL: '💆\u200d♀️',
                FIELD_NAME: 'Twarz massage z female sign',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'face_massage': {
                FIELD_SYMBOL: '💆',
                FIELD_NAME: 'Masaż twarzy',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'face_massage_with_male_sign': {
                FIELD_SYMBOL: '💆\u200d♂️',
                FIELD_NAME: 'Twarz massage z male sign',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'person_in_steamy_room_with_female_sign': {
                FIELD_SYMBOL: '🧖\u200d♀️',
                FIELD_NAME: 'Person in steamy room z female sign',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'person_in_steamy_room': {
                FIELD_SYMBOL: '🧖',
                FIELD_NAME: 'Osoba W Pokoju Parnym',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'person_in_steamy_room_with_male_sign': {
                FIELD_SYMBOL: '🧖\u200d♂️',
                FIELD_NAME: 'Person in steamy room z male sign',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'woman_with_heavy_black_heart_with_man': {
                FIELD_SYMBOL: '👩\u200d❤️\u200d👨',
                FIELD_NAME: 'Woman z heavy czarny sercem z man',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'woman_with_heavy_black_heart_with_woman': {
                FIELD_SYMBOL: '👩\u200d❤️\u200d👩',
                FIELD_NAME: 'Woman z heavy czarny sercem z woman',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'adult_with_heavy_black_heart_with_adult': {
                FIELD_SYMBOL: '🧑\u200d❤️\u200d🧑',
                FIELD_NAME: 'Adult z heavy czarny sercem z adult',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'man_with_heavy_black_heart_with_man': {
                FIELD_SYMBOL: '👨\u200d❤️\u200d👨',
                FIELD_NAME: 'Man z heavy czarny sercem z man',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'woman_with_heavy_black_heart_with_kiss_mark_with_man': {
                FIELD_SYMBOL: '👩\u200d❤️\u200d💋\u200d👨',
                FIELD_NAME: 'Woman z heavy czarny sercem z kiss mark z man',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'woman_with_heavy_black_heart_with_kiss_mark_with_woman': {
                FIELD_SYMBOL: '👩\u200d❤️\u200d💋\u200d👩',
                FIELD_NAME: 'Woman z heavy czarny sercem z kiss mark z woman',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'adult_with_heavy_black_heart_with_kiss_mark_with_adult': {
                FIELD_SYMBOL: '🧑\u200d❤️\u200d💋\u200d🧑',
                FIELD_NAME: 'Adult z heavy czarny sercem z kiss mark z adult',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'man_with_heavy_black_heart_with_kiss_mark_with_man': {
                FIELD_SYMBOL: '👨\u200d❤️\u200d💋\u200d👨',
                FIELD_NAME: 'Man z heavy czarny sercem z kiss mark z man',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
        },
        BODY_PARTS: {
            'flexed_biceps': {
                FIELD_SYMBOL: '💪',
                FIELD_NAME: 'Zgięte bicepsy',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: False
            },
            'mechanical_arm': {
                FIELD_SYMBOL: '🦾',
                FIELD_NAME: 'Ramię mechaniczne',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'foot': {
                FIELD_SYMBOL: '🦶',
                FIELD_NAME: 'Stopa',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: False
            },
            'leg': {
                FIELD_SYMBOL: '🦵',
                FIELD_NAME: 'Noga',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: False
            },
            'mechanical_leg': {
                FIELD_SYMBOL: '🦿',
                FIELD_NAME: 'Mechaniczna noga',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: False
            },
            'kiss_mark': {
                FIELD_SYMBOL: '💋',
                FIELD_NAME: 'Ślad pocałunku',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'mouth': {
                FIELD_SYMBOL: '👄',
                FIELD_NAME: 'Usta',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'biting_lip': {
                FIELD_SYMBOL: '🫦',
                FIELD_NAME: 'Przygryzanie Wargi',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'tooth': {
                FIELD_SYMBOL: '🦷',
                FIELD_NAME: 'Ząb',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'tongue': {
                FIELD_SYMBOL: '👅',
                FIELD_NAME: 'Język',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'ear': {
                FIELD_SYMBOL: '👂',
                FIELD_NAME: 'Ucho',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: False
            },
            'ear_with_hearing_aid': {
                FIELD_SYMBOL: '🦻',
                FIELD_NAME: 'Ucho z aparatem słuchowym',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: False
            },
            'nose': {
                FIELD_SYMBOL: '👃',
                FIELD_NAME: 'Nos',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: False
            },
            'eye': {
                FIELD_SYMBOL: '👁',
                FIELD_NAME: 'Oko',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'eyes': {
                FIELD_SYMBOL: '️👀',
                FIELD_NAME: 'Oczy',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'anatomical_heart': {
                FIELD_SYMBOL: '🫀',
                FIELD_NAME: 'Anatomiczne serce',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'lungs': {
                FIELD_SYMBOL: '🫁',
                FIELD_NAME: 'Płuca',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'brain': {
                FIELD_SYMBOL: '🧠',
                FIELD_NAME: 'Mózg',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
        },
        ACTIVITIES_AND_POSTURES: {
            'dancer': {
                FIELD_SYMBOL: '💃',
                FIELD_NAME: 'Tancerz',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'man_dancing': {
                FIELD_SYMBOL: '🕺',
                FIELD_NAME: 'Człowiek tańczy',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'adult_with_ballet_shoes': {
                FIELD_SYMBOL: '🧑\u200d🩰',
                FIELD_NAME: 'Adult z ballet shoes',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'woman_with_bunny_ears_with_female_sign': {
                FIELD_SYMBOL: '👯\u200d♀️',
                FIELD_NAME: 'Woman z bunny ears z female sign',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'woman_with_bunny_ears': {
                FIELD_SYMBOL: '👯',
                FIELD_NAME: 'Kobieta z uszy królika',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'woman_with_bunny_ears_with_male_sign': {
                FIELD_SYMBOL: '👯\u200d♂️',
                FIELD_NAME: 'Woman z bunny ears z male sign',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'man_in_business_suit_levitating': {
                FIELD_SYMBOL: '🕴️',
                FIELD_NAME: 'Człowiek w garniturze Lewitujący',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'woman_with_manual_wheelchair': {
                FIELD_SYMBOL: '👩\u200d🦽',
                FIELD_NAME: 'Woman z manual wheelchair',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'adult_with_manual_wheelchair': {
                FIELD_SYMBOL: '🧑\u200d🦽',
                FIELD_NAME: 'Adult z manual wheelchair',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'man_with_manual_wheelchair': {
                FIELD_SYMBOL: '👨\u200d🦽',
                FIELD_NAME: 'Man z manual wheelchair',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'woman_with_manual_wheelchair_with_black_rightwards_arrow': {
                FIELD_SYMBOL: '👩\u200d🦽\u200d➡️',
                FIELD_NAME: 'Woman z manual wheelchair z czarny rightwards strzałka',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'adult_with_manual_wheelchair_with_black_rightwards_arrow': {
                FIELD_SYMBOL: '🧑\u200d🦽\u200d➡️',
                FIELD_NAME: 'Adult z manual wheelchair z czarny rightwards strzałka',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'man_with_manual_wheelchair_with_black_rightwards_arrow': {
                FIELD_SYMBOL: '👨\u200d🦽\u200d➡️',
                FIELD_NAME: 'Man z manual wheelchair z czarny rightwards strzałka',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'woman_with_motorized_wheelchair': {
                FIELD_SYMBOL: '👩\u200d🦼',
                FIELD_NAME: 'Woman z motorized wheelchair',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'adult_with_motorized_wheelchair': {
                FIELD_SYMBOL: '🧑\u200d🦼',
                FIELD_NAME: 'Adult z motorized wheelchair',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'man_with_motorized_wheelchair': {
                FIELD_SYMBOL: '👨\u200d🦼',
                FIELD_NAME: 'Man z motorized wheelchair',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'woman_with_motorized_wheelchair_with_black_rightwards_arrow': {
                FIELD_SYMBOL: '👩\u200d🦼\u200d➡️',
                FIELD_NAME: 'Woman z motorized wheelchair z czarny rightwards strzałka',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'adult_with_motorized_wheelchair_with_black_rightwards_arrow': {
                FIELD_SYMBOL: '🧑\u200d🦼\u200d➡️',
                FIELD_NAME: 'Adult z motorized wheelchair z czarny rightwards strzałka',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'man_with_motorized_wheelchair_with_black_rightwards_arrow': {
                FIELD_SYMBOL: '👨\u200d🦼\u200d➡️',
                FIELD_NAME: 'Man z motorized wheelchair z czarny rightwards strzałka',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'pedestrian_with_female_sign': {
                FIELD_SYMBOL: '🚶\u200d♀️',
                FIELD_NAME: 'Pedestrian z female sign',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: True
            },
            'pedestrian': {
                FIELD_SYMBOL: '🚶',
                FIELD_NAME: 'Pieszy',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'pedestrian_with_male_sign': {
                FIELD_SYMBOL: '🚶\u200d♂️',
                FIELD_NAME: 'Pedestrian z male sign',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: True
            },
            'pedestrian_with_female_sign_with_black_rightwards_arrow': {
                FIELD_SYMBOL: '🚶\u200d♀️\u200d➡️',
                FIELD_NAME: 'Pedestrian z female sign z czarny rightwards strzałka',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: True
            },
            'pedestrian_with_black_rightwards_arrow': {
                FIELD_SYMBOL: '🚶\u200d➡️',
                FIELD_NAME: 'Pedestrian z czarny rightwards strzałka',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'pedestrian_with_male_sign_with_black_rightwards_arrow': {
                FIELD_SYMBOL: '🚶\u200d♂️\u200d➡️',
                FIELD_NAME: 'Pedestrian z male sign z czarny rightwards strzałka',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: True
            },
            'woman_with_probing_cane': {
                FIELD_SYMBOL: '👩\u200d🦯',
                FIELD_NAME: 'Woman z probing cane',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'adult_with_probing_cane': {
                FIELD_SYMBOL: '🧑\u200d🦯',
                FIELD_NAME: 'Adult z probing cane',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'man_with_probing_cane': {
                FIELD_SYMBOL: '👨\u200d🦯',
                FIELD_NAME: 'Man z probing cane',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'woman_with_probing_cane_with_black_rightwards_arrow': {
                FIELD_SYMBOL: '👩\u200d🦯\u200d➡️',
                FIELD_NAME: 'Woman z probing cane z czarny rightwards strzałka',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'adult_with_probing_cane_with_black_rightwards_arrow': {
                FIELD_SYMBOL: '🧑\u200d🦯\u200d➡️',
                FIELD_NAME: 'Adult z probing cane z czarny rightwards strzałka',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'man_with_probing_cane_with_black_rightwards_arrow': {
                FIELD_SYMBOL: '👨\u200d🦯\u200d➡️',
                FIELD_NAME: 'Man z probing cane z czarny rightwards strzałka',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'kneeling_person_with_female_sign': {
                FIELD_SYMBOL: '🧎\u200d♀️',
                FIELD_NAME: 'Kneeling person z female sign',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'kneeling_person': {
                FIELD_SYMBOL: '🧎',
                FIELD_NAME: 'Klęcząca osoba',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'kneeling_person_with_male_sign': {
                FIELD_SYMBOL: '🧎\u200d♂️',
                FIELD_NAME: 'Kneeling person z male sign',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'runner_with_female_sign': {
                FIELD_SYMBOL: '🏃\u200d♀️',
                FIELD_NAME: 'Runner z female sign',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'runner': {
                FIELD_SYMBOL: '🏃',
                FIELD_NAME: 'Biegacz',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'runner_with_male_sign': {
                FIELD_SYMBOL: '🏃\u200d♂️',
                FIELD_NAME: 'Runner z male sign',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'runner_with_female_sign_with_black_rightwards_arrow': {
                FIELD_SYMBOL: '🏃\u200d♀️\u200d➡️',
                FIELD_NAME: 'Runner z female sign z czarny rightwards strzałka',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'runner_with_black_rightwards_arrow': {
                FIELD_SYMBOL: '🏃\u200d➡️',
                FIELD_NAME: 'Runner z czarny rightwards strzałka',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'runner_with_male_sign_with_black_rightwards_arrow': {
                FIELD_SYMBOL: '🏃\u200d♂️\u200d➡️',
                FIELD_NAME: 'Runner z male sign z czarny rightwards strzałka',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'kneeling_person_with_female_sign_with_black_rightwards_arrow': {
                FIELD_SYMBOL: '🧎\u200d♀️\u200d➡️',
                FIELD_NAME: 'Kneeling person z female sign z czarny rightwards strzałka',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'kneeling_person_with_black_rightwards_arrow': {
                FIELD_SYMBOL: '🧎\u200d➡️',
                FIELD_NAME: 'Kneeling person z czarny rightwards strzałka',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'kneeling_person_with_male_sign_with_black_rightwards_arrow': {
                FIELD_SYMBOL: '🧎\u200d♂️\u200d➡️',
                FIELD_NAME: 'Kneeling person z male sign z czarny rightwards strzałka',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'standing_person_with_female_sign': {
                FIELD_SYMBOL: '🧍\u200d♀️',
                FIELD_NAME: 'Standing person z female sign',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'standing_person': {
                FIELD_SYMBOL: '🧍',
                FIELD_NAME: 'Stojąca osoba',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'standing_person_with_male_sign': {
                FIELD_SYMBOL: '🧍\u200d♂️',
                FIELD_NAME: 'Standing person z male sign',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'man_and_woman_holding_hands': {
                FIELD_SYMBOL: '👫',
                FIELD_NAME: 'Mężczyzna i kobieta trzymając się za ręce',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'two_women_holding_hands': {
                FIELD_SYMBOL: '👭',
                FIELD_NAME: 'Dwie kobiety trzymając się za ręce',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: False
            },
            'two_men_holding_hands': {
                FIELD_SYMBOL: '👬',
                FIELD_NAME: 'Dwóch mężczyzn, trzymając się za ręce',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: False
            },
            'skier': {
                FIELD_SYMBOL: '⛷️',
                FIELD_NAME: 'Narciarz',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'snowboarder': {
                FIELD_SYMBOL: '🏂',
                FIELD_NAME: 'Snowboarder',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'parachute': {
                FIELD_SYMBOL: '🪂',
                FIELD_NAME: 'Spadochron',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'weight_lifter_with_female_sign': {
                FIELD_SYMBOL: '🏋️\u200d♀️',
                FIELD_NAME: 'Weight lifter z female sign',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'weight_lifter': {
                FIELD_SYMBOL: '🏋️',
                FIELD_NAME: 'Podnośnik wagi',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: False
            },
            'weight_lifter_with_male_sign': {
                FIELD_SYMBOL: '🏋️\u200d♂️',
                FIELD_NAME: 'Weight lifter z male sign',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'wrestlers_with_female_sign': {
                FIELD_SYMBOL: '🤼\u200d♀️',
                FIELD_NAME: 'Wrestlers z female sign',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: True
            },
            'wrestlers': {
                FIELD_SYMBOL: '🤼',
                FIELD_NAME: 'Zapaśnicy',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: True
            },
            'wrestlers_with_male_sign': {
                FIELD_SYMBOL: '🤼\u200d♂️',
                FIELD_NAME: 'Wrestlers z male sign',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: True
            },
            'person_doing_cartwheel_with_female_sign': {
                FIELD_SYMBOL: '🤸\u200d♀️',
                FIELD_NAME: 'Person doing cartwheel z female sign',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'person_doing_cartwheel': {
                FIELD_SYMBOL: '🤸',
                FIELD_NAME: 'Osoba robi Cartwheel',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'person_doing_cartwheel_with_male_sign': {
                FIELD_SYMBOL: '🤸\u200d♂️',
                FIELD_NAME: 'Person doing cartwheel z male sign',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'person_with_ball_with_female_sign': {
                FIELD_SYMBOL: '⛹️\u200d♀️',
                FIELD_NAME: 'Person z ball z female sign',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'person_with_ball': {
                FIELD_SYMBOL: '⛹️',
                FIELD_NAME: 'Osoba z piłką',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'person_with_ball_with_male_sign': {
                FIELD_SYMBOL: '⛹️\u200d♂️',
                FIELD_NAME: 'Person z ball z male sign',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'fencer': {
                FIELD_SYMBOL: '🤺',
                FIELD_NAME: 'Szermierz',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'handball_with_female_sign': {
                FIELD_SYMBOL: '🤾\u200d♀️',
                FIELD_NAME: 'Handball z female sign',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: True
            },
            'handball': {
                FIELD_SYMBOL: '🤾',
                FIELD_NAME: 'Gra w piłkę ręczną',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: True
            },
            'handball_with_male_sign': {
                FIELD_SYMBOL: '🤾\u200d♂️',
                FIELD_NAME: 'Handball z male sign',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: True
            },
            'golfer_with_female_sign': {
                FIELD_SYMBOL: '🏌️\u200d♀️',
                FIELD_NAME: 'Golfer z female sign',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'golfer': {
                FIELD_SYMBOL: '🏌️',
                FIELD_NAME: 'Golfista',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'golfer_with_male_sign': {
                FIELD_SYMBOL: '🏌️\u200d♂️',
                FIELD_NAME: 'Golfer z male sign',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'horse_racing': {
                FIELD_SYMBOL: '🏇',
                FIELD_NAME: 'Wyścigi konne',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'person_in_lotus_position_with_female_sign': {
                FIELD_SYMBOL: '🧘\u200d♀️',
                FIELD_NAME: 'Person in lotus position z female sign',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'person_in_lotus_position': {
                FIELD_SYMBOL: '🧘',
                FIELD_NAME: 'Osoba W Pozycji Lotosu',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'person_in_lotus_position_with_male_sign': {
                FIELD_SYMBOL: '🧘\u200d♂️',
                FIELD_NAME: 'Person in lotus position z male sign',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'surfer_with_female_sign': {
                FIELD_SYMBOL: '🏄\u200d♀️',
                FIELD_NAME: 'Surfer z female sign',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'surfer': {
                FIELD_SYMBOL: '🏄',
                FIELD_NAME: 'Surfer',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'surfer_with_male_sign': {
                FIELD_SYMBOL: '🏄\u200d♂️',
                FIELD_NAME: 'Surfer z male sign',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'swimmer_with_female_sign': {
                FIELD_SYMBOL: '🏊\u200d♀️',
                FIELD_NAME: 'Swimmer z female sign',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'swimmer': {
                FIELD_SYMBOL: '🏊',
                FIELD_NAME: 'Pływak',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'swimmer_with_male_sign': {
                FIELD_SYMBOL: '🏊\u200d♂️',
                FIELD_NAME: 'Swimmer z male sign',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'water_polo_with_female_sign': {
                FIELD_SYMBOL: '🤽\u200d♀️',
                FIELD_NAME: 'Water polo z female sign',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: True
            },
            'water_polo': {
                FIELD_SYMBOL: '🤽',
                FIELD_NAME: 'Wodne polo',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'water_polo_with_male_sign': {
                FIELD_SYMBOL: '🤽\u200d♂️',
                FIELD_NAME: 'Water polo z male sign',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: True
            },
            'rowboat_with_female_sign': {
                FIELD_SYMBOL: '🚣\u200d♀️',
                FIELD_NAME: 'Rowboat z female sign',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'rowboat': {
                FIELD_SYMBOL: '🚣',
                FIELD_NAME: 'Rowboat',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'rowboat_with_male_sign': {
                FIELD_SYMBOL: '🚣\u200d♂️',
                FIELD_NAME: 'Rowboat z male sign',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'person_climbing_with_female_sign': {
                FIELD_SYMBOL: '🧗\u200d♀️',
                FIELD_NAME: 'Person climbing z female sign',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'person_climbing': {
                FIELD_SYMBOL: '🧗',
                FIELD_NAME: 'Wspinaczka osobowa',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'person_climbing_with_male_sign': {
                FIELD_SYMBOL: '🧗\u200d♂️',
                FIELD_NAME: 'Person climbing z male sign',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'mountain_bicyclist_with_female_sign': {
                FIELD_SYMBOL: '🚵\u200d♀️',
                FIELD_NAME: 'Mountain bicyclist z female sign',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'mountain_bicyclist': {
                FIELD_SYMBOL: '🚵',
                FIELD_NAME: 'Mountain Bicyclist',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'mountain_bicyclist_with_male_sign': {
                FIELD_SYMBOL: '🚵\u200d♂️',
                FIELD_NAME: 'Mountain bicyclist z male sign',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'bicyclist_with_female_sign': {
                FIELD_SYMBOL: '🚴\u200d♀️',
                FIELD_NAME: 'Bicyclist z female sign',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'bicyclist': {
                FIELD_SYMBOL: '🚴',
                FIELD_NAME: 'Kolarz',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'bicyclist_with_male_sign': {
                FIELD_SYMBOL: '🚴\u200d♂️',
                FIELD_NAME: 'Bicyclist z male sign',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'juggling_with_female_sign': {
                FIELD_SYMBOL: '🤹\u200d♀️',
                FIELD_NAME: 'Juggling z female sign',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'juggling': {
                FIELD_SYMBOL: '🤹',
                FIELD_NAME: 'Żonglerka',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'juggling_with_male_sign': {
                FIELD_SYMBOL: '🤹\u200d♂️',
                FIELD_NAME: 'Juggling z male sign',
                FIELD_SUPPORT_COLOR: True,
                FIELD_SUPPORT_SEX: True
            },
            'speaking_head_in_silhouette': {
                FIELD_SYMBOL: '🗣️',
                FIELD_NAME: 'Mówiąc Głową W Sylwetce',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'bust_in_silhouette': {
                FIELD_SYMBOL: '👤',
                FIELD_NAME: 'Popiersie w sylwetce',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'busts_in_silhouette': {
                FIELD_SYMBOL: '👥',
                FIELD_NAME: 'Popiersia W Sylwetce',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'people_hugging': {
                FIELD_SYMBOL: '🫂',
                FIELD_NAME: 'Przytulanie ludzi',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
        },
        CLOTHING_AND_ACCESSORIES: {
            'lipstick': {
                FIELD_SYMBOL: '💄',
                FIELD_NAME: 'Szminka',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'nail_polish': {
                FIELD_SYMBOL: '💅',
                FIELD_NAME: 'Lakier do paznokci',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'selfie': {
                FIELD_SYMBOL: '🤳',
                FIELD_NAME: 'Selfie',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'knot': {
                FIELD_SYMBOL: '🪢',
                FIELD_NAME: 'Węzeł',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'ball_of_yarn': {
                FIELD_SYMBOL: '🧶',
                FIELD_NAME: 'Piłka Przędzy',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'spool_of_thread': {
                FIELD_SYMBOL: '🧵',
                FIELD_NAME: 'Szpula nici',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'sewing_needle': {
                FIELD_SYMBOL: '🪡',
                FIELD_NAME: 'Igła',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'coat': {
                FIELD_SYMBOL: '🧥',
                FIELD_NAME: 'Płaszcz',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'lab_coat': {
                FIELD_SYMBOL: '🥼',
                FIELD_NAME: 'Fartuch laboratoryjny',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'safety_vest': {
                FIELD_SYMBOL: '🦺',
                FIELD_NAME: 'Kamizelka bezpieczeństwa',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'womans_clothes': {
                FIELD_SYMBOL: '👚',
                FIELD_NAME: 'Womans Odzież',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            't_shirt': {
                FIELD_SYMBOL: '👕',
                FIELD_NAME: 'Podkoszulek',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'jeans': {
                FIELD_SYMBOL: '👖',
                FIELD_NAME: 'Dżinsy',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'briefs': {
                FIELD_SYMBOL: '🩲',
                FIELD_NAME: 'Majtki',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'shorts': {
                FIELD_SYMBOL: '🩳',
                FIELD_NAME: 'Szorty',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'necktie': {
                FIELD_SYMBOL: '👔',
                FIELD_NAME: 'Krawat',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'dress': {
                FIELD_SYMBOL: '👗',
                FIELD_NAME: 'Sukienka',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'bikini': {
                FIELD_SYMBOL: '👙',
                FIELD_NAME: 'Bikini',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'one_piece_swimsuit': {
                FIELD_SYMBOL: '🩱',
                FIELD_NAME: 'Jednoczęściowy kostium kąpielowy',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'kimono': {
                FIELD_SYMBOL: '👘',
                FIELD_NAME: 'Kimono',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'sari': {
                FIELD_SYMBOL: '🥻',
                FIELD_NAME: 'Sari',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'thong_sandal': {
                FIELD_SYMBOL: '🩴',
                FIELD_NAME: 'Sandały typu stringi',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'flat_shoe': {
                FIELD_SYMBOL: '🥿',
                FIELD_NAME: 'Płaskie buty',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'high_heeled_shoe': {
                FIELD_SYMBOL: '👠',
                FIELD_NAME: 'But na wysokim obcasie',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'womans_sandal': {
                FIELD_SYMBOL: '👡',
                FIELD_NAME: 'Womans Sandal',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'womans_boots': {
                FIELD_SYMBOL: '👢',
                FIELD_NAME: 'Womans Boots',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'mans_shoe': {
                FIELD_SYMBOL: '👞',
                FIELD_NAME: 'Mans Shoe',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'athletic_shoe': {
                FIELD_SYMBOL: '👟',
                FIELD_NAME: 'Buty sportowe',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'hiking_boot': {
                FIELD_SYMBOL: '🥾',
                FIELD_NAME: 'But do wędrówek',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'socks': {
                FIELD_SYMBOL: '🧦',
                FIELD_NAME: 'Skarpety',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'gloves': {
                FIELD_SYMBOL: '🧤',
                FIELD_NAME: 'Rękawiczki',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'scarf': {
                FIELD_SYMBOL: '🧣',
                FIELD_NAME: 'Szalik',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'top_hat': {
                FIELD_SYMBOL: '🎩',
                FIELD_NAME: 'Cylinder',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'billed_cap': {
                FIELD_SYMBOL: '🧢',
                FIELD_NAME: 'Zafakturowana czapka',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'womans_hat': {
                FIELD_SYMBOL: '👒',
                FIELD_NAME: 'Womans Hat',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'graduation_cap': {
                FIELD_SYMBOL: '🎓',
                FIELD_NAME: 'Czapka Graduation',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'helmet_with_white_cross': {
                FIELD_SYMBOL: '⛑️',
                FIELD_NAME: 'Kask z Białym Krzyżem',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'military_helmet': {
                FIELD_SYMBOL: '🪖',
                FIELD_NAME: 'Hełm wojskowy',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'crown': {
                FIELD_SYMBOL: '👑',
                FIELD_NAME: 'Korona',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'ring': {
                FIELD_SYMBOL: '💍',
                FIELD_NAME: 'Pierścień',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'pouch': {
                FIELD_SYMBOL: '👝',
                FIELD_NAME: 'Kieszonka',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'purse': {
                FIELD_SYMBOL: '👛',
                FIELD_NAME: 'Portmonetka',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'handbag': {
                FIELD_SYMBOL: '👜',
                FIELD_NAME: 'Torebka',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'briefcase': {
                FIELD_SYMBOL: '💼',
                FIELD_NAME: 'Aktówka',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'school_satchel': {
                FIELD_SYMBOL: '🎒',
                FIELD_NAME: 'Tornister szkolny',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'luggage': {
                FIELD_SYMBOL: '🧳',
                FIELD_NAME: 'Bagaż',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'eyeglasses': {
                FIELD_SYMBOL: '👓',
                FIELD_NAME: 'Okulary',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'dark_sunglasses': {
                FIELD_SYMBOL: '🕶️',
                FIELD_NAME: 'Ciemne okulary',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'goggles': {
                FIELD_SYMBOL: '🥽',
                FIELD_NAME: 'Okulary ochronne',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'closed_umbrella': {
                FIELD_SYMBOL: '🌂',
                FIELD_NAME: 'Zamknięty parasol',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'probing_cane': {
                FIELD_SYMBOL: '🦯',
                FIELD_NAME: 'Laska do sondowania',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'manual_wheelchair': {
                FIELD_SYMBOL: '🦽',
                FIELD_NAME: 'Ręczny wózek inwalidzki',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'motorized_wheelchair': {
                FIELD_SYMBOL: '🦼',
                FIELD_NAME: 'Zmotoryzowany wózek inwalidzki',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'crutch': {
                FIELD_SYMBOL: '🩼',
                FIELD_NAME: 'Kula',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
        },
        ANIMALS: {
            'dog_face': {
                FIELD_SYMBOL: '🐶',
                FIELD_NAME: 'Pysk',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'cat_face': {
                FIELD_SYMBOL: '🐱',
                FIELD_NAME: 'Kocia twarz',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'mouse_face': {
                FIELD_SYMBOL: '🐭',
                FIELD_NAME: 'Twarz Myszy',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'hamster_face': {
                FIELD_SYMBOL: '🐹',
                FIELD_NAME: 'Twarz chomika',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'rabbit_face': {
                FIELD_SYMBOL: '🐰',
                FIELD_NAME: 'Królik Twarz',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'fox_face': {
                FIELD_SYMBOL: '🦊',
                FIELD_NAME: 'Twarz Lisa',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'bear_face': {
                FIELD_SYMBOL: '🐻',
                FIELD_NAME: 'Twarz Niedźwiedzia',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'panda_face': {
                FIELD_SYMBOL: '🐼',
                FIELD_NAME: 'Twarz Pandy',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'bear_face_with_snowflake': {
                FIELD_SYMBOL: '🐻\u200d❄️',
                FIELD_NAME: 'Bear twarz z snowflake',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'koala': {
                FIELD_SYMBOL: '🐨',
                FIELD_NAME: 'Koala',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'tiger_face': {
                FIELD_SYMBOL: '🐯',
                FIELD_NAME: 'Tygrysia Twarz',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'lion_face': {
                FIELD_SYMBOL: '🦁',
                FIELD_NAME: 'Twarz Lwa',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'cow_face': {
                FIELD_SYMBOL: '🐮',
                FIELD_NAME: 'Twarz krowy',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'pig_face': {
                FIELD_SYMBOL: '🐷',
                FIELD_NAME: 'Twarz świni',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'pig_nose': {
                FIELD_SYMBOL: '🐽',
                FIELD_NAME: 'Świński nos',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'frog_face': {
                FIELD_SYMBOL: '🐸',
                FIELD_NAME: 'Żaba Twarz',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'monkey_face': {
                FIELD_SYMBOL: '🐵',
                FIELD_NAME: 'Twarz małpy',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'see_no_evil_monkey': {
                FIELD_SYMBOL: '🙈',
                FIELD_NAME: 'Zobacz-No-Evil Monkey',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'hear_no_evil_monkey': {
                FIELD_SYMBOL: '🙉',
                FIELD_NAME: 'Słuchaj, nie zła małpa',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'speak_no_evil_monkey': {
                FIELD_SYMBOL: '🙊',
                FIELD_NAME: 'Mów-No-Evil Monkey',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'monkey': {
                FIELD_SYMBOL: '🐒',
                FIELD_NAME: 'Małpa',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'chicken': {
                FIELD_SYMBOL: '🐔',
                FIELD_NAME: 'kurczak',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'penguin': {
                FIELD_SYMBOL: '🐧',
                FIELD_NAME: 'Pingwin',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'bird': {
                FIELD_SYMBOL: '🐦',
                FIELD_NAME: 'Ptak',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'baby_chick': {
                FIELD_SYMBOL: '🐤',
                FIELD_NAME: 'Baby Chick',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'hatching_chick': {
                FIELD_SYMBOL: '🐣',
                FIELD_NAME: 'Pisklę',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'front_facing_baby_chick': {
                FIELD_SYMBOL: '🐥',
                FIELD_NAME: 'Przednia laska z przodu',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'goose': {
                FIELD_SYMBOL: '🪿',
                FIELD_NAME: 'Gęś',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'duck': {
                FIELD_SYMBOL: '🦆',
                FIELD_NAME: 'kaczka',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'bird_with_black_large_square': {
                FIELD_SYMBOL: '🐦\u200d⬛',
                FIELD_NAME: 'Bird z czarny large kwadrat',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'eagle': {
                FIELD_SYMBOL: '🦅',
                FIELD_NAME: 'Orzeł',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'owl': {
                FIELD_SYMBOL: '🦉',
                FIELD_NAME: 'Sowa',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'bat': {
                FIELD_SYMBOL: '🦇',
                FIELD_NAME: 'Nietoperz',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'wolf_face': {
                FIELD_SYMBOL: '🐺',
                FIELD_NAME: 'Wilcza Twarz',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'boar': {
                FIELD_SYMBOL: '🐗',
                FIELD_NAME: 'Dzik',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'horse_face': {
                FIELD_SYMBOL: '🐴',
                FIELD_NAME: 'Twarz konia',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'unicorn_face': {
                FIELD_SYMBOL: '🦄',
                FIELD_NAME: 'Jednorożec Twarz',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'moose': {
                FIELD_SYMBOL: '🫎',
                FIELD_NAME: 'Łoś',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'honeybee': {
                FIELD_SYMBOL: '🐝',
                FIELD_NAME: 'Pszczoła miodna',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'worm': {
                FIELD_SYMBOL: '🪱',
                FIELD_NAME: 'Robak',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'bug': {
                FIELD_SYMBOL: '🐛',
                FIELD_NAME: 'Pluskwa',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'butterfly': {
                FIELD_SYMBOL: '🦋',
                FIELD_NAME: 'Motyl',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'snail': {
                FIELD_SYMBOL: '🐌',
                FIELD_NAME: 'Ślimak',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'lady_beetle': {
                FIELD_SYMBOL: '🐞',
                FIELD_NAME: 'Lady Beetle',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'ant': {
                FIELD_SYMBOL: '🐜',
                FIELD_NAME: 'Mrówka',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'fly': {
                FIELD_SYMBOL: '🪰',
                FIELD_NAME: 'latać',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'beetle': {
                FIELD_SYMBOL: '🪲',
                FIELD_NAME: 'Chrząszcz',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'cockroach': {
                FIELD_SYMBOL: '🪳',
                FIELD_NAME: 'Karaluch',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'mosquito': {
                FIELD_SYMBOL: '🦟',
                FIELD_NAME: 'Komar',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'cricket': {
                FIELD_SYMBOL: '🦗',
                FIELD_NAME: 'Krykiet',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'spider': {
                FIELD_SYMBOL: '🕷️',
                FIELD_NAME: 'Pająk',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'spider_web': {
                FIELD_SYMBOL: '🕸️',
                FIELD_NAME: 'Pajęcza sieć',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'scorpion': {
                FIELD_SYMBOL: '🦂',
                FIELD_NAME: 'Skorpion',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'turtle': {
                FIELD_SYMBOL: '🐢',
                FIELD_NAME: 'żółw',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'snake': {
                FIELD_SYMBOL: '🐍',
                FIELD_NAME: 'Wąż',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'lizard': {
                FIELD_SYMBOL: '🦎',
                FIELD_NAME: 'Jaszczurka',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            't_rex': {
                FIELD_SYMBOL: '🦖',
                FIELD_NAME: 'T-Rex',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'sauropod': {
                FIELD_SYMBOL: '🦕',
                FIELD_NAME: 'Sauropod',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'octopus': {
                FIELD_SYMBOL: '🐙',
                FIELD_NAME: 'Ośmiornica',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'squid': {
                FIELD_SYMBOL: '🦑',
                FIELD_NAME: 'Kałamarnica',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'jellyfish': {
                FIELD_SYMBOL: '🪼',
                FIELD_NAME: 'Meduza',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'shrimp': {
                FIELD_SYMBOL: '🦐',
                FIELD_NAME: 'Krewetka',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'lobster': {
                FIELD_SYMBOL: '🦞',
                FIELD_NAME: 'Homar',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'crab': {
                FIELD_SYMBOL: '🦀',
                FIELD_NAME: 'Krab',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'blowfish': {
                FIELD_SYMBOL: '🐡',
                FIELD_NAME: 'Blowfish',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'tropical_fish': {
                FIELD_SYMBOL: '🐠',
                FIELD_NAME: 'Tropikalna ryba',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'fish': {
                FIELD_SYMBOL: '🐟',
                FIELD_NAME: 'Ryba',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'dolphin': {
                FIELD_SYMBOL: '🐬',
                FIELD_NAME: 'Delfin',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'spouting_whale': {
                FIELD_SYMBOL: '🐳',
                FIELD_NAME: 'Spouting Whale',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'whale': {
                FIELD_SYMBOL: '🐋',
                FIELD_NAME: 'Wieloryb',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'emoji': {
                FIELD_SYMBOL: '\U0001facd',
                FIELD_NAME: 'Orka',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'shark': {
                FIELD_SYMBOL: '🦈',
                FIELD_NAME: 'Rekin',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'seal': {
                FIELD_SYMBOL: '🦭',
                FIELD_NAME: 'Foka',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'crocodile': {
                FIELD_SYMBOL: '🐊',
                FIELD_NAME: 'Krokodyl',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'tiger': {
                FIELD_SYMBOL: '🐅',
                FIELD_NAME: 'Tygrys',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'leopard': {
                FIELD_SYMBOL: '🐆',
                FIELD_NAME: 'Lampart',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'zebra_face': {
                FIELD_SYMBOL: '🦓',
                FIELD_NAME: 'Twarz Zebry',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'gorilla': {
                FIELD_SYMBOL: '🦍',
                FIELD_NAME: 'Goryl',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'orangutan': {
                FIELD_SYMBOL: '🦧',
                FIELD_NAME: 'Orangutan',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'emoji_2': {
                FIELD_SYMBOL: '\U0001fac8',
                FIELD_NAME: 'Owłosione stworzenie',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'mammoth': {
                FIELD_SYMBOL: '🦣',
                FIELD_NAME: 'Mamut',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'elephant': {
                FIELD_SYMBOL: '🐘',
                FIELD_NAME: 'Słoń',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'hippopotamus': {
                FIELD_SYMBOL: '🦛',
                FIELD_NAME: 'Hipopotam',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'rhinoceros': {
                FIELD_SYMBOL: '🦏',
                FIELD_NAME: 'Nosorożec',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'dromedary_camel': {
                FIELD_SYMBOL: '🐪',
                FIELD_NAME: 'Dromader Camel',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'bactrian_camel': {
                FIELD_SYMBOL: '🐫',
                FIELD_NAME: 'Dwugarbny wielbłąd',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'giraffe_face': {
                FIELD_SYMBOL: '🦒',
                FIELD_NAME: 'Twarz Żyrafy',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'kangaroo': {
                FIELD_SYMBOL: '🦘',
                FIELD_NAME: 'Kangur',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'bison': {
                FIELD_SYMBOL: '🦬',
                FIELD_NAME: 'Bizon',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'water_buffalo': {
                FIELD_SYMBOL: '🐃',
                FIELD_NAME: 'Wodny bawół',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'ox': {
                FIELD_SYMBOL: '🐂',
                FIELD_NAME: 'Wół',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'cow': {
                FIELD_SYMBOL: '🐄',
                FIELD_NAME: 'Krowa',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'donkey': {
                FIELD_SYMBOL: '🫏',
                FIELD_NAME: 'Osioł',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'horse': {
                FIELD_SYMBOL: '🐎',
                FIELD_NAME: 'Koń',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'pig': {
                FIELD_SYMBOL: '🐖',
                FIELD_NAME: 'Świnia',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'ram': {
                FIELD_SYMBOL: '🐏',
                FIELD_NAME: 'Baran',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'sheep': {
                FIELD_SYMBOL: '🐑',
                FIELD_NAME: 'Owca',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'llama': {
                FIELD_SYMBOL: '🦙',
                FIELD_NAME: 'Lama',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'goat': {
                FIELD_SYMBOL: '🐐',
                FIELD_NAME: 'Koza',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'deer': {
                FIELD_SYMBOL: '🦌',
                FIELD_NAME: 'Jeleń',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'dog': {
                FIELD_SYMBOL: '🐕',
                FIELD_NAME: 'Pies',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'poodle': {
                FIELD_SYMBOL: '🐩',
                FIELD_NAME: 'Pudel',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'guide_dog': {
                FIELD_SYMBOL: '🦮',
                FIELD_NAME: 'Pies przewodnik',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'dog_with_safety_vest': {
                FIELD_SYMBOL: '🐕\u200d🦺',
                FIELD_NAME: 'Pies z safety vest',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'cat': {
                FIELD_SYMBOL: '🐈',
                FIELD_NAME: 'Kot',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'cat_with_black_large_square': {
                FIELD_SYMBOL: '🐈\u200d⬛',
                FIELD_NAME: 'Kot z czarny large kwadrat',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'feather': {
                FIELD_SYMBOL: '🪶',
                FIELD_NAME: 'Pióro',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'wing': {
                FIELD_SYMBOL: '🪽',
                FIELD_NAME: 'Skrzydło',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'rooster': {
                FIELD_SYMBOL: '🐓',
                FIELD_NAME: 'Kogut',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'turkey': {
                FIELD_SYMBOL: '🦃',
                FIELD_NAME: 'indyk',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'dodo': {
                FIELD_SYMBOL: '🦤',
                FIELD_NAME: 'Dront',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'peacock': {
                FIELD_SYMBOL: '🦚',
                FIELD_NAME: 'Paw',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'parrot': {
                FIELD_SYMBOL: '🦜',
                FIELD_NAME: 'Papuga',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'swan': {
                FIELD_SYMBOL: '🦢',
                FIELD_NAME: 'Łabędź',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'flamingo': {
                FIELD_SYMBOL: '🦩',
                FIELD_NAME: 'Flaming',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'dove_of_peace': {
                FIELD_SYMBOL: '🕊️',
                FIELD_NAME: 'Gołąb pokoju',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'rabbit': {
                FIELD_SYMBOL: '🐇',
                FIELD_NAME: 'Królik',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'raccoon': {
                FIELD_SYMBOL: '🦝',
                FIELD_NAME: 'szop pracz',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'skunk': {
                FIELD_SYMBOL: '🦨',
                FIELD_NAME: 'Skunks',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'badger': {
                FIELD_SYMBOL: '🦡',
                FIELD_NAME: 'Borsuk',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'beaver': {
                FIELD_SYMBOL: '🦫',
                FIELD_NAME: 'Bóbr',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'otter': {
                FIELD_SYMBOL: '🦦',
                FIELD_NAME: 'Wydra',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'sloth': {
                FIELD_SYMBOL: '🦥',
                FIELD_NAME: 'Leniwiec',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'mouse': {
                FIELD_SYMBOL: '🐁',
                FIELD_NAME: 'Mysz',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'rat': {
                FIELD_SYMBOL: '🐀',
                FIELD_NAME: 'Szczur',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'chipmunk': {
                FIELD_SYMBOL: '🐿️',
                FIELD_NAME: 'Wiewiórka',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'hedgehog': {
                FIELD_SYMBOL: '🦔',
                FIELD_NAME: 'Jeż',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'paw_prints': {
                FIELD_SYMBOL: '🐾',
                FIELD_NAME: 'Odciski łap',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'dragon': {
                FIELD_SYMBOL: '🐉',
                FIELD_NAME: 'smok',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'dragon_face': {
                FIELD_SYMBOL: '🐲',
                FIELD_NAME: 'Smocza Twarz',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'bird_with_fire': {
                FIELD_SYMBOL: '🐦\u200d🔥',
                FIELD_NAME: 'Bird z fire',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'nest_with_eggs': {
                FIELD_SYMBOL: '🪺',
                FIELD_NAME: 'Gniazdo Z Jajkami',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'empty_nest': {
                FIELD_SYMBOL: '🪹',
                FIELD_NAME: 'Puste Gniazdo',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'spiral_shell': {
                FIELD_SYMBOL: '🐚',
                FIELD_NAME: 'Spiralna skorupa',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
        },
        NATURE_AND_PLANTS: {
            'cactus': {
                FIELD_SYMBOL: '🌵',
                FIELD_NAME: 'Kaktus',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'christmas_tree': {
                FIELD_SYMBOL: '🎄',
                FIELD_NAME: 'Drzewko świąteczne',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'evergreen_tree': {
                FIELD_SYMBOL: '🌲',
                FIELD_NAME: 'Wiecznie zielone drzewo',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'deciduous_tree': {
                FIELD_SYMBOL: '🌳',
                FIELD_NAME: 'Drzewo liściaste',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'palm_tree': {
                FIELD_SYMBOL: '🌴',
                FIELD_NAME: 'Drzewo palmowe',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'emoji': {
                FIELD_SYMBOL: '\U0001fabe',
                FIELD_NAME: 'Drzewo bez liści',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'wood': {
                FIELD_SYMBOL: '🪵',
                FIELD_NAME: 'Drewno',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'seedling': {
                FIELD_SYMBOL: '🌱',
                FIELD_NAME: 'Sadzonka',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'herb': {
                FIELD_SYMBOL: '🌿',
                FIELD_NAME: 'Ziele',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'shamrock': {
                FIELD_SYMBOL: '☘️',
                FIELD_NAME: 'koniczyna',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'four_leaf_clover': {
                FIELD_SYMBOL: '🍀',
                FIELD_NAME: 'Czterolistna koniczyna',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'pine_decoration': {
                FIELD_SYMBOL: '🎍',
                FIELD_NAME: 'Dekoracja Sosnowa',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'potted_plant': {
                FIELD_SYMBOL: '🪴',
                FIELD_NAME: 'Roślina doniczkowa',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'tanabata_tree': {
                FIELD_SYMBOL: '🎋',
                FIELD_NAME: 'Drzewo Tanabata',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'leaf_fluttering_in_wind': {
                FIELD_SYMBOL: '🍃',
                FIELD_NAME: 'Trzepotliwy Liść W Wiatrze',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'fallen_leaf': {
                FIELD_SYMBOL: '🍂',
                FIELD_NAME: 'Fallen Leaf',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'maple_leaf': {
                FIELD_SYMBOL: '🍁',
                FIELD_NAME: 'liść klonu',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'mushroom': {
                FIELD_SYMBOL: '🍄',
                FIELD_NAME: 'Grzyb',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'mushroom_with_large_brown_square': {
                FIELD_SYMBOL: '🍄\u200d🟫',
                FIELD_NAME: 'Mushroom z large brązowy kwadrat',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'coral': {
                FIELD_SYMBOL: '🪸',
                FIELD_NAME: 'Koralowiec',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'rock': {
                FIELD_SYMBOL: '🪨',
                FIELD_NAME: 'Skała',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'emoji_2': {
                FIELD_SYMBOL: '\U0001f6d8',
                FIELD_NAME: 'Osuwisko',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'ear_of_rice': {
                FIELD_SYMBOL: '🌾',
                FIELD_NAME: 'Ucho Ryżu',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'bouquet': {
                FIELD_SYMBOL: '💐',
                FIELD_NAME: 'Bukiet',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'tulip': {
                FIELD_SYMBOL: '🌷',
                FIELD_NAME: 'Tulipan',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'rose': {
                FIELD_SYMBOL: '🌹',
                FIELD_NAME: 'Róża',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'wilted_flower': {
                FIELD_SYMBOL: '🥀',
                FIELD_NAME: 'Zwiędły Kwiat',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'hyacinth': {
                FIELD_SYMBOL: '🪻',
                FIELD_NAME: 'Hiacynt',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'lotus': {
                FIELD_SYMBOL: '🪷',
                FIELD_NAME: 'Lotos',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'hibiscus': {
                FIELD_SYMBOL: '🌺',
                FIELD_NAME: 'Poślubnik',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'cherry_blossom': {
                FIELD_SYMBOL: '🌸',
                FIELD_NAME: 'Kwiat Wiśni',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'blossom': {
                FIELD_SYMBOL: '🌼',
                FIELD_NAME: 'Kwitnąć',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'sunflower': {
                FIELD_SYMBOL: '🌻',
                FIELD_NAME: 'Słonecznik',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'high_voltage_sign': {
                FIELD_SYMBOL: '⚡️',
                FIELD_NAME: 'Znak wysokiego napięcia',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'fire': {
                FIELD_SYMBOL: '🔥',
                FIELD_NAME: 'Ogień',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'emoji_3': {
                FIELD_SYMBOL: '\U0001faef',
                FIELD_NAME: 'Chmura walki',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'water_wave': {
                FIELD_SYMBOL: '🌊',
                FIELD_NAME: 'Fala wodna',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'bubbles': {
                FIELD_SYMBOL: '🫧',
                FIELD_NAME: 'Bąbelki',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
        },
        UNIVERSE: {
            'sun_with_face': {
                FIELD_SYMBOL: '🌞',
                FIELD_NAME: 'Słońce z twarzą',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'full_moon_with_face': {
                FIELD_SYMBOL: '🌝',
                FIELD_NAME: 'Księżyc w pełni z twarzą',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'first_quarter_moon_with_face': {
                FIELD_SYMBOL: '🌛',
                FIELD_NAME: 'Pierwszy kwartał księżyca z twarzą',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'last_quarter_moon_with_face': {
                FIELD_SYMBOL: '🌜',
                FIELD_NAME: 'Ostatni kwartał księżyca z twarzą',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'new_moon_with_face': {
                FIELD_SYMBOL: '🌚',
                FIELD_NAME: 'Księżyc w nowiu z twarzą',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'full_moon_symbol': {
                FIELD_SYMBOL: '🌕',
                FIELD_NAME: 'Symbol pełni księżyca',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'waning_gibbous_moon_symbol': {
                FIELD_SYMBOL: '🌖',
                FIELD_NAME: 'Waning Gibbous Moon Symbol',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'last_quarter_moon_symbol': {
                FIELD_SYMBOL: '🌗',
                FIELD_NAME: 'Ostatni symbol księżyca',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'waning_crescent_moon_symbol': {
                FIELD_SYMBOL: '🌘',
                FIELD_NAME: 'Waning Crescent Moon Symbol',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'new_moon_symbol': {
                FIELD_SYMBOL: '🌑',
                FIELD_NAME: 'Symbol nowiu',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'waxing_crescent_moon_symbol': {
                FIELD_SYMBOL: '🌒',
                FIELD_NAME: 'Symbol wosku księżyca',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'first_quarter_moon_symbol': {
                FIELD_SYMBOL: '🌓',
                FIELD_NAME: 'Pierwszy symbol księżyca',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'waxing_gibbous_moon_symbol': {
                FIELD_SYMBOL: '🌔',
                FIELD_NAME: 'Woskowanie Gibbous Moon Symbol',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'crescent_moon': {
                FIELD_SYMBOL: '🌙',
                FIELD_NAME: 'Półksiężyc',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'earth_globe_americas': {
                FIELD_SYMBOL: '🌎',
                FIELD_NAME: 'Earth Globe Americas',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'earth_globe_europe_africa': {
                FIELD_SYMBOL: '🌍',
                FIELD_NAME: 'Earth Globe Europa-Afryka',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'earth_globe_asia_australia': {
                FIELD_SYMBOL: '🌏',
                FIELD_NAME: 'Earth Globe Azja-Australia',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'ringed_planet': {
                FIELD_SYMBOL: '🪐',
                FIELD_NAME: 'Planeta z pierścieniami',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'dizzy_symbol': {
                FIELD_SYMBOL: '💫',
                FIELD_NAME: 'Dizzy Symbol',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'white_medium_star': {
                FIELD_SYMBOL: '⭐️',
                FIELD_NAME: 'Biała średnia gwiazda',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'glowing_star': {
                FIELD_SYMBOL: '🌟',
                FIELD_NAME: 'Świecąca Gwiazda',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'sparkles': {
                FIELD_SYMBOL: '✨',
                FIELD_NAME: 'Błyska',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'comet': {
                FIELD_SYMBOL: '☄️',
                FIELD_NAME: 'Kometa',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'collision_symbol': {
                FIELD_SYMBOL: '💥',
                FIELD_NAME: 'Symbol kolizji',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'satellite': {
                FIELD_SYMBOL: '🛰️',
                FIELD_NAME: 'Satelita',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'rocket': {
                FIELD_SYMBOL: '🚀',
                FIELD_NAME: 'Rakieta',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'flying_saucer': {
                FIELD_SYMBOL: '🛸',
                FIELD_NAME: 'Latający spodek',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'coin': {
                FIELD_SYMBOL: '🪙',
                FIELD_NAME: 'Moneta',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'telescope': {
                FIELD_SYMBOL: '🔭',
                FIELD_NAME: 'Teleskop',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
        },
        WEATHER: {
            'cloud_with_tornado': {
                FIELD_SYMBOL: '🌪️',
                FIELD_NAME: 'Chmura z Tornado',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'rainbow': {
                FIELD_SYMBOL: '🌈',
                FIELD_NAME: 'Tęcza',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'black_sun_with_rays': {
                FIELD_SYMBOL: '☀️',
                FIELD_NAME: 'Czarne słońce z promieniami',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'white_sun_with_small_cloud': {
                FIELD_SYMBOL: '🌤️',
                FIELD_NAME: 'Białe słońce z małą chmurką',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'sun_behind_cloud': {
                FIELD_SYMBOL: '⛅️',
                FIELD_NAME: 'Sun Behind Cloud',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'white_sun_behind_cloud': {
                FIELD_SYMBOL: '🌥️',
                FIELD_NAME: 'White Sun Behind Cloud',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'cloud': {
                FIELD_SYMBOL: '☁️',
                FIELD_NAME: 'Chmura',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'white_sun_behind_cloud_with_rain': {
                FIELD_SYMBOL: '🌦️',
                FIELD_NAME: 'Białe słońce za chmurą z deszczem',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'cloud_with_rain': {
                FIELD_SYMBOL: '🌧️',
                FIELD_NAME: 'Chmura z deszczem',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'thunder_cloud_and_rain': {
                FIELD_SYMBOL: '⛈️',
                FIELD_NAME: 'Chmura piorunów i deszcz',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'cloud_with_lightning': {
                FIELD_SYMBOL: '🌩️',
                FIELD_NAME: 'Chmura z błyskawicą',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'cloud_with_snow': {
                FIELD_SYMBOL: '🌨️',
                FIELD_NAME: 'Chmura ze śniegiem',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'snowflake': {
                FIELD_SYMBOL: '❄️',
                FIELD_NAME: 'Płatek śniegu',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'snowman': {
                FIELD_SYMBOL: '☃️',
                FIELD_NAME: 'Bałwan',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'snowman_without_snow': {
                FIELD_SYMBOL: '⛄️',
                FIELD_NAME: 'Bałwan Bez Śniegu',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'wind_blowing_face': {
                FIELD_SYMBOL: '🌬️',
                FIELD_NAME: 'Twarz wiatru',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'dash_symbol': {
                FIELD_SYMBOL: '💨',
                FIELD_NAME: 'Symbol kreski',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'droplet': {
                FIELD_SYMBOL: '💧',
                FIELD_NAME: 'Kropelka',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'splashing_sweat_symbol': {
                FIELD_SYMBOL: '💦',
                FIELD_NAME: 'Symbol rozpryskiwania potu',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'umbrella_with_rain_drops': {
                FIELD_SYMBOL: '☔️',
                FIELD_NAME: 'Parasol z kroplami deszczu',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'umbrella': {
                FIELD_SYMBOL: '☂️',
                FIELD_NAME: 'Parasol',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'fog': {
                FIELD_SYMBOL: '🌫️',
                FIELD_NAME: 'Mgła',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
        },
        FRUITS_AND_VEGETABLES: {
            'green_apple': {
                FIELD_SYMBOL: '🍏',
                FIELD_NAME: 'Zielone jabłko',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'red_apple': {
                FIELD_SYMBOL: '🍎',
                FIELD_NAME: 'czerwone jabłko',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'pear': {
                FIELD_SYMBOL: '🍐',
                FIELD_NAME: 'Gruszka',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'tangerine': {
                FIELD_SYMBOL: '🍊',
                FIELD_NAME: 'Mandarynka',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'lemon': {
                FIELD_SYMBOL: '🍋',
                FIELD_NAME: 'Cytrynowy',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'lemon_with_large_green_square': {
                FIELD_SYMBOL: '🍋\u200d🟩',
                FIELD_NAME: 'Lemon z large zielony kwadrat',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'banana': {
                FIELD_SYMBOL: '🍌',
                FIELD_NAME: 'Banan',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'watermelon': {
                FIELD_SYMBOL: '🍉',
                FIELD_NAME: 'Arbuz',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'grapes': {
                FIELD_SYMBOL: '🍇',
                FIELD_NAME: 'Winogrona',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'strawberry': {
                FIELD_SYMBOL: '🍓',
                FIELD_NAME: 'Truskawka',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'blueberries': {
                FIELD_SYMBOL: '🫐',
                FIELD_NAME: 'Jagody',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'melon': {
                FIELD_SYMBOL: '🍈',
                FIELD_NAME: 'Melon',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'cherries': {
                FIELD_SYMBOL: '🍒',
                FIELD_NAME: 'Wiśnie',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'peach': {
                FIELD_SYMBOL: '🍑',
                FIELD_NAME: 'Brzoskwinia',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'mango': {
                FIELD_SYMBOL: '🥭',
                FIELD_NAME: 'Mango',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'pineapple': {
                FIELD_SYMBOL: '🍍',
                FIELD_NAME: 'Ananas',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'coconut': {
                FIELD_SYMBOL: '🥥',
                FIELD_NAME: 'Orzech kokosowy',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'kiwifruit': {
                FIELD_SYMBOL: '🥝',
                FIELD_NAME: 'Kiwi',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'tomato': {
                FIELD_SYMBOL: '🍅',
                FIELD_NAME: 'Pomidor',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'aubergine': {
                FIELD_SYMBOL: '🍆',
                FIELD_NAME: 'Bakłażan',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'avocado': {
                FIELD_SYMBOL: '🥑',
                FIELD_NAME: 'Awokado',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'pea_pod': {
                FIELD_SYMBOL: '🫛',
                FIELD_NAME: 'Strąk Grochu',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'broccoli': {
                FIELD_SYMBOL: '🥦',
                FIELD_NAME: 'brokuły',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'leafy_green': {
                FIELD_SYMBOL: '🥬',
                FIELD_NAME: 'Liściasta zieleń',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'cucumber': {
                FIELD_SYMBOL: '🥒',
                FIELD_NAME: 'Ogórek',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'hot_pepper': {
                FIELD_SYMBOL: '🌶️',
                FIELD_NAME: 'Ostra papryczka',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'bell_pepper': {
                FIELD_SYMBOL: '🫑',
                FIELD_NAME: 'Papryka',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'ear_of_maize': {
                FIELD_SYMBOL: '🌽',
                FIELD_NAME: 'Ucho Kukurydzy',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'carrot': {
                FIELD_SYMBOL: '🥕',
                FIELD_NAME: 'Marchewka',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'olive': {
                FIELD_SYMBOL: '🫒',
                FIELD_NAME: 'Oliwa',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'garlic': {
                FIELD_SYMBOL: '🧄',
                FIELD_NAME: 'czosnek',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'onion': {
                FIELD_SYMBOL: '🧅',
                FIELD_NAME: 'Cebula',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'potato': {
                FIELD_SYMBOL: '🥔',
                FIELD_NAME: 'Ziemniak',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'emoji': {
                FIELD_SYMBOL: '\U0001fadc',
                FIELD_NAME: 'Warzywo korzeniowe',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'roasted_sweet_potato': {
                FIELD_SYMBOL: '🍠',
                FIELD_NAME: 'Pieczone słodkie ziemniaki',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'ginger_root': {
                FIELD_SYMBOL: '🫚',
                FIELD_NAME: 'Korzeń Imbiru',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
        },
        FOOD_AND_DRINKS: {
            'croissant': {
                FIELD_SYMBOL: '🥐',
                FIELD_NAME: 'Rogalik',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'bagel': {
                FIELD_SYMBOL: '🥯',
                FIELD_NAME: 'Bajgiel',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'bread': {
                FIELD_SYMBOL: '🍞',
                FIELD_NAME: 'Chleb',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'baguette_bread': {
                FIELD_SYMBOL: '🥖',
                FIELD_NAME: 'Chleb Bagietkowy',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'pretzel': {
                FIELD_SYMBOL: '🥨',
                FIELD_NAME: 'Precel',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'cheese_wedge': {
                FIELD_SYMBOL: '🧀',
                FIELD_NAME: 'Klin klinowy',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'egg': {
                FIELD_SYMBOL: '🥚',
                FIELD_NAME: 'jajko',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'cooking': {
                FIELD_SYMBOL: '🍳',
                FIELD_NAME: 'Gotowanie',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'butter': {
                FIELD_SYMBOL: '🧈',
                FIELD_NAME: 'masło',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'pancakes': {
                FIELD_SYMBOL: '🥞',
                FIELD_NAME: 'naleśniki',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'waffle': {
                FIELD_SYMBOL: '🧇',
                FIELD_NAME: 'Wafel',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'bacon': {
                FIELD_SYMBOL: '🥓',
                FIELD_NAME: 'Boczek',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'cut_of_meat': {
                FIELD_SYMBOL: '🥩',
                FIELD_NAME: 'Cięcie Mięsa',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'poultry_leg': {
                FIELD_SYMBOL: '🍗',
                FIELD_NAME: 'Noga drobiu',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'meat_on_bone': {
                FIELD_SYMBOL: '🍖',
                FIELD_NAME: 'Mięso Na Kości',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'bone': {
                FIELD_SYMBOL: '🦴',
                FIELD_NAME: 'Kość',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'hot_dog': {
                FIELD_SYMBOL: '🌭',
                FIELD_NAME: 'Hot dog',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'hamburger': {
                FIELD_SYMBOL: '🍔',
                FIELD_NAME: 'Hamburger',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'french_fries': {
                FIELD_SYMBOL: '🍟',
                FIELD_NAME: 'Frytki',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'slice_of_pizza': {
                FIELD_SYMBOL: '🍕',
                FIELD_NAME: 'Kawałek pizzy',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'flatbread': {
                FIELD_SYMBOL: '🫓',
                FIELD_NAME: 'Podpłomyki',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'sandwich': {
                FIELD_SYMBOL: '🥪',
                FIELD_NAME: 'Kanapka',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'stuffed_flatbread': {
                FIELD_SYMBOL: '🥙',
                FIELD_NAME: 'Nadziewane Flatbread',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'falafel': {
                FIELD_SYMBOL: '🧆',
                FIELD_NAME: 'Falafel',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'taco': {
                FIELD_SYMBOL: '🌮',
                FIELD_NAME: 'Taco',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'burrito': {
                FIELD_SYMBOL: '🌯',
                FIELD_NAME: 'Burrito',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'tamale': {
                FIELD_SYMBOL: '🫔',
                FIELD_NAME: 'Tamale',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'green_salad': {
                FIELD_SYMBOL: '🥗',
                FIELD_NAME: 'Zielona sałatka',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'shallow_pan_of_food': {
                FIELD_SYMBOL: '🥘',
                FIELD_NAME: 'Płytka Pan Food',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'fondue': {
                FIELD_SYMBOL: '🫕',
                FIELD_NAME: 'Fondue',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'canned_food': {
                FIELD_SYMBOL: '🥫',
                FIELD_NAME: 'Jedzenie w puszce',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'jar': {
                FIELD_SYMBOL: '🫙',
                FIELD_NAME: 'Słoik',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'spaghetti': {
                FIELD_SYMBOL: '🍝',
                FIELD_NAME: 'Spaghetti',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'steaming_bowl': {
                FIELD_SYMBOL: '🍜',
                FIELD_NAME: 'Parująca miska',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'pot_of_food': {
                FIELD_SYMBOL: '🍲',
                FIELD_NAME: 'Pot żywności',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'curry_and_rice': {
                FIELD_SYMBOL: '🍛',
                FIELD_NAME: 'Curry i ryż',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'sushi': {
                FIELD_SYMBOL: '🍣',
                FIELD_NAME: 'Sushi',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'bento_box': {
                FIELD_SYMBOL: '🍱',
                FIELD_NAME: 'Bento Box',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'dumpling': {
                FIELD_SYMBOL: '🥟',
                FIELD_NAME: 'Kluska',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'oyster': {
                FIELD_SYMBOL: '🦪',
                FIELD_NAME: 'Ostryga',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'fried_shrimp': {
                FIELD_SYMBOL: '🍤',
                FIELD_NAME: 'Smażone Krewetki',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'rice_ball': {
                FIELD_SYMBOL: '🍙',
                FIELD_NAME: 'Kulka ryżowa',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'cooked_rice': {
                FIELD_SYMBOL: '🍚',
                FIELD_NAME: 'Gotowany ryż',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'rice_cracker': {
                FIELD_SYMBOL: '🍘',
                FIELD_NAME: 'Ryżowy Krakers',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'fish_cake_with_swirl_design': {
                FIELD_SYMBOL: '🍥',
                FIELD_NAME: 'Ciasto Rybne z Projektem Wirowym',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'fortune_cookie': {
                FIELD_SYMBOL: '🥠',
                FIELD_NAME: 'Ciastko z wróżbą',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'moon_cake': {
                FIELD_SYMBOL: '🥮',
                FIELD_NAME: 'Księżycowe ciasto',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'oden': {
                FIELD_SYMBOL: '🍢',
                FIELD_NAME: 'Oden',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'dango': {
                FIELD_SYMBOL: '🍡',
                FIELD_NAME: 'Dango',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'shaved_ice': {
                FIELD_SYMBOL: '🍧',
                FIELD_NAME: 'Ogolony Lód',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'ice_cream': {
                FIELD_SYMBOL: '🍨',
                FIELD_NAME: 'Lody',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'soft_ice_cream': {
                FIELD_SYMBOL: '🍦',
                FIELD_NAME: 'Miękkie Lody',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'pie': {
                FIELD_SYMBOL: '🥧',
                FIELD_NAME: 'Ciasto',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'cupcake': {
                FIELD_SYMBOL: '🧁',
                FIELD_NAME: 'Babeczka',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'shortcake': {
                FIELD_SYMBOL: '🍰',
                FIELD_NAME: 'Ciastko',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'birthday_cake': {
                FIELD_SYMBOL: '🎂',
                FIELD_NAME: 'Tort urodzinowy',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'custard': {
                FIELD_SYMBOL: '🍮',
                FIELD_NAME: 'krem',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'lollipop': {
                FIELD_SYMBOL: '🍭',
                FIELD_NAME: 'Lizak',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'candy': {
                FIELD_SYMBOL: '🍬',
                FIELD_NAME: 'cukierek',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'chocolate_bar': {
                FIELD_SYMBOL: '🍫',
                FIELD_NAME: 'Tabliczka czekolady',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'popcorn': {
                FIELD_SYMBOL: '🍿',
                FIELD_NAME: 'Prażona kukurydza',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'doughnut': {
                FIELD_SYMBOL: '🍩',
                FIELD_NAME: 'Pączek',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'cookie': {
                FIELD_SYMBOL: '🍪',
                FIELD_NAME: 'Ciastko',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'chestnut': {
                FIELD_SYMBOL: '🌰',
                FIELD_NAME: 'kasztan',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'peanuts': {
                FIELD_SYMBOL: '🥜',
                FIELD_NAME: 'Orzeszki ziemne',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'beans': {
                FIELD_SYMBOL: '🫘',
                FIELD_NAME: 'Fasola',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'honey_pot': {
                FIELD_SYMBOL: '🍯',
                FIELD_NAME: 'Garnek miodu',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'glass_of_milk': {
                FIELD_SYMBOL: '🥛',
                FIELD_NAME: 'Szklanka mleka',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'pouring_liquid': {
                FIELD_SYMBOL: '🫗',
                FIELD_NAME: 'Nalewanie Płynu',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'baby_bottle': {
                FIELD_SYMBOL: '🍼',
                FIELD_NAME: 'Butelka dla dziecka',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'teapot': {
                FIELD_SYMBOL: '🫖',
                FIELD_NAME: 'Czajniczek',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'hot_beverage': {
                FIELD_SYMBOL: '☕️',
                FIELD_NAME: 'Gorący napój',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'teacup_without_handle': {
                FIELD_SYMBOL: '🍵',
                FIELD_NAME: 'Filiżanka bez uchwytu',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'beverage_box': {
                FIELD_SYMBOL: '🧃',
                FIELD_NAME: 'Pudełko na napoje',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'cup_with_straw': {
                FIELD_SYMBOL: '🥤',
                FIELD_NAME: 'Kubek Z Słomką',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'bubble_tea': {
                FIELD_SYMBOL: '🧋',
                FIELD_NAME: 'Herbata z bąbelkami',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'sake_bottle_and_cup': {
                FIELD_SYMBOL: '🍶',
                FIELD_NAME: 'Sake Bottle and Cup',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'beer_mug': {
                FIELD_SYMBOL: '🍺',
                FIELD_NAME: 'Kufel do piwa',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'clinking_beer_mugs': {
                FIELD_SYMBOL: '🍻',
                FIELD_NAME: 'Clinking Beer Mugs',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'clinking_glasses': {
                FIELD_SYMBOL: '🥂',
                FIELD_NAME: 'Clinking Glasses',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'wine_glass': {
                FIELD_SYMBOL: '🍷',
                FIELD_NAME: 'Lampka wina',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'tumbler_glass': {
                FIELD_SYMBOL: '🥃',
                FIELD_NAME: 'Tumbler Glass',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'cocktail_glass': {
                FIELD_SYMBOL: '🍸',
                FIELD_NAME: 'Szklanka do drinków',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'tropical_drink': {
                FIELD_SYMBOL: '🍹',
                FIELD_NAME: 'Tropikalny napój',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'mate_drink': {
                FIELD_SYMBOL: '🧉',
                FIELD_NAME: 'Napój Mate',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'bottle_with_popping_cork': {
                FIELD_SYMBOL: '🍾',
                FIELD_NAME: 'Butelka z Popping Cork',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'ice_cube': {
                FIELD_SYMBOL: '🧊',
                FIELD_NAME: 'Kostka lodu',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'spoon': {
                FIELD_SYMBOL: '🥄',
                FIELD_NAME: 'Łyżka',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'fork_and_knife': {
                FIELD_SYMBOL: '🍴',
                FIELD_NAME: 'Widelec i nóż',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'fork_and_knife_with_plate': {
                FIELD_SYMBOL: '🍽️',
                FIELD_NAME: 'Widelec i nóż z talerzem',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'bowl_with_spoon': {
                FIELD_SYMBOL: '🥣',
                FIELD_NAME: 'Miska Z łyżką',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'takeout_box': {
                FIELD_SYMBOL: '🥡',
                FIELD_NAME: 'Pudełko na wynos',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'chopsticks': {
                FIELD_SYMBOL: '🥢',
                FIELD_NAME: 'Pałeczki do jedzenia',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'salt_shaker': {
                FIELD_SYMBOL: '🧂',
                FIELD_NAME: 'Solniczka',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
        },
        SPORT: {
            'soccer_ball': {
                FIELD_SYMBOL: '⚽️',
                FIELD_NAME: 'Piłka nożna',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'basketball_and_hoop': {
                FIELD_SYMBOL: '🏀',
                FIELD_NAME: 'Koszykówka i obręcz',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'american_football': {
                FIELD_SYMBOL: '🏈',
                FIELD_NAME: 'futbol amerykański',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'baseball': {
                FIELD_SYMBOL: '⚾️',
                FIELD_NAME: 'Baseball',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'softball': {
                FIELD_SYMBOL: '🥎',
                FIELD_NAME: 'Softball',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'tennis_racquet_and_ball': {
                FIELD_SYMBOL: '🎾',
                FIELD_NAME: 'Rakieta tenisowa i piłka',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'volleyball': {
                FIELD_SYMBOL: '🏐',
                FIELD_NAME: 'Siatkówka',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'rugby_football': {
                FIELD_SYMBOL: '🏉',
                FIELD_NAME: 'Piłka nożna rugby',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'flying_disc': {
                FIELD_SYMBOL: '🥏',
                FIELD_NAME: 'Latający dysk',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'billiards': {
                FIELD_SYMBOL: '🎱',
                FIELD_NAME: 'Bilard',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'yo_yo': {
                FIELD_SYMBOL: '🪀',
                FIELD_NAME: 'Jo-jo',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'table_tennis_paddle_and_ball': {
                FIELD_SYMBOL: '🏓',
                FIELD_NAME: 'Wiosło i piłka do tenisa stołowego',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'badminton_racquet_and_shuttlecock': {
                FIELD_SYMBOL: '🏸',
                FIELD_NAME: 'Rakietka do badmintona i wolant',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'ice_hockey_stick_and_puck': {
                FIELD_SYMBOL: '🏒',
                FIELD_NAME: 'Kij do hokeja na lodzie i krążek',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'field_hockey_stick_and_ball': {
                FIELD_SYMBOL: '🏑',
                FIELD_NAME: 'Kij na lodzie i piłka',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'lacrosse_stick_and_ball': {
                FIELD_SYMBOL: '🥍',
                FIELD_NAME: 'Lacrosse Stick and Ball',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'cricket_bat_and_ball': {
                FIELD_SYMBOL: '🏏',
                FIELD_NAME: 'Kij krykietowy i piłka',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'boomerang': {
                FIELD_SYMBOL: '🪃',
                FIELD_NAME: 'Bumerang',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'goal_net': {
                FIELD_SYMBOL: '🥅',
                FIELD_NAME: 'Sieć bramkowa',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'flag_in_hole': {
                FIELD_SYMBOL: '⛳️',
                FIELD_NAME: 'Flaga w otworze',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'kite': {
                FIELD_SYMBOL: '🪁',
                FIELD_NAME: 'Latawiec',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'playground_slide': {
                FIELD_SYMBOL: '🛝',
                FIELD_NAME: 'Zjeżdżalnia',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'bow_and_arrow': {
                FIELD_SYMBOL: '🏹',
                FIELD_NAME: 'Łuk i strzała',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'fishing_pole_and_fish': {
                FIELD_SYMBOL: '🎣',
                FIELD_NAME: 'Wędka i ryby',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'diving_mask': {
                FIELD_SYMBOL: '🤿',
                FIELD_NAME: 'Maska do nurkowania',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'boxing_glove': {
                FIELD_SYMBOL: '🥊',
                FIELD_NAME: 'Rękawica bokserska',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'martial_arts_uniform': {
                FIELD_SYMBOL: '🥋',
                FIELD_NAME: 'Mundur sztuk walki',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'running_shirt_with_sash': {
                FIELD_SYMBOL: '🎽',
                FIELD_NAME: 'Koszulka do biegania z szarfą',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'skateboard': {
                FIELD_SYMBOL: '🛹',
                FIELD_NAME: 'Deskorolka',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'roller_skate': {
                FIELD_SYMBOL: '🛼',
                FIELD_NAME: 'Görkorcsolya',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'sled': {
                FIELD_SYMBOL: '🛷',
                FIELD_NAME: 'Sanki',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'ice_skate': {
                FIELD_SYMBOL: '⛸️',
                FIELD_NAME: 'Lodowa łyżwa',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'curling_stone': {
                FIELD_SYMBOL: '🥌',
                FIELD_NAME: 'Curling Stone',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'ski_and_ski_boot': {
                FIELD_SYMBOL: '🎿',
                FIELD_NAME: 'Buty narciarskie i narciarskie',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'trophy': {
                FIELD_SYMBOL: '🏆',
                FIELD_NAME: 'Trofeum',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'first_place_medal': {
                FIELD_SYMBOL: '🥇',
                FIELD_NAME: 'Medal Pierwszego Miejsca',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'second_place_medal': {
                FIELD_SYMBOL: '🥈',
                FIELD_NAME: 'Medal drugiego miejsca',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'third_place_medal': {
                FIELD_SYMBOL: '🥉',
                FIELD_NAME: 'Medal trzeciego miejsca',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'sports_medal': {
                FIELD_SYMBOL: '🏅',
                FIELD_NAME: 'Medal sportowy',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'military_medal': {
                FIELD_SYMBOL: '🎖️',
                FIELD_NAME: 'Medal wojskowy',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'rosette': {
                FIELD_SYMBOL: '🏵️',
                FIELD_NAME: 'Rozeta',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'canoe': {
                FIELD_SYMBOL: '🛶',
                FIELD_NAME: 'Kajak',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'sailboat': {
                FIELD_SYMBOL: '⛵️',
                FIELD_NAME: 'Żaglówka',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
        },
        ART_AND_CULTURE: {
            'reminder_ribbon': {
                FIELD_SYMBOL: '🎗️',
                FIELD_NAME: 'Przypomnienie wstążki',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'ticket': {
                FIELD_SYMBOL: '🎫',
                FIELD_NAME: 'Bilet',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'admission_tickets': {
                FIELD_SYMBOL: '🎟️',
                FIELD_NAME: 'Bilety wstępu',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'circus_tent': {
                FIELD_SYMBOL: '🎪',
                FIELD_NAME: 'Namiot cyrkowy',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'performing_arts': {
                FIELD_SYMBOL: '🎭',
                FIELD_NAME: 'Sztuki widowiskowe',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'ballet_shoes': {
                FIELD_SYMBOL: '🩰',
                FIELD_NAME: 'Baletki',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'artist_palette': {
                FIELD_SYMBOL: '🎨',
                FIELD_NAME: 'Paleta artystów',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'emoji': {
                FIELD_SYMBOL: '\U0001fadf',
                FIELD_NAME: 'Chlapanie',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'clapper_board': {
                FIELD_SYMBOL: '🎬',
                FIELD_NAME: 'Zarząd klapy',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'fountain': {
                FIELD_SYMBOL: '⛲',
                FIELD_NAME: 'Fontanna',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'film_frames': {
                FIELD_SYMBOL: '🎞️',
                FIELD_NAME: 'Ramki filmowe',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
        },
        SOUND_AND_MUSIC: {
            'microphone': {
                FIELD_SYMBOL: '🎤',
                FIELD_NAME: 'Mikrofon',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'headphone': {
                FIELD_SYMBOL: '🎧',
                FIELD_NAME: 'Słuchawki',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'musical_score': {
                FIELD_SYMBOL: '🎼',
                FIELD_NAME: 'Zapis nutowy',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'musical_keyboard': {
                FIELD_SYMBOL: '🎹',
                FIELD_NAME: 'Klawiatura muzyczna',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'maracas': {
                FIELD_SYMBOL: '🪇',
                FIELD_NAME: 'Marakasy',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'drum_with_drumsticks': {
                FIELD_SYMBOL: '🥁',
                FIELD_NAME: 'Bęben z pałeczkami',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'long_drum': {
                FIELD_SYMBOL: '🪘',
                FIELD_NAME: 'Długi bęben',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'saxophone': {
                FIELD_SYMBOL: '🎷',
                FIELD_NAME: 'Saksofon',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'trumpet': {
                FIELD_SYMBOL: '🎺',
                FIELD_NAME: 'Trąbka',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'emoji': {
                FIELD_SYMBOL: '\U0001fa8a',
                FIELD_NAME: 'Puzon',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'accordion': {
                FIELD_SYMBOL: '🪗',
                FIELD_NAME: 'Akordeon',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'guitar': {
                FIELD_SYMBOL: '🎸',
                FIELD_NAME: 'Gitara',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'banjo': {
                FIELD_SYMBOL: '🪕',
                FIELD_NAME: 'Banjo',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'emoji_2': {
                FIELD_SYMBOL: '\U0001fa89',
                FIELD_NAME: 'Harfa',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'violin': {
                FIELD_SYMBOL: '🎻',
                FIELD_NAME: 'Skrzypce',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'flute': {
                FIELD_SYMBOL: '🪈',
                FIELD_NAME: 'Flet',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'musical_note': {
                FIELD_SYMBOL: '🎵',
                FIELD_NAME: 'Nuta',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'multiple_musical_notes': {
                FIELD_SYMBOL: '🎶',
                FIELD_NAME: 'Wiele nut',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'speaker': {
                FIELD_SYMBOL: '🔈',
                FIELD_NAME: 'Głośnik',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'speaker_with_cancellation_stroke': {
                FIELD_SYMBOL: '🔇',
                FIELD_NAME: 'Głośnik ze skokiem anulowania',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'speaker_with_one_sound_wave': {
                FIELD_SYMBOL: '🔉',
                FIELD_NAME: 'Głośnik z One Sound Wave',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'speaker_with_three_sound_waves': {
                FIELD_SYMBOL: '🔊',
                FIELD_NAME: 'Głośnik z trzema falami dźwiękowymi',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'bell': {
                FIELD_SYMBOL: '🔔',
                FIELD_NAME: 'dzwon',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'bell_with_cancellation_stroke': {
                FIELD_SYMBOL: '🔕',
                FIELD_NAME: 'Dzwon z udarem anulowania',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'cheering_megaphone': {
                FIELD_SYMBOL: '📣',
                FIELD_NAME: 'Dopingujący megafon',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'public_address_loudspeaker': {
                FIELD_SYMBOL: '📢',
                FIELD_NAME: 'Głośnik nagłośnieniowy',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
        },
        TRANSPORT: {
            'automobile': {
                FIELD_SYMBOL: '🚗',
                FIELD_NAME: 'Samochód',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'taxi': {
                FIELD_SYMBOL: '🚕',
                FIELD_NAME: 'Taxi',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'recreational_vehicle': {
                FIELD_SYMBOL: '🚙',
                FIELD_NAME: 'Pojazd rekreacyjny',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'bus': {
                FIELD_SYMBOL: '🚌',
                FIELD_NAME: 'Autobus',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'trolleybus': {
                FIELD_SYMBOL: '🚎',
                FIELD_NAME: 'Trolejbusowy',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'racing_car': {
                FIELD_SYMBOL: '🏎️',
                FIELD_NAME: 'Samochód wyścigowy',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'police_car': {
                FIELD_SYMBOL: '🚓',
                FIELD_NAME: 'Radiowóz',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'ambulance': {
                FIELD_SYMBOL: '🚑',
                FIELD_NAME: 'Karetka pogotowia',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'fire_engine': {
                FIELD_SYMBOL: '🚒',
                FIELD_NAME: 'Fire Engine',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'minibus': {
                FIELD_SYMBOL: '🚐',
                FIELD_NAME: 'Minibus',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'pickup_truck': {
                FIELD_SYMBOL: '🛻',
                FIELD_NAME: 'Teherautó',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'delivery_truck': {
                FIELD_SYMBOL: '🚚',
                FIELD_NAME: 'Ciężarówka dostawcza',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'articulated_lorry': {
                FIELD_SYMBOL: '🚛',
                FIELD_NAME: 'Przegubowa ciężarówka',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'tractor': {
                FIELD_SYMBOL: '🚜',
                FIELD_NAME: 'Ciągnik',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'scooter': {
                FIELD_SYMBOL: '🛴',
                FIELD_NAME: 'Skuter',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'bicycle': {
                FIELD_SYMBOL: '🚲',
                FIELD_NAME: 'Rower',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'motor_scooter': {
                FIELD_SYMBOL: '🛵',
                FIELD_NAME: 'Skuter',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'racing_motorcycle': {
                FIELD_SYMBOL: '🏍️',
                FIELD_NAME: 'Wyścigowy motocykl',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'auto_rickshaw': {
                FIELD_SYMBOL: '🛺',
                FIELD_NAME: 'Auto riksa',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'wheel': {
                FIELD_SYMBOL: '🛞',
                FIELD_NAME: 'Koło Pojazdu',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'police_cars_revolving_light': {
                FIELD_SYMBOL: '🚨',
                FIELD_NAME: 'Rewolwerowe światło samochodów policyjnych',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'oncoming_police_car': {
                FIELD_SYMBOL: '🚔',
                FIELD_NAME: 'Nadjeżdżający samochód policyjny',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'oncoming_bus': {
                FIELD_SYMBOL: '🚍',
                FIELD_NAME: 'Nadjeżdżający autobus',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'oncoming_automobile': {
                FIELD_SYMBOL: '🚘',
                FIELD_NAME: 'Nadchodzący samochód',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'oncoming_taxi': {
                FIELD_SYMBOL: '🚖',
                FIELD_NAME: 'Nadjeżdżająca taksówka',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'aerial_tramway': {
                FIELD_SYMBOL: '🚡',
                FIELD_NAME: 'Tramwaj powietrzny',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'mountain_cableway': {
                FIELD_SYMBOL: '🚠',
                FIELD_NAME: 'Kolejka linowa górska',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'suspension_railway': {
                FIELD_SYMBOL: '🚟',
                FIELD_NAME: 'Kolej wisząca',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'railway_car': {
                FIELD_SYMBOL: '🚃',
                FIELD_NAME: 'Wagon kolejowy',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'tram_car': {
                FIELD_SYMBOL: '🚋',
                FIELD_NAME: 'Tramwaj samochodowy',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'mountain_railway': {
                FIELD_SYMBOL: '🚞',
                FIELD_NAME: 'Kolej górska',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'monorail': {
                FIELD_SYMBOL: '🚝',
                FIELD_NAME: 'Jednoszynowy',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'high_speed_train': {
                FIELD_SYMBOL: '🚄',
                FIELD_NAME: 'Pociąg ekspresowy',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'high_speed_train_with_bullet_nose': {
                FIELD_SYMBOL: '🚅',
                FIELD_NAME: 'Szybki pociąg z Bullet Nose',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'light_rail': {
                FIELD_SYMBOL: '🚈',
                FIELD_NAME: 'Lekka kolej',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'steam_locomotive': {
                FIELD_SYMBOL: '🚂',
                FIELD_NAME: 'Lokomotywa parowa',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'train': {
                FIELD_SYMBOL: '🚆',
                FIELD_NAME: 'Pociąg',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'metro': {
                FIELD_SYMBOL: '🚇',
                FIELD_NAME: 'Metro',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'tram': {
                FIELD_SYMBOL: '🚊',
                FIELD_NAME: 'Tramwajowy',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'station': {
                FIELD_SYMBOL: '🚉',
                FIELD_NAME: 'Stacja',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'airplane': {
                FIELD_SYMBOL: '✈️',
                FIELD_NAME: 'Samolot',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'airplane_departure': {
                FIELD_SYMBOL: '🛫',
                FIELD_NAME: 'Odlot samolotu',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'airplane_arriving': {
                FIELD_SYMBOL: '🛬',
                FIELD_NAME: 'Przylot samolotu',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'small_airplane': {
                FIELD_SYMBOL: '🛩️',
                FIELD_NAME: 'Mały samolot',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'seat': {
                FIELD_SYMBOL: '💺',
                FIELD_NAME: 'Siedzenie',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'helicopter': {
                FIELD_SYMBOL: '🚁',
                FIELD_NAME: 'Śmigłowiec',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'speedboat': {
                FIELD_SYMBOL: '🚤',
                FIELD_NAME: 'Łódź motorowa',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'motor_boat': {
                FIELD_SYMBOL: '🛥️',
                FIELD_NAME: 'Łódź motorowa',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'passenger_ship': {
                FIELD_SYMBOL: '🛳️',
                FIELD_NAME: 'Statek pasażerski',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'ferry': {
                FIELD_SYMBOL: '⛴️',
                FIELD_NAME: 'Prom',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'ship': {
                FIELD_SYMBOL: '🚢',
                FIELD_NAME: 'Statek',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'ring_buoy': {
                FIELD_SYMBOL: '🛟',
                FIELD_NAME: 'Koło Ratunkowe',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'anchor': {
                FIELD_SYMBOL: '⚓️',
                FIELD_NAME: 'Kotwica',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'hook': {
                FIELD_SYMBOL: '🪝',
                FIELD_NAME: 'Hak',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'fuel_pump': {
                FIELD_SYMBOL: '⛽️',
                FIELD_NAME: 'Pompa paliwowa',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'construction_sign': {
                FIELD_SYMBOL: '🚧',
                FIELD_NAME: 'Znak budowlany',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'vertical_traffic_light': {
                FIELD_SYMBOL: '🚦',
                FIELD_NAME: 'Pionowe światła drogowe',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'horizontal_traffic_light': {
                FIELD_SYMBOL: '🚥',
                FIELD_NAME: 'Sygnalizacja świetlna pozioma',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'bus_stop': {
                FIELD_SYMBOL: '🚏',
                FIELD_NAME: 'Przystanek autobusowy',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'world_map': {
                FIELD_SYMBOL: '🗺️',
                FIELD_NAME: 'Mapa świata',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'railway_track': {
                FIELD_SYMBOL: '🛤️',
                FIELD_NAME: 'Tor kolejowy',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'motorway': {
                FIELD_SYMBOL: '🛣️',
                FIELD_NAME: 'Autostrada',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
        },
        TRAVEL_AND_PLACES: {
            'compass': {
                FIELD_SYMBOL: '🧭',
                FIELD_NAME: 'Kompas',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'moyai': {
                FIELD_SYMBOL: '🗿',
                FIELD_NAME: 'Moyai',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'statue_of_liberty': {
                FIELD_SYMBOL: '🗽',
                FIELD_NAME: 'Statua Wolności',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'tokyo_tower': {
                FIELD_SYMBOL: '🗼',
                FIELD_NAME: 'wieża Tokyo',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'european_castle': {
                FIELD_SYMBOL: '🏰',
                FIELD_NAME: 'Europejski zamek',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'japanese_castle': {
                FIELD_SYMBOL: '🏯️',
                FIELD_NAME: 'Japoński zamek',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'umbrella_on_ground': {
                FIELD_SYMBOL: '⛱️',
                FIELD_NAME: 'Parasol Na Ziemi',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'beach_with_umbrella': {
                FIELD_SYMBOL: '🏖️',
                FIELD_NAME: 'Plaża z parasolem',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'desert_island': {
                FIELD_SYMBOL: '🏝️',
                FIELD_NAME: 'Pustynna wyspa',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'desert': {
                FIELD_SYMBOL: '🏜️',
                FIELD_NAME: 'Pustynia',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'volcano': {
                FIELD_SYMBOL: '🌋',
                FIELD_NAME: 'Wulkan',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'mountain': {
                FIELD_SYMBOL: '⛰️',
                FIELD_NAME: 'Góra',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'snow_capped_mountain': {
                FIELD_SYMBOL: '🏔️',
                FIELD_NAME: 'Ośnieżona góra',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'mount_fuji': {
                FIELD_SYMBOL: '🗻',
                FIELD_NAME: 'góra Fuji',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'camping': {
                FIELD_SYMBOL: '🏕️',
                FIELD_NAME: 'Kemping',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'tent': {
                FIELD_SYMBOL: '⛺️',
                FIELD_NAME: 'Namiot',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'silhouette_of_japan': {
                FIELD_SYMBOL: '🗾',
                FIELD_NAME: 'Sylwetka Japonii',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'moon_viewing_ceremony': {
                FIELD_SYMBOL: '🎑',
                FIELD_NAME: 'Ceremonia oglądania księżyca',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'national_park': {
                FIELD_SYMBOL: '🏞️',
                FIELD_NAME: 'Park Narodowy',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'sunrise': {
                FIELD_SYMBOL: '🌅',
                FIELD_NAME: 'wschód słońca',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'sunrise_over_mountains': {
                FIELD_SYMBOL: '🌄',
                FIELD_NAME: 'Wschód słońca nad górami',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'shooting_star': {
                FIELD_SYMBOL: '🌠',
                FIELD_NAME: 'Spadająca gwiazda',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'firework_sparkler': {
                FIELD_SYMBOL: '🎇',
                FIELD_NAME: 'Fajerwerk Brylant',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'fireworks': {
                FIELD_SYMBOL: '🎆',
                FIELD_NAME: 'Fajerwerki',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'sunset_over_buildings': {
                FIELD_SYMBOL: '🌇',
                FIELD_NAME: 'Zachód słońca nad budynkami',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'cityscape_at_dusk': {
                FIELD_SYMBOL: '🌆',
                FIELD_NAME: 'Pejzaż Miejski O Zmierzchu',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'cityscape': {
                FIELD_SYMBOL: '🏙️',
                FIELD_NAME: 'Pejzaż miejski',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'night_with_stars': {
                FIELD_SYMBOL: '🌃',
                FIELD_NAME: 'Noc z gwiazdami',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'milky_way': {
                FIELD_SYMBOL: '🌌',
                FIELD_NAME: 'droga Mleczna',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'bridge_at_night': {
                FIELD_SYMBOL: '🌉',
                FIELD_NAME: 'Most W Nocy',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'foggy': {
                FIELD_SYMBOL: '🌁',
                FIELD_NAME: 'Mglisty',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
        },
        BUILDINGS: {
            'hut': {
                FIELD_SYMBOL: '🛖',
                FIELD_NAME: 'Chata',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'house_building': {
                FIELD_SYMBOL: '🏠',
                FIELD_NAME: 'Budowa domu',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'house_with_garden': {
                FIELD_SYMBOL: '🏡',
                FIELD_NAME: 'Dom z ogrodem',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'house_buildings': {
                FIELD_SYMBOL: '🏘️',
                FIELD_NAME: 'Budynki mieszkalne',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'derelict_house_building': {
                FIELD_SYMBOL: '🏚️',
                FIELD_NAME: 'Opuszczony dom',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'building_construction': {
                FIELD_SYMBOL: '🏗️',
                FIELD_NAME: 'Budownictwo',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'factory': {
                FIELD_SYMBOL: '🏭',
                FIELD_NAME: 'Fabryka',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'office_building': {
                FIELD_SYMBOL: '🏢',
                FIELD_NAME: 'Budynek biurowy',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'department_store': {
                FIELD_SYMBOL: '🏬',
                FIELD_NAME: 'Dom handlowy',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'japanese_post_office': {
                FIELD_SYMBOL: '🏣',
                FIELD_NAME: 'Poczta Japońska',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'european_post_office': {
                FIELD_SYMBOL: '🏤',
                FIELD_NAME: 'Europejski Urząd Pocztowy',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'hospital': {
                FIELD_SYMBOL: '🏥',
                FIELD_NAME: 'Szpital',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'bank': {
                FIELD_SYMBOL: '🏦',
                FIELD_NAME: 'Bank',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'hotel': {
                FIELD_SYMBOL: '🏨',
                FIELD_NAME: 'Hotel',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'convenience_store': {
                FIELD_SYMBOL: '🏪',
                FIELD_NAME: 'Sklep spożywczy',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'school': {
                FIELD_SYMBOL: '🏫',
                FIELD_NAME: 'Szkoła',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'love_hotel': {
                FIELD_SYMBOL: '🏩',
                FIELD_NAME: 'Hotel miłości',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'wedding': {
                FIELD_SYMBOL: '💒',
                FIELD_NAME: 'Ślub',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'classical_building': {
                FIELD_SYMBOL: '🏛️',
                FIELD_NAME: 'Klasyczny budynek',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'church': {
                FIELD_SYMBOL: '⛪️',
                FIELD_NAME: 'Kościół',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'mosque': {
                FIELD_SYMBOL: '🕌',
                FIELD_NAME: 'Meczet',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'synagogue': {
                FIELD_SYMBOL: '🕍',
                FIELD_NAME: 'Synagoga',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'hindu_temple': {
                FIELD_SYMBOL: '🛕',
                FIELD_NAME: 'Świątynia hinduska',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'kaaba': {
                FIELD_SYMBOL: '🕋',
                FIELD_NAME: 'Kaaba',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'shinto_shrine': {
                FIELD_SYMBOL: '⛩️',
                FIELD_NAME: 'Shinto Shrine',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
        },
        ENTERTAINMENT: {
            'game_die': {
                FIELD_SYMBOL: '🎲',
                FIELD_NAME: 'Zgiń grę',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'black_chess_pawn': {
                FIELD_SYMBOL: '♟️',
                FIELD_NAME: 'Czarny pionek szachowy',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'direct_hit': {
                FIELD_SYMBOL: '🎯',
                FIELD_NAME: 'Bezpośrednie uderzenie',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'bowling': {
                FIELD_SYMBOL: '🎳',
                FIELD_NAME: 'Kręgle',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'video_game': {
                FIELD_SYMBOL: '🎮',
                FIELD_NAME: 'Gra wideo',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'slot_machine': {
                FIELD_SYMBOL: '🎰',
                FIELD_NAME: 'Automat',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'jigsaw_puzzle_piece': {
                FIELD_SYMBOL: '🧩',
                FIELD_NAME: 'Kawałek układanki',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'stadium': {
                FIELD_SYMBOL: '🏟️',
                FIELD_NAME: 'stadion',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'ferris_wheel': {
                FIELD_SYMBOL: '🎡',
                FIELD_NAME: 'Diabelski młyn',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'roller_coaster': {
                FIELD_SYMBOL: '🎢',
                FIELD_NAME: 'Kolejka górska',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'carousel_horse': {
                FIELD_SYMBOL: '🎠',
                FIELD_NAME: 'Koń karuzeli',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'black_spade_suit': {
                FIELD_SYMBOL: '♠️',
                FIELD_NAME: 'Czarny kombinezon pikowy',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'black_club_suit': {
                FIELD_SYMBOL: '♣️',
                FIELD_NAME: 'Czarny garnitur klubu',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'black_heart_suit': {
                FIELD_SYMBOL: '♥️',
                FIELD_NAME: 'Czarny garnitur z sercem',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'black_diamond_suit': {
                FIELD_SYMBOL: '♦️',
                FIELD_NAME: 'Czarny diamentowy garnitur',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'playing_card_black_joker': {
                FIELD_SYMBOL: '🃏',
                FIELD_NAME: 'Karta do gry Czarny Joker',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'flower_playing_cards': {
                FIELD_SYMBOL: '🎴',
                FIELD_NAME: 'Kwiatowe karty do gry',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'mahjong_tile_red_dragon': {
                FIELD_SYMBOL: '🀄️',
                FIELD_NAME: 'Mahjong Tile Red Dragon',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
        },
        ELECTRONIC_DEVICES: {
            'watch': {
                FIELD_SYMBOL: '⌚️',
                FIELD_NAME: 'Zegarek',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'mobile_phone': {
                FIELD_SYMBOL: '📱',
                FIELD_NAME: 'Telefon komórkowy',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'mobile_phone_with_rightwards_arrow_at_left': {
                FIELD_SYMBOL: '📲',
                FIELD_NAME: 'Telefon komórkowy ze strzałką w prawo po lewej stronie',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'personal_computer': {
                FIELD_SYMBOL: '💻',
                FIELD_NAME: 'Komputer osobisty',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'keyboard': {
                FIELD_SYMBOL: '⌨️',
                FIELD_NAME: 'Klawiatura',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'desktop_computer': {
                FIELD_SYMBOL: '🖥️',
                FIELD_NAME: 'Komputer stacjonarny',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'printer': {
                FIELD_SYMBOL: '🖨️',
                FIELD_NAME: 'Drukarka',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'three_button_mouse': {
                FIELD_SYMBOL: '🖱️',
                FIELD_NAME: 'Mysz z trzema przyciskami',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'trackball': {
                FIELD_SYMBOL: '🖲️',
                FIELD_NAME: 'Trackball',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'joystick': {
                FIELD_SYMBOL: '🕹️',
                FIELD_NAME: 'Drążek sterowy',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'minidisc': {
                FIELD_SYMBOL: '💽',
                FIELD_NAME: 'Minidisc',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'floppy_disk': {
                FIELD_SYMBOL: '💾',
                FIELD_NAME: 'Dyskietka',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'optical_disc': {
                FIELD_SYMBOL: '💿',
                FIELD_NAME: 'Dysk optyczny',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'dvd': {
                FIELD_SYMBOL: '📀',
                FIELD_NAME: 'Płyta DVD',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'videocassette': {
                FIELD_SYMBOL: '📼',
                FIELD_NAME: 'Kaseta wideo',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'camera': {
                FIELD_SYMBOL: '📷',
                FIELD_NAME: 'Aparat fotograficzny',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'camera_with_flash': {
                FIELD_SYMBOL: '📸',
                FIELD_NAME: 'Aparat z lampą błyskową',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'video_camera': {
                FIELD_SYMBOL: '📹',
                FIELD_NAME: 'Kamera wideo',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'movie_camera': {
                FIELD_SYMBOL: '🎥',
                FIELD_NAME: 'Kamera filmowa',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'film_projector': {
                FIELD_SYMBOL: '📽️',
                FIELD_NAME: 'Projektor filmowy',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'telephone_receiver': {
                FIELD_SYMBOL: '📞',
                FIELD_NAME: 'Odbiornik telefoniczny',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'black_telephone': {
                FIELD_SYMBOL: '☎️',
                FIELD_NAME: 'Czarny telefon',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'pager': {
                FIELD_SYMBOL: '📟',
                FIELD_NAME: 'Pager',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'fax_machine': {
                FIELD_SYMBOL: '📠',
                FIELD_NAME: 'Faks',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'television': {
                FIELD_SYMBOL: '📺',
                FIELD_NAME: 'Telewizja',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'radio': {
                FIELD_SYMBOL: '📻',
                FIELD_NAME: 'Radio',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'studio_microphone': {
                FIELD_SYMBOL: '🎙️',
                FIELD_NAME: 'Mikrofon studyjny',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'level_slider': {
                FIELD_SYMBOL: '🎚️',
                FIELD_NAME: 'Suwak poziomu',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'control_knobs': {
                FIELD_SYMBOL: '🎛️',
                FIELD_NAME: 'Pokrętła sterowania',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'satellite_antenna': {
                FIELD_SYMBOL: '📡',
                FIELD_NAME: 'Antena satelitarna',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'battery': {
                FIELD_SYMBOL: '🔋',
                FIELD_NAME: 'Bateria',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'low_battery': {
                FIELD_SYMBOL: '🪫',
                FIELD_NAME: 'Słaba Bateria',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'electric_plug': {
                FIELD_SYMBOL: '🔌',
                FIELD_NAME: 'Wtyczka elektryczna',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'electric_light_bulb': {
                FIELD_SYMBOL: '💡',
                FIELD_NAME: 'Żarówka',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'electric_torch': {
                FIELD_SYMBOL: '🔦',
                FIELD_NAME: 'Latarka elektryczna',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
        },
        CLOCKS_AND_TIME: {
            'stopwatch': {
                FIELD_SYMBOL: '⏱️',
                FIELD_NAME: 'Stoper',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'timer_clock': {
                FIELD_SYMBOL: '⏲️',
                FIELD_NAME: 'Zegar sterujący',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'alarm_clock': {
                FIELD_SYMBOL: '⏰',
                FIELD_NAME: 'Budzik',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'mantelpiece_clock': {
                FIELD_SYMBOL: '🕰️',
                FIELD_NAME: 'Zegar z Mantelpiece',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'hourglass': {
                FIELD_SYMBOL: '⌛️',
                FIELD_NAME: 'Klepsydra',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'hourglass_with_flowing_sand': {
                FIELD_SYMBOL: '⏳',
                FIELD_NAME: 'Klepsydra z płynącym piaskiem',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'clock_face_one_oclock': {
                FIELD_SYMBOL: '🕐',
                FIELD_NAME: 'Clock Face One Oclock',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'clock_face_two_oclock': {
                FIELD_SYMBOL: '🕑',
                FIELD_NAME: 'Twarz zegara Dwie godziny',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'clock_face_three_oclock': {
                FIELD_SYMBOL: '🕒',
                FIELD_NAME: 'Twarz zegara Trzy godziny',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'clock_face_four_oclock': {
                FIELD_SYMBOL: '🕓',
                FIELD_NAME: 'Zegarowa twarz Cztery godziny',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'clock_face_five_oclock': {
                FIELD_SYMBOL: '🕔',
                FIELD_NAME: 'Twarz zegara Pięć godzin',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'clock_face_six_oclock': {
                FIELD_SYMBOL: '🕕',
                FIELD_NAME: 'Clock Face Six Oclock',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'clock_face_seven_oclock': {
                FIELD_SYMBOL: '🕖',
                FIELD_NAME: 'Clock Face Seven Oclock',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'clock_face_eight_oclock': {
                FIELD_SYMBOL: '🕗',
                FIELD_NAME: 'Clock Face Eight Oclock',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'clock_face_nine_oclock': {
                FIELD_SYMBOL: '🕘',
                FIELD_NAME: 'Clock Face Nine Oclock',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'clock_face_ten_oclock': {
                FIELD_SYMBOL: '🕙',
                FIELD_NAME: 'Zegarowa twarz Dziesięć',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'clock_face_eleven_oclock': {
                FIELD_SYMBOL: '🕚',
                FIELD_NAME: 'Clock Face Eleven Oclock',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'clock_face_twelve_oclock': {
                FIELD_SYMBOL: '🕛',
                FIELD_NAME: 'Tarczy zegara Dwanaście godzin',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'clock_face_one_thirty': {
                FIELD_SYMBOL: '🕜',
                FIELD_NAME: 'Zegarowa Twarz Trzydzieści',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'clock_face_two_thirty': {
                FIELD_SYMBOL: '🕝',
                FIELD_NAME: 'Zegarowa Twarz Dwa-Trzydzieści',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'clock_face_three_thirty': {
                FIELD_SYMBOL: '🕞',
                FIELD_NAME: 'Twarz zegara trzydzieści trzydzieści',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'clock_face_four_thirty': {
                FIELD_SYMBOL: '🕟',
                FIELD_NAME: 'Twarz zegara czterdzieści trzydzieści',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'clock_face_five_thirty': {
                FIELD_SYMBOL: '🕠',
                FIELD_NAME: 'Twarz zegara Piąta trzydzieści',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'clock_face_six_thirty': {
                FIELD_SYMBOL: '🕡',
                FIELD_NAME: 'Clock Face Six-Thirty',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'clock_face_seven_thirty': {
                FIELD_SYMBOL: '🕢',
                FIELD_NAME: 'Tarcza zegara Siedem trzydzieści',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'clock_face_eight_thirty': {
                FIELD_SYMBOL: '🕣',
                FIELD_NAME: 'Zegarowa twarz ósma-trzydzieści',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'clock_face_nine_thirty': {
                FIELD_SYMBOL: '🕤',
                FIELD_NAME: 'Zegarowa Dziewięć-Trzydzieści',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'clock_face_ten_thirty': {
                FIELD_SYMBOL: '🕥',
                FIELD_NAME: 'Tarcza zegara Dziesiąta trzydzieści',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'clock_face_eleven_thirty': {
                FIELD_SYMBOL: '🕦',
                FIELD_NAME: 'Zegarowa twarz jedenaście-trzydzieści',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'clock_face_twelve_thirty': {
                FIELD_SYMBOL: '🕧',
                FIELD_NAME: 'Tarcza zegara dwunasta trzydzieści',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
        },
        MONEY_AND_VALUABLES: {
            'money_with_wings': {
                FIELD_SYMBOL: '💸',
                FIELD_NAME: 'Pieniądze ze skrzydłami',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'banknote_with_dollar_sign': {
                FIELD_SYMBOL: '💵',
                FIELD_NAME: 'Banknot z znakiem dolara',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'banknote_with_yen_sign': {
                FIELD_SYMBOL: '💴',
                FIELD_NAME: 'Banknot ze znakiem jena',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'banknote_with_euro_sign': {
                FIELD_SYMBOL: '💶',
                FIELD_NAME: 'Banknot z Euro znakiem',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'banknote_with_pound_sign': {
                FIELD_SYMBOL: '💷',
                FIELD_NAME: 'Banknot ze znakiem funta',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'money_bag': {
                FIELD_SYMBOL: '💰',
                FIELD_NAME: 'Torba z pieniędzmi',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'credit_card': {
                FIELD_SYMBOL: '💳',
                FIELD_NAME: 'Karta kredytowa',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'gem_stone': {
                FIELD_SYMBOL: '💎',
                FIELD_NAME: 'Kamień szlachetny',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'emoji': {
                FIELD_SYMBOL: '\U0001fa8e',
                FIELD_NAME: 'Skrzynia skarbów',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'heavy_dollar_sign': {
                FIELD_SYMBOL: '💲',
                FIELD_NAME: 'Ciężki znak dolara',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'currency_exchange': {
                FIELD_SYMBOL: '💱',
                FIELD_NAME: 'Wymiana walut',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'chart_with_upwards_trend_and_yen_sign': {
                FIELD_SYMBOL: '💹',
                FIELD_NAME: 'Wykres z trendem w górę i znakiem jena',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
        },
        OBJECTS_AND_TOOLS: {
            'emoji': {
                FIELD_SYMBOL: '\U0001fac6',
                FIELD_NAME: 'Odcisk palca',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'identification_card': {
                FIELD_SYMBOL: '🪪',
                FIELD_NAME: 'Dowód Tożsamości',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'compression': {
                FIELD_SYMBOL: '🗜️',
                FIELD_NAME: 'Kompresja',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'candle': {
                FIELD_SYMBOL: '🕯️',
                FIELD_NAME: 'Świeca',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'diya_lamp': {
                FIELD_SYMBOL: '🪔',
                FIELD_NAME: 'Lampa Diya',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'fire_extinguisher': {
                FIELD_SYMBOL: '🧯',
                FIELD_NAME: 'Gaśnica',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'oil_drum': {
                FIELD_SYMBOL: '🛢️',
                FIELD_NAME: 'Bęben olejowy',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'scales': {
                FIELD_SYMBOL: '⚖️',
                FIELD_NAME: 'Waga',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'ladder': {
                FIELD_SYMBOL: '🪜',
                FIELD_NAME: 'Drabina',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'toolbox': {
                FIELD_SYMBOL: '🧰',
                FIELD_NAME: 'Przybornik',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'screwdriver': {
                FIELD_SYMBOL: '🪛',
                FIELD_NAME: 'Śrubokręt',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'wrench': {
                FIELD_SYMBOL: '🔧',
                FIELD_NAME: 'Klucz',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'hammer': {
                FIELD_SYMBOL: '🔨',
                FIELD_NAME: 'Młot',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'hammer_and_pick': {
                FIELD_SYMBOL: '⚒️',
                FIELD_NAME: 'Hammer and Pick',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'hammer_and_wrench': {
                FIELD_SYMBOL: '🛠️',
                FIELD_NAME: 'Młotek i klucz',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'pick': {
                FIELD_SYMBOL: '⛏️',
                FIELD_NAME: 'Wybierać',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'emoji_2': {
                FIELD_SYMBOL: '\U0001fa8f',
                FIELD_NAME: 'Łopata',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'carpentry_saw': {
                FIELD_SYMBOL: '🪚',
                FIELD_NAME: 'Piła stolarska',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'nut_and_bolt': {
                FIELD_SYMBOL: '🔩',
                FIELD_NAME: 'Nakrętka i śruba',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'gear': {
                FIELD_SYMBOL: '⚙️',
                FIELD_NAME: 'Koło zębate',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'mouse_trap': {
                FIELD_SYMBOL: '🪤',
                FIELD_NAME: 'Pułapka na myszy',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'brick': {
                FIELD_SYMBOL: '🧱',
                FIELD_NAME: 'Cegła',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'chains': {
                FIELD_SYMBOL: '⛓️',
                FIELD_NAME: 'Więzy',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'chains_with_collision_symbol': {
                FIELD_SYMBOL: '⛓️\u200d💥',
                FIELD_NAME: 'Chains z collision symbol',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'magnet': {
                FIELD_SYMBOL: '🧲',
                FIELD_NAME: 'Magnes',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'pistol': {
                FIELD_SYMBOL: '🔫',
                FIELD_NAME: 'Pistolet',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'bomb': {
                FIELD_SYMBOL: '💣',
                FIELD_NAME: 'Bomba',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'firecracker': {
                FIELD_SYMBOL: '🧨',
                FIELD_NAME: 'Petarda',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'axe': {
                FIELD_SYMBOL: '🪓',
                FIELD_NAME: 'Topór',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'hocho': {
                FIELD_SYMBOL: '🔪',
                FIELD_NAME: 'Hocho',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'dagger_knife': {
                FIELD_SYMBOL: '🗡️',
                FIELD_NAME: 'Nóż Sztylet',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'crossed_swords': {
                FIELD_SYMBOL: '⚔️',
                FIELD_NAME: 'Skrzyżowane miecze',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'shield': {
                FIELD_SYMBOL: '🛡️',
                FIELD_NAME: 'Tarcza',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'smoking_symbol': {
                FIELD_SYMBOL: '🚬',
                FIELD_NAME: 'Symbol palenia',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'coffin': {
                FIELD_SYMBOL: '⚰️',
                FIELD_NAME: 'Trumna',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'headstone': {
                FIELD_SYMBOL: '🪦',
                FIELD_NAME: 'Nagrobek',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'funeral_urn': {
                FIELD_SYMBOL: '⚱️',
                FIELD_NAME: 'Urna pogrzebowa',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'amphora': {
                FIELD_SYMBOL: '🏺',
                FIELD_NAME: 'Amfora',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'crystal_ball': {
                FIELD_SYMBOL: '🔮',
                FIELD_NAME: 'Kryształowa kula',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'prayer_beads': {
                FIELD_SYMBOL: '📿',
                FIELD_NAME: 'Różańce',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'nazar_amulet': {
                FIELD_SYMBOL: '🧿',
                FIELD_NAME: 'Nazar Amulet',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'hamsa': {
                FIELD_SYMBOL: '🪬',
                FIELD_NAME: 'Chamsa',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'barber_pole': {
                FIELD_SYMBOL: '💈',
                FIELD_NAME: 'Polak fryzjerski',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'broom': {
                FIELD_SYMBOL: '🧹',
                FIELD_NAME: 'Miotła',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'plunger': {
                FIELD_SYMBOL: '🪠',
                FIELD_NAME: 'Tłok nurnikowy',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'basket': {
                FIELD_SYMBOL: '🧺',
                FIELD_NAME: 'Kosz',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'roll_of_paper': {
                FIELD_SYMBOL: '🧻',
                FIELD_NAME: 'Rolka papieru',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'toilet': {
                FIELD_SYMBOL: '🚽',
                FIELD_NAME: 'Toaleta',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'potable_water_symbol': {
                FIELD_SYMBOL: '🚰',
                FIELD_NAME: 'Symbol wody pitnej',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'shower': {
                FIELD_SYMBOL: '🚿',
                FIELD_NAME: 'Prysznic',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'bathtub': {
                FIELD_SYMBOL: '🛁',
                FIELD_NAME: 'Wanna',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'bath': {
                FIELD_SYMBOL: '🛀',
                FIELD_NAME: 'Kąpiel',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'bar_of_soap': {
                FIELD_SYMBOL: '🧼',
                FIELD_NAME: 'Kostka mydła',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'toothbrush': {
                FIELD_SYMBOL: '🪥',
                FIELD_NAME: 'Szczoteczka do zębów',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'razor': {
                FIELD_SYMBOL: '🪒',
                FIELD_NAME: 'Brzytwa',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'hair_pick': {
                FIELD_SYMBOL: '🪮',
                FIELD_NAME: 'Grzebień Fryzjerski',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'sponge': {
                FIELD_SYMBOL: '🧽',
                FIELD_NAME: 'Gąbka',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'bucket': {
                FIELD_SYMBOL: '🪣',
                FIELD_NAME: 'Wiadro',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'lotion_bottle': {
                FIELD_SYMBOL: '🧴',
                FIELD_NAME: 'Butelka z balsamem',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'bellhop_bell': {
                FIELD_SYMBOL: '🛎️',
                FIELD_NAME: 'Bellhop Bell',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'key': {
                FIELD_SYMBOL: '🔑',
                FIELD_NAME: 'Klawisz',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'old_key': {
                FIELD_SYMBOL: '🗝️',
                FIELD_NAME: 'Stary klucz',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'door': {
                FIELD_SYMBOL: '🚪',
                FIELD_NAME: 'Drzwi',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'chair': {
                FIELD_SYMBOL: '🪑',
                FIELD_NAME: 'Krzesło',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'couch_and_lamp': {
                FIELD_SYMBOL: '🛋️',
                FIELD_NAME: 'Kanapa i lampa',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'bed': {
                FIELD_SYMBOL: '🛏️',
                FIELD_NAME: 'Łóżko',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'sleeping_accommodation': {
                FIELD_SYMBOL: '🛌',
                FIELD_NAME: 'Spanie Zakwaterowanie',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'teddy_bear': {
                FIELD_SYMBOL: '🧸',
                FIELD_NAME: 'Miś',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'nesting_dolls': {
                FIELD_SYMBOL: '🪆',
                FIELD_NAME: 'Zagnieżdżanie lalek',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'frame_with_picture': {
                FIELD_SYMBOL: '🖼️',
                FIELD_NAME: 'Ramka z obrazem',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'mirror': {
                FIELD_SYMBOL: '🪞',
                FIELD_NAME: 'Lustro',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'window': {
                FIELD_SYMBOL: '🪟',
                FIELD_NAME: 'Okno',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'shopping_bags': {
                FIELD_SYMBOL: '🛍️',
                FIELD_NAME: 'Torby na zakupy',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'shopping_trolley': {
                FIELD_SYMBOL: '🛒',
                FIELD_NAME: 'Wózek na zakupy',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'wrapped_present': {
                FIELD_SYMBOL: '🎁',
                FIELD_NAME: 'Wrapped Present',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'balloon': {
                FIELD_SYMBOL: '🎈',
                FIELD_NAME: 'Balon',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'carp_streamer': {
                FIELD_SYMBOL: '🎏',
                FIELD_NAME: 'Carp Streamer',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'ribbon': {
                FIELD_SYMBOL: '🎀',
                FIELD_NAME: 'Faborek',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'magic_wand': {
                FIELD_SYMBOL: '🪄',
                FIELD_NAME: 'magiczna różdżka',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'pinata': {
                FIELD_SYMBOL: '🪅',
                FIELD_NAME: 'Pinata',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'confetti_ball': {
                FIELD_SYMBOL: '🎊',
                FIELD_NAME: 'Konfetti Ball',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'party_popper': {
                FIELD_SYMBOL: '🎉',
                FIELD_NAME: 'Party Popper',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'japanese_dolls': {
                FIELD_SYMBOL: '🎎',
                FIELD_NAME: 'Japońskie lalki',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'folding_hand_fan': {
                FIELD_SYMBOL: '🪭',
                FIELD_NAME: 'Wachlarz',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'izakaya_lantern': {
                FIELD_SYMBOL: '🏮',
                FIELD_NAME: 'Latarnia Izakaya',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'wind_chime': {
                FIELD_SYMBOL: '🎐',
                FIELD_NAME: 'Wiatr Chime',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'mirror_ball': {
                FIELD_SYMBOL: '🪩',
                FIELD_NAME: 'Kula Dyskotekowa',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'red_gift_envelope': {
                FIELD_SYMBOL: '🧧',
                FIELD_NAME: 'Czerwona koperta na prezent',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'link_symbol': {
                FIELD_SYMBOL: '🔗',
                FIELD_NAME: 'Symbol łącza',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'lock_with_ink_pen': {
                FIELD_SYMBOL: '🔏',
                FIELD_NAME: 'Zablokuj za pomocą pióra atramentowego',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'closed_lock_with_key': {
                FIELD_SYMBOL: '🔐',
                FIELD_NAME: 'Zamknięty zamek z kluczem',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'lock': {
                FIELD_SYMBOL: '🔒',
                FIELD_NAME: 'Zamek',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'open_lock': {
                FIELD_SYMBOL: '🔓',
                FIELD_NAME: 'Otwórz blokadę',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
        },
        SCIENCE_AND_HEALTH: {
            'alembic': {
                FIELD_SYMBOL: '⚗️',
                FIELD_NAME: 'Alembik',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'microscope': {
                FIELD_SYMBOL: '🔬',
                FIELD_NAME: 'Mikroskop',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'hole': {
                FIELD_SYMBOL: '🕳️',
                FIELD_NAME: 'Otwór',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'x_ray': {
                FIELD_SYMBOL: '🩻',
                FIELD_NAME: 'Zdjęcie Rentgenowskie',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'adhesive_bandage': {
                FIELD_SYMBOL: '🩹',
                FIELD_NAME: 'Bandaż samoprzylepny',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'stethoscope': {
                FIELD_SYMBOL: '🩺',
                FIELD_NAME: 'Stetoskop',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'pill': {
                FIELD_SYMBOL: '💊',
                FIELD_NAME: 'Pigułka',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'syringe': {
                FIELD_SYMBOL: '💉',
                FIELD_NAME: 'Strzykawka',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'drop_of_blood': {
                FIELD_SYMBOL: '🩸',
                FIELD_NAME: 'Kropla krwi',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'dna_double_helix': {
                FIELD_SYMBOL: '🧬',
                FIELD_NAME: 'Dna Double Helix',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'microbe': {
                FIELD_SYMBOL: '🦠',
                FIELD_NAME: 'Mikrob',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'petri_dish': {
                FIELD_SYMBOL: '🧫',
                FIELD_NAME: 'Szalka Petriego',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'test_tube': {
                FIELD_SYMBOL: '🧪',
                FIELD_NAME: 'Probówka',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'thermometer': {
                FIELD_SYMBOL: '🌡️',
                FIELD_NAME: 'Termometr',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
        },
        OFFICE_TOOLS: {
            'envelope': {
                FIELD_SYMBOL: '✉️',
                FIELD_NAME: 'Koperta',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'envelope_with_downwards_arrow_above': {
                FIELD_SYMBOL: '📩',
                FIELD_NAME: 'Koperta ze strzałką w dół powyżej',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'incoming_envelope': {
                FIELD_SYMBOL: '📨',
                FIELD_NAME: 'Przychodząca koperta',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'e_mail_symbol': {
                FIELD_SYMBOL: '📧',
                FIELD_NAME: 'Symbol e-maila',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'love_letter': {
                FIELD_SYMBOL: '💌',
                FIELD_NAME: 'List miłosny',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'inbox_tray': {
                FIELD_SYMBOL: '📥',
                FIELD_NAME: 'Skrzynka odbiorcza',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'outbox_tray': {
                FIELD_SYMBOL: '📤',
                FIELD_NAME: 'Skrzynka nadawcza',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'package': {
                FIELD_SYMBOL: '📦',
                FIELD_NAME: 'Pakiet',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'label': {
                FIELD_SYMBOL: '🏷️',
                FIELD_NAME: 'Etykieta',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'placard': {
                FIELD_SYMBOL: '🪧',
                FIELD_NAME: 'Afisz',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'closed_mailbox_with_lowered_flag': {
                FIELD_SYMBOL: '📪',
                FIELD_NAME: 'Zamknięta skrzynka pocztowa z obniżoną flagą',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'closed_mailbox_with_raised_flag': {
                FIELD_SYMBOL: '📫',
                FIELD_NAME: 'Zamknięta skrzynka pocztowa z flagą podniesioną',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'open_mailbox_with_raised_flag': {
                FIELD_SYMBOL: '📬',
                FIELD_NAME: 'Otwórz skrzynkę pocztową z flagą podniesioną',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'open_mailbox_with_lowered_flag': {
                FIELD_SYMBOL: '📭',
                FIELD_NAME: 'Otwórz skrzynkę pocztową z obniżoną flagą',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'postbox': {
                FIELD_SYMBOL: '📮',
                FIELD_NAME: 'Skrzynka pocztowa',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'postal_horn': {
                FIELD_SYMBOL: '📯',
                FIELD_NAME: 'Róg pocztowy',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'scroll': {
                FIELD_SYMBOL: '📜',
                FIELD_NAME: 'Zwój',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'page_with_curl': {
                FIELD_SYMBOL: '📃',
                FIELD_NAME: 'Strona z zawinięciem',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'page_facing_up': {
                FIELD_SYMBOL: '📄',
                FIELD_NAME: 'Strona zwrócona w górę',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'bookmark_tabs': {
                FIELD_SYMBOL: '📑',
                FIELD_NAME: 'Zakładki zakładek',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'receipt': {
                FIELD_SYMBOL: '🧾',
                FIELD_NAME: 'Paragon',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'bar_chart': {
                FIELD_SYMBOL: '📊',
                FIELD_NAME: 'Wykres słupkowy',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'chart_with_upwards_trend': {
                FIELD_SYMBOL: '📈',
                FIELD_NAME: 'Wykres z trendem w górę',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'chart_with_downwards_trend': {
                FIELD_SYMBOL: '📉',
                FIELD_NAME: 'Wykres z trendem w dół',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'spiral_note_pad': {
                FIELD_SYMBOL: '🗒️',
                FIELD_NAME: 'Spiralny notes',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'spiral_calendar_pad': {
                FIELD_SYMBOL: '🗓️',
                FIELD_NAME: 'Spiral Calendar Pad',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'tear_off_calendar': {
                FIELD_SYMBOL: '📆',
                FIELD_NAME: 'Kalendarz odrywania',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'calendar': {
                FIELD_SYMBOL: '📅',
                FIELD_NAME: 'Kalendarz',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'wastebasket': {
                FIELD_SYMBOL: '🗑️',
                FIELD_NAME: 'Kosz na śmieci',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'card_index': {
                FIELD_SYMBOL: '📇',
                FIELD_NAME: 'Indeks kart',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'card_file_box': {
                FIELD_SYMBOL: '🗃️',
                FIELD_NAME: 'Pudełko z kartami',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'ballot_box_with_ballot': {
                FIELD_SYMBOL: '🗳️',
                FIELD_NAME: 'Urny z kartą do głosowania',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'file_cabinet': {
                FIELD_SYMBOL: '🗄️',
                FIELD_NAME: 'Szafka na akta',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'clipboard': {
                FIELD_SYMBOL: '📋',
                FIELD_NAME: 'Schowek',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'file_folder': {
                FIELD_SYMBOL: '📁',
                FIELD_NAME: 'Folder z plikami',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'open_file_folder': {
                FIELD_SYMBOL: '📂',
                FIELD_NAME: 'Otwórz folder plików',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'card_index_dividers': {
                FIELD_SYMBOL: '🗂️',
                FIELD_NAME: 'Dzielniki indeksu kart',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'rolled_up_newspaper': {
                FIELD_SYMBOL: '🗞️',
                FIELD_NAME: 'Zwijana gazeta',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'newspaper': {
                FIELD_SYMBOL: '📰',
                FIELD_NAME: 'Gazeta',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'notebook': {
                FIELD_SYMBOL: '📓',
                FIELD_NAME: 'Notatnik',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'notebook_with_decorative_cover': {
                FIELD_SYMBOL: '📔',
                FIELD_NAME: 'Notatnik z ozdobną pokrywą',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'ledger': {
                FIELD_SYMBOL: '📒',
                FIELD_NAME: 'Księga główna',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'closed_book': {
                FIELD_SYMBOL: '📕',
                FIELD_NAME: 'Zamknięta księga',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'green_book': {
                FIELD_SYMBOL: '📗',
                FIELD_NAME: 'Zielona Książka',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'blue_book': {
                FIELD_SYMBOL: '📘',
                FIELD_NAME: 'Niebieska książka',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'orange_book': {
                FIELD_SYMBOL: '📙',
                FIELD_NAME: 'Pomarańczowa książka',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'books': {
                FIELD_SYMBOL: '📚',
                FIELD_NAME: 'Książki',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'open_book': {
                FIELD_SYMBOL: '📖',
                FIELD_NAME: 'Otwarta książka',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'bookmark': {
                FIELD_SYMBOL: '🔖',
                FIELD_NAME: 'Zakładka',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'safety_pin': {
                FIELD_SYMBOL: '🧷',
                FIELD_NAME: 'Agrafka',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'paperclip': {
                FIELD_SYMBOL: '📎',
                FIELD_NAME: 'Spinacz',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'linked_paperclips': {
                FIELD_SYMBOL: '🖇️',
                FIELD_NAME: 'Połączone spinacze do papieru',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'triangular_ruler': {
                FIELD_SYMBOL: '📐',
                FIELD_NAME: 'Trójkątna miarka',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'straight_ruler': {
                FIELD_SYMBOL: '📏',
                FIELD_NAME: 'Prosta miarka',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'abacus': {
                FIELD_SYMBOL: '🧮',
                FIELD_NAME: 'Liczydło',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'pushpin': {
                FIELD_SYMBOL: '📌',
                FIELD_NAME: 'Pinezka',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'round_pushpin': {
                FIELD_SYMBOL: '📍',
                FIELD_NAME: 'Okrągła Pinezka',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'black_scissors': {
                FIELD_SYMBOL: '✂️',
                FIELD_NAME: 'Czarne nożyczki',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'lower_left_ballpoint_pen': {
                FIELD_SYMBOL: '🖊️',
                FIELD_NAME: 'Dolny lewy długopis',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'lower_left_fountain_pen': {
                FIELD_SYMBOL: '🖋️',
                FIELD_NAME: 'Dolne lewe pióro wieczne',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'black_nib': {
                FIELD_SYMBOL: '✒️',
                FIELD_NAME: 'Czarna stalówka',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'lower_left_paintbrush': {
                FIELD_SYMBOL: '🖌️',
                FIELD_NAME: 'Dolny lewy pędzel',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'lower_left_crayon': {
                FIELD_SYMBOL: '🖍️',
                FIELD_NAME: 'Dolna lewa kredka',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'memo': {
                FIELD_SYMBOL: '📝',
                FIELD_NAME: 'Notatka',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'pencil': {
                FIELD_SYMBOL: '✏️',
                FIELD_NAME: 'Ołówek',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'left_pointing_magnifying_glass': {
                FIELD_SYMBOL: '🔍',
                FIELD_NAME: 'Lewe szkło powiększające',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'right_pointing_magnifying_glass': {
                FIELD_SYMBOL: '🔎',
                FIELD_NAME: 'Prawe szkło powiększające',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
        },
        FLAGS: {
            'waving_white_flag': {
                FIELD_SYMBOL: '🏳️',
                FIELD_NAME: 'Macha białą flagą',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'waving_black_flag': {
                FIELD_SYMBOL: '🏴',
                FIELD_NAME: 'Macha Czarną Flagą',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'waving_black_flag_with_skull_and_crossbones': {
                FIELD_SYMBOL: '🏴\u200d☠️',
                FIELD_NAME: 'Waving czarny flaga z skull i crossbones',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'chequered_flag': {
                FIELD_SYMBOL: '🏁',
                FIELD_NAME: 'Flaga w kratkę',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'triangular_flag_on_post': {
                FIELD_SYMBOL: '🚩',
                FIELD_NAME: 'Trójkątna flaga na poczcie',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'waving_white_flag_with_rainbow': {
                FIELD_SYMBOL: '🏳️\u200d🌈',
                FIELD_NAME: 'Waving biały flaga z rainbow',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'waving_white_flag_with_male_with_stroke_and_male_and_female_sign': {
                FIELD_SYMBOL: '🏳️\u200d⚧️',
                FIELD_NAME: 'Waving biały flaga z male z stroke i male i female sign',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_u_with_regional_indicator_symbol_letter_n': {
                FIELD_SYMBOL: '🇺🇳',
                FIELD_NAME: 'Regional indicator symbol letter u z regional indicator symbol letter n',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_a_with_regional_indicator_symbol_letter_f': {
                FIELD_SYMBOL: '🇦🇫',
                FIELD_NAME: 'Regional indicator symbol letter a z regional indicator symbol letter f',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_a_with_regional_indicator_symbol_letter_l': {
                FIELD_SYMBOL: '🇦🇱',
                FIELD_NAME: 'Regional indicator symbol letter a z regional indicator symbol letter l',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_d_with_regional_indicator_symbol_letter_z': {
                FIELD_SYMBOL: '🇩🇿',
                FIELD_NAME: 'Regional indicator symbol letter d z regional indicator symbol letter z',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_a_with_regional_indicator_symbol_letter_d': {
                FIELD_SYMBOL: '🇦🇩',
                FIELD_NAME: 'Regional indicator symbol letter a z regional indicator symbol letter d',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_a_with_regional_indicator_symbol_letter_o': {
                FIELD_SYMBOL: '🇦🇴',
                FIELD_NAME: 'Regional indicator symbol letter a z regional indicator symbol letter o',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_a_with_regional_indicator_symbol_letter_i': {
                FIELD_SYMBOL: '🇦🇮',
                FIELD_NAME: 'Regional indicator symbol letter a z regional indicator symbol letter i',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_a_with_regional_indicator_symbol_letter_q': {
                FIELD_SYMBOL: '🇦🇶',
                FIELD_NAME: 'Regional indicator symbol letter a z regional indicator symbol letter q',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_a_with_regional_indicator_symbol_letter_g': {
                FIELD_SYMBOL: '🇦🇬',
                FIELD_NAME: 'Regional indicator symbol letter a z regional indicator symbol letter g',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_s_with_regional_indicator_symbol_letter_a': {
                FIELD_SYMBOL: '🇸🇦',
                FIELD_NAME: 'Regional indicator symbol letter s z regional indicator symbol letter a',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_a_with_regional_indicator_symbol_letter_r': {
                FIELD_SYMBOL: '🇦🇷',
                FIELD_NAME: 'Regional indicator symbol letter a z regional indicator symbol letter r',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_a_with_regional_indicator_symbol_letter_m': {
                FIELD_SYMBOL: '🇦🇲',
                FIELD_NAME: 'Regional indicator symbol letter a z regional indicator symbol letter m',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_a_with_regional_indicator_symbol_letter_w': {
                FIELD_SYMBOL: '🇦🇼',
                FIELD_NAME: 'Regional indicator symbol letter a z regional indicator symbol letter w',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_a_with_regional_indicator_symbol_letter_u': {
                FIELD_SYMBOL: '🇦🇺',
                FIELD_NAME: 'Regional indicator symbol letter a z regional indicator symbol letter u',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_a_with_regional_indicator_symbol_letter_t': {
                FIELD_SYMBOL: '🇦🇹',
                FIELD_NAME: 'Regional indicator symbol letter a z regional indicator symbol letter t',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_a_with_regional_indicator_symbol_letter_z': {
                FIELD_SYMBOL: '🇦🇿',
                FIELD_NAME: 'Regional indicator symbol letter a z regional indicator symbol letter z',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_b_with_regional_indicator_symbol_letter_s': {
                FIELD_SYMBOL: '🇧🇸',
                FIELD_NAME: 'Regional indicator symbol letter b z regional indicator symbol letter s',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_b_with_regional_indicator_symbol_letter_h': {
                FIELD_SYMBOL: '🇧🇭',
                FIELD_NAME: 'Regional indicator symbol letter b z regional indicator symbol letter h',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_b_with_regional_indicator_symbol_letter_d': {
                FIELD_SYMBOL: '🇧🇩',
                FIELD_NAME: 'Regional indicator symbol letter b z regional indicator symbol letter d',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_b_with_regional_indicator_symbol_letter_b': {
                FIELD_SYMBOL: '🇧🇧',
                FIELD_NAME: 'Regional indicator symbol letter b z regional indicator symbol letter b',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_b_with_regional_indicator_symbol_letter_e': {
                FIELD_SYMBOL: '🇧🇪',
                FIELD_NAME: 'Regional indicator symbol letter b z regional indicator symbol letter e',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_b_with_regional_indicator_symbol_letter_z': {
                FIELD_SYMBOL: '🇧🇿',
                FIELD_NAME: 'Regional indicator symbol letter b z regional indicator symbol letter z',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_b_with_regional_indicator_symbol_letter_j': {
                FIELD_SYMBOL: '🇧🇯',
                FIELD_NAME: 'Regional indicator symbol letter b z regional indicator symbol letter j',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_b_with_regional_indicator_symbol_letter_m': {
                FIELD_SYMBOL: '🇧🇲',
                FIELD_NAME: 'Regional indicator symbol letter b z regional indicator symbol letter m',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_b_with_regional_indicator_symbol_letter_t': {
                FIELD_SYMBOL: '🇧🇹',
                FIELD_NAME: 'Regional indicator symbol letter b z regional indicator symbol letter t',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_b_with_regional_indicator_symbol_letter_y': {
                FIELD_SYMBOL: '🇧🇾',
                FIELD_NAME: 'Regional indicator symbol letter b z regional indicator symbol letter y',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_b_with_regional_indicator_symbol_letter_o': {
                FIELD_SYMBOL: '🇧🇴',
                FIELD_NAME: 'Regional indicator symbol letter b z regional indicator symbol letter o',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_b_with_regional_indicator_symbol_letter_a': {
                FIELD_SYMBOL: '🇧🇦',
                FIELD_NAME: 'Regional indicator symbol letter b z regional indicator symbol letter a',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_b_with_regional_indicator_symbol_letter_w': {
                FIELD_SYMBOL: '🇧🇼',
                FIELD_NAME: 'Regional indicator symbol letter b z regional indicator symbol letter w',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_b_with_regional_indicator_symbol_letter_r': {
                FIELD_SYMBOL: '🇧🇷',
                FIELD_NAME: 'Regional indicator symbol letter b z regional indicator symbol letter r',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_b_with_regional_indicator_symbol_letter_n': {
                FIELD_SYMBOL: '🇧🇳',
                FIELD_NAME: 'Regional indicator symbol letter b z regional indicator symbol letter n',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_v_with_regional_indicator_symbol_letter_g': {
                FIELD_SYMBOL: '🇻🇬',
                FIELD_NAME: 'Regional indicator symbol letter v z regional indicator symbol letter g',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_b_with_regional_indicator_symbol_letter_g': {
                FIELD_SYMBOL: '🇧🇬',
                FIELD_NAME: 'Regional indicator symbol letter b z regional indicator symbol letter g',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_b_with_regional_indicator_symbol_letter_f': {
                FIELD_SYMBOL: '🇧🇫',
                FIELD_NAME: 'Regional indicator symbol letter b z regional indicator symbol letter f',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_b_with_regional_indicator_symbol_letter_i': {
                FIELD_SYMBOL: '🇧🇮',
                FIELD_NAME: 'Regional indicator symbol letter b z regional indicator symbol letter i',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_c_with_regional_indicator_symbol_letter_l': {
                FIELD_SYMBOL: '🇨🇱',
                FIELD_NAME: 'Regional indicator symbol letter c z regional indicator symbol letter l',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_c_with_regional_indicator_symbol_letter_n': {
                FIELD_SYMBOL: '🇨🇳',
                FIELD_NAME: 'Regional indicator symbol letter c z regional indicator symbol letter n',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_h_with_regional_indicator_symbol_letter_r': {
                FIELD_SYMBOL: '🇭🇷',
                FIELD_NAME: 'Regional indicator symbol letter h z regional indicator symbol letter r',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_c_with_regional_indicator_symbol_letter_i': {
                FIELD_SYMBOL: '🇨🇮',
                FIELD_NAME: 'Regional indicator symbol letter c z regional indicator symbol letter i',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_c_with_regional_indicator_symbol_letter_w': {
                FIELD_SYMBOL: '🇨🇼',
                FIELD_NAME: 'Regional indicator symbol letter c z regional indicator symbol letter w',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_c_with_regional_indicator_symbol_letter_y': {
                FIELD_SYMBOL: '🇨🇾',
                FIELD_NAME: 'Regional indicator symbol letter c z regional indicator symbol letter y',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_t_with_regional_indicator_symbol_letter_d': {
                FIELD_SYMBOL: '🇹🇩',
                FIELD_NAME: 'Regional indicator symbol letter t z regional indicator symbol letter d',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_i_with_regional_indicator_symbol_letter_o': {
                FIELD_SYMBOL: '🇮🇴',
                FIELD_NAME: 'Regional indicator symbol letter i z regional indicator symbol letter o',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_m_with_regional_indicator_symbol_letter_e': {
                FIELD_SYMBOL: '🇲🇪',
                FIELD_NAME: 'Regional indicator symbol letter m z regional indicator symbol letter e',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_c_with_regional_indicator_symbol_letter_z': {
                FIELD_SYMBOL: '🇨🇿',
                FIELD_NAME: 'Regional indicator symbol letter c z regional indicator symbol letter z',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_d_with_regional_indicator_symbol_letter_k': {
                FIELD_SYMBOL: '🇩🇰',
                FIELD_NAME: 'Regional indicator symbol letter d z regional indicator symbol letter k',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_c_with_regional_indicator_symbol_letter_d': {
                FIELD_SYMBOL: '🇨🇩',
                FIELD_NAME: 'Regional indicator symbol letter c z regional indicator symbol letter d',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_d_with_regional_indicator_symbol_letter_m': {
                FIELD_SYMBOL: '🇩🇲',
                FIELD_NAME: 'Regional indicator symbol letter d z regional indicator symbol letter m',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_d_with_regional_indicator_symbol_letter_o': {
                FIELD_SYMBOL: '🇩🇴',
                FIELD_NAME: 'Regional indicator symbol letter d z regional indicator symbol letter o',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_d_with_regional_indicator_symbol_letter_j': {
                FIELD_SYMBOL: '🇩🇯',
                FIELD_NAME: 'Regional indicator symbol letter d z regional indicator symbol letter j',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_e_with_regional_indicator_symbol_letter_g': {
                FIELD_SYMBOL: '🇪🇬',
                FIELD_NAME: 'Regional indicator symbol letter e z regional indicator symbol letter g',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_e_with_regional_indicator_symbol_letter_c': {
                FIELD_SYMBOL: '🇪🇨',
                FIELD_NAME: 'Regional indicator symbol letter e z regional indicator symbol letter c',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_e_with_regional_indicator_symbol_letter_r': {
                FIELD_SYMBOL: '🇪🇷',
                FIELD_NAME: 'Regional indicator symbol letter e z regional indicator symbol letter r',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_e_with_regional_indicator_symbol_letter_e': {
                FIELD_SYMBOL: '🇪🇪',
                FIELD_NAME: 'Regional indicator symbol letter e z regional indicator symbol letter e',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_s_with_regional_indicator_symbol_letter_z': {
                FIELD_SYMBOL: '🇸🇿',
                FIELD_NAME: 'Regional indicator symbol letter s z regional indicator symbol letter z',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_e_with_regional_indicator_symbol_letter_t': {
                FIELD_SYMBOL: '🇪🇹',
                FIELD_NAME: 'Regional indicator symbol letter e z regional indicator symbol letter t',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_f_with_regional_indicator_symbol_letter_k': {
                FIELD_SYMBOL: '🇫🇰',
                FIELD_NAME: 'Regional indicator symbol letter f z regional indicator symbol letter k',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_f_with_regional_indicator_symbol_letter_j': {
                FIELD_SYMBOL: '🇫🇯',
                FIELD_NAME: 'Regional indicator symbol letter f z regional indicator symbol letter j',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_p_with_regional_indicator_symbol_letter_h': {
                FIELD_SYMBOL: '🇵🇭',
                FIELD_NAME: 'Regional indicator symbol letter p z regional indicator symbol letter h',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_f_with_regional_indicator_symbol_letter_i': {
                FIELD_SYMBOL: '🇫🇮',
                FIELD_NAME: 'Regional indicator symbol letter f z regional indicator symbol letter i',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_f_with_regional_indicator_symbol_letter_r': {
                FIELD_SYMBOL: '🇫🇷',
                FIELD_NAME: 'Regional indicator symbol letter f z regional indicator symbol letter r',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_t_with_regional_indicator_symbol_letter_f': {
                FIELD_SYMBOL: '🇹🇫',
                FIELD_NAME: 'Regional indicator symbol letter t z regional indicator symbol letter f',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_g_with_regional_indicator_symbol_letter_a': {
                FIELD_SYMBOL: '🇬🇦',
                FIELD_NAME: 'Regional indicator symbol letter g z regional indicator symbol letter a',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_g_with_regional_indicator_symbol_letter_m': {
                FIELD_SYMBOL: '🇬🇲',
                FIELD_NAME: 'Regional indicator symbol letter g z regional indicator symbol letter m',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_g_with_regional_indicator_symbol_letter_s': {
                FIELD_SYMBOL: '🇬🇸',
                FIELD_NAME: 'Regional indicator symbol letter g z regional indicator symbol letter s',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_g_with_regional_indicator_symbol_letter_h': {
                FIELD_SYMBOL: '🇬🇭',
                FIELD_NAME: 'Regional indicator symbol letter g z regional indicator symbol letter h',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_g_with_regional_indicator_symbol_letter_i': {
                FIELD_SYMBOL: '🇬🇮',
                FIELD_NAME: 'Regional indicator symbol letter g z regional indicator symbol letter i',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_g_with_regional_indicator_symbol_letter_r': {
                FIELD_SYMBOL: '🇬🇷',
                FIELD_NAME: 'Regional indicator symbol letter g z regional indicator symbol letter r',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_g_with_regional_indicator_symbol_letter_d': {
                FIELD_SYMBOL: '🇬🇩',
                FIELD_NAME: 'Regional indicator symbol letter g z regional indicator symbol letter d',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_g_with_regional_indicator_symbol_letter_l': {
                FIELD_SYMBOL: '🇬🇱',
                FIELD_NAME: 'Regional indicator symbol letter g z regional indicator symbol letter l',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_g_with_regional_indicator_symbol_letter_e': {
                FIELD_SYMBOL: '🇬🇪',
                FIELD_NAME: 'Regional indicator symbol letter g z regional indicator symbol letter e',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_g_with_regional_indicator_symbol_letter_u': {
                FIELD_SYMBOL: '🇬🇺',
                FIELD_NAME: 'Regional indicator symbol letter g z regional indicator symbol letter u',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_g_with_regional_indicator_symbol_letter_g': {
                FIELD_SYMBOL: '🇬🇬',
                FIELD_NAME: 'Regional indicator symbol letter g z regional indicator symbol letter g',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_g_with_regional_indicator_symbol_letter_y': {
                FIELD_SYMBOL: '🇬🇾',
                FIELD_NAME: 'Regional indicator symbol letter g z regional indicator symbol letter y',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_g_with_regional_indicator_symbol_letter_f': {
                FIELD_SYMBOL: '🇬🇫',
                FIELD_NAME: 'Regional indicator symbol letter g z regional indicator symbol letter f',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_g_with_regional_indicator_symbol_letter_p': {
                FIELD_SYMBOL: '🇬🇵',
                FIELD_NAME: 'Regional indicator symbol letter g z regional indicator symbol letter p',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_g_with_regional_indicator_symbol_letter_t': {
                FIELD_SYMBOL: '🇬🇹',
                FIELD_NAME: 'Regional indicator symbol letter g z regional indicator symbol letter t',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_g_with_regional_indicator_symbol_letter_n': {
                FIELD_SYMBOL: '🇬🇳',
                FIELD_NAME: 'Regional indicator symbol letter g z regional indicator symbol letter n',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_g_with_regional_indicator_symbol_letter_w': {
                FIELD_SYMBOL: '🇬🇼',
                FIELD_NAME: 'Regional indicator symbol letter g z regional indicator symbol letter w',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_g_with_regional_indicator_symbol_letter_q': {
                FIELD_SYMBOL: '🇬🇶',
                FIELD_NAME: 'Regional indicator symbol letter g z regional indicator symbol letter q',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_h_with_regional_indicator_symbol_letter_t': {
                FIELD_SYMBOL: '🇭🇹',
                FIELD_NAME: 'Regional indicator symbol letter h z regional indicator symbol letter t',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_e_with_regional_indicator_symbol_letter_s': {
                FIELD_SYMBOL: '🇪🇸',
                FIELD_NAME: 'Regional indicator symbol letter e z regional indicator symbol letter s',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_n_with_regional_indicator_symbol_letter_l': {
                FIELD_SYMBOL: '🇳🇱',
                FIELD_NAME: 'Regional indicator symbol letter n z regional indicator symbol letter l',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_h_with_regional_indicator_symbol_letter_n': {
                FIELD_SYMBOL: '🇭🇳',
                FIELD_NAME: 'Regional indicator symbol letter h z regional indicator symbol letter n',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_h_with_regional_indicator_symbol_letter_k': {
                FIELD_SYMBOL: '🇭🇰',
                FIELD_NAME: 'Regional indicator symbol letter h z regional indicator symbol letter k',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_i_with_regional_indicator_symbol_letter_n': {
                FIELD_SYMBOL: '🇮🇳',
                FIELD_NAME: 'Regional indicator symbol letter i z regional indicator symbol letter n',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_i_with_regional_indicator_symbol_letter_d': {
                FIELD_SYMBOL: '🇮🇩',
                FIELD_NAME: 'Regional indicator symbol letter i z regional indicator symbol letter d',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_i_with_regional_indicator_symbol_letter_q': {
                FIELD_SYMBOL: '🇮🇶',
                FIELD_NAME: 'Regional indicator symbol letter i z regional indicator symbol letter q',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_i_with_regional_indicator_symbol_letter_r': {
                FIELD_SYMBOL: '🇮🇷',
                FIELD_NAME: 'Regional indicator symbol letter i z regional indicator symbol letter r',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_i_with_regional_indicator_symbol_letter_e': {
                FIELD_SYMBOL: '🇮🇪',
                FIELD_NAME: 'Regional indicator symbol letter i z regional indicator symbol letter e',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_i_with_regional_indicator_symbol_letter_s': {
                FIELD_SYMBOL: '🇮🇸',
                FIELD_NAME: 'Regional indicator symbol letter i z regional indicator symbol letter s',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_i_with_regional_indicator_symbol_letter_l': {
                FIELD_SYMBOL: '🇮🇱',
                FIELD_NAME: 'Regional indicator symbol letter i z regional indicator symbol letter l',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_j_with_regional_indicator_symbol_letter_m': {
                FIELD_SYMBOL: '🇯🇲',
                FIELD_NAME: 'Regional indicator symbol letter j z regional indicator symbol letter m',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_j_with_regional_indicator_symbol_letter_p': {
                FIELD_SYMBOL: '🇯🇵',
                FIELD_NAME: 'Regional indicator symbol letter j z regional indicator symbol letter p',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'crossed_flags': {
                FIELD_SYMBOL: '🎌',
                FIELD_NAME: 'Skrzyżowane flagi',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_y_with_regional_indicator_symbol_letter_e': {
                FIELD_SYMBOL: '🇾🇪',
                FIELD_NAME: 'Regional indicator symbol letter y z regional indicator symbol letter e',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_j_with_regional_indicator_symbol_letter_e': {
                FIELD_SYMBOL: '🇯🇪',
                FIELD_NAME: 'Regional indicator symbol letter j z regional indicator symbol letter e',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_j_with_regional_indicator_symbol_letter_o': {
                FIELD_SYMBOL: '🇯🇴',
                FIELD_NAME: 'Regional indicator symbol letter j z regional indicator symbol letter o',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_k_with_regional_indicator_symbol_letter_y': {
                FIELD_SYMBOL: '🇰🇾',
                FIELD_NAME: 'Regional indicator symbol letter k z regional indicator symbol letter y',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_k_with_regional_indicator_symbol_letter_h': {
                FIELD_SYMBOL: '🇰🇭',
                FIELD_NAME: 'Regional indicator symbol letter k z regional indicator symbol letter h',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_c_with_regional_indicator_symbol_letter_m': {
                FIELD_SYMBOL: '🇨🇲',
                FIELD_NAME: 'Regional indicator symbol letter c z regional indicator symbol letter m',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_c_with_regional_indicator_symbol_letter_a': {
                FIELD_SYMBOL: '🇨🇦',
                FIELD_NAME: 'Regional indicator symbol letter c z regional indicator symbol letter a',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_q_with_regional_indicator_symbol_letter_a': {
                FIELD_SYMBOL: '🇶🇦',
                FIELD_NAME: 'Regional indicator symbol letter q z regional indicator symbol letter a',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_k_with_regional_indicator_symbol_letter_z': {
                FIELD_SYMBOL: '🇰🇿',
                FIELD_NAME: 'Regional indicator symbol letter k z regional indicator symbol letter z',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_k_with_regional_indicator_symbol_letter_e': {
                FIELD_SYMBOL: '🇰🇪',
                FIELD_NAME: 'Regional indicator symbol letter k z regional indicator symbol letter e',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_k_with_regional_indicator_symbol_letter_g': {
                FIELD_SYMBOL: '🇰🇬',
                FIELD_NAME: 'Regional indicator symbol letter k z regional indicator symbol letter g',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_k_with_regional_indicator_symbol_letter_i': {
                FIELD_SYMBOL: '🇰🇮',
                FIELD_NAME: 'Regional indicator symbol letter k z regional indicator symbol letter i',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_c_with_regional_indicator_symbol_letter_o': {
                FIELD_SYMBOL: '🇨🇴',
                FIELD_NAME: 'Regional indicator symbol letter c z regional indicator symbol letter o',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_k_with_regional_indicator_symbol_letter_m': {
                FIELD_SYMBOL: '🇰🇲',
                FIELD_NAME: 'Regional indicator symbol letter k z regional indicator symbol letter m',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_c_with_regional_indicator_symbol_letter_g': {
                FIELD_SYMBOL: '🇨🇬',
                FIELD_NAME: 'Regional indicator symbol letter c z regional indicator symbol letter g',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_k_with_regional_indicator_symbol_letter_r': {
                FIELD_SYMBOL: '🇰🇷',
                FIELD_NAME: 'Regional indicator symbol letter k z regional indicator symbol letter r',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_k_with_regional_indicator_symbol_letter_p': {
                FIELD_SYMBOL: '🇰🇵',
                FIELD_NAME: 'Regional indicator symbol letter k z regional indicator symbol letter p',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_x_with_regional_indicator_symbol_letter_k': {
                FIELD_SYMBOL: '🇽🇰',
                FIELD_NAME: 'Regional indicator symbol letter x z regional indicator symbol letter k',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_c_with_regional_indicator_symbol_letter_r': {
                FIELD_SYMBOL: '🇨🇷',
                FIELD_NAME: 'Regional indicator symbol letter c z regional indicator symbol letter r',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_c_with_regional_indicator_symbol_letter_u': {
                FIELD_SYMBOL: '🇨🇺',
                FIELD_NAME: 'Regional indicator symbol letter c z regional indicator symbol letter u',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_k_with_regional_indicator_symbol_letter_w': {
                FIELD_SYMBOL: '🇰🇼',
                FIELD_NAME: 'Regional indicator symbol letter k z regional indicator symbol letter w',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_l_with_regional_indicator_symbol_letter_a': {
                FIELD_SYMBOL: '🇱🇦',
                FIELD_NAME: 'Regional indicator symbol letter l z regional indicator symbol letter a',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_l_with_regional_indicator_symbol_letter_s': {
                FIELD_SYMBOL: '🇱🇸',
                FIELD_NAME: 'Regional indicator symbol letter l z regional indicator symbol letter s',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_l_with_regional_indicator_symbol_letter_b': {
                FIELD_SYMBOL: '🇱🇧',
                FIELD_NAME: 'Regional indicator symbol letter l z regional indicator symbol letter b',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_l_with_regional_indicator_symbol_letter_r': {
                FIELD_SYMBOL: '🇱🇷',
                FIELD_NAME: 'Regional indicator symbol letter l z regional indicator symbol letter r',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_l_with_regional_indicator_symbol_letter_y': {
                FIELD_SYMBOL: '🇱🇾',
                FIELD_NAME: 'Regional indicator symbol letter l z regional indicator symbol letter y',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_l_with_regional_indicator_symbol_letter_i': {
                FIELD_SYMBOL: '🇱🇮',
                FIELD_NAME: 'Regional indicator symbol letter l z regional indicator symbol letter i',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_l_with_regional_indicator_symbol_letter_t': {
                FIELD_SYMBOL: '🇱🇹',
                FIELD_NAME: 'Regional indicator symbol letter l z regional indicator symbol letter t',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_l_with_regional_indicator_symbol_letter_u': {
                FIELD_SYMBOL: '🇱🇺',
                FIELD_NAME: 'Regional indicator symbol letter l z regional indicator symbol letter u',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_l_with_regional_indicator_symbol_letter_v': {
                FIELD_SYMBOL: '🇱🇻',
                FIELD_NAME: 'Regional indicator symbol letter l z regional indicator symbol letter v',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_m_with_regional_indicator_symbol_letter_k': {
                FIELD_SYMBOL: '🇲🇰',
                FIELD_NAME: 'Regional indicator symbol letter m z regional indicator symbol letter k',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_m_with_regional_indicator_symbol_letter_g': {
                FIELD_SYMBOL: '🇲🇬',
                FIELD_NAME: 'Regional indicator symbol letter m z regional indicator symbol letter g',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_y_with_regional_indicator_symbol_letter_t': {
                FIELD_SYMBOL: '🇾🇹',
                FIELD_NAME: 'Regional indicator symbol letter y z regional indicator symbol letter t',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_m_with_regional_indicator_symbol_letter_o': {
                FIELD_SYMBOL: '🇲🇴',
                FIELD_NAME: 'Regional indicator symbol letter m z regional indicator symbol letter o',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_m_with_regional_indicator_symbol_letter_w': {
                FIELD_SYMBOL: '🇲🇼',
                FIELD_NAME: 'Regional indicator symbol letter m z regional indicator symbol letter w',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_m_with_regional_indicator_symbol_letter_v': {
                FIELD_SYMBOL: '🇲🇻',
                FIELD_NAME: 'Regional indicator symbol letter m z regional indicator symbol letter v',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_m_with_regional_indicator_symbol_letter_y': {
                FIELD_SYMBOL: '🇲🇾',
                FIELD_NAME: 'Regional indicator symbol letter m z regional indicator symbol letter y',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_m_with_regional_indicator_symbol_letter_l': {
                FIELD_SYMBOL: '🇲🇱',
                FIELD_NAME: 'Regional indicator symbol letter m z regional indicator symbol letter l',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_m_with_regional_indicator_symbol_letter_t': {
                FIELD_SYMBOL: '🇲🇹',
                FIELD_NAME: 'Regional indicator symbol letter m z regional indicator symbol letter t',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_m_with_regional_indicator_symbol_letter_p': {
                FIELD_SYMBOL: '🇲🇵',
                FIELD_NAME: 'Regional indicator symbol letter m z regional indicator symbol letter p',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_m_with_regional_indicator_symbol_letter_a': {
                FIELD_SYMBOL: '🇲🇦',
                FIELD_NAME: 'Regional indicator symbol letter m z regional indicator symbol letter a',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_m_with_regional_indicator_symbol_letter_q': {
                FIELD_SYMBOL: '🇲🇶',
                FIELD_NAME: 'Regional indicator symbol letter m z regional indicator symbol letter q',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_m_with_regional_indicator_symbol_letter_r': {
                FIELD_SYMBOL: '🇲🇷',
                FIELD_NAME: 'Regional indicator symbol letter m z regional indicator symbol letter r',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_m_with_regional_indicator_symbol_letter_u': {
                FIELD_SYMBOL: '🇲🇺',
                FIELD_NAME: 'Regional indicator symbol letter m z regional indicator symbol letter u',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_m_with_regional_indicator_symbol_letter_x': {
                FIELD_SYMBOL: '🇲🇽',
                FIELD_NAME: 'Regional indicator symbol letter m z regional indicator symbol letter x',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_f_with_regional_indicator_symbol_letter_m': {
                FIELD_SYMBOL: '🇫🇲',
                FIELD_NAME: 'Regional indicator symbol letter f z regional indicator symbol letter m',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_m_with_regional_indicator_symbol_letter_m': {
                FIELD_SYMBOL: '🇲🇲',
                FIELD_NAME: 'Regional indicator symbol letter m z regional indicator symbol letter m',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_m_with_regional_indicator_symbol_letter_d': {
                FIELD_SYMBOL: '🇲🇩',
                FIELD_NAME: 'Regional indicator symbol letter m z regional indicator symbol letter d',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_m_with_regional_indicator_symbol_letter_c': {
                FIELD_SYMBOL: '🇲🇨',
                FIELD_NAME: 'Regional indicator symbol letter m z regional indicator symbol letter c',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_m_with_regional_indicator_symbol_letter_n': {
                FIELD_SYMBOL: '🇲🇳',
                FIELD_NAME: 'Regional indicator symbol letter m z regional indicator symbol letter n',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_m_with_regional_indicator_symbol_letter_s': {
                FIELD_SYMBOL: '🇲🇸',
                FIELD_NAME: 'Regional indicator symbol letter m z regional indicator symbol letter s',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_m_with_regional_indicator_symbol_letter_z': {
                FIELD_SYMBOL: '🇲🇿',
                FIELD_NAME: 'Regional indicator symbol letter m z regional indicator symbol letter z',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_n_with_regional_indicator_symbol_letter_a': {
                FIELD_SYMBOL: '🇳🇦',
                FIELD_NAME: 'Regional indicator symbol letter n z regional indicator symbol letter a',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_n_with_regional_indicator_symbol_letter_r': {
                FIELD_SYMBOL: '🇳🇷',
                FIELD_NAME: 'Regional indicator symbol letter n z regional indicator symbol letter r',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_n_with_regional_indicator_symbol_letter_p': {
                FIELD_SYMBOL: '🇳🇵',
                FIELD_NAME: 'Regional indicator symbol letter n z regional indicator symbol letter p',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_b_with_regional_indicator_symbol_letter_q': {
                FIELD_SYMBOL: '🇧🇶',
                FIELD_NAME: 'Regional indicator symbol letter b z regional indicator symbol letter q',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_d_with_regional_indicator_symbol_letter_e': {
                FIELD_SYMBOL: '🇩🇪',
                FIELD_NAME: 'Regional indicator symbol letter d z regional indicator symbol letter e',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_n_with_regional_indicator_symbol_letter_e': {
                FIELD_SYMBOL: '🇳🇪',
                FIELD_NAME: 'Regional indicator symbol letter n z regional indicator symbol letter e',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_n_with_regional_indicator_symbol_letter_g': {
                FIELD_SYMBOL: '🇳🇬',
                FIELD_NAME: 'Regional indicator symbol letter n z regional indicator symbol letter g',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_n_with_regional_indicator_symbol_letter_i': {
                FIELD_SYMBOL: '🇳🇮',
                FIELD_NAME: 'Regional indicator symbol letter n z regional indicator symbol letter i',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_n_with_regional_indicator_symbol_letter_u': {
                FIELD_SYMBOL: '🇳🇺',
                FIELD_NAME: 'Regional indicator symbol letter n z regional indicator symbol letter u',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_n_with_regional_indicator_symbol_letter_f': {
                FIELD_SYMBOL: '🇳🇫',
                FIELD_NAME: 'Regional indicator symbol letter n z regional indicator symbol letter f',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_n_with_regional_indicator_symbol_letter_o': {
                FIELD_SYMBOL: '🇳🇴',
                FIELD_NAME: 'Regional indicator symbol letter n z regional indicator symbol letter o',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_n_with_regional_indicator_symbol_letter_c': {
                FIELD_SYMBOL: '🇳🇨',
                FIELD_NAME: 'Regional indicator symbol letter n z regional indicator symbol letter c',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_n_with_regional_indicator_symbol_letter_z': {
                FIELD_SYMBOL: '🇳🇿',
                FIELD_NAME: 'Regional indicator symbol letter n z regional indicator symbol letter z',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_o_with_regional_indicator_symbol_letter_m': {
                FIELD_SYMBOL: '🇴🇲',
                FIELD_NAME: 'Regional indicator symbol letter o z regional indicator symbol letter m',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_p_with_regional_indicator_symbol_letter_k': {
                FIELD_SYMBOL: '🇵🇰',
                FIELD_NAME: 'Regional indicator symbol letter p z regional indicator symbol letter k',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_p_with_regional_indicator_symbol_letter_w': {
                FIELD_SYMBOL: '🇵🇼',
                FIELD_NAME: 'Regional indicator symbol letter p z regional indicator symbol letter w',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_p_with_regional_indicator_symbol_letter_a': {
                FIELD_SYMBOL: '🇵🇦',
                FIELD_NAME: 'Regional indicator symbol letter p z regional indicator symbol letter a',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_p_with_regional_indicator_symbol_letter_g': {
                FIELD_SYMBOL: '🇵🇬',
                FIELD_NAME: 'Regional indicator symbol letter p z regional indicator symbol letter g',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_p_with_regional_indicator_symbol_letter_y': {
                FIELD_SYMBOL: '🇵🇾',
                FIELD_NAME: 'Regional indicator symbol letter p z regional indicator symbol letter y',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_p_with_regional_indicator_symbol_letter_e': {
                FIELD_SYMBOL: '🇵🇪',
                FIELD_NAME: 'Regional indicator symbol letter p z regional indicator symbol letter e',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_p_with_regional_indicator_symbol_letter_n': {
                FIELD_SYMBOL: '🇵🇳',
                FIELD_NAME: 'Regional indicator symbol letter p z regional indicator symbol letter n',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_p_with_regional_indicator_symbol_letter_f': {
                FIELD_SYMBOL: '🇵🇫',
                FIELD_NAME: 'Regional indicator symbol letter p z regional indicator symbol letter f',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_p_with_regional_indicator_symbol_letter_l': {
                FIELD_SYMBOL: '🇵🇱',
                FIELD_NAME: 'Regional indicator symbol letter p z regional indicator symbol letter l',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_p_with_regional_indicator_symbol_letter_r': {
                FIELD_SYMBOL: '🇵🇷',
                FIELD_NAME: 'Regional indicator symbol letter p z regional indicator symbol letter r',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_p_with_regional_indicator_symbol_letter_t': {
                FIELD_SYMBOL: '🇵🇹',
                FIELD_NAME: 'Regional indicator symbol letter p z regional indicator symbol letter t',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_z_with_regional_indicator_symbol_letter_a': {
                FIELD_SYMBOL: '🇿🇦',
                FIELD_NAME: 'Regional indicator symbol letter z z regional indicator symbol letter a',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_c_with_regional_indicator_symbol_letter_f': {
                FIELD_SYMBOL: '🇨🇫',
                FIELD_NAME: 'Regional indicator symbol letter c z regional indicator symbol letter f',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_c_with_regional_indicator_symbol_letter_v': {
                FIELD_SYMBOL: '🇨🇻',
                FIELD_NAME: 'Regional indicator symbol letter c z regional indicator symbol letter v',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_r_with_regional_indicator_symbol_letter_e': {
                FIELD_SYMBOL: '🇷🇪',
                FIELD_NAME: 'Regional indicator symbol letter r z regional indicator symbol letter e',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_r_with_regional_indicator_symbol_letter_u': {
                FIELD_SYMBOL: '🇷🇺',
                FIELD_NAME: 'Regional indicator symbol letter r z regional indicator symbol letter u',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_r_with_regional_indicator_symbol_letter_o': {
                FIELD_SYMBOL: '🇷🇴',
                FIELD_NAME: 'Regional indicator symbol letter r z regional indicator symbol letter o',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_r_with_regional_indicator_symbol_letter_w': {
                FIELD_SYMBOL: '🇷🇼',
                FIELD_NAME: 'Regional indicator symbol letter r z regional indicator symbol letter w',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_e_with_regional_indicator_symbol_letter_h': {
                FIELD_SYMBOL: '🇪🇭',
                FIELD_NAME: 'Regional indicator symbol letter e z regional indicator symbol letter h',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_k_with_regional_indicator_symbol_letter_n': {
                FIELD_SYMBOL: '🇰🇳',
                FIELD_NAME: 'Regional indicator symbol letter k z regional indicator symbol letter n',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_l_with_regional_indicator_symbol_letter_c': {
                FIELD_SYMBOL: '🇱🇨',
                FIELD_NAME: 'Regional indicator symbol letter l z regional indicator symbol letter c',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_v_with_regional_indicator_symbol_letter_c': {
                FIELD_SYMBOL: '🇻🇨',
                FIELD_NAME: 'Regional indicator symbol letter v z regional indicator symbol letter c',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_b_with_regional_indicator_symbol_letter_l': {
                FIELD_SYMBOL: '🇧🇱',
                FIELD_NAME: 'Regional indicator symbol letter b z regional indicator symbol letter l',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_p_with_regional_indicator_symbol_letter_m': {
                FIELD_SYMBOL: '🇵🇲',
                FIELD_NAME: 'Regional indicator symbol letter p z regional indicator symbol letter m',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_s_with_regional_indicator_symbol_letter_v': {
                FIELD_SYMBOL: '🇸🇻',
                FIELD_NAME: 'Regional indicator symbol letter s z regional indicator symbol letter v',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_w_with_regional_indicator_symbol_letter_s': {
                FIELD_SYMBOL: '🇼🇸',
                FIELD_NAME: 'Regional indicator symbol letter w z regional indicator symbol letter s',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_a_with_regional_indicator_symbol_letter_s': {
                FIELD_SYMBOL: '🇦🇸',
                FIELD_NAME: 'Regional indicator symbol letter a z regional indicator symbol letter s',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_s_with_regional_indicator_symbol_letter_m': {
                FIELD_SYMBOL: '🇸🇲',
                FIELD_NAME: 'Regional indicator symbol letter s z regional indicator symbol letter m',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_c_with_regional_indicator_symbol_letter_q': {
                FIELD_SYMBOL: '🇨🇶',
                FIELD_NAME: 'Regional indicator symbol letter c z regional indicator symbol letter q',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_s_with_regional_indicator_symbol_letter_n': {
                FIELD_SYMBOL: '🇸🇳',
                FIELD_NAME: 'Regional indicator symbol letter s z regional indicator symbol letter n',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_r_with_regional_indicator_symbol_letter_s': {
                FIELD_SYMBOL: '🇷🇸',
                FIELD_NAME: 'Regional indicator symbol letter r z regional indicator symbol letter s',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_s_with_regional_indicator_symbol_letter_c': {
                FIELD_SYMBOL: '🇸🇨',
                FIELD_NAME: 'Regional indicator symbol letter s z regional indicator symbol letter c',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_s_with_regional_indicator_symbol_letter_l': {
                FIELD_SYMBOL: '🇸🇱',
                FIELD_NAME: 'Regional indicator symbol letter s z regional indicator symbol letter l',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_s_with_regional_indicator_symbol_letter_g': {
                FIELD_SYMBOL: '🇸🇬',
                FIELD_NAME: 'Regional indicator symbol letter s z regional indicator symbol letter g',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_s_with_regional_indicator_symbol_letter_x': {
                FIELD_SYMBOL: '🇸🇽',
                FIELD_NAME: 'Regional indicator symbol letter s z regional indicator symbol letter x',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_s_with_regional_indicator_symbol_letter_k': {
                FIELD_SYMBOL: '🇸🇰',
                FIELD_NAME: 'Regional indicator symbol letter s z regional indicator symbol letter k',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_s_with_regional_indicator_symbol_letter_i': {
                FIELD_SYMBOL: '🇸🇮',
                FIELD_NAME: 'Regional indicator symbol letter s z regional indicator symbol letter i',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_s_with_regional_indicator_symbol_letter_o': {
                FIELD_SYMBOL: '🇸🇴',
                FIELD_NAME: 'Regional indicator symbol letter s z regional indicator symbol letter o',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_l_with_regional_indicator_symbol_letter_k': {
                FIELD_SYMBOL: '🇱🇰',
                FIELD_NAME: 'Regional indicator symbol letter l z regional indicator symbol letter k',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_u_with_regional_indicator_symbol_letter_s': {
                FIELD_SYMBOL: '🇺🇸',
                FIELD_NAME: 'Regional indicator symbol letter u z regional indicator symbol letter s',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_s_with_regional_indicator_symbol_letter_d': {
                FIELD_SYMBOL: '🇸🇩',
                FIELD_NAME: 'Regional indicator symbol letter s z regional indicator symbol letter d',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_s_with_regional_indicator_symbol_letter_s': {
                FIELD_SYMBOL: '🇸🇸',
                FIELD_NAME: 'Regional indicator symbol letter s z regional indicator symbol letter s',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_s_with_regional_indicator_symbol_letter_r': {
                FIELD_SYMBOL: '🇸🇷',
                FIELD_NAME: 'Regional indicator symbol letter s z regional indicator symbol letter r',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_s_with_regional_indicator_symbol_letter_y': {
                FIELD_SYMBOL: '🇸🇾',
                FIELD_NAME: 'Regional indicator symbol letter s z regional indicator symbol letter y',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_c_with_regional_indicator_symbol_letter_h': {
                FIELD_SYMBOL: '🇨🇭',
                FIELD_NAME: 'Regional indicator symbol letter c z regional indicator symbol letter h',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_s_with_regional_indicator_symbol_letter_e': {
                FIELD_SYMBOL: '🇸🇪',
                FIELD_NAME: 'Regional indicator symbol letter s z regional indicator symbol letter e',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_t_with_regional_indicator_symbol_letter_j': {
                FIELD_SYMBOL: '🇹🇯',
                FIELD_NAME: 'Regional indicator symbol letter t z regional indicator symbol letter j',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_t_with_regional_indicator_symbol_letter_h': {
                FIELD_SYMBOL: '🇹🇭',
                FIELD_NAME: 'Regional indicator symbol letter t z regional indicator symbol letter h',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_t_with_regional_indicator_symbol_letter_w': {
                FIELD_SYMBOL: '🇹🇼',
                FIELD_NAME: 'Regional indicator symbol letter t z regional indicator symbol letter w',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_t_with_regional_indicator_symbol_letter_z': {
                FIELD_SYMBOL: '🇹🇿',
                FIELD_NAME: 'Regional indicator symbol letter t z regional indicator symbol letter z',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_p_with_regional_indicator_symbol_letter_s': {
                FIELD_SYMBOL: '🇵🇸',
                FIELD_NAME: 'Regional indicator symbol letter p z regional indicator symbol letter s',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_t_with_regional_indicator_symbol_letter_l': {
                FIELD_SYMBOL: '🇹🇱',
                FIELD_NAME: 'Regional indicator symbol letter t z regional indicator symbol letter l',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_t_with_regional_indicator_symbol_letter_g': {
                FIELD_SYMBOL: '🇹🇬',
                FIELD_NAME: 'Regional indicator symbol letter t z regional indicator symbol letter g',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_t_with_regional_indicator_symbol_letter_k': {
                FIELD_SYMBOL: '🇹🇰',
                FIELD_NAME: 'Regional indicator symbol letter t z regional indicator symbol letter k',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_t_with_regional_indicator_symbol_letter_o': {
                FIELD_SYMBOL: '🇹🇴',
                FIELD_NAME: 'Regional indicator symbol letter t z regional indicator symbol letter o',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_t_with_regional_indicator_symbol_letter_t': {
                FIELD_SYMBOL: '🇹🇹',
                FIELD_NAME: 'Regional indicator symbol letter t z regional indicator symbol letter t',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_t_with_regional_indicator_symbol_letter_n': {
                FIELD_SYMBOL: '🇹🇳',
                FIELD_NAME: 'Regional indicator symbol letter t z regional indicator symbol letter n',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_t_with_regional_indicator_symbol_letter_r': {
                FIELD_SYMBOL: '🇹🇷',
                FIELD_NAME: 'Regional indicator symbol letter t z regional indicator symbol letter r',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_t_with_regional_indicator_symbol_letter_m': {
                FIELD_SYMBOL: '🇹🇲',
                FIELD_NAME: 'Regional indicator symbol letter t z regional indicator symbol letter m',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_t_with_regional_indicator_symbol_letter_c': {
                FIELD_SYMBOL: '🇹🇨',
                FIELD_NAME: 'Regional indicator symbol letter t z regional indicator symbol letter c',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_t_with_regional_indicator_symbol_letter_v': {
                FIELD_SYMBOL: '🇹🇻',
                FIELD_NAME: 'Regional indicator symbol letter t z regional indicator symbol letter v',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_u_with_regional_indicator_symbol_letter_g': {
                FIELD_SYMBOL: '🇺🇬',
                FIELD_NAME: 'Regional indicator symbol letter u z regional indicator symbol letter g',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_u_with_regional_indicator_symbol_letter_a': {
                FIELD_SYMBOL: '🇺🇦',
                FIELD_NAME: 'Regional indicator symbol letter u z regional indicator symbol letter a',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_e_with_regional_indicator_symbol_letter_u': {
                FIELD_SYMBOL: '🇪🇺',
                FIELD_NAME: 'Regional indicator symbol letter e z regional indicator symbol letter u',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_u_with_regional_indicator_symbol_letter_y': {
                FIELD_SYMBOL: '🇺🇾',
                FIELD_NAME: 'Regional indicator symbol letter u z regional indicator symbol letter y',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_u_with_regional_indicator_symbol_letter_z': {
                FIELD_SYMBOL: '🇺🇿',
                FIELD_NAME: 'Regional indicator symbol letter u z regional indicator symbol letter z',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_v_with_regional_indicator_symbol_letter_u': {
                FIELD_SYMBOL: '🇻🇺',
                FIELD_NAME: 'Regional indicator symbol letter v z regional indicator symbol letter u',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_w_with_regional_indicator_symbol_letter_f': {
                FIELD_SYMBOL: '🇼🇫',
                FIELD_NAME: 'Regional indicator symbol letter w z regional indicator symbol letter f',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_v_with_regional_indicator_symbol_letter_a': {
                FIELD_SYMBOL: '🇻🇦',
                FIELD_NAME: 'Regional indicator symbol letter v z regional indicator symbol letter a',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_v_with_regional_indicator_symbol_letter_e': {
                FIELD_SYMBOL: '🇻🇪',
                FIELD_NAME: 'Regional indicator symbol letter v z regional indicator symbol letter e',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_h_with_regional_indicator_symbol_letter_u': {
                FIELD_SYMBOL: '🇭🇺',
                FIELD_NAME: 'Regional indicator symbol letter h z regional indicator symbol letter u',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_g_with_regional_indicator_symbol_letter_b': {
                FIELD_SYMBOL: '🇬🇧',
                FIELD_NAME: 'Regional indicator symbol letter g z regional indicator symbol letter b',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'waving_black_flag_with_tag_latin_small_letter_g_with_tag_latin_small_letter_b_with_tag_latin_small_letter_e_with_tag_latin_small_letter_n_with_tag_latin_small_letter_g_with_cancel_tag': {
                FIELD_SYMBOL: '🏴\U000e0067\U000e0062\U000e0065\U000e006e\U000e0067\U000e007f',
                FIELD_NAME: 'Waving czarny flaga z tag latin small letter g z tag latin small letter b z tag latin small letter e z tag latin small letter n z tag latin small letter g z cancel tag',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'waving_black_flag_with_tag_latin_small_letter_g_with_tag_latin_small_letter_b_with_tag_latin_small_letter_s_with_tag_latin_small_letter_c_with_tag_latin_small_letter_t_with_cancel_tag': {
                FIELD_SYMBOL: '🏴\U000e0067\U000e0062\U000e0073\U000e0063\U000e0074\U000e007f',
                FIELD_NAME: 'Waving czarny flaga z tag latin small letter g z tag latin small letter b z tag latin small letter s z tag latin small letter c z tag latin small letter t z cancel tag',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'waving_black_flag_with_tag_latin_small_letter_g_with_tag_latin_small_letter_b_with_tag_latin_small_letter_w_with_tag_latin_small_letter_l_with_tag_latin_small_letter_s_with_cancel_tag': {
                FIELD_SYMBOL: '🏴\U000e0067\U000e0062\U000e0077\U000e006c\U000e0073\U000e007f',
                FIELD_NAME: 'Waving czarny flaga z tag latin small letter g z tag latin small letter b z tag latin small letter w z tag latin small letter l z tag latin small letter s z cancel tag',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_v_with_regional_indicator_symbol_letter_n': {
                FIELD_SYMBOL: '🇻🇳',
                FIELD_NAME: 'Regional indicator symbol letter v z regional indicator symbol letter n',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_i_with_regional_indicator_symbol_letter_t': {
                FIELD_SYMBOL: '🇮🇹',
                FIELD_NAME: 'Regional indicator symbol letter i z regional indicator symbol letter t',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_c_with_regional_indicator_symbol_letter_x': {
                FIELD_SYMBOL: '🇨🇽',
                FIELD_NAME: 'Regional indicator symbol letter c z regional indicator symbol letter x',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_i_with_regional_indicator_symbol_letter_m': {
                FIELD_SYMBOL: '🇮🇲',
                FIELD_NAME: 'Regional indicator symbol letter i z regional indicator symbol letter m',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_s_with_regional_indicator_symbol_letter_h': {
                FIELD_SYMBOL: '🇸🇭',
                FIELD_NAME: 'Regional indicator symbol letter s z regional indicator symbol letter h',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_a_with_regional_indicator_symbol_letter_x': {
                FIELD_SYMBOL: '🇦🇽',
                FIELD_NAME: 'Regional indicator symbol letter a z regional indicator symbol letter x',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_c_with_regional_indicator_symbol_letter_k': {
                FIELD_SYMBOL: '🇨🇰',
                FIELD_NAME: 'Regional indicator symbol letter c z regional indicator symbol letter k',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_v_with_regional_indicator_symbol_letter_i': {
                FIELD_SYMBOL: '🇻🇮',
                FIELD_NAME: 'Regional indicator symbol letter v z regional indicator symbol letter i',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_i_with_regional_indicator_symbol_letter_c': {
                FIELD_SYMBOL: '🇮🇨',
                FIELD_NAME: 'Regional indicator symbol letter i z regional indicator symbol letter c',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_c_with_regional_indicator_symbol_letter_c': {
                FIELD_SYMBOL: '🇨🇨',
                FIELD_NAME: 'Regional indicator symbol letter c z regional indicator symbol letter c',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_m_with_regional_indicator_symbol_letter_h': {
                FIELD_SYMBOL: '🇲🇭',
                FIELD_NAME: 'Regional indicator symbol letter m z regional indicator symbol letter h',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_f_with_regional_indicator_symbol_letter_o': {
                FIELD_SYMBOL: '🇫🇴',
                FIELD_NAME: 'Regional indicator symbol letter f z regional indicator symbol letter o',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_s_with_regional_indicator_symbol_letter_b': {
                FIELD_SYMBOL: '🇸🇧',
                FIELD_NAME: 'Regional indicator symbol letter s z regional indicator symbol letter b',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_s_with_regional_indicator_symbol_letter_t': {
                FIELD_SYMBOL: '🇸🇹',
                FIELD_NAME: 'Regional indicator symbol letter s z regional indicator symbol letter t',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_z_with_regional_indicator_symbol_letter_m': {
                FIELD_SYMBOL: '🇿🇲',
                FIELD_NAME: 'Regional indicator symbol letter z z regional indicator symbol letter m',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_z_with_regional_indicator_symbol_letter_w': {
                FIELD_SYMBOL: '🇿🇼',
                FIELD_NAME: 'Regional indicator symbol letter z z regional indicator symbol letter w',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'regional_indicator_symbol_letter_a_with_regional_indicator_symbol_letter_e': {
                FIELD_SYMBOL: '🇦🇪',
                FIELD_NAME: 'Regional indicator symbol letter a z regional indicator symbol letter e',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
        },
        SYMBOLS: {
            'pink_heart': {
                FIELD_SYMBOL: '🩷',
                FIELD_NAME: 'Różowe Serce',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'heavy_black_heart': {
                FIELD_SYMBOL: '❤️',
                FIELD_NAME: 'Czarny symbol serca',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'orange_heart': {
                FIELD_SYMBOL: '🧡',
                FIELD_NAME: 'Pomarańczowe Serce',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'yellow_heart': {
                FIELD_SYMBOL: '💛',
                FIELD_NAME: 'Żółte serce',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'green_heart': {
                FIELD_SYMBOL: '💚',
                FIELD_NAME: 'Zielone serce',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'light_blue_heart': {
                FIELD_SYMBOL: '🩵',
                FIELD_NAME: 'Jasnoniebieskie Serce',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'blue_heart': {
                FIELD_SYMBOL: '💙',
                FIELD_NAME: 'Niebieskie serce',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'purple_heart': {
                FIELD_SYMBOL: '💜',
                FIELD_NAME: 'Fioletowe serce',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'black_heart': {
                FIELD_SYMBOL: '🖤',
                FIELD_NAME: 'Czarne serce',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'grey_heart': {
                FIELD_SYMBOL: '🩶',
                FIELD_NAME: 'Szare Serce',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'white_heart': {
                FIELD_SYMBOL: '🤍',
                FIELD_NAME: 'Białe serce',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'brown_heart': {
                FIELD_SYMBOL: '🤎',
                FIELD_NAME: 'Brązowe serce',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'broken_heart': {
                FIELD_SYMBOL: '💔',
                FIELD_NAME: 'Złamane serce',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'heavy_black_heart_with_fire': {
                FIELD_SYMBOL: '❤️\u200d🔥',
                FIELD_NAME: 'Heavy czarny sercem z fire',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'heavy_black_heart_with_adhesive_bandage': {
                FIELD_SYMBOL: '❤️\u200d🩹',
                FIELD_NAME: 'Heavy czarny sercem z adhesive bandage',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'heavy_heart_exclamation_mark_ornament': {
                FIELD_SYMBOL: '❣️',
                FIELD_NAME: 'Ornament z wykrzyknikiem ciężkiego serca',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'two_hearts': {
                FIELD_SYMBOL: '💕',
                FIELD_NAME: 'Dwa serca',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'revolving_hearts': {
                FIELD_SYMBOL: '💞',
                FIELD_NAME: 'Obracające się serca',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'beating_heart': {
                FIELD_SYMBOL: '💓',
                FIELD_NAME: 'Bijące serce',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'growing_heart': {
                FIELD_SYMBOL: '💗',
                FIELD_NAME: 'Rosnące Serce',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'sparkling_heart': {
                FIELD_SYMBOL: '💖',
                FIELD_NAME: 'Musujące Serce',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'heart_with_arrow': {
                FIELD_SYMBOL: '💘',
                FIELD_NAME: 'Serce ze strzałką',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'heart_with_ribbon': {
                FIELD_SYMBOL: '💝',
                FIELD_NAME: 'Serce ze wstążką',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
        },
        AV_SYMBOLS: {
            'mobile_phone_off': {
                FIELD_SYMBOL: '📴',
                FIELD_NAME: 'Telefon komórkowy wyłączony',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'vibration_mode': {
                FIELD_SYMBOL: '📳',
                FIELD_NAME: 'Tryb wibracji',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'low_brightness_symbol': {
                FIELD_SYMBOL: '🔅',
                FIELD_NAME: 'Symbol niskiej jasności',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'high_brightness_symbol': {
                FIELD_SYMBOL: '🔆',
                FIELD_NAME: 'Symbol wysokiej jasności',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'wireless': {
                FIELD_SYMBOL: '🛜',
                FIELD_NAME: 'Bezprzewodowy',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'cinema': {
                FIELD_SYMBOL: '🎦',
                FIELD_NAME: 'Kino',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'antenna_with_bars': {
                FIELD_SYMBOL: '📶',
                FIELD_NAME: 'Antena z prętami',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'eject_symbol': {
                FIELD_SYMBOL: '⏏️',
                FIELD_NAME: 'Wysuń symbol',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'black_right_pointing_triangle': {
                FIELD_SYMBOL: '▶️',
                FIELD_NAME: 'Czarny prawy trójkąt wskazujący',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'double_vertical_bar': {
                FIELD_SYMBOL: '⏸️',
                FIELD_NAME: 'Podwójny pionowy pasek',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'black_right_pointing_triangle_with_double_vertical_bar': {
                FIELD_SYMBOL: '⏯️',
                FIELD_NAME: 'Czarny trójkąt wskazujący z podwójnym pionowym paskiem',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'black_square_for_stop': {
                FIELD_SYMBOL: '⏹️',
                FIELD_NAME: 'Czarny kwadrat dla przystanku',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'black_circle_for_record': {
                FIELD_SYMBOL: '⏺️',
                FIELD_NAME: 'Czarny krąg do nagrywania',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'black_right_pointing_double_triangle_with_vertical_bar': {
                FIELD_SYMBOL: '⏭️',
                FIELD_NAME: 'Czarny trójkąt z prawej strony z pionowym paskiem',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'black_left_pointing_double_triangle_with_vertical_bar': {
                FIELD_SYMBOL: '⏮️',
                FIELD_NAME: 'Czarny lewy trójkątny trójkąt z pionowym paskiem',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'black_right_pointing_double_triangle': {
                FIELD_SYMBOL: '⏩️',
                FIELD_NAME: 'Czarny trójkąt trójkątny z prawej strony',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'black_left_pointing_double_triangle': {
                FIELD_SYMBOL: '⏪️',
                FIELD_NAME: 'Czarny lewy trójkąt wskazujący',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'black_up_pointing_double_triangle': {
                FIELD_SYMBOL: '⏫️',
                FIELD_NAME: 'Czarny trójkąt skierowany w górę',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'black_down_pointing_double_triangle': {
                FIELD_SYMBOL: '⏬️',
                FIELD_NAME: 'Czarny trójkąt skierowany w dół',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'black_left_pointing_triangle': {
                FIELD_SYMBOL: '◀️',
                FIELD_NAME: 'Czarny lewy trójkąt wskazujący',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'up_pointing_small_red_triangle': {
                FIELD_SYMBOL: '🔼',
                FIELD_NAME: 'Wskazujący mały czerwony trójkąt',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'down_pointing_small_red_triangle': {
                FIELD_SYMBOL: '🔽',
                FIELD_NAME: 'Mały czerwony trójkąt skierowany w dół',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'twisted_rightwards_arrows': {
                FIELD_SYMBOL: '🔀',
                FIELD_NAME: 'Skręcone strzałki w prawo',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'clockwise_rightwards_and_leftwards_open_circle_arrows': {
                FIELD_SYMBOL: '🔁',
                FIELD_NAME: 'Strzałki w prawo i w lewo Otwarte koło',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'clockwise_rightwards_and_leftwards_open_circle_arrows_with_circled_one_overlay': {
                FIELD_SYMBOL: '🔂',
                FIELD_NAME: 'Zgodnie z ruchem wskazówek zegara w prawo i po lewej stronie Otwieranie strzałek okręgu za pomocą jednej nakładki z kółkiem',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
        },
        MATHEMATICAL_SYMBOLS: {
            'heavy_plus_sign': {
                FIELD_SYMBOL: '➕',
                FIELD_NAME: 'Ciężki znak plus',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'heavy_minus_sign': {
                FIELD_SYMBOL: '➖',
                FIELD_NAME: 'Ciężki znak minus',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'heavy_division_sign': {
                FIELD_SYMBOL: '➗',
                FIELD_NAME: 'Znak ciężkiej dywizji',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'heavy_multiplication_x': {
                FIELD_SYMBOL: '✖️',
                FIELD_NAME: 'Ciężkie mnożenie X',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'heavy_equals_sign': {
                FIELD_SYMBOL: '🟰',
                FIELD_NAME: 'Gruby Znak Równości',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'permanent_paper_sign': {
                FIELD_SYMBOL: '♾️',
                FIELD_NAME: 'Znak stałego papieru',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
        },
        RELIGIOUS_SYMBOLS: {
            'peace_symbol': {
                FIELD_SYMBOL: '☮️',
                FIELD_NAME: 'Znak pokoju',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'latin_cross': {
                FIELD_SYMBOL: '✝️',
                FIELD_NAME: 'Krzyż Łaciński',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'star_and_crescent': {
                FIELD_SYMBOL: '☪️',
                FIELD_NAME: 'Gwiazda i półksiężyc',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'om_symbol': {
                FIELD_SYMBOL: '🕉️',
                FIELD_NAME: 'Symbol Om',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'wheel_of_dharma': {
                FIELD_SYMBOL: '☸️',
                FIELD_NAME: 'Koło Dharmy',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'khanda': {
                FIELD_SYMBOL: '🪯',
                FIELD_NAME: 'Khanda',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'star_of_david': {
                FIELD_SYMBOL: '✡️',
                FIELD_NAME: 'Gwiazda Dawida',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'six_pointed_star_with_middle_dot': {
                FIELD_SYMBOL: '🔯',
                FIELD_NAME: 'Sześć spiczastych gwiazd z środkową kropką',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'menorah_with_nine_branches': {
                FIELD_SYMBOL: '🕎',
                FIELD_NAME: 'Menora z dziewięcioma gałęziami',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'yin_yang': {
                FIELD_SYMBOL: '☯️',
                FIELD_NAME: 'Yin Yang',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'orthodox_cross': {
                FIELD_SYMBOL: '☦️',
                FIELD_NAME: 'Krzyż prawosławny',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'place_of_worship': {
                FIELD_SYMBOL: '🛐',
                FIELD_NAME: 'Miejsce kultu',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
        },
        OTHER_SYMBOLS: {
            'heart_decoration': {
                FIELD_SYMBOL: '💟',
                FIELD_NAME: 'Dekoracja Serca',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'ophiuchus': {
                FIELD_SYMBOL: '⛎',
                FIELD_NAME: 'Wężownik',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'atom_symbol': {
                FIELD_SYMBOL: '⚛️',
                FIELD_NAME: 'Symbol Atomu',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'eight_pointed_black_star': {
                FIELD_SYMBOL: '✴️',
                FIELD_NAME: 'Osiem Pointed Black Star',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'white_flower': {
                FIELD_SYMBOL: '💮',
                FIELD_NAME: 'Biały kwiat',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'cross_mark': {
                FIELD_SYMBOL: '❌',
                FIELD_NAME: 'Znak krzyża',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'heavy_large_circle': {
                FIELD_SYMBOL: '⭕️',
                FIELD_NAME: 'Ciężki Duży Krąg',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'octagonal_sign': {
                FIELD_SYMBOL: '🛑️',
                FIELD_NAME: 'Znak ośmiokątny',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'name_badge': {
                FIELD_SYMBOL: '📛',
                FIELD_NAME: 'Odznaka imienia',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'hundred_points_symbol': {
                FIELD_SYMBOL: '💯',
                FIELD_NAME: 'Symbol stu punktów',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'anger_symbol': {
                FIELD_SYMBOL: '💢',
                FIELD_NAME: 'Symbol gniewu',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'hot_springs': {
                FIELD_SYMBOL: '♨️',
                FIELD_NAME: 'Gorące źródła',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'part_alternation_mark': {
                FIELD_SYMBOL: '〽️',
                FIELD_NAME: 'Znak zmiany części',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'children_crossing': {
                FIELD_SYMBOL: '🚸',
                FIELD_NAME: 'Przejście dla dzieci',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'trident_emblem': {
                FIELD_SYMBOL: '🔱',
                FIELD_NAME: 'Trident Emblem',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'fleur_de_lis': {
                FIELD_SYMBOL: '⚜️',
                FIELD_NAME: 'Fleur-De-Lis',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'japanese_symbol_for_beginner': {
                FIELD_SYMBOL: '🔰',
                FIELD_NAME: 'Japoński symbol dla początkujących',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'black_universal_recycling_symbol': {
                FIELD_SYMBOL: '♻️',
                FIELD_NAME: 'Czarny uniwersalny symbol recyklingu',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'white_heavy_check_mark': {
                FIELD_SYMBOL: '✅',
                FIELD_NAME: 'Biały znacznik wyboru',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'sparkle': {
                FIELD_SYMBOL: '❇️',
                FIELD_NAME: 'Iskierka',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'eight_spoked_asterisk': {
                FIELD_SYMBOL: '✳️',
                FIELD_NAME: 'Osiem Spoked Asterisk',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'negative_squared_cross_mark': {
                FIELD_SYMBOL: '❎',
                FIELD_NAME: 'Negatywny kwadratowy znak krzyża',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'globe_with_meridians': {
                FIELD_SYMBOL: '🌐',
                FIELD_NAME: 'Globe with Meridians',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'diamond_shape_with_a_dot_inside': {
                FIELD_SYMBOL: '💠',
                FIELD_NAME: 'Diamentowy kształt z kropką w środku',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'cyclone': {
                FIELD_SYMBOL: '🌀',
                FIELD_NAME: 'Cyklon',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'sleeping_symbol': {
                FIELD_SYMBOL: '💤️',
                FIELD_NAME: 'Symbol spania',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'elevator': {
                FIELD_SYMBOL: '🛗',
                FIELD_NAME: 'Winda',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'adult_with_adult_with_child': {
                FIELD_SYMBOL: '🧑\u200d🧑\u200d🧒',
                FIELD_NAME: 'Adult z adult z child',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'adult_with_adult_with_child_with_child': {
                FIELD_SYMBOL: '🧑\u200d🧑\u200d🧒\u200d🧒',
                FIELD_NAME: 'Adult z adult z child z child',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'adult_with_child': {
                FIELD_SYMBOL: '🧑\u200d🧒',
                FIELD_NAME: 'Adult z child',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'adult_with_child_with_child': {
                FIELD_SYMBOL: '🧑\u200d🧒\u200d🧒',
                FIELD_NAME: 'Adult z child z child',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'male_with_stroke_and_male_and_female_sign': {
                FIELD_SYMBOL: '⚧️',
                FIELD_NAME: 'Mężczyzna z udarem i męskim i żeńskim znakiem',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'squared_katakana_koko': {
                FIELD_SYMBOL: '🈁',
                FIELD_NAME: 'Kwadrat Katakana Koko',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'eye_with_left_speech_bubble': {
                FIELD_SYMBOL: '👁️\u200d🗨️',
                FIELD_NAME: 'Okiem z lewo speech bubble',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'wavy_dash': {
                FIELD_SYMBOL: '〰️',
                FIELD_NAME: 'Falisty Dash',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'curly_loop': {
                FIELD_SYMBOL: '➰',
                FIELD_NAME: 'Curly Loop',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'double_curly_loop': {
                FIELD_SYMBOL: '➿',
                FIELD_NAME: 'Podwójna kręta pętla',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'heavy_check_mark': {
                FIELD_SYMBOL: '✔️',
                FIELD_NAME: 'Ciężki znacznik wyboru',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'ballot_box_with_check': {
                FIELD_SYMBOL: '☑️',
                FIELD_NAME: 'Urny z czekiem',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'radio_button': {
                FIELD_SYMBOL: '🔘',
                FIELD_NAME: 'Przycisk radiowy',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'speech_balloon': {
                FIELD_SYMBOL: '💬',
                FIELD_NAME: 'Balon Mowy',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'thought_balloon': {
                FIELD_SYMBOL: '💭',
                FIELD_NAME: 'Balon Myśli',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'right_anger_bubble': {
                FIELD_SYMBOL: '🗯️',
                FIELD_NAME: 'Prawy bąbelek gniewu',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
        },
        ZODIAC_SIGNS: {
            'aries': {
                FIELD_SYMBOL: '♈️',
                FIELD_NAME: 'Baran',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'taurus': {
                FIELD_SYMBOL: '♉️',
                FIELD_NAME: 'Byk',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'gemini': {
                FIELD_SYMBOL: '♊️',
                FIELD_NAME: 'Bliźnięta',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'cancer': {
                FIELD_SYMBOL: '♋️',
                FIELD_NAME: 'Rak',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'leo': {
                FIELD_SYMBOL: '♌️',
                FIELD_NAME: 'Lew',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'virgo': {
                FIELD_SYMBOL: '♍️',
                FIELD_NAME: 'Panna',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'libra': {
                FIELD_SYMBOL: '♎️',
                FIELD_NAME: 'Libra',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'scorpius': {
                FIELD_SYMBOL: '♏️',
                FIELD_NAME: 'Scorpius',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'sagittarius': {
                FIELD_SYMBOL: '♐️',
                FIELD_NAME: 'Strzelec',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'capricorn': {
                FIELD_SYMBOL: '♑️',
                FIELD_NAME: 'Koziorożec',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'aquarius': {
                FIELD_SYMBOL: '♒️',
                FIELD_NAME: 'Wodnik',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'pisces': {
                FIELD_SYMBOL: '♓️',
                FIELD_NAME: 'Ryby',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
        },
        WARNING_SIGNS: {
            'radioactive_sign': {
                FIELD_SYMBOL: '☢️',
                FIELD_NAME: 'Radioaktywny znak',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'biohazard_sign': {
                FIELD_SYMBOL: '☣️',
                FIELD_NAME: 'Znak zagrożenia biologicznego',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'warning_sign': {
                FIELD_SYMBOL: '⚠️',
                FIELD_NAME: 'Znak ostrzegawczy',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'no_entry': {
                FIELD_SYMBOL: '⛔',
                FIELD_NAME: 'Brak wejścia',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'no_entry_sign': {
                FIELD_SYMBOL: '🚫',
                FIELD_NAME: 'Brak wpisu',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'no_pedestrians': {
                FIELD_SYMBOL: '🚷',
                FIELD_NAME: 'Żadnych pieszych',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'do_not_litter_symbol': {
                FIELD_SYMBOL: '🚯',
                FIELD_NAME: 'Nie używaj symbolu miotu',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'no_bicycles': {
                FIELD_SYMBOL: '🚳',
                FIELD_NAME: 'Brak rowerów',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'non_potable_water_symbol': {
                FIELD_SYMBOL: '🚱',
                FIELD_NAME: 'Symbol wody niezdatnej do picia',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'no_one_under_eighteen_symbol': {
                FIELD_SYMBOL: '🔞',
                FIELD_NAME: 'Nikt pod osiemnastym symbolem',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'no_mobile_phones': {
                FIELD_SYMBOL: '📵',
                FIELD_NAME: 'Brak telefonów komórkowych',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'no_smoking_symbol': {
                FIELD_SYMBOL: '🚭',
                FIELD_NAME: 'Symbol zakazu palenia',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
        },
        ARROW_SIGNS: {
            'black_rightwards_arrow': {
                FIELD_SYMBOL: '➡️',
                FIELD_NAME: 'Czarna strzałka w prawo',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'leftwards_black_arrow': {
                FIELD_SYMBOL: '⬅️',
                FIELD_NAME: 'Czarna strzałka od lewej strony',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'upwards_black_arrow': {
                FIELD_SYMBOL: '⬆️',
                FIELD_NAME: 'Czarna strzałka w górę',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'downwards_black_arrow': {
                FIELD_SYMBOL: '⬇️',
                FIELD_NAME: 'W dół czarna strzałka',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'north_east_arrow': {
                FIELD_SYMBOL: '↗️',
                FIELD_NAME: 'North East Arrow',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'south_east_arrow': {
                FIELD_SYMBOL: '↘️',
                FIELD_NAME: 'South East Arrow',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'south_west_arrow': {
                FIELD_SYMBOL: '↙️',
                FIELD_NAME: 'South West Arrow',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'north_west_arrow': {
                FIELD_SYMBOL: '↖️',
                FIELD_NAME: 'North West Arrow',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'up_down_arrow': {
                FIELD_SYMBOL: '↕️',
                FIELD_NAME: 'Strzałka w górę',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'left_right_arrow': {
                FIELD_SYMBOL: '↔️',
                FIELD_NAME: 'Strzałka w lewo w prawo',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'rightwards_arrow_with_hook': {
                FIELD_SYMBOL: '↪️',
                FIELD_NAME: 'Strzałka w prawo z hakiem',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'leftwards_arrow_with_hook': {
                FIELD_SYMBOL: '↩️',
                FIELD_NAME: 'Leftwards Arrow with Hook',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'arrow_pointing_rightwards_then_curving_upwards': {
                FIELD_SYMBOL: '⤴️',
                FIELD_NAME: 'Strzałka skierowana w prawo, a następnie zakrzywiona w górę',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'arrow_pointing_rightwards_then_curving_downwards': {
                FIELD_SYMBOL: '⤵️',
                FIELD_NAME: 'Strzałka skierowana w prawo, a następnie zakrzywiona w dół',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'anticlockwise_downwards_and_upwards_open_circle_arrows': {
                FIELD_SYMBOL: '🔄',
                FIELD_NAME: 'Anticlockwise Downwards and Upwards Open Circle Arrows',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'clockwise_downwards_and_upwards_open_circle_arrows': {
                FIELD_SYMBOL: '🔃',
                FIELD_NAME: 'Strzałki w prawo iw dół Otwarte strzałki okręgu',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'end_with_leftwards_arrow_above': {
                FIELD_SYMBOL: '🔚',
                FIELD_NAME: 'Zakończ z lewą strzałą powyżej',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'back_with_leftwards_arrow_above': {
                FIELD_SYMBOL: '🔙',
                FIELD_NAME: 'Powrót z lewą strzałą powyżej',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'on_with_exclamation_mark_with_left_right_arrow_above': {
                FIELD_SYMBOL: '🔛',
                FIELD_NAME: 'On z wykrzyknikiem z strzałką w lewo w prawo powyżej',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'top_with_upwards_arrow_above': {
                FIELD_SYMBOL: '🔝',
                FIELD_NAME: 'Góra ze strzałką w górę powyżej',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'soon_with_rightwards_arrow_above': {
                FIELD_SYMBOL: '🔜',
                FIELD_NAME: 'Wkrótce ze strzałką w prawo powyżej',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
        },
        TRANSPORT_SIGNS: {
            'automated_teller_machine': {
                FIELD_SYMBOL: '🏧',
                FIELD_NAME: 'Bankomat',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'baby_symbol': {
                FIELD_SYMBOL: '🚼',
                FIELD_NAME: 'Symbol dziecka',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'restroom': {
                FIELD_SYMBOL: '🚻',
                FIELD_NAME: 'Ubikacja',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'mens_symbol': {
                FIELD_SYMBOL: '🚹',
                FIELD_NAME: 'Męski symbol',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'womens_symbol': {
                FIELD_SYMBOL: '🚺',
                FIELD_NAME: 'Symbol kobiety',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'put_litter_in_its_place_symbol': {
                FIELD_SYMBOL: '🚮',
                FIELD_NAME: 'Umieść miot w symbolu miejsca',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'left_luggage': {
                FIELD_SYMBOL: '🛅',
                FIELD_NAME: 'Lewy bagaż',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'baggage_claim': {
                FIELD_SYMBOL: '🛄',
                FIELD_NAME: 'Roszczenie bagażowe',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'passport_control': {
                FIELD_SYMBOL: '🛂',
                FIELD_NAME: 'Kontrola paszportowa',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'customs': {
                FIELD_SYMBOL: '🛃',
                FIELD_NAME: 'Zwyczaje',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'water_closet': {
                FIELD_SYMBOL: '🚾',
                FIELD_NAME: 'Szafa na wodę',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'wheelchair_symbol': {
                FIELD_SYMBOL: '♿',
                FIELD_NAME: 'Symbol wózka inwalidzkiego',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
        },
        ALPHANUMERIC_SIGNS: {
            'squared_id': {
                FIELD_SYMBOL: '🆔',
                FIELD_NAME: 'Kwadratowy Id',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'circled_ideograph_accept': {
                FIELD_SYMBOL: '🉑',
                FIELD_NAME: 'Okrągły Ideogram Zaakceptuj',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'squared_cjk_unified_ideograph_6709': {
                FIELD_SYMBOL: '🈶',
                FIELD_NAME: 'Ujednolicony ideogram CJK do kwadratu-6709',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'squared_cjk_unified_ideograph_7121': {
                FIELD_SYMBOL: '🈚️',
                FIELD_NAME: 'Ujednolicony ideogram CJK do kwadratu-7121',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'squared_cjk_unified_ideograph_7533': {
                FIELD_SYMBOL: '🈸',
                FIELD_NAME: 'Ujednolicony ideogram CJK do kwadratu-7533',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'squared_cjk_unified_ideograph_55b6': {
                FIELD_SYMBOL: '🈺',
                FIELD_NAME: 'Ujednolicony ideogram CJK do kwadratu-55b6',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'squared_cjk_unified_ideograph_6708': {
                FIELD_SYMBOL: '🈷️',
                FIELD_NAME: 'Ujednolicony ideogram CJK do kwadratu-6708',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'squared_vs': {
                FIELD_SYMBOL: '🆚',
                FIELD_NAME: 'Kwadratowe Vs',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'circled_ideograph_advantage': {
                FIELD_SYMBOL: '🉐',
                FIELD_NAME: 'Zaleta kółka Ideogram',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'circled_ideograph_secret': {
                FIELD_SYMBOL: '㊙️',
                FIELD_NAME: 'Zakreślony Ideogram Secret',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'circled_ideograph_congratulation': {
                FIELD_SYMBOL: '㊗️',
                FIELD_NAME: 'Okrągła Ideogramiczna gratulacje',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'squared_cjk_unified_ideograph_5408': {
                FIELD_SYMBOL: '🈴',
                FIELD_NAME: 'Ujednolicony ideogram CJK do kwadratu-5408',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'squared_cjk_unified_ideograph_6e80': {
                FIELD_SYMBOL: '🈵',
                FIELD_NAME: 'Ujednolicony ideogram CJK do kwadratu-6e80',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'squared_cjk_unified_ideograph_5272': {
                FIELD_SYMBOL: '🈹',
                FIELD_NAME: 'Ujednolicony ideogram CJK do kwadratu-5272',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'squared_cjk_unified_ideograph_7981': {
                FIELD_SYMBOL: '🈲',
                FIELD_NAME: 'Ujednolicony ideogram CJK do kwadratu-7981',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'negative_squared_latin_capital_letter_a': {
                FIELD_SYMBOL: '🅰️',
                FIELD_NAME: 'Ujemna kwadratowa łacińska litera A',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'negative_squared_latin_capital_letter_b': {
                FIELD_SYMBOL: '🅱️',
                FIELD_NAME: 'Ujemna kwadratowa łacińska litera B',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'negative_squared_ab': {
                FIELD_SYMBOL: '🆎',
                FIELD_NAME: 'Negatywne kwadraty Ab',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'squared_cl': {
                FIELD_SYMBOL: '🆑',
                FIELD_NAME: 'Kwadrat Cl',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'negative_squared_latin_capital_letter_o': {
                FIELD_SYMBOL: '🅾️',
                FIELD_NAME: 'Negatywna kwadratowa łacińska litera O',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'squared_sos': {
                FIELD_SYMBOL: '🆘',
                FIELD_NAME: 'Kwadrat Sos',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'squared_cjk_unified_ideograph_6307': {
                FIELD_SYMBOL: '🈯️',
                FIELD_NAME: 'Ujednolicony ideogram CJK do kwadratu-6307',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'circled_latin_capital_letter_m': {
                FIELD_SYMBOL: 'Ⓜ️',
                FIELD_NAME: 'Zakreślona łacińska litera M',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'negative_squared_latin_capital_letter_p': {
                FIELD_SYMBOL: '🅿️',
                FIELD_NAME: 'Ujemna kwadratowa łacińska litera P',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'squared_cjk_unified_ideograph_7a7a': {
                FIELD_SYMBOL: '🈳',
                FIELD_NAME: 'Ujednolicony ideogram CJK do kwadratu-7a7a',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'squared_katakana_sa': {
                FIELD_SYMBOL: '🈂️',
                FIELD_NAME: 'Kwadratowa Katakana Sa',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'input_symbol_for_symbols': {
                FIELD_SYMBOL: '🔣',
                FIELD_NAME: 'Wprowadź symbol symboli',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'information_source': {
                FIELD_SYMBOL: 'ℹ️',
                FIELD_NAME: 'Źródło informacji',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'input_symbol_for_latin_letters': {
                FIELD_SYMBOL: '🔤',
                FIELD_NAME: 'Wpisz symbol liter łacińskich',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'input_symbol_for_latin_small_letters': {
                FIELD_SYMBOL: '🔡',
                FIELD_NAME: 'Wpisz symbol małych liter łacińskich',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'input_symbol_for_latin_capital_letters': {
                FIELD_SYMBOL: '🔠',
                FIELD_NAME: 'Wpisz symbol łacińskich wielkich liter',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'squared_ng': {
                FIELD_SYMBOL: '🆖',
                FIELD_NAME: 'Kwadrat Ng',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'squared_ok': {
                FIELD_SYMBOL: '🆗',
                FIELD_NAME: 'Kwadrat Ok',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'squared_up_with_exclamation_mark': {
                FIELD_SYMBOL: '🆙',
                FIELD_NAME: 'Squared Up with Exclamation Mark',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'squared_cool': {
                FIELD_SYMBOL: '🆒',
                FIELD_NAME: 'Squared Cool',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'squared_new': {
                FIELD_SYMBOL: '🆕',
                FIELD_NAME: 'Kwadratowy nowy',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'squared_free': {
                FIELD_SYMBOL: '🆓',
                FIELD_NAME: 'Kwadrat wolny',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'trade_mark_sign': {
                FIELD_SYMBOL: '™️',
                FIELD_NAME: 'Znak towarowy',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'copyright_sign': {
                FIELD_SYMBOL: '©️',
                FIELD_NAME: 'Znak praw autorskich',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'registered_sign': {
                FIELD_SYMBOL: '®️',
                FIELD_NAME: 'Zarejestrowany znak',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
        },
        NUMERIC_SIGNS: {
            'digit_zero_with_combining_enclosing_keycap': {
                FIELD_SYMBOL: '0️⃣',
                FIELD_NAME: 'Cyfra zero z combining enclosing klawisz',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'digit_one_with_combining_enclosing_keycap': {
                FIELD_SYMBOL: '1️⃣',
                FIELD_NAME: 'Cyfra one z combining enclosing klawisz',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'digit_two_with_combining_enclosing_keycap': {
                FIELD_SYMBOL: '2️⃣',
                FIELD_NAME: 'Cyfra two z combining enclosing klawisz',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'digit_three_with_combining_enclosing_keycap': {
                FIELD_SYMBOL: '3️⃣',
                FIELD_NAME: 'Cyfra three z combining enclosing klawisz',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'digit_four_with_combining_enclosing_keycap': {
                FIELD_SYMBOL: '4️⃣',
                FIELD_NAME: 'Cyfra four z combining enclosing klawisz',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'digit_five_with_combining_enclosing_keycap': {
                FIELD_SYMBOL: '5️⃣',
                FIELD_NAME: 'Cyfra five z combining enclosing klawisz',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'digit_six_with_combining_enclosing_keycap': {
                FIELD_SYMBOL: '6️⃣',
                FIELD_NAME: 'Cyfra six z combining enclosing klawisz',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'digit_seven_with_combining_enclosing_keycap': {
                FIELD_SYMBOL: '7️⃣',
                FIELD_NAME: 'Cyfra seven z combining enclosing klawisz',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'digit_eight_with_combining_enclosing_keycap': {
                FIELD_SYMBOL: '8️⃣',
                FIELD_NAME: 'Cyfra eight z combining enclosing klawisz',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'digit_nine_with_combining_enclosing_keycap': {
                FIELD_SYMBOL: '9️⃣',
                FIELD_NAME: 'Cyfra nine z combining enclosing klawisz',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'keycap_ten': {
                FIELD_SYMBOL: '🔟',
                FIELD_NAME: 'Klawiatura numer dziesięć',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'input_symbol_for_numbers': {
                FIELD_SYMBOL: '🔢',
                FIELD_NAME: 'Wprowadź symbol liczb',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'number_sign_with_combining_enclosing_keycap': {
                FIELD_SYMBOL: '#️⃣',
                FIELD_NAME: 'Liczba sign z combining enclosing klawisz',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'asterisk_with_combining_enclosing_keycap': {
                FIELD_SYMBOL: '*️⃣',
                FIELD_NAME: 'Asterisk z combining enclosing klawisz',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
        },
        PUNCTUATION_SIGNS: {
            'heavy_exclamation_mark_symbol': {
                FIELD_SYMBOL: '❗️',
                FIELD_NAME: 'Symbol ciężkiego wykrzyknika',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'white_exclamation_mark_ornament': {
                FIELD_SYMBOL: '❕',
                FIELD_NAME: 'Ornament biały wykrzyknik',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'black_question_mark_ornament': {
                FIELD_SYMBOL: '❓',
                FIELD_NAME: 'Czarny ornament ze znakiem zapytania',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'white_question_mark_ornament': {
                FIELD_SYMBOL: '❔',
                FIELD_NAME: 'Biały ornament ze znakiem zapytania',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'double_exclamation_mark': {
                FIELD_SYMBOL: '‼️',
                FIELD_NAME: 'Podwójny wykrzyknik',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'exclamation_question_mark': {
                FIELD_SYMBOL: '⁉️',
                FIELD_NAME: 'Znak zapytania wykrzyknika',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
        },
        GEOMETRIC_SIGNS: {
            'large_red_circle': {
                FIELD_SYMBOL: '🔴',
                FIELD_NAME: 'Duży Czerwony Okrąg',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'large_orange_circle': {
                FIELD_SYMBOL: '🟠',
                FIELD_NAME: 'Duże pomarańczowe koło',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'large_yellow_circle': {
                FIELD_SYMBOL: '🟡',
                FIELD_NAME: 'Duże żółte kółko',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'large_green_circle': {
                FIELD_SYMBOL: '🟢',
                FIELD_NAME: 'Duże zielone kółko',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'large_blue_circle': {
                FIELD_SYMBOL: '🔵',
                FIELD_NAME: 'Duży niebieski okrąg',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'large_purple_circle': {
                FIELD_SYMBOL: '🟣',
                FIELD_NAME: 'Duże fioletowe koło',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'medium_black_circle': {
                FIELD_SYMBOL: '⚫️',
                FIELD_NAME: 'Średni czarny krąg',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'medium_white_circle': {
                FIELD_SYMBOL: '⚪️',
                FIELD_NAME: 'Średni biały okrąg',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'large_brown_circle': {
                FIELD_SYMBOL: '🟤',
                FIELD_NAME: 'Duże brązowe koło',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'up_pointing_red_triangle': {
                FIELD_SYMBOL: '🔺',
                FIELD_NAME: 'Wskazujący czerwony trójkąt',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'down_pointing_red_triangle': {
                FIELD_SYMBOL: '🔻',
                FIELD_NAME: 'Czerwony trójkąt skierowany w dół',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'small_orange_diamond': {
                FIELD_SYMBOL: '🔸',
                FIELD_NAME: 'Mały pomarańczowy diament',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'small_blue_diamond': {
                FIELD_SYMBOL: '🔹',
                FIELD_NAME: 'Mały niebieski diament',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'large_orange_diamond': {
                FIELD_SYMBOL: '🔶',
                FIELD_NAME: 'Duży pomarańczowy diament',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'large_blue_diamond': {
                FIELD_SYMBOL: '🔷',
                FIELD_NAME: 'Duży niebieski diament',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'white_square_button': {
                FIELD_SYMBOL: '🔳',
                FIELD_NAME: 'Przycisk białego kwadratu',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'black_square_button': {
                FIELD_SYMBOL: '🔲',
                FIELD_NAME: 'Przycisk czarny kwadrat',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'black_small_square': {
                FIELD_SYMBOL: '▪️',
                FIELD_NAME: 'Czarny mały kwadrat',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'white_small_square': {
                FIELD_SYMBOL: '▫️',
                FIELD_NAME: 'Biały mały kwadrat',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'black_medium_small_square': {
                FIELD_SYMBOL: '◾️',
                FIELD_NAME: 'Czarny średni mały kwadrat',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'white_medium_small_square': {
                FIELD_SYMBOL: '◽️',
                FIELD_NAME: 'Biały Średni Mały Kwadrat',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'black_medium_square': {
                FIELD_SYMBOL: '◼️',
                FIELD_NAME: 'Czarny średni kwadrat',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'white_medium_square': {
                FIELD_SYMBOL: '◻️',
                FIELD_NAME: 'Biały średni kwadrat',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'large_red_square': {
                FIELD_SYMBOL: '🟥',
                FIELD_NAME: 'Duży czerwony kwadrat',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'large_orange_square': {
                FIELD_SYMBOL: '🟧',
                FIELD_NAME: 'Duży pomarańczowy kwadrat',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'large_yellow_square': {
                FIELD_SYMBOL: '🟨',
                FIELD_NAME: 'Duży żółty kwadrat',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'large_green_square': {
                FIELD_SYMBOL: '🟩',
                FIELD_NAME: 'Duży zielony plac',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'large_blue_square': {
                FIELD_SYMBOL: '🟦',
                FIELD_NAME: 'Duży niebieski kwadrat',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'large_purple_square': {
                FIELD_SYMBOL: '🟪',
                FIELD_NAME: 'Duży fioletowy kwadrat',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'black_large_square': {
                FIELD_SYMBOL: '⬛️',
                FIELD_NAME: 'Czarny duży kwadrat',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'white_large_square': {
                FIELD_SYMBOL: '⬜️',
                FIELD_NAME: 'Biały duży plac',
                FIELD_SUPPORT_COLOR: False,
                FIELD_SUPPORT_SEX: False
            },
            'large_brown_square': {
                FIELD_SYMBOL: '🟫',
                FIELD_NAME: 'Duży brązowy kwadrat',
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

    @classmethod
    def get_group_name(cls, group_key: str) -> str:
        """Returns translated group name for display."""
        return cls.GROUP_TRANSLATIONS.get(group_key, group_key)

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

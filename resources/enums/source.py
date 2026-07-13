from core.enums.enum_str import EnumStr


class Source(EnumStr):
    # https://wiki.openstreetmap.org/wiki/Key:source
    EXTRAPOLATION = 'extrapolation'
    HISTORICAL = 'historical'
    IMAGE = 'image'
    KNOWLEDGE = 'knowledge'
    SURVEY = 'survey'
    VOICE = 'voice'

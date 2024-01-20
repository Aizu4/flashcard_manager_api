from typing import Literal, Optional

from ninja import ModelSchema, Schema

from v1.models import Deck
from v1.schemas.card_schemas import CardSchema
from v1.schemas.tag_schemas import TagSchema


class DeckSimpleSchema(ModelSchema):
    class Config:
        model = Deck
        model_fields = "__all__"


class DeckSchema(ModelSchema):
    card_set: list[CardSchema]
    tag_set: list[TagSchema]

    class Config:
        model = Deck
        model_fields = "__all__"


class DeckPostSchema(Schema):
    name: str
    slug: Optional[str] = None
    front_language_code: Optional[str] = None
    back_language_code: Optional[str] = None


class DeckPatchSchema(Schema):
    name: Optional[str] = None
    slug: Optional[str] = None
    front_language_code: Optional[str] = None
    back_language_code: Optional[str] = None
    public: Optional[bool] = None


class DeckCSVSettingsSchema(Schema):
    separator: Literal[',', ';', '\t', '|']
    quotechar: Literal['\'', '"', '`']
    with_images: Optional[bool] = False

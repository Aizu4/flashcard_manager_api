from ninja import ModelSchema, Schema

from v1.models import Deck
from v1.schemas.card_schemas import CardSchema


class DeckSimpleSchema(ModelSchema):
    class Config:
        model = Deck
        model_fields = "__all__"


class DeckSchema(ModelSchema):
    card_set: list[CardSchema]

    class Config:
        model = Deck
        model_fields = "__all__"


class DeckPostSchema(Schema):
    name: str
    slug: str | None = None
    front_language_code: str | None = None
    back_language_code: str | None = None


class DeckPatchSchema(Schema):
    name: str | None = None
    slug: str | None = None
    front_language_code: str | None = None
    back_language_code: str | None = None

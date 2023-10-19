from typing import Optional

from ninja import ModelSchema, Schema
from pydantic.fields import Undefined

from v1.models import Deck


class DeckSchema(ModelSchema):
    class Config:
        model = Deck
        model_fields = "__all__"


class DeckPostSchema(Schema):
    name: str
    slug: str | Undefined = None


class DeckPatchSchema(Schema):
    name: str | None = None
    slug: str | None = None

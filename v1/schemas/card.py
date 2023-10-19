from ninja import ModelSchema, Schema
from pydantic.fields import Undefined

from v1.models import Card


class CardSchema(ModelSchema):
    class Config:
        model = Card
        model_fields = "__all__"


class CardPostSchema(Schema):
    name: str
    slug: str | Undefined = None


class CardPatchSchema(Schema):
    name: str | None = None
    slug: str | None = None

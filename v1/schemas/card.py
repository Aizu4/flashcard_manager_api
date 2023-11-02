from ninja import ModelSchema, Schema

from v1.models import Card


class CardSchema(ModelSchema):
    class Config:
        model = Card
        model_fields = "__all__"


class CardPostSchema(Schema):
    front: str | None = None
    back: str | None = None
    data: dict | None = None
    notes: str | None = None


class CardPatchSchema(Schema):
    name: str | None = None
    slug: str | None = None

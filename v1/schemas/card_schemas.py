from typing import Optional

from ninja import ModelSchema, Schema

from v1.models import Card
from v1.schemas.tag_schemas import TagSchema


class CardSchema(ModelSchema):
    tags: list[TagSchema]

    class Config:
        model = Card
        model_fields = "__all__"
        model_exclude = ["image"]


class CardPostSchema(Schema):
    front: Optional[str] = None
    back: Optional[str] = None
    data: Optional[dict] = None
    notes: Optional[str] = None
    example_front: Optional[str] = None
    example_back: Optional[str] = None


class CardPatchSchema(Schema):
    front: Optional[str] = None
    back: Optional[str] = None
    data: Optional[dict] = None
    notes: Optional[str] = None
    example_front: Optional[str] = None
    example_back: Optional[str] = None


class CardsFromTextPostSchema(Schema):
    content: str
    generate_translations: Optional[bool] = False
    generate_sentences: Optional[bool] = False

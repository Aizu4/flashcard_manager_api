from typing import Optional

from ninja import ModelSchema, Schema

from v1.models import Tag


class TagSchema(ModelSchema):
    class Config:
        model = Tag
        model_fields = "__all__"


class TagPostSchema(Schema):
    name: str


class TagPatchSchema(Schema):
    name: Optional[str] = None

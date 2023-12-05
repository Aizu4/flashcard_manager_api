from django.contrib.auth.models import User
from django.db import models
from django.db.models import QuerySet

from v1.models import BaseModel
from v1.models.mixins import TimestampMixin, SlugMixin, AccessCheckMixin


class Deck(SlugMixin, TimestampMixin, AccessCheckMixin, BaseModel):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    name = models.CharField(max_length=128)
    public = models.BooleanField(default=False)
    front_language_code = models.CharField(max_length=3, null=True)
    back_language_code = models.CharField(max_length=3, null=True)

    @classmethod
    def editable_by(cls, user: User) -> QuerySet['Deck']:
        if user.is_superuser:
            return cls.objects.all()
        return cls.objects.filter(user=user)

    @classmethod
    def visible_by(cls, user: User) -> QuerySet['Deck']:
        return cls.editable_by(user) | cls.editable_by(user).filter(public=True)

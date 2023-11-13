from django.contrib.auth.models import User
from django.db import models

from v1.models import BaseModel
from v1.models.mixins import TimestampMixin, SlugMixin


class Deck(SlugMixin, TimestampMixin, BaseModel):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    name = models.CharField(max_length=128)
    public = models.BooleanField(default=False)
    front_language_iso = models.CharField(max_length=3, null=True)
    back_language_iso = models.CharField(max_length=3, null=True)

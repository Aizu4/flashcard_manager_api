from django.contrib.auth.models import User
from django.db import models

from v1.models import BaseModel
from v1.models.mixins.slug_mixin import SlugMixin


class Deck(SlugMixin, BaseModel):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    name = models.CharField(max_length=128)
    public = models.BooleanField(default=False)

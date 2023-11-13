from django.contrib.auth.models import User
from django.db import models

from v1.models import BaseModel, Deck
from v1.models.mixins import TimestampMixin


class Card(TimestampMixin, BaseModel):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE)
    front = models.TextField(default='')
    back = models.TextField(default='')
    data = models.JSONField(default=dict)
    notes = models.TextField(default='')
    example = models.TextField(default='')

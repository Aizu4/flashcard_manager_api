from django.db import models

from v1.models import BaseModel, Deck


class Card(BaseModel):
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE)
    front = models.TextField(default='')
    back = models.TextField(default='')
    data = models.JSONField(default=dict)
    notes = models.TextField(default='')

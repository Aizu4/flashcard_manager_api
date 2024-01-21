from django.db import models
from v1.models import BaseModel, Deck, Card


class Tag(BaseModel):
    name = models.CharField(max_length=32)
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE)
    cards = models.ManyToManyField(Card, related_name='tags')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'deck'], name='unique_tag_in_deck')
        ]

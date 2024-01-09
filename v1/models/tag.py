from django.db import models
from v1.models import BaseModel, Deck


class Tag(BaseModel):
    name = models.CharField(max_length=32)
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'deck'], name='unique_tag_in_deck')
        ]

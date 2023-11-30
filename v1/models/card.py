from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver

from v1.models import BaseModel, Deck
from v1.models.mixins import TimestampMixin


class Card(TimestampMixin, BaseModel):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE)
    front = models.TextField(default='')
    back = models.TextField(default='')
    example_front = models.TextField(default='')
    example_back = models.TextField(default='')
    notes = models.TextField(default='')
    image = models.ImageField(upload_to='static/cards/images', null=True, blank=True)


@receiver(post_delete, sender=Card)
def post_delete(instance, **_kwargs):
    if instance.image:
        instance.image.delete()

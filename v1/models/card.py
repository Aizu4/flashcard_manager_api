from django.contrib.auth.models import User
from django.db import models
from django.db.models import QuerySet
from django.db.models.signals import post_delete
from django.dispatch import receiver

from v1.models import BaseModel, Deck
from v1.models.mixins import TimestampMixin, AccessCheckMixin


class Card(TimestampMixin, AccessCheckMixin, BaseModel):
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE)
    front = models.TextField(default='')
    back = models.TextField(default='')
    example_front = models.TextField(default='')
    example_back = models.TextField(default='')
    notes = models.TextField(default='')
    image = models.ImageField(upload_to='static/cards/images', null=True, blank=True)

    @property
    def user(self):
        return self.deck.user

    @property
    def public(self):
        return self.deck.public

    @classmethod
    def ediable_by(cls, user: User) -> QuerySet['Card']:
        if user.is_superuser:
            return cls.objects.all()
        return cls.objects.filter(deck__user=user)

    @classmethod
    def visible_by(cls, user: User) -> QuerySet['Card']:
        return cls.ediable_by(user) | cls.ediable_by(user).filter(deck__public=True)


@receiver(post_delete, sender=Card)
def post_delete(instance, **_kwargs):
    if instance.image:
        instance.image.delete()

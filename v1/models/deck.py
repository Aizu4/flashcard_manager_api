import random

from django.contrib.auth.models import User
from django.db import models
from django.db.models import QuerySet
from django.db.models.signals import pre_save
from django.dispatch import receiver

from v1.models import BaseModel
from v1.models.mixins import TimestampMixin, AccessCheckMixin


def slug_generator(length=8):
    return ''.join(random.choices('123456789abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ', k=length))


class Deck(TimestampMixin, AccessCheckMixin, BaseModel):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    name = models.CharField(max_length=128)
    public = models.BooleanField(default=False)
    front_language_code = models.CharField(max_length=3, null=True)
    back_language_code = models.CharField(max_length=3, null=True)
    slug = models.CharField(max_length=16, unique=True, db_index=True, null=True)

    @classmethod
    def editable_by(cls, user: User | None) -> QuerySet['Deck']:
        if not user:
            return cls.objects.none()
        if user.is_superuser:
            return cls.objects.all()
        return cls.objects.filter(user=user)

    @classmethod
    def visible_by(cls, user: User | None) -> QuerySet['Deck']:
        return cls.editable_by(user) | cls.objects.filter(public=True)


@receiver(pre_save, sender=Deck)
def pre_save_handler(sender: Deck, instance, **_kwargs):
    if not instance.public:
        instance.slug = None

    elif not instance.slug:
        instance.slug = slug_generator()

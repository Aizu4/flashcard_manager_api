import random

from django.db import models


def _slug_generator(length=8):
    return ''.join(random.choices('123456789abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ', k=length))


class SlugMixin(models.Model):
    slug = models.CharField(max_length=16, default=_slug_generator, unique=True, db_index=True)

    class Meta:
        abstract = True

    @staticmethod
    def _slug_generator(length=8):
        return ''.join(random.choices('123456789abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ', k=length))

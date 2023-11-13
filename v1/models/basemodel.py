import uuid

from django.db import models


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True

    def __repr__(self):
        return f"<{str(type(self))[1:-1]}: {self.__dict__}>"

    def __str__(self):
        return f"{str(type(self))[1:-1]}: {self.__dict__}"

    def update(self, **kwargs):
        for attr, val in kwargs.items():
            setattr(self, attr, val)

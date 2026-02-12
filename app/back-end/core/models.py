from django.db import models
import uuid
# Create your models here.


# class UUIDPkMixin:
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4,
#                           editable=False)


class UUIDModel(models.Model,
                # UUIDPkMixin,
                ):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True

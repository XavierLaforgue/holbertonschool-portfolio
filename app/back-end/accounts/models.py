from django.db import models
import uuid

# Create your models here.


class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          editable=False)
    bio = models.TextField(blank=True, null=True, max_length=500)

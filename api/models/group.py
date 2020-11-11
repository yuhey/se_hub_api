from django.db import models
import uuid


class Group(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=64, blank=False)
    url = models.CharField(max_length=256, blank=False)
    domain = models.CharField(max_length=32, blank=True)
    is_company = models.BooleanField(default=True)

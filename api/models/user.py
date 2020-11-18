from django.db import models
import uuid

from api.models.group import Group


class User(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(max_length=64, unique=True)
    password = models.CharField(max_length=64, blank=False, null=False)
    name = models.CharField(max_length=32, blank=True, null=True)
    description = models.CharField(max_length=256, blank=True, null=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)

from django.db import models
import uuid

from api.models.group import Group


class Ad(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    count = models.IntegerField(default=0)

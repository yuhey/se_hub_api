from django.db import models
from django.utils import timezone
import uuid

from api.models.user import User


class Data(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=64)
    file = models.FileField(null=False)
    insert_datetime = models.DateTimeField(default=timezone.now)

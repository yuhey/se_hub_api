from django.db import models
from django.utils import timezone
import uuid

from api.models.user import User


class Disclosure(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=64, blank=False, null=False)
    description = models.CharField(max_length=1024, blank=False)
    kind = models.CharField(max_length=1, blank=False, null=False)
    limit = models.CharField(max_length=1, blank=False, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='file/%Y/%m/%d', null=True)
    is_alarmed = models.BooleanField(default=False)
    is_delete = models.BooleanField(default=False)
    insert_datetime = models.DateTimeField(default=timezone.now)

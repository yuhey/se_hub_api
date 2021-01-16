from django.db import models
from django.utils import timezone
import uuid

from api.models.data import Data
from api.models.user import User


class Disclosure(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=64, blank=False, null=False)
    description = models.CharField(max_length=1024, blank=False)
    kind = models.CharField(max_length=1, blank=False, null=False)
    limit = models.CharField(max_length=1, blank=False, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    data = models.ForeignKey(Data, on_delete=models.SET_NULL, null=True)
    insert_datetime = models.DateTimeField(default=timezone.now)

from django.db import models
from django.utils import timezone
import uuid


class Disclosure(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=64, blank=False, null=False)
    description = models.CharField(max_length=1024, blank=False)
    kind = models.CharField(max_length=1, blank=False, null=False)
    limit = models.CharField(max_length=1, blank=False, null=False)
    user_id = models.UUIDField(null=False, editable=False)
    group_id = models.UUIDField(null=False, editable=False)
    data_id = models.UUIDField(null=False, editable=False)
    insert_datetime = models.DateTimeField(default=timezone.now)

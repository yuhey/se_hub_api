from django.db import models
from django.utils import timezone
import uuid


class Message(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=64, blank=False, null=False)
    description = models.CharField(max_length=1024, blank=False)
    disclosure_id = models.UUIDField(null=False, editable=False)
    user1_id = models.UUIDField(null=False, editable=False)
    user2_id = models.UUIDField(null=False, editable=False)
    data_id = models.UUIDField(null=False, editable=False)
    is_read = models.BooleanField(null=False, default=False)
    insert_datetime = models.DateTimeField(default=timezone.now)

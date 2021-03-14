from django.db import models
from django.utils import timezone
import uuid

from api.models.room import Room
from api.models.user import User


class Message(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.CharField(max_length=1024, blank=True, null=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=False)
    from_user = models.ForeignKey(User, related_name='from_user', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='to_user', on_delete=models.CASCADE)
    file = models.FileField(upload_to='file/%Y/%m/%d', null=True)
    is_read = models.BooleanField(null=False, default=False)
    is_delete = models.BooleanField(default=False)
    insert_datetime = models.DateTimeField(default=timezone.now)

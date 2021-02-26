from django.db import models
from django.utils import timezone
import uuid

from api.models.disclosure import Disclosure
from api.models.user import User


class Message(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=64, blank=True, null=True)
    description = models.CharField(max_length=1024, blank=True, null=True)
    message = models.ForeignKey('self', related_name='origin_message', on_delete=models.CASCADE, null=True)
    disclosure = models.ForeignKey(Disclosure, on_delete=models.CASCADE, null=True)
    from_user = models.ForeignKey(User, related_name='from_user', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='to_user', on_delete=models.CASCADE)
    file = models.FileField(upload_to='file/%Y/%m/%d', null=True)
    is_read = models.BooleanField(null=False, default=False)
    no_read_count = models.IntegerField(default=0)
    is_alarmed = models.BooleanField(default=False)
    is_delete = models.BooleanField(default=False)
    update_user = models.ForeignKey(User, related_name='update_user', on_delete=models.CASCADE)
    insert_datetime = models.DateTimeField(default=timezone.now)
    update_datetime = models.DateTimeField(default=timezone.now)

from django.db import models
from django.utils import timezone
import uuid

from api.models.disclosure import Disclosure
from api.models.user import User


class Room(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=64, blank=True, null=True)
    disclosure = models.ForeignKey(Disclosure, on_delete=models.CASCADE, null=True)
    user1 = models.ForeignKey(User, related_name='user1', on_delete=models.CASCADE)
    user2 = models.ForeignKey(User, related_name='user2', on_delete=models.CASCADE)
    no_read_count = models.IntegerField(default=0)
    is_alarmed = models.BooleanField(default=False)
    is_delete = models.BooleanField(default=False)
    update_user = models.ForeignKey(User, related_name='update_user', on_delete=models.CASCADE, null=True)
    update_datetime = models.DateTimeField(default=timezone.now)

from django.db import models
import uuid

from api.models.user import User


class Bp(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    follow_group = models.ForeignKey(User, related_name='follow_group', on_delete=models.CASCADE)
    followed_group = models.ForeignKey(User, related_name='followed_group', on_delete=models.CASCADE)

from django.db import models
import uuid

from api.models import User


class Bp(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    follow = models.ForeignKey(User, related_name='follow', on_delete=models.CASCADE)
    followed = models.ForeignKey(User, related_name='followed', on_delete=models.CASCADE)

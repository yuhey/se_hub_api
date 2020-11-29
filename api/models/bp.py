from django.db import models
import uuid

from api.models.group import Group


class Bp(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    follow = models.ForeignKey(Group, related_name='follow', on_delete=models.CASCADE)
    followed = models.ForeignKey(Group, related_name='followed', on_delete=models.CASCADE)

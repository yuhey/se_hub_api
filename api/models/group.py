from django.db import models
import uuid


class Group(models.Model):

    class Meta:
        db_table = 'group'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=64, blank=True, null=True)
    description = models.CharField(max_length=256, blank=True, null=True)
    url = models.CharField(max_length=256, blank=True, null=True)
    domain = models.CharField(max_length=32, blank=True, null=True)
    img = models.ImageField(upload_to='img/', null=True)

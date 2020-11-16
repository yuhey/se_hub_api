from django.db import models
from django.utils import timezone
import uuid


class Bp(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    group1_id = models.UUIDField(null=False, editable=False)
    group2_id = models.UUIDField(null=False, editable=False)

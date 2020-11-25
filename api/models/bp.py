from django.db import models
import uuid

from api.models.company import Company


class Bp(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    follow_company = models.ForeignKey(Company, related_name='follow', on_delete=models.CASCADE)
    followed_company = models.ForeignKey(Company, related_name='followed', on_delete=models.CASCADE)

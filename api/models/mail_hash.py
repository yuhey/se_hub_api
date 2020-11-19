from django.db import models


class MailHash(models.Model):

    class Meta:
        db_table = 'mail_hash'

    email = models.EmailField(max_length=64, unique=True)
    hash_cd = models.TextField(max_length=32, null=False, blank=False)

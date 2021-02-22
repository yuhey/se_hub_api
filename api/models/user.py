from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
import uuid

from django.utils.translation import ugettext_lazy as _

from api.models.group import Group


class CustomUserManager(BaseUserManager):

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):

        if not email:
            raise ValueError('The given email must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):

        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(_('email address'), unique=True)
    name = models.CharField(_('user name'), max_length=32, null=True, blank=True)
    description = models.CharField(max_length=256, blank=True, null=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='company', null=True)
    img = models.ImageField(upload_to='img/', null=True)
    should_send_message = models.BooleanField(default=True)
    should_send_bp = models.BooleanField(default=True)
    can_find_name = models.BooleanField(default=False)
    key = models.UUIDField(default=uuid.uuid4, editable=False)
    is_freeze = models.BooleanField(default=False)
    is_delete = models.BooleanField(default=False)
    # default
    is_staff = models.BooleanField(_('staff status'), default=False)
    is_active = models.BooleanField(_('active'), default=True)
    username = None
    first_name = None
    last_name = None

    objects = CustomUserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

from django.contrib import admin

from .models.user import User
from .models.group import Group


admin.site.register(User)
admin.site.register(Group)

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django import forms

from django.utils.translation import ugettext_lazy as _

from .models.bp import Bp
from .models.data import Data
from .models.disclosure import Disclosure
from .models.message import Message
from .models.user import User
from .models.group import Group


class MyUserAdmin(UserAdmin):
    ordering = ('email',)


admin.site.register(Bp)
admin.site.register(Data)
admin.site.register(Disclosure)
admin.site.register(Group)
admin.site.register(Message)
admin.site.register(User, MyUserAdmin)

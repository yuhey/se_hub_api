from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group as GroupAdmin

from .models.ad import Ad
from .models.bp import Bp
from .models.data import Data
from .models.disclosure import Disclosure
from .models.mail_hash import MailHash
from .models.message import Message
from .models.user import User
from .models.group import Group


class MyUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password', )}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password'),
        }),
    )
    list_display = ('id', 'name', 'email',)
    list_filter = ('email',)
    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(Ad)
admin.site.register(Bp)
admin.site.register(Data)
admin.site.register(Disclosure)
admin.site.unregister(GroupAdmin)
admin.site.register(Group)
admin.site.register(MailHash)
admin.site.register(Message)
admin.site.register(User, MyUserAdmin)

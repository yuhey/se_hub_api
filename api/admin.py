from django.contrib import admin

from .models.bp import Bp
from .models.data import Data
from .models.disclosure import Disclosure
from .models.message import Message
from .models.user import User
from .models.group import Group


admin.site.register(Bp)
admin.site.register(Data)
admin.site.register(Disclosure)
admin.site.register(Group)
admin.site.register(Message)
admin.site.register(User)

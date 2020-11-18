from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include

import api


urlpatterns = [
    path('admin/', admin.site.urls),
    url('api/', include('api.urls')),
]

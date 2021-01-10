from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include

from se_hub_api import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    url('api/', include('api.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

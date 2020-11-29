from django.conf.urls import url
from django.urls import path

from api.views.bp import BpAPI
from api.views.group import GroupAPI
from api.views.user import UserAPI

from rest_framework_jwt.views import obtain_jwt_token


urlpatterns = [
    url(r'^auth', obtain_jwt_token),
    path('user/', UserAPI.as_view(), name='user'),
    path('group/', GroupAPI.as_view(), name='group'),
    path('bp/', BpAPI.as_view(), name='bp'),
]

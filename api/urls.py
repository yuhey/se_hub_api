from django.conf.urls import url
from django.urls import include, path
from rest_framework import routers

from api.views.bp import BpViewSet
from api.views.data import DataViewSet
from api.views.disclosure import DisclosureViewSet
from api.views.message import MessageViewSet
from api.views.user import UserAPI


urlpatterns = [
    path('user/', UserAPI.as_view(), name='user'),
]

from django.conf.urls import url
from django.urls import path

from api.views.bp import BpAPI
from api.views.disclosure import DisclosureAPI
from api.views.group import GroupAPI
from api.views.message.list import MessageListAPI
from api.views.message.message import MessageAPI
from api.views.user import UserAPI

from rest_framework_jwt.views import obtain_jwt_token


urlpatterns = [
    url(r'^auth', obtain_jwt_token),
    path('user/', UserAPI.as_view()),
    path('user/<uuid:user_id>/', UserAPI.as_view()),
    path('group/', GroupAPI.as_view(), name='group'),
    path('bp/', BpAPI.as_view(), name='bp'),
    path('disclosure/', DisclosureAPI.as_view(), name='disclosure'),
    path('message/', MessageAPI.as_view(), name='message'),
    path('message/list/', MessageListAPI.as_view(), name='message_list'),
]

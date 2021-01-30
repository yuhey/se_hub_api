from django.conf.urls import url
from django.urls import path

#from api.views.ad.ad import AdAPI
from api.views.bp.bp import BpAPI
from api.views.bp.list import BpListAPI
from api.views.disclosure.disclosure import DisclosureAPI
from api.views.disclosure.list import DisclosureListAPI
from api.views.group.group import GroupAPI
from api.views.group.image import GroupImageAPI
from api.views.message.list import MessageListAPI
from api.views.message.message import MessageAPI
from api.views.user.hash import HashAPI
from api.views.user.image import UserImageAPI
from api.views.user.user import UserAPI

from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    url(r'^auth', obtain_jwt_token),
    path('user/', UserAPI.as_view()),
    path('user/<uuid:user_id>/', UserAPI.as_view()),
    path('user/hash/', HashAPI.as_view()),
    path('user/img/<uuid:user_id>/', UserImageAPI.as_view()),
    path('group/<uuid:group_id>/', GroupAPI.as_view()),
    path('group/img/<uuid:group_id>/', GroupImageAPI.as_view()),
    path('bp/', BpAPI.as_view()),
    path('bp/<uuid:user_id>/', BpAPI.as_view()),
    path('bp/<uuid:user_id>/<uuid:other_id>/', BpAPI.as_view()),
    path('bp/list/<uuid:user_id>/', BpListAPI.as_view()),
    path('disclosure/', DisclosureAPI.as_view()),
    path('disclosure/<uuid:disclosure_id>/', DisclosureAPI.as_view()),
    path('disclosure/list/', DisclosureListAPI.as_view()),
    path('disclosure/list/<uuid:other_id>/', DisclosureListAPI.as_view()),
    path('message/', MessageAPI.as_view()),
    path('message/<uuid:message_id>/<str:count>/', MessageAPI.as_view()),
    path('message/list/<uuid:user_id>/<str:count>/', MessageListAPI.as_view()),
    #path('ad/', AdAPI.as_view()),
    #path('ad/<str:count>/', AdAPI.as_view()),
    #path('ad/<uuid:ad_id>/', AdAPI.as_view()),
]

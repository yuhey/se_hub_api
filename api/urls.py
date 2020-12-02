from django.conf.urls import url
from django.urls import path

from api.views.bp.bp import BpAPI
from api.views.bp.list import BpListAPI
from api.views.disclosure.disclosure import DisclosureAPI
from api.views.disclosure.list import DisclosureListAPI
from api.views.group.group import GroupAPI
from api.views.message.list import MessageListAPI
from api.views.message.message import MessageAPI
from api.views.user.user import UserAPI

from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    url(r'^auth', obtain_jwt_token),
    path('user/', UserAPI.as_view()),
    path('user/<uuid:user_id>/', UserAPI.as_view()),
    path('group/<uuid:group_id>/', GroupAPI.as_view()),
    path('bp/', BpAPI.as_view()),
    path('bp/<uuid:follow_id>/', BpAPI.as_view()),
    path('bp/<uuid:follow_id>/<uuid:followed_id>', BpAPI.as_view()),
    path('bp/list/<uuid:group_id>/', BpListAPI.as_view()),
    path('disclosure/', DisclosureAPI.as_view()),
    path('disclosure/<uuid:disclosure_id>/', DisclosureAPI.as_view()),
    path('disclosure/list/<uuid:viewer_id>/<str:kind>/<str:count>/', DisclosureListAPI.as_view()),
    path('disclosure/list/<uuid:viewer_id>/<uuid:user_id>/<str:kind>/<str:count>/', DisclosureListAPI.as_view()),
    path('message/', MessageAPI.as_view()),
    path('message/<uuid:message_id>/<str:count>/', MessageAPI.as_view()),
    path('message/list/<uuid:user_id>/<str:count>/', MessageListAPI.as_view()),
]

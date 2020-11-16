from rest_framework import routers

from api.views.bp import BpViewSet
from api.views.data import DataViewSet
from api.views.disclosure import DisclosureViewSet
from api.views.message import MessageViewSet
from api.views.user import UserViewSet


router = routers.DefaultRouter()
router.register(r'bp', BpViewSet)
router.register(r'data', DataViewSet)
router.register(r'disclosure', DisclosureViewSet)
router.register(r'message', MessageViewSet)
router.register(r'user', UserViewSet)

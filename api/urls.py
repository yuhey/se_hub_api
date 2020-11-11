from rest_framework import routers
from api.views.user import UserViewSet


router = routers.DefaultRouter()
router.register(r'user', UserViewSet)

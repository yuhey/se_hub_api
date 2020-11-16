from rest_framework import generics, status, viewsets
from rest_framework.response import Response

from api.models.bp import Bp
from api.models.user import User
from api.serializers.bp import BpSerializer
from api.serializers.user import UserSerializer


class BpViewSet(viewsets.ModelViewSet):

    queryset = Bp.objects.all()
    serializer_class = BpSerializer

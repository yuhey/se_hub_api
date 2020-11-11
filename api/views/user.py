from rest_framework import generics, status, viewsets
from rest_framework.response import Response

from api.models.user import User
from api.serializers.user import UserSerializer


class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer

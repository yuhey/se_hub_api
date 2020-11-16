from rest_framework import generics, status, viewsets
from rest_framework.response import Response

from api.models.bp import Bp
from api.models.data import Data
from api.models.disclosure import Disclosure
from api.models.user import User
from api.serializers.bp import BpSerializer
from api.serializers.data import DataSerializer
from api.serializers.disclosure import DisclosureSerializer
from api.serializers.user import UserSerializer


class DisclosureViewSet(viewsets.ModelViewSet):

    queryset = Disclosure.objects.all()
    serializer_class = DisclosureSerializer

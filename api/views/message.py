from rest_framework import generics, status, viewsets
from rest_framework.response import Response

from api.models.bp import Bp
from api.models.data import Data
from api.models.message import Message
from api.models.user import User
from api.serializers.bp import BpSerializer
from api.serializers.data import DataSerializer
from api.serializers.message import MessageSerializer
from api.serializers.user import UserSerializer


class MessageViewSet(viewsets.ModelViewSet):

    queryset = Message.objects.all()
    serializer_class = MessageSerializer

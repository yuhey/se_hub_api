import json

from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models.disclosure import Disclosure
from api.models.message import Message
from api.models.user import User
from api.utils import utils
from api.utils.number import MESSAGE_COUNT


class MessageAPI(APIView):

    @staticmethod
    def get(request, message_id, count):

        message_qs = Message.objects.filter(Q(id=message_id) | Q(message__id=message_id)).order_by('insert_datetime')
        message_qs = utils.get_qs_for_count(message_qs, count, MESSAGE_COUNT)

        return Response(message_qs.values(), status=status.HTTP_200_OK)

    @staticmethod
    def post(request):

        # リクエストボディ取得
        request_data = json.loads(request.body.decode('utf-8'))
        title = request_data.get('title')
        description = request_data.get('description')
        message_id = request_data.get('message_id')
        disclosure_id = request_data.get('disclosure_id')
        from_id = request_data.get('user_id')
        to_id = request_data.get('other_id')

        if not description or not from_id or not to_id:
            return Response([], status=status.HTTP_400_BAD_REQUEST)

        if not User.objects.filter(id=from_id).exists():
            return Response([], status=status.HTTP_400_BAD_REQUEST)
        if not User.objects.filter(id=to_id).exists():
            return Response([], status=status.HTTP_400_BAD_REQUEST)

        from_user = User.objects.get(id=from_id)
        to_user = User.objects.get(id=to_id)
        if not from_user or not to_user:
            return Response([], status=status.HTTP_400_BAD_REQUEST)

        origin_message = None
        if message_id:
            origin_message = Message.objects.filter(id=message_id).first()

        disclosure = None
        if disclosure_id:
            disclosure = Disclosure.objects.filter(id=disclosure_id).first()

        message = Message(
            title=title,
            description=description,
            message=origin_message,
            disclosure=disclosure,
            from_user=from_user,
            to_user=to_user,
        )
        message.save()

        return Response([], status=status.HTTP_200_OK)

import json

from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models.disclosure import Disclosure
from api.models.message import Message
from api.models.user import User


class MessageListAPI(APIView):

    MESSAGE_COUNT = 20

    def get(self, request, *args, **kwargs):

        # クエリパラメータを取得
        user_id = self.request.query_params.get('id')
        count = self.request.query_params.get('count')

        if not user_id or not count:
            return Response([], status=status.HTTP_400_BAD_REQUEST)

        message_qs = Message.objects.filter(
            (Q(from_user__id=user_id) | Q(to_user__id=user_id)) & Q(message__isnull=False)).order_by('insert_datetime')
        max_count = message_qs.count()
        if max_count > self.MESSAGE_COUNT:
            start_count = max_count - (count * self.MESSAGE_COUNT)
            if start_count < 0:
                start_count = 0
            end_count = max_count - ((count - 1) * self.MESSAGE_COUNT)
            message_qs = message_qs[start_count:end_count]

        return Response(message_qs.values(), status=status.HTTP_200_OK)

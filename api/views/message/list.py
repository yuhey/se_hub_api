import json

from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models.message import Message
from api.utils import utils
from api.utils.number import MESSAGE_TITLE_COUNT


class MessageListAPI(APIView):

    @staticmethod
    def post(request, user_id):
        # リクエストボディ取得
        request_data = json.loads(request.body.decode('utf-8'))
        count = request_data.get('count')

        message_qs = Message.objects.filter(
            (Q(from_user__id=user_id) | Q(to_user__id=user_id)) & Q(message__isnull=True)).order_by('insert_datetime')
        message_qs = utils.get_qs_for_count(message_qs, count, MESSAGE_TITLE_COUNT)

        return Response(message_qs.values('id', 'title', 'description', 'from_user__img', 'from_user__name',
                                          'from_user__group__name'), status=status.HTTP_200_OK)

import json

from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import User
from api.models.message import Message
from api.utils import utils
from api.utils.number import MESSAGE_TITLE_COUNT


class MessageListAPI(APIView):

    @staticmethod
    def post(request, user_id):
        # リクエストボディ取得
        request_data = json.loads(request.body.decode('utf-8'))
        count = request_data.get('count')

        message_qs = Message.objects \
            .filter(message__isnull=True) \
            .filter(Q(from_user__id=user_id)
                    | Q(to_user__id=user_id))

        # ブロックユーザーのメッセージを除外する
        user_qs = User.objects.filter(id=user_id)
        if not user_qs:
            return Response([], status=status.HTTP_400_BAD_REQUEST)
        user = user_qs.first()
        if user.block_user_csv:
            block_user_list = user.block_user_csv.split(',')
            if block_user_list:
                message_qs = message_qs\
                    .exclude(from_user__id__in=block_user_list) \
                    .exclude(to_user__id__in=block_user_list)

        message_qs.order_by('-update_datetime')
        message_qs = utils.get_qs_for_count(message_qs, count, MESSAGE_TITLE_COUNT)

        return Response(message_qs.values('id', 'title', 'description', 'from_user__id', 'from_user__img',
                                          'from_user__name', 'from_user__group__name', 'to_user__id', 'to_user__img',
                                          'to_user__name', 'to_user__group__name', 'no_read_count', 'update_user'),
                        status=status.HTTP_200_OK)

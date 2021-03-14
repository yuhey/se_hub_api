import json

from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import User
from api.models.room import Room
from api.utils import utils
from api.utils.number import MESSAGE_TITLE_COUNT


class MessageListAPI(APIView):

    @staticmethod
    def post(request, user_id):
        # リクエストボディ取得
        request_data = json.loads(request.body.decode('utf-8'))
        count = request_data.get('count')

        room_qs = Room.objects.filter(Q(user1__id=user_id) | Q(user2__id=user_id))

        # ブロックユーザーのメッセージを除外する
        user_qs = User.objects.filter(id=user_id)
        if not user_qs:
            return Response([], status=status.HTTP_400_BAD_REQUEST)
        user = user_qs.first()
        if user.block_user_csv:
            block_user_list = user.block_user_csv.split(',')
            if block_user_list:
                room_qs = room_qs \
                    .exclude(user1__id__in=block_user_list) \
                    .exclude(user2__id__in=block_user_list)

        room_qs.order_by('-update_datetime')
        room_qs = utils.get_qs_for_count(room_qs, count, MESSAGE_TITLE_COUNT)

        return Response(room_qs.values('id', 'title', 'user1__id', 'user1__img', 'user1__name',
                                       'user1__group__name', 'user2__id', 'user2__img', 'user2__name',
                                       'user2__group__name', 'no_read_count', 'update_user', 'update_datetime',
                                       'disclosure__id', 'disclosure__title', 'disclosure__description')
                        .order_by('-update_datetime'), status=status.HTTP_200_OK)

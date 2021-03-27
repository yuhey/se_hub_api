from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import User
from api.models.room import Room


class MessageNoticeAPI(APIView):

    @staticmethod
    def get(request, user_id):

        message_count = 0

        room_qs = Room.objects.filter(Q(user1__id=user_id) | Q(user2__id=user_id)).exclude(update_user__id=user_id)

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

        for room in room_qs:
            message_count += room.no_read_count

        notice_dict = {
            'message_count': message_count,
        }

        return Response(notice_dict, status=status.HTTP_200_OK)

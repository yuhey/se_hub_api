import json

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from api.models.user import User
from api.utils.status import SHOULD_SEND_MESSAGE, SHOULD_SEND_BP, CAN_FIND_NAME


class UserSettingsAPI(APIView):

    @staticmethod
    def put(request, user_id):

        # リクエストボディ取得
        request_data = json.loads(request.body.decode('utf-8'))
        kind = request_data.get('kind')
        is_enable = request_data.get('is_enable')

        user_qs = User.objects.filter(id=user_id)
        if user_qs:
            user = user_qs.first()
            if kind == SHOULD_SEND_MESSAGE:
                user.should_send_message = is_enable
            elif kind == SHOULD_SEND_BP:
                user.should_send_bp = is_enable
            elif kind == CAN_FIND_NAME:
                user.can_find_name = is_enable
            user.save()

        return Response([], status=status.HTTP_200_OK)

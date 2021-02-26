from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response

from api.models.disclosure import Disclosure
from api.models.message import Message


class MessageAlarmAPI(APIView):

    def get_permissions(self):
        if self.request.method == 'PUT':
            self.permission_classes = (AllowAny,)
        return super(MessageAlarmAPI, self).get_permissions()

    @staticmethod
    def put(request, message_id):

        message_qs = Message.objects.filter(id=message_id)
        if not message_qs:
            return Response({'error_message': '通報対象のメッセージが存在しません。'},
                            status=status.HTTP_204_NO_CONTENT)

        message = message_qs.first()
        message.is_alarmed = True
        message.save()

        return Response([], status=status.HTTP_200_OK)

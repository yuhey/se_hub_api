from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response

from api.models.room import Room


class MessageAlarmAPI(APIView):

    def get_permissions(self):
        if self.request.method == 'PUT':
            self.permission_classes = (AllowAny,)
        return super(MessageAlarmAPI, self).get_permissions()

    @staticmethod
    def put(request, room_id):

        room_qs = Room.objects.filter(id=room_id)
        if not room_qs:
            return Response({'error_message': '通報対象のトークルームが存在しません。'}, status=status.HTTP_204_NO_CONTENT)

        room = room_qs.first()
        room.is_alarmed = True
        room.save()

        return Response([], status=status.HTTP_200_OK)

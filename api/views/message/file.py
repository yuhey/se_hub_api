import os

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from api.models.message import Message


class MessageFileAPI(APIView):

    @staticmethod
    def put(request, message_id):

        # ファイル取得
        file = request.FILES.get('file')

        if not file:
            return Response([], status=status.HTTP_204_NO_CONTENT)

        # メッセージ情報を更新する
        message = Message.objects.filter(id=message_id).first()
        if not message:
            return Response([], status=status.HTTP_204_NO_CONTENT)
        message.file = file
        message.save()

        return Response([], status=status.HTTP_200_OK)

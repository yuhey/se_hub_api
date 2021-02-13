import os

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from api.models.disclosure import Disclosure
from api.models.message import Message


class DisclosureFileAPI(APIView):

    @staticmethod
    def put(request, message_id):

        # ファイル取得
        file = request.FILES.get('file')

        if not file:
            return Response([], status=status.HTTP_204_NO_CONTENT)

        # メッセージ情報を更新する
        disclosure = Disclosure.objects.filter(id=message_id).first()
        if not disclosure:
            return Response([], status=status.HTTP_204_NO_CONTENT)
        disclosure.file = file
        disclosure.save()

        return Response([], status=status.HTTP_200_OK)

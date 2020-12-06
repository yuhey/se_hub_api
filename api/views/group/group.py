import json

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from api.models.group import Group


class GroupAPI(APIView):

    @staticmethod
    def put(request, group_id):

        # リクエストボディ取得
        request_data = json.loads(request.body.decode('utf-8'))
        name = request_data.get('name')
        description = request_data.get('description')
        url = request_data.get('url')
        img = request_data.get('img')

        # 法人グループ情報を更新する
        group = Group.objects.filter(id=group_id).first()
        if not group:
            return Response([], status=status.HTTP_400_BAD_REQUEST)
        group.name = name
        group.description = description
        group.url = url
        group.img = img
        group.save()

        return Response([], status=status.HTTP_200_OK)

    @staticmethod
    def delete(request, group_id):

        # 法人グループを削除する
        group = Group.objects.filter(id=group_id).first()
        if not group:
            return Response([], status=status.HTTP_400_BAD_REQUEST)
        group.delete()

        return Response([], status=status.HTTP_200_OK)
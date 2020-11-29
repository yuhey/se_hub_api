import json

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from api.models.group import Group


class GroupAPI(APIView):

    def put(self, request, *args, **kwargs):

        # クエリパラメータ取得
        group_id = self.request.query_params.get('id')
        if not group_id:
            return Response([], status=status.HTTP_400_BAD_REQUEST)

        # リクエストボディ取得
        request_data = json.loads(self.request.body)
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

    def delete(self, request, *args, **kwargs):

        # クエリパラメータ取得
        group_id = self.request.query_params.get('id')
        if not group_id:
            return Response([], status=status.HTTP_400_BAD_REQUEST)

        # 法人グループを削除する
        group = Group.objects.filter(id=group_id).first()
        if not group:
            return Response([], status=status.HTTP_400_BAD_REQUEST)
        group.delete()

        return Response([], status=status.HTTP_200_OK)

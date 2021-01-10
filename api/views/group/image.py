from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from api.models.group import Group


class GroupImageAPI(APIView):

    @staticmethod
    def put(request, group_id):

        # グループ画像取得
        img = request.files.get('group_img')

        # 法人グループ情報を更新する
        group = Group.objects.filter(id=group_id).first()
        if not group:
            return Response([], status=status.HTTP_204_NO_CONTENT)
        group.img = img
        group.save()

        return Response([], status=status.HTTP_200_OK)

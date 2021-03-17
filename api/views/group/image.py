import os

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from api.models.group import Group
from se_hub_api import settings


class GroupImageAPI(APIView):

    @staticmethod
    def put(request, group_id):

        # グループ画像取得
        img = request.FILES.get('group_img')

        # グループ画像のパスを作成
        GROUP_IMAGE_PATH = os.path.join(settings.BASE_DIR, 'media', 'img', img.name)
        # グループ画像を削除する
        if os.path.isfile(GROUP_IMAGE_PATH):
            os.remove(GROUP_IMAGE_PATH)

        # 法人グループ情報を更新する
        group = Group.objects.filter(id=group_id).first()
        if not group:
            return Response({'message': '該当の法人情報は存在しません'}, status=status.HTTP_204_NO_CONTENT)
        group.img = img
        group.save()

        return Response([], status=status.HTTP_200_OK)

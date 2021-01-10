import os

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from api.models.user import User
from se_hub_api import settings


class UserImageAPI(APIView):

    @staticmethod
    def put(request, user_id):

        # ユーザー画像取得
        img = request.FILES.get('user_img')

        if not img:
            return Response([], status=status.HTTP_204_NO_CONTENT)

        # ユーザー画像のパスを作成
        USER_IMAGE_PATH = os.path.join(settings.BASE_DIR, 'media', 'img', img.name)
        print(USER_IMAGE_PATH)

        # ユーザー画像を削除する
        if os.path.isfile(USER_IMAGE_PATH):
            os.remove(USER_IMAGE_PATH)

        # ユーザー情報を更新する
        user = User.objects.filter(id=user_id).first()
        if not user:
            return Response([], status=status.HTTP_204_NO_CONTENT)
        user.img = img
        user.save()

        return Response([], status=status.HTTP_200_OK)

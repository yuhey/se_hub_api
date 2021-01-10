from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from api.models.user import User


class UserImageAPI(APIView):

    @staticmethod
    def put(request, user_id):

        # ユーザー画像取得
        img = request.files.get('user_img')

        # ユーザー情報を更新する
        user = User.objects.filter(id=user_id).first()
        if not user:
            return Response([], status=status.HTTP_204_NO_CONTENT)
        user.img = img
        user.save()

        return Response([], status=status.HTTP_200_OK)

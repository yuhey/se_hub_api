import json

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models.mail_hash import MailHash
from api.utils.hash import create_hash


class UserHashAPI(APIView):

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = (AllowAny,)
        return super(UserHashAPI, self).get_permissions()

    @staticmethod
    def post(request):

        # リクエストボディ取得
        request_data = json.loads(request.body.decode('utf-8'))
        email = request_data.get('email')

        if not email:
            return Response([], status=status.HTTP_400_BAD_REQUEST)

        # メールハッシュを登録する
        mail_hash = MailHash(
            email=email,
            hash_cd=create_hash(),
        )
        mail_hash.save()

        return Response([], status=status.HTTP_200_OK)

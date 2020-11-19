from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from api.models.mail_hash import MailHash
from api.utils.hash import create_hash


class AuthAPI(APIView):

    #
    # E-Mail が有効か判断するためのハッシュ値を生成し、
    # E-Mailに紐づける
    #
    def post(self):

        email = self.request.POST.get('email')

        if not email:
            return Response([], status=status.HTTP_400_BAD_REQUEST)

        # 32桁数字(ハッシュ値)を作成
        hash_cd = create_hash(length=32)

        # メールアドレスが既にハッシュ値を持っている場合(削除)
        mail_hash = MailHash.objects.filter(email=email)
        if mail_hash.exists():
            mail_hash.delete()

        # メールアドレスとハッシュ値を登録
        mail_hash = MailHash(
            email=email,
            hash_cd=hash_cd,
        )
        mail_hash.save()

        # メール送信処理
        # TODO メール送信処理

        return Response([], status=status.HTTP_201_CREATED)

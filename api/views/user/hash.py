import json

from django.core.mail import send_mail
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models.mail_hash import MailHash
from api.utils.hash import create_hash


class HashAPI(APIView):

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = (AllowAny,)
        return super(HashAPI, self).get_permissions()

    @staticmethod
    def post(request):

        # リクエストボディ取得
        request_data = json.loads(request.body.decode('utf-8'))
        email = request_data.get('email')

        if not email:
            return Response({'message': 'Eメールアドレスが存在しません'}, status=status.HTTP_400_BAD_REQUEST)

        mail_hash = MailHash.objects.filter(email=email).first()

        # メールハッシュが登録されていない場合（新規登録）
        if not mail_hash:
            # メールハッシュを登録する
            mail_hash = MailHash(
                email=email,
                hash_cd=create_hash(),
            )
            mail_hash.save()
        # メールハッシュが既に登録されている場合（更新）
        else:
            mail_hash.hash_cd = create_hash()
            mail_hash.save()

        # 登録メールアドレス宛に、確認コードを添付したメールを送信する
        hash_cd = mail_hash.hash_cd
        signature = '//TODO SE-Hub署名'
        message = f'''
            SE-Hubの登録完了用の確認コードを送付いたします。

            確認コード: {hash_cd}
            
            {signature}
        '''
        send_mail(
            subject='【SE-Hub】登録完了用確認コードのご連絡',
            message=message,
            from_email='info@se-hub.jp',
            recipient_list=[email]
        )

        return Response([], status=status.HTTP_200_OK)

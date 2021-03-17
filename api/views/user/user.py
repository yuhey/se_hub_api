import json

from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response

from api.models.group import Group
from api.models.mail_hash import MailHash
from api.models.user import User


class UserAPI(APIView):

    def get_permissions(self):
        if self.request.method == 'GET' \
                or self.request.method == 'POST':
            self.permission_classes = (AllowAny,)
        return super(UserAPI, self).get_permissions()

    @staticmethod
    def get(request, user_id):

        user_qs = User.objects \
            .filter(id=user_id) \
            .filter(is_delete=False)

        if not user_qs.exists():
            return Response({'message': '該当のユーザーは存在しません'}, status=status.HTTP_204_NO_CONTENT)

        return Response(
            user_qs.first().values('id', 'name', 'email', 'description', 'img', 'key', 'should_send_message',
                                   'should_send_bp', 'can_find_name', 'group__id', 'group__name', 'group__description',
                                   'group__url', 'group__img'),
            status=status.HTTP_200_OK)

    @staticmethod
    def post(request):

        # リクエストボディ取得
        request_data = json.loads(request.body.decode('utf-8'))
        name = request_data.get('name')
        email = request_data.get('email')
        password = request_data.get('password')
        hash_cd = request_data.get('hash_cd')

        if not email or not password or not hash_cd:
            return Response({'message': '登録に必要なデータが足りていません'}, status=status.HTTP_400_BAD_REQUEST)

        hash_qs = MailHash.objects.filter(email=email, hash_cd=hash_cd)
        if not hash_qs.exists():
            # メールアドレスに紐づくハッシュコードを削除する
            hash_qs = MailHash.objects.filter(email=email)
            hash_qs.delete()
            return Response({'errorMessage': '確認コード違います。\nお手数をお掛けしますが、「登録情報入力」からやり直してください。'},
                            status=status.HTTP_400_BAD_REQUEST)

        # ハッシュを削除する
        hash_qs.delete()

        # メールアドレスからドメインを取得する
        domain = email.split('@')[-1]

        # ドメインから法人グループを取得
        group = Group.objects.filter(domain=domain).first()

        # 法人グループとして登録されている場合
        if group:
            group = Group.objects.get(domain=domain)
        # 法人グループとして登録されていない場合
        else:
            unit = domain.split('.')
            # co.jpドメインでない場合は、ドメインをNoneにしてグループを作成する
            # ドメインが入っているグループ(co.jp)は、法人グループとして扱う
            if len(unit) < 3 or unit[-2] != 'co' or unit[-1] != 'jp':
                domain = None
            group = Group(
                domain=domain,
            )
            group.save()

        user_qs = User.objects.filter(email=email)
        # 過去に一度でも登録されたメールアドレスの場合
        if user_qs:
            user = user_qs.first()
            # 法人メールアドレス&過去に退会したメールアドレスの場合
            if user.is_delete and domain:
                user.name = name
                user.password = make_password(password)
                user.is_delete = False
                user.save()
            elif not user.is_delete and domain:
                return Response({'error_message': '既に登録されているメールアドレスです。'},
                                status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error_message': 'このメールアドレスは登録できません。'},
                                status=status.HTTP_400_BAD_REQUEST)
        # 一度も登録されたことのないメールアドレスの場合
        else:
            # ユーザーを登録する
            user = User(
                name=name,
                email=email,
                password=make_password(password),
                group=group,
            )
            user.save()

        # 登録完了通知を送信する
        signature = '//TODO SE-Hub署名'
        message = f'''
            SE-Hub への登録が完了しました。

            ご登録いただいたメールアドレスとパスワードから、ログインが可能となりました。
            SE-Hubを末永くよろしくお願いいたします。

            {signature}
        '''
        send_mail(
            subject='【SE-Hub】ご登録完了のお知らせ',
            message=message,
            from_email='info@se-hub.jp',
            recipient_list=[email]
        )

        return Response([], status=status.HTTP_200_OK)

    @staticmethod
    def put(request, user_id):

        # リクエストボディ取得
        request_data = json.loads(request.body.decode('utf-8'))
        name = request_data.get('name')
        description = request_data.get('description')

        # ユーザー情報を更新する
        user = User.objects.filter(id=user_id).first()
        if not user:
            return Response([], status=status.HTTP_204_NO_CONTENT)
        user.name = name
        user.description = description
        user.save()

        return Response([], status=status.HTTP_200_OK)

    @staticmethod
    def delete(request, user_id):

        # ユーザー情報を削除する
        user_qs = User.objects.filter(id=user_id)
        if not user_qs:
            return Response([], status=status.HTTP_204_NO_CONTENT)
        user = user_qs.first()
        user.is_delete = True
        user.save()

        return Response([], status=status.HTTP_200_OK)

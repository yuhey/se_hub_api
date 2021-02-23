import json

from django.core.mail import send_mail
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import User
from api.models.bp import Bp
from api.utils import utils
from api.utils.status import BP, WT, RQ, NN


class BpAPI(APIView):

    @staticmethod
    def get(request, user_id, other_id):

        is_follow = Bp.objects.filter(follow__id=user_id, followed__id=other_id).exists()
        is_followed = Bp.objects.filter(follow__id=other_id, followed__id=user_id).exists()
        bp_status = None
        if is_follow and is_followed:
            bp_status = BP
        elif not is_follow and is_followed:
            bp_status = RQ
        elif is_follow and not is_followed:
            bp_status = WT
        else:
            bp_status = NN
        bp_dict = {
            'bp_status': bp_status
        }
        return Response(bp_dict, status=status.HTTP_200_OK)

    @staticmethod
    def post(request):

        # リクエストボディ取得
        request_data = json.loads(request.body.decode('utf-8'))
        user_id = request_data.get('user_id')
        other_id = request_data.get('other_id')

        # ユーザーID存在チェック
        if not User.objects.filter(id=user_id).exists():
            return Response([], status=status.HTTP_400_BAD_REQUEST)
        if not User.objects.filter(id=other_id).exists():
            return Response([], status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.get(id=user_id)
        other = User.objects.get(id=other_id)

        # BP申請チェック
        is_follow = Bp.objects.filter(follow__id=user_id, followed__id=other_id).exists()
        if not is_follow:
            bp = Bp(
                follow=user,
                followed=other,
            )
            bp.save()

        # BP申請をメールで通知する(other)
        if not other.is_delete and other.should_send_bp:
            signature = '//TODO SE-Hub署名'
            user_name = user.name
            group_name = user.group.name
            if group_name:
                group_name = '@' + group_name
            else:
                group_name = ''
            subject = f'【SE-Hub】{user_name}{group_name}さん からBPリクエストが届きました。'
            message = f'''
                {user_name}{group_name}さん からBPリクエストが届きました。

                以下リンクから確認できます。
                https://se-hub.jp/bp

                {signature}
            '''
            # BP承認orBPリクエスト判別
            if Bp.objects.filter(follow__id=other_id, followed__id=user_id).exists():
                subject = f'【SE-Hub】{user_name}{group_name}さん にBPリクエストが承認されました。'
                message = f'''
                    {user_name}{group_name}さん にBPリクエストが承認されました。

                    以下リンクから確認できます。
                    https://se-hub.jp/bp

                    {signature}
                '''

            send_mail(
                subject=subject,
                message=message,
                from_email='info@se-hub.jp',
                recipient_list=[other.email]
            )

        return Response([], status=status.HTTP_200_OK)

    @staticmethod
    def delete(request, user_id, other_id):

        bp_qs = Bp.objects.filter(follow__id=user_id, followed__id=other_id)
        if bp_qs:
            bp_qs.delete()

        return Response([], status=status.HTTP_200_OK)

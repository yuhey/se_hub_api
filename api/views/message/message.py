import json

from django.core.mail import send_mail
from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from django.utils import timezone

from api.models.disclosure import Disclosure
from api.models.message import Message
from api.models.user import User
from api.utils import utils
from api.utils.number import MESSAGE_COUNT


class MessageAPI(APIView):

    @staticmethod
    def get(request, message_id, count):

        message_qs = Message.objects.filter(Q(id=message_id) | Q(message__id=message_id)).order_by('-insert_datetime')
        message_qs = utils.get_qs_for_count(message_qs, count, MESSAGE_COUNT)
        message_qs = message_qs.order_by('insert_datetime')

        #TODO 未読カウントを0にする処理を追加(user_idが必要)

        return Response(message_qs.values('id', 'description', 'file', 'is_read', 'insert_datetime',
                                          'from_user__id', 'from_user__img'), status=status.HTTP_200_OK)

    @staticmethod
    def post(request):

        # リクエストボディ取得
        request_data = json.loads(request.body.decode('utf-8'))
        title = request_data.get('title')
        description = request_data.get('description')
        message_id = request_data.get('message_id')
        disclosure_id = request_data.get('disclosure_id')
        from_id = request_data.get('user_id')
        to_id = request_data.get('other_id')

        if not from_id or not to_id:
            return Response([], status=status.HTTP_400_BAD_REQUEST)

        if not User.objects.filter(id=from_id).exists():
            return Response([], status=status.HTTP_400_BAD_REQUEST)
        if not User.objects.filter(id=to_id).exists():
            return Response([], status=status.HTTP_400_BAD_REQUEST)

        from_user = User.objects.get(id=from_id)
        to_user = User.objects.get(id=to_id)
        if not from_user or not to_user:
            return Response([], status=status.HTTP_400_BAD_REQUEST)

        origin_message = None
        if message_id:
            origin_message = Message.objects.filter(id=message_id).first()

        disclosure = None
        if disclosure_id:
            disclosure = Disclosure.objects.filter(id=disclosure_id).first()

        message = Message(
            title=title,
            description=description,
            message=origin_message,
            disclosure=disclosure,
            from_user=from_user,
            to_user=to_user,
            update_user=from_user,
        )
        message.save()

        # 未読カウントをカウントアップ、更新日付を更新する
        if origin_message:
            origin_message.no_read_count = origin_message.no_read_count + 1
            origin_message.update_datetime = timezone.datetime.now()
            origin_message.update_user = from_user
            origin_message.save()

        # メッセージ受信をメールで通知する(to_user)
        if to_user.should_send_message:
            signature = '//TODO SE-Hub署名'
            user_name = from_user.name
            group_name = from_user.group.name
            if group_name:
                group_name = '@' + group_name
            else:
                group_name = ''
            subject = f'【SE-Hub】{user_name}{group_name}さん からメッセージが届きました。'
            msg = f'''
                {user_name}{group_name}さん からメッセージが届きました。

                以下リンクから確認できます。
                https://se-hub.jp/message

                {signature}
            '''
            send_mail(
                subject=subject,
                message=msg,
                from_email='info@se-hub.jp',
                recipient_list=[to_user.email]
            )

        return Response({'message_id': message.id}, status=status.HTTP_200_OK)

    @staticmethod
    def put(request, message_id):

        # リクエストボディ取得
        request_data = json.loads(request.body.decode('utf-8'))
        user_id = request_data.get('user_id')

        if not user_id:
            return Response([], status=status.HTTP_400_BAD_REQUEST)

        message_qs = Message.objects\
            .filter(message__id=message_id)\
            .filter(to_user__id=user_id)\
            .filter(is_read=False)
        if message_qs:
            for message in message_qs:
                message.is_read = True
                message.save()
            # 未読数を0にする
            origin_message_qs = Message.objects.filter(origin_message__id=message_id)
            if origin_message_qs:
                origin_message = origin_message_qs.first()
                origin_message.no_read_count = 0

        return Response({}, status=status.HTTP_200_OK)

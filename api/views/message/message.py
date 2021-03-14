import json

from django.core.mail import send_mail
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from django.utils import timezone

from api.models.disclosure import Disclosure
from api.models.message import Message
from api.models.room import Room
from api.models.user import User
from api.utils import utils
from api.utils.number import MESSAGE_COUNT


class MessageAPI(APIView):

    @staticmethod
    def get(request, room_id, count):

        message_qs = Message.objects.filter(room__id=room_id).order_by('-insert_datetime')
        message_qs = utils.get_qs_for_count(message_qs, count, MESSAGE_COUNT)
        message_qs = message_qs.order_by('insert_datetime')

        return Response(message_qs.values('id', 'description', 'file', 'is_read', 'insert_datetime',
                                          'from_user__id', 'from_user__img'), status=status.HTTP_200_OK)

    @staticmethod
    def post(request):

        # リクエストボディ取得
        request_data = json.loads(request.body.decode('utf-8'))
        title = request_data.get('title')
        description = request_data.get('description')
        room_id = request_data.get('room_id')
        disclosure_id = request_data.get('disclosure_id')
        from_id = request_data.get('user_id')
        to_id = request_data.get('other_id')

        if not from_id or not to_id:
            return Response({'message': '送信ユーザー、または受信ユーザーのIDが確認できませんでした。'}, status=status.HTTP_400_BAD_REQUEST)

        if not User.objects.filter(id=from_id).exists():
            return Response([], status=status.HTTP_400_BAD_REQUEST)
        if not User.objects.filter(id=to_id).exists():
            return Response([], status=status.HTTP_400_BAD_REQUEST)

        from_user = User.objects.get(id=from_id)
        to_user = User.objects.get(id=to_id)
        if not from_user or not to_user:
            return Response([], status=status.HTTP_400_BAD_REQUEST)

        disclosure = None
        if disclosure_id:
            disclosure = Disclosure.objects.filter(id=disclosure_id).first()

        room = None
        if room_id:
            room = Room.objects.filter(id=room_id).first()
        else:
            room = Room(
                title=title,
                disclosure=disclosure,
                user1=from_user,
                user2=to_user,
            )
            room.save()

        message = Message(
            description=description,
            room=room,
            from_user=from_user,
            to_user=to_user,
        )
        message.save()

        # 未読カウントをカウントアップ、更新日付を更新する
        room.no_read_count = room.no_read_count + 1
        room.update_datetime = timezone.datetime.now()
        room.update_user = from_user
        room.save()

        # メッセージ受信をメールで通知する(to_user)
        if not to_user.is_delete and to_user.should_send_message:
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
    def put(request, room_id):

        # リクエストボディ取得
        request_data = json.loads(request.body.decode('utf-8'))
        user_id = request_data.get('user_id')

        if not user_id:
            return Response([], status=status.HTTP_400_BAD_REQUEST)

        message_qs = Message.objects \
            .filter(room__id=room_id) \
            .filter(to_user__id=user_id) \
            .filter(is_read=False)
        if message_qs:
            for message in message_qs:
                message.is_read = True
                message.save()

        # 未読数を0にする
        room_qs = Room.objects\
            .filter(id=room_id)\
            .exclude(update_user__id=user_id)
        if room_qs:
            room = room_qs.first()
            room.no_read_count = 0
            room.save()

        return Response({}, status=status.HTTP_200_OK)

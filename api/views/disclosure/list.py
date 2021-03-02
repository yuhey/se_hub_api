import json

from django.db.models import Q
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import User
from api.models.disclosure import Disclosure
from api.utils import utils
from api.utils.number import DISCLOSURE_COUNT
from api.utils.status import NO_LIMIT, LOGIN_USER, BP_USER, ALL
from api.utils.utils import get_qs_for_count


class DisclosureListAPI(APIView):

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = (AllowAny,)
        return super(DisclosureListAPI, self).get_permissions()

    @staticmethod
    def post(request, other_id=None):

        # リクエストボディ取得
        request_data = json.loads(request.body.decode('utf-8'))
        user_id = request_data.get('user_id')
        kind = request_data.get('kind')
        count = request_data.get('count')
        search_string = request_data.get('search_string')

        if not kind or not count:
            return Response([], status=status.HTTP_400_BAD_REQUEST)

        disclosure_qs = Disclosure.objects \
            .filter(is_delete=False) \
            .filter(user__is_delete=False)

        if other_id:
            disclosure_qs = disclosure_qs.filter(user__id=other_id)

        # 全選択以外の場合
        if kind != ALL:
            disclosure_qs = disclosure_qs.filter(kind=kind)

        if user_id:
            bp_list = utils.get_bp_list(user_id)
            disclosure_qs = disclosure_qs.filter(Q(limit__in=(NO_LIMIT, LOGIN_USER,)) | Q(user__id__in=bp_list))
            # ブロックユーザーの投稿を除外
            user_qs = User.objects.filter(id=user_id)
            if user_qs:
                user = user_qs.first()
                if user.block_user_csv:
                    block_user_list = user.block_user_csv.split(',')
                    if block_user_list:
                        disclosure_qs = disclosure_qs.exclude(user__id__in=block_user_list)

        else:
            disclosure_qs = disclosure_qs.filter(limit=NO_LIMIT)

        # 文字列による検索（＠XXXはユーザー検索）
        if search_string:
            search_string_list = search_string.split('\\s')
            for search_string_item in search_string_list:
                if search_string_item[0] == '@'\
                        or search_string_item[0] == '＠':
                    disclosure_qs = disclosure_qs.filter(
                        Q(user__group__name__icontains=search_string[1:])
                        | Q(user__name__icontains=search_string[1:]))
                else:
                    disclosure_qs = disclosure_qs.filter(
                        Q(title__icontains=search_string_item) | Q(description__icontains=search_string_item))

        disclosure_qs = disclosure_qs.order_by('-insert_datetime')
        disclosure_qs = get_qs_for_count(disclosure_qs, count, DISCLOSURE_COUNT)

        return Response(disclosure_qs.values('id', 'title', 'description', 'user__id', 'user__name', 'user__img',
                                             'user__group__name', 'insert_datetime').order_by('-insert_datetime'),
                        status=status.HTTP_200_OK)

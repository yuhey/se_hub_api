import json

from django.db.models import Q
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

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

        if not kind or not count:
            return Response([], status=status.HTTP_400_BAD_REQUEST)

        disclosure_qs = Disclosure.objects.all()

        if other_id:
            disclosure_qs = disclosure_qs.filter(user__id=other_id)

        # 全選択以外の場合
        if kind != ALL:
            disclosure_qs = disclosure_qs.filter(kind=kind)

        if user_id:
            bp_list = utils.get_bp_list(user_id)
            disclosure_qs = disclosure_qs.filter(Q(limit__in=(NO_LIMIT, LOGIN_USER,)) | Q(user__id__in=bp_list))
        else:
            disclosure_qs = disclosure_qs.filter(limit=NO_LIMIT)

        disclosure_qs = disclosure_qs.order_by('insert_datetime')

        disclosure_qs = get_qs_for_count(disclosure_qs, count, DISCLOSURE_COUNT)

        return Response(disclosure_qs.values('id', 'title', 'description', 'user__id', 'user__name', 'user__img'), status=status.HTTP_200_OK)

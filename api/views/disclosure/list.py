from django.db.models import Q
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models.disclosure import Disclosure
from api.utils import utils
from api.utils.number import DISCLOSURE_COUNT
from api.utils.status import NO_LIMIT, LOGIN_USER
from api.utils.utils import get_qs_for_count


class DisclosureListAPI(APIView):

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = (AllowAny,)
        return super(DisclosureListAPI, self).get_permissions()

    @staticmethod
    def get(request, viewer_id, kind, count, user_id=None):

        disclosure_qs = Disclosure.objects.all()

        if user_id:
            disclosure_qs = disclosure_qs.filter(user__id=user_id)

        # 全選択以外の場合
        if kind != '0':
            disclosure_qs = disclosure_qs.filter(kind=kind)

        if viewer_id:
            bp_list = utils.get_bp_list(viewer_id)
            disclosure_qs = disclosure_qs.filter(Q(limit__in=(NO_LIMIT, LOGIN_USER,)) | Q(user__id=bp_list))
        else:
            disclosure_qs = disclosure_qs.filter(limit=NO_LIMIT)

        disclosure_qs = get_qs_for_count(disclosure_qs, count, DISCLOSURE_COUNT)

        disclosure_qs = disclosure_qs.order_by('insert_datetime')[(count-1)*10:count*10]

        return Response(disclosure_qs.values(), status=status.HTTP_200_OK)

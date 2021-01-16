import json

from django.db.models import F
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models.bp import Bp
from api.utils import utils
from api.utils.status import BP, RQ, WT


class BpListAPI(APIView):

    @staticmethod
    def post(request, user_id):

        # リクエストボディ取得
        request_data = json.loads(request.body.decode('utf-8'))
        bp_status = request_data.get('bp_status')

        bp_list = utils.get_bp_list(user_id)
        bp_vqs = None

        if bp_status == BP:
            bp_qs = Bp.objects.filter(follow__id__in=bp_list)
            bp_vqs = bp_qs.values('followed__id', 'followed__name', 'followed__description', 'followed__img')
        elif bp_status == RQ:
            bp_qs = Bp.objects.filter(followed__id=user_id)
            bp_qs = bp_qs.exclude(follow__id__in=bp_list)
            bp_vqs = bp_qs.values('follow__id', 'follow__name', 'follow__description', 'follow__img')
        elif bp_status == WT:
            bp_qs = Bp.objects.filter(follow__id=user_id)
            bp_qs = bp_qs.exclude(followed__id__in=bp_list)
            bp_vqs = bp_qs.values('followed__id', 'followed__name', 'followed__description', 'followed__img')

        return Response(bp_vqs, status=status.HTTP_200_OK)

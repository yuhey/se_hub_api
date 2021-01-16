import json

from django.db.models import F
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models.bp import Bp
from api.utils import utils
from api.utils.serializer import BP_SERIALIZER
from api.utils.status import BP, RQ, WT


class BpListAPI(APIView):

    @staticmethod
    def get(request, user_id):

        # リクエストボディ取得
        request_data = json.loads(request.body.decode('utf-8'))
        bp_status = request_data.get('bp_status')

        bp_list = utils.get_bp_list(user_id)
        bp_qs = Bp.objects.all()

        if bp_status == BP:
            bp_qs = bp_qs.filter(follow__id__in=bp_list)
            bp_qs.annotate(followed=F('f_user'))
        elif bp_status == RQ:
            bp_qs = bp_qs.filter(followed__id=user_id)
            bp_qs = bp_qs.exclude(follow__id__in=bp_list)
            bp_qs.annotate(follow=F('f_user'))
        elif bp_status == WT:
            bp_qs = bp_qs.filter(follow__id=user_id)
            bp_qs = bp_qs.exclude(followed__id__in=bp_list)
            bp_qs.annotate(followed=F('f_user'))

        return Response(bp_qs.values('f_user__id', 'f_user__name', 'f_user__description', 'f_user__img'), status=status.HTTP_200_OK)

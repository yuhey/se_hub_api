import json

from django.db.models import F, Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import User
from api.models.bp import Bp
from api.utils import utils
from api.utils.status import BP, RQ, WT, NN


class BpListAPI(APIView):

    @staticmethod
    def post(request, user_id):

        # リクエストボディ取得
        request_data = json.loads(request.body.decode('utf-8'))
        bp_status = request_data.get('bp_status')
        search_string = request_data.get('search_string')

        bp_list = utils.get_bp_list(user_id)
        bp_vqs = None
        print(bp_list)

        if bp_status == BP:
            bp_qs = Bp.objects.filter(followed__id__in=bp_list)
            bp_vqs = bp_qs.values(user__id=F('followed__id'), user__name=F('followed__name'),
                                  user__description=F('followed__description'), user__img=F('followed__img'),
                                  user__group__name=F('followed__group__name'))
        elif bp_status == RQ:
            bp_qs = Bp.objects.filter(followed__id=user_id)
            bp_qs = bp_qs.exclude(follow__id__in=bp_list)
            bp_vqs = bp_qs.values(user__id=F('follow__id'), user__name=F('follow__name'),
                                  user__description=F('follow__description'), user__img=F('follow__img'),
                                  user__group__name=F('follow__group__name'))
        elif bp_status == WT:
            bp_qs = Bp.objects.filter(follow__id=user_id)
            bp_qs = bp_qs.exclude(followed__id__in=bp_list)
            bp_vqs = bp_qs.values(user__id=F('followed__id'), user__name=F('followed__name'),
                                  user__description=F('followed__description'), user__img=F('followed__img'),
                                  user__group__name=F('followed__group__name'))
        elif bp_status == NN:
            user_qs = User.objects.filter(can_find_name=True)
            if search_string:
                user_qs = user_qs.filter(Q(group__name__icontains=search_string) | Q(name__icontains=search_string))
            bp_relative_list = utils.get_bp_relative_list(user_id)
            user_qs = user_qs.exclude(id=user_id)
            if bp_relative_list:
                user_qs = user_qs.exclude(id__in=bp_relative_list)
            bp_vqs = user_qs.values(user__id=F('id'), user__name=F('name'), user__description=F('description'),
                                    user__img=F('img'), user__group__name=F('group__name'))

        return Response(bp_vqs, status=status.HTTP_200_OK)

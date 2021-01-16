import json

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models.bp import Bp
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

        # BP申請登録
        is_follow = Bp.objects.filter(follow__id=user_id, followed__id=other_id).exists()
        if not is_follow:
            bp = Bp(
                follow_id=user_id,
                followed_id=other_id,
            )
            bp.save()

        return Response([], status=status.HTTP_200_OK)

    @staticmethod
    def delete(request, other_id):

        # リクエストボディ取得
        request_data = json.loads(request.body.decode('utf-8'))
        user_id = request_data.get('user_id')

        bp_qs = Bp.objects.filter(follow__id=user_id, followed__id=other_id)
        if bp_qs:
            bp_qs.delete()

        return Response([], status=status.HTTP_200_OK)

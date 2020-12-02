import json

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models.bp import Bp


class BpAPI(APIView):

    @staticmethod
    def get(request, follow_id, followed_id):

        is_follow = Bp.objects.filter(follow__id=follow_id, followed__id=followed_id).exists()
        is_followed = Bp.objects.filter(follow__id=followed_id, followed__id=follow_id).exists()
        bp_dict = {
            'is_follow': is_follow,
            'is_followed': is_followed,
        }
        return Response(bp_dict, status=status.HTTP_200_OK)

    @staticmethod
    def post(request):

        # リクエストボディ取得
        request_data = json.loads(request.body.decode('utf-8'))
        follow_id = request_data.get('follow_id')
        followed_id = request_data.get('followed_id')

        # BP申請登録
        is_follow = Bp.objects.filter(follow__id=follow_id, followed__id=followed_id).exists()
        if not is_follow:
            bp = Bp(
                follow_id=follow_id,
                followed_id=followed_id,
            )
            bp.save()

        return Response([], status=status.HTTP_200_OK)

    @staticmethod
    def delete(request, followed_id):

        # リクエストボディ取得
        request_data = json.loads(request.body.decode('utf-8'))
        follow_id = request_data.get('follow_id')

        bp_qs = Bp.objects.filter(follow_company__id=follow_id, followed_company__id=followed_id)
        if bp_qs:
            bp_qs.delete()

        return Response([], status=status.HTTP_200_OK)

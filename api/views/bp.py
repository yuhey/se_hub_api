import json

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models.bp import Bp


class BpAPI(APIView):

    FOLLOW_SERIALIZER = 'id, followed_company__name, followed_company__description, followed_company__img'
    FOLLOWED_SERIALIZER = 'id, follow_company__name, follow_company__description, follow_company__img'

    def get(self, request, *args, **kwargs):

        # クエリパラメータを取得
        company_id = self.request.query_params.get('id')
        if not company_id:
            return Response([], status=status.HTTP_400_BAD_REQUEST)

        followed_id = self.request.query_params.get('followed_id')
        if not followed_id:
            is_follow = Bp.objects.filter(follow_company__id=company_id, followed_company__id=followed_id).exists()
            is_followed = Bp.objects.filter(follow_company__id=followed_id, followed_company__id=company_id).exists()
            bp_dict = {
                'is_follow': is_follow,
                'is_followed': is_followed,
            }
            return Response(bp_dict, status=status.HTTP_200_OK)

        follow_qs = Bp.objects.filter(follow_company__id=company_id)

        followed_list = list(follow_qs.values_list('followed_company__id'))

        followed_qs = Bp.objects.filter(followed_company_id=company_id)

        bp_qs = follow_qs.filter(follow_company__id__in=followed_list)

        bp_list = list(bp_qs.values_list('follow_company__id'))

        followed_qs = followed_qs.exclude(follow_company__id=bp_list)

        follow_qs = follow_qs.exclude(followed_company__id=bp_list)

        bp_dict = {
            'bp': bp_qs.values(self.FOLLOW_SERIALIZER),
            'follow': follow_qs.values(self.FOLLOW_SERIALIZER),
            'followed': followed_qs.values(self.FOLLOWED_SERIALIZER)
        }

        return Response(bp_dict, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):

        # リクエストボディ取得
        request_data = json.loads(self.request.body)
        follow_id = request_data.get('follow_id')
        followed_id = request_data.get('followed_id')

        # BP申請登録
        bp_qs = Bp.objects.filter(follow_company__id=follow_id, followed_company__id=followed_id)
        if not bp_qs.exists():
            bp = Bp(
                follow_id=follow_id,
                followed_id=followed_id,
            )
            bp.save()

        return Response([], status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):

        # クエリパラメータの取得
        followed_id = self.request.query_params.get('id')
        if not followed_id:
            return Response([], status=status.HTTP_400_BAD_REQUEST)

        # リクエストボディ取得
        request_data = json.loads(self.request.body)
        follow_id = request_data.get('follow_id')

        bp_qs = Bp.objects.filter(follow_company__id=follow_id, followed_company__id=followed_id)
        if bp_qs:
            bp_qs.delete()

        return Response([], status=status.HTTP_200_OK)

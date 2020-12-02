import json

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response

from api.models.ad import Ad
from api.models.group import Group


class AdAPI(APIView):

    def get_permissions(self):
        self.permission_classes = (AllowAny,)
        return super(AdAPI, self).get_permissions()

    @staticmethod
    def get(request, count):

        ad_qs = Ad.objects.filter(count__gt=0).order_by('?')[:count]
        return Response(ad_qs, status=status.HTTP_200_OK)

    @staticmethod
    def post(request):

        # リクエストボディ取得
        request_data = json.loads(request.body.decode('utf-8'))
        group_id = request_data.get('group_id')
        count = request_data.get('count')

        group_qs = Group.objects.filter(id=group_id)
        if not group_qs.exists():
            return Response([], status=status.HTTP_400_BAD_REQUEST)

        group = group_qs.first()

        ad_qs = Ad.objects.filter(group__id=group_id)
        ad = ad_qs.first()
        if not ad_qs.exists():
            ad = Ad(
                group=group,
            )
            ad.save()

        ad.count = ad.count + count
        ad.save()

        return Response([], status=status.HTTP_200_OK)

    @staticmethod
    def put(request, ad_id):

        ad_qs = Ad.objects.filter(id=ad_id)
        if not ad_qs.exists():
            return Response([], status=status.HTTP_400_BAD_REQUEST)

        ad = ad_qs.first()
        if ad.count > 0:
            ad.count = ad.count - 1
            ad.save()

        return Response([], status=status.HTTP_200_OK)

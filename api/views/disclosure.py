import json

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models.company import Company
from api.models.disclosure import Disclosure
from api.models.user import User


class DisclosureAPI(APIView):

    NO_LIMIT = 0
    LOGIN_USER = 1
    BP_USER = 2

    def get(self, request, *args, **kwargs):

        # クエリパラメータを取得
        viewer_id = self.request.query_params.get('id')
        user_id = self.request.query_params.get('user_id')
        count = self.request.query_params.get('count')
        kind = self.request.query_params.get('kind')

        disclosure_qs = Disclosure.objects.all()

        if user_id:
            disclosure_qs = disclosure_qs.filter(user__id=user_id)
        elif kind:
            disclosure_qs = disclosure_qs.filter(kind=kind)

        if viewer_id:
            disclosure_qs = disclosure_qs.filter(limit__in=(self.NO_LIMIT, self.LOGIN_USER,))
            # TODO add BP filter
        else:
            disclosure_qs = disclosure_qs.filter(limit=self.NO_LIMIT)

        disclosure_qs = disclosure_qs.order_by('insert_datetime')[(count-1)*10:count*10]

        return Response(disclosure_qs.values(), status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):

        # リクエストボディ取得
        request_data = json.loads(self.request.body)
        title = request_data.get('title')
        description = request_data.get('description')
        kind = request_data.get('kind')
        limit = request_data.get('limit')
        data = request_data.get('data')
        user_id = request_data.get('user_id')
        company_id = request_data.get('company_id')

        if not title or not description or not kind\
                or not limit or not user_id or not company_id:
            return Response([], status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(id=user_id).first()
        if not user:
            return Response([], status=status.HTTP_400_BAD_REQUEST)

        company = Company.objects.filter(id=company_id).first()
        if not company:
            return Response([], status=status.HTTP_400_BAD_REQUEST)

        disclosure = Disclosure(
            title=title,
            description=description,
            kind=kind,
            limit=limit,
            data=data,
            user=user,
            company=company,
        )
        disclosure.save()

        return Response([], status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):

        # クエリパラメータを取得
        disclosure_id = self.request.query_params.get('id')

        if not disclosure_id:
            return Response([], status=status.HTTP_400_BAD_REQUEST)

        disclosure = Disclosure.objects.filter(id=disclosure_id)
        disclosure.delete()

        return Response([], status=status.HTTP_200_OK)


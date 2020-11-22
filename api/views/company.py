import json

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from api.models.company import Company


class CompanyAPI(APIView):

    def put(self, request, *args, **kwargs):

        # クエリパラメータ取得
        company_id = self.request.query_params.get('id')
        if not company_id:
            return Response([], status=status.HTTP_400_BAD_REQUEST)

        # リクエストボディ取得
        request_data = json.loads(self.request.body)
        name = request_data.get('name')
        description = request_data.get('description')
        url = request_data.get('url')
        img = request_data.get('img')

        # 法人グループ情報を更新する
        company = Company.objects.filter(id=company_id).first()
        if not company:
            return Response([], status=status.HTTP_400_BAD_REQUEST)
        company.name = name
        company.description = description
        company.url = url
        company.img = img
        company.save()

        return Response([], status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):

        # クエリパラメータ取得
        company_id = self.request.query_params.get('id')
        if not company_id:
            return Response([], status=status.HTTP_400_BAD_REQUEST)

        # 法人グループを削除する
        company = Company.objects.filter(id=company_id).first()
        if not company:
            return Response([], status=status.HTTP_400_BAD_REQUEST)
        company.delete()

        return Response([], status=status.HTTP_200_OK)

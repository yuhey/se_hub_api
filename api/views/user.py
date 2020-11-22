import json

from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from api.models.company import Company
from api.models.user import User, CustomUserManager


class UserAPI(APIView):

    def get_permissions(self):
        if self.request.method == 'GET'\
                or self.request.method == 'POST':
            self.permission_classes = (AllowAny,)
        return super(UserAPI, self).get_permissions()

    def get(self, request, *args, **kwargs):

        user_id = self.request.query_params.get('id')

        if not user_id:
            return Response([], status=status.HTTP_400_BAD_REQUEST)

        queryset = User.objects.filter(id=user_id)
        return Response(
            queryset.values('id', 'name', 'email', 'description', 'company__id', 'company__name', 'company__url'),
            status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):

        request_data = json.loads(self.request.body)

        email = request_data.get('email')
        password = request_data.get('password')

        if not email or not password:
            return Response([], status=status.HTTP_400_BAD_REQUEST)

        # メールアドレスからドメインを取得する
        domain = email.split('@')[-1]

        # ドメインから法人グループを取得
        is_company = Company.objects.filter(domain=domain).exists()
        company = None

        # 法人グループとして登録されている場合
        if is_company:
            company = Company.objects.get(domain=domain)
        # 法人グループとして登録されていない場合
        else:
            unit = domain.split('.')
            # co.jpドメインなら法人グループを作成する
            if len(unit) > 2 \
                    and unit[-2] == 'co' and unit[-1] == 'jp':
                company = Company(
                    domain=domain,
                )
                company.save()

        # ユーザーを登録する
        user = User(
            email=email,
            password=make_password(password),
            company=company,
        )
        if company:
            user.company = company
            user.save()

        return Response(user.objects.all.values(), status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):

        # クエリパラメータ取得
        user_id = self.request.query_params.get('id')
        if not user_id:
            return Response([], status=status.HTTP_400_BAD_REQUEST)

        # リクエストボディ取得
        request_data = json.loads(self.request.body)
        name = request_data.get('name')
        description = request_data.get('description')
        img = request_data.get('img')

        # ユーザー情報を更新する
        user = User.objects.filter(id=user_id).first()
        if not user:
            return Response([], status=status.HTTP_400_BAD_REQUEST)
        user.name = name
        user.description = description
        user.img = img
        user.save()

        return Response([], status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):

        # クエリパラメータ取得
        user_id = self.request.query_params.get('id')
        if not user_id:
            return Response([], status=status.HTTP_400_BAD_REQUEST)

        # ユーザー情報を更新する
        user = User.objects.filter(id=user_id).first()
        if not user:
            return Response([], status=status.HTTP_400_BAD_REQUEST)

        user.delete()

        return Response([], status=status.HTTP_200_OK)

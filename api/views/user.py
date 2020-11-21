from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from api.models.company import Group
from api.models.user import User


class UserAPI(APIView):

    def get(self):

        user_id = self.request.query_params.get('id')

        if not user_id:
            return Response([], status=status.HTTP_400_BAD_REQUEST)

        queryset = User.objects.filter(id=user_id)
        return Response(
            queryset.values('id', 'name', 'email', 'description', 'group__id', 'group__name', 'group__url'),
            status=status.HTTP_200_OK)

    def post(self):

        email = self.request.POST.get('email')
        password = self.request.POST.get('password')

        if not email or not password:
            return Response([], status=status.HTTP_400_BAD_REQUEST)

        # メールアドレスからドメインを取得する
        domain = email.split('.')[-1]

        # ドメインから法人グループを取得
        is_company = Group.objects.filter(domain=domain).exists()

        # 法人グループとして登録されている場合
        if is_company:
            group = Group.objects.get(domain=domain)
        # 法人グループとして登録されていない場合
        else:
            unit = domain.split('.')
            # co.jpドメインなら法人フラグを立てる
            if len(unit) > 2\
                    and unit[-2] == 'co' and unit[-1] == 'jp':
                is_company = True
            # それ以外のドメインは、グループを設定しない（個人事業主として扱う）
            else:
                domain = None
            # グループを登録する
            group = Group(
                domain=domain,
                is_company=is_company,
            )
            group.save()

        # ユーザーを登録する
        user = User(
            email=email,
            password=password,
            group=group,
        )
        user.save()

        return Response(user.objects.all.values(), status=status.HTTP_200_OK)

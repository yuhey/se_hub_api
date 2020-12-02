import json

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models.group import Group
from api.models.disclosure import Disclosure
from api.models.user import User


class DisclosureAPI(APIView):

    @staticmethod
    def post(request):

        # リクエストボディ取得
        request_data = json.loads(request.body.decode('utf-8'))
        title = request_data.get('title')
        description = request_data.get('description')
        kind = request_data.get('kind')
        limit = request_data.get('limit')
        data = request_data.get('data')
        user_id = request_data.get('user_id')
        group_id = request_data.get('group_id')

        if not title or not description or not kind\
                or not limit or not user_id or not group_id:
            return Response([], status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(id=user_id).first()
        if not user:
            return Response([], status=status.HTTP_400_BAD_REQUEST)

        group = Group.objects.filter(id=group_id).first()
        if not group:
            return Response([], status=status.HTTP_400_BAD_REQUEST)

        disclosure = Disclosure(
            title=title,
            description=description,
            kind=kind,
            limit=limit,
            data=data,
            user=user,
            group=group,
        )
        disclosure.save()

        return Response([], status=status.HTTP_200_OK)

    @staticmethod
    def delete(request, disclosure_id):

        disclosure_qs = Disclosure.objects.filter(id=disclosure_id)
        if disclosure_qs:
            disclosure_qs.delete()

        return Response([], status=status.HTTP_200_OK)

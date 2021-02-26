from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response

from api.models.disclosure import Disclosure


class DisclosureAlarmAPI(APIView):

    def get_permissions(self):
        if self.request.method == 'PUT':
            self.permission_classes = (AllowAny,)
        return super(DisclosureAlarmAPI, self).get_permissions()

    @staticmethod
    def put(request, disclosure_id):

        disclosure_qs = Disclosure.objects.filter(id=disclosure_id)
        if not disclosure_qs:
            return Response({'error_message': '通報対象の投稿が存在しません。'},
                            status=status.HTTP_204_NO_CONTENT)

        disclosure = disclosure_qs.first()
        disclosure.is_alarmed = True
        disclosure.save()

        return Response([], status=status.HTTP_200_OK)

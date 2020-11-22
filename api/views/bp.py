from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models.bp import Bp


class BpAPI(APIView):

    def get(self, request, *args, **kwargs):

        user_id = self.request.query_params.get('id')

        if not user_id:
            return Response([], status=status.HTTP_400_BAD_REQUEST)

        queryset = Bp.objects.filter(id=user_id)

        return Response(queryset.values(), status=status.HTTP_200_OK)

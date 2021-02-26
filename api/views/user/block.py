from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response

from api.models.bp import Bp
from api.models.user import User


class UserBlockAPI(APIView):

    def get_permissions(self):
        if self.request.method == 'PUT':
            self.permission_classes = (AllowAny,)
        return super(UserBlockAPI, self).get_permissions()

    @staticmethod
    def put(request, user_id, other_id):

        bp_qs = Bp.objects\
            .filter(follow__id=user_id)\
            .filter(followed__id=other_id)
        if bp_qs:
            bp = bp_qs.first()
            bp.delete()

        user_qs = User.objects.filter(id=user_id)
        if user_qs:
            user = user_qs.first()
            block_user_csv = user.block_user_csv
            if block_user_csv:
                block_user_list = block_user_csv.split(',')
                block_user_list.append(str(other_id))
                user.block_user_csv = ','.join(block_user_list)
            else:
                user.block_user_csv = str(other_id)
            user.save()

        return Response([], status=status.HTTP_200_OK)

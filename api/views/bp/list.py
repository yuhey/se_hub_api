from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models.bp import Bp
from api.utils import utils
from api.utils.serializer import FOLLOW_SERIALIZER, FOLLOWED_SERIALIZER


class BpListAPI(APIView):

    @staticmethod
    def get(request, group_id):

        bp_list = utils.get_bp_list(group_id)
        bp_qs = Bp.objects.filter(follow__id__in=bp_list)

        followed_qs = Bp.objects.filter(followed__id=group_id)
        followed_qs = followed_qs.exclude(follow__id__in=bp_list)

        follow_qs = Bp.objects.filter(follow__id=group_id)
        follow_qs = follow_qs.exclude(followed__id__in=bp_list)

        bp_dict = {
            'bp': bp_qs.values(FOLLOW_SERIALIZER),
            'follow': follow_qs.values(FOLLOW_SERIALIZER),
            'followed': followed_qs.values(FOLLOWED_SERIALIZER),
        }

        return Response(bp_dict, status=status.HTTP_200_OK)


from django.db.models import F

from api.models.bp import Bp


def get_bp_list(user_id):

    bp_list = list()
    follow_qs = Bp.objects.filter(follow__id=user_id)
    followed_qs = Bp.objects.filter(followed__id=user_id)

    if follow_qs and followed_qs:
        bp_list = list(set(follow_qs.values(user_id=F('follow__id')).values_list())
                       & set(followed_qs.values(user_id=F('followed__id')).values_list()))

    return bp_list


def get_qs_for_count(qs, count, unit):

    return_qs = qs
    max_count = qs.count()
    if max_count > unit:
        start_count = max_count - (count * unit)
        if start_count < 0:
            start_count = 0
        end_count = max_count - ((count - 1) * unit)
        return_qs = qs[start_count:end_count]
    return return_qs

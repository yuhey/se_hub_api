from api.models.bp import Bp


def get_bp_list(group_id):

    bp_list = list()
    follow_qs = Bp.objects.filter(follow__id=group_id)
    followed_qs = Bp.objects.filter(followed__id=group_id)

    if follow_qs and followed_qs:
        bp_list = list(set(follow_qs.values_list) & set(followed_qs.values_list))

    return bp_list

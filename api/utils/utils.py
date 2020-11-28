from api.models.bp import Bp


def get_bp_list(company_id):

    bp_list = list()
    follow_qs = Bp.objects.filter(follow_company__id=company_id)
    followed_qs = Bp.objects.filter(followed_company__id=company_id)

    if follow_qs and followed_qs:
        bp_list = list(set(follow_qs.values_list) & set(followed_qs.values_list))

    return bp_list

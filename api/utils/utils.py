from django.db.models import F

from api.models import User
from api.models.bp import Bp


# 指定ユーザーに紐づくBPユーザーのユーザーIDをリスト形式で返す
def get_bp_list(user_id):

    bp_list = list()
    follow_qs = Bp.objects.filter(followed__id=user_id)
    followed_qs = Bp.objects.filter(follow__id=user_id)

    if follow_qs and followed_qs:
        follow_id_list = convert_vqs_to_list(follow_qs.values(user_id=F('follow__id')), 'user_id')
        followed_id_list = convert_vqs_to_list(followed_qs.values(user_id=F('followed__id')), 'user_id')
        bp_list = list(set(follow_id_list) & set(followed_id_list))

    return bp_list


# 指定ユーザーに紐づくBP,リクエスト,承認待ちのユーザーIDをリスト形式で返す
def get_bp_relative_list(user_id):

    bp_relative_list = list()
    follow_qs = Bp.objects.filter(follow__id=user_id)
    followed_qs = Bp.objects.filter(followed__id=user_id)

    if follow_qs and not followed_qs:
        bp_relative_list = convert_vqs_to_list(follow_qs.values(user_id=F('followed__id')), 'user_id')
    elif not follow_qs and followed_qs:
        bp_relative_list = convert_vqs_to_list(followed_qs.values(user_id=F('follow__id')), 'user_id')
    elif follow_qs and followed_qs:
        follow_id_list = convert_vqs_to_list(follow_qs.values(user_id=F('followed__id')), 'user_id')
        followed_id_list = convert_vqs_to_list(followed_qs.values(user_id=F('follow__id')), 'user_id')
        bp_relative_list.extend(follow_id_list)
        bp_relative_list.extend(followed_id_list)
        bp_relative_list = list(set(bp_relative_list))

    return bp_relative_list


# クエリストリングから指定項目のみのリスト形式を返す
def convert_vqs_to_list(vqs, key):

    lst = list()

    for v in vqs:
        lst.append(v.get(key))

    return lst


# クエリストリングから指定の件数(=unit)を取得して返す
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


# メッセージ受信時にメールで通知をするかのフラグを返す
def should_send_message(user_id):

    user_qs = User.objects.filter(id=user_id)
    if not user_qs.exists():
        return False

    user = user_qs.first()
    return user.should_send_bp

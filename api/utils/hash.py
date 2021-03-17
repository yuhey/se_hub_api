import random


# 6桁のランダムな確認コードを返す
def create_hash():
    rnd = str(random.randint(0, 999999))
    return rnd.zfill(6)

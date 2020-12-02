import random


def create_hash():
    rnd = str(random.randint(0, 999999))
    return rnd.zfill(6)

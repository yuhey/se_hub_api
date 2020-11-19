import random, string


def create_hash(length):
    random_list = [random.choice(string.ascii_letters + string.digits) for i in range(length)]
    return ''.join(random_list)

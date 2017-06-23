"""
place for functions that will be used in other files
"""
import random
import string


def random_string(n):
    return ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=n))

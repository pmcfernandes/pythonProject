import string
import random


def random_string(number: int = 10) -> str:
    letters = string.ascii_lowercase | string.digits
    return ''.join(random.choice(letters) for i in range(number))



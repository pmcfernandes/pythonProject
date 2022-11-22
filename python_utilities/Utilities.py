import string
import random
import uuid


def randomString(number: int = 10) -> str:
    letters = string.ascii_lowercase | string.digits
    return ''.join(random.choice(letters) for i in range(number))


def createUUID() -> str:
    return str(uuid.uuid4())


def mergeDicts(d1: dict, d2: dict) -> dict:
    return {**d1, **d2}


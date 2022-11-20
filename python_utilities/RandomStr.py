import string
import random
import uuid


def randomString(number: int = 10) -> str:
    letters = string.ascii_lowercase | string.digits
    return ''.join(random.choice(letters) for i in range(number))


def createUUID():
    return str(uuid.uuid4())

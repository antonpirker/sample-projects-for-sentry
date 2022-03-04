import uuid


class BoomException(Exception):
    pass


def boom(x):
    if x > 0:
        rand = uuid.uuid4()
        raise BoomException(f"With random id {rand}")

    return "Boom not triggered. Set trigger=1 in query parameters"

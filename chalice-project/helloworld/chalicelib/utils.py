import uuid


class BoomException(Exception):
    pass


def boom(x):
    if x > 0:
        rand = uuid.uuid4()
        msg = f"With random id " + str(rand)
        raise BoomException(msg)

    return "Boom not triggered. Set trigger=1 in query parameters"

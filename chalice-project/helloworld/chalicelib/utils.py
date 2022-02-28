class BoomException(Exception):
    pass


def boom(x):
    if x > 0:
        raise BoomException()

    return "Boom not triggered. Set trigger=1 in query parameters"

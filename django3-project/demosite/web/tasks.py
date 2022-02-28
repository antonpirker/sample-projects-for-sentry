from celery import Task
from celery import shared_task


class ShouldNOTShowUpException(Exception):
    pass


class SHOULDShowUpExceptions(Exception):
    pass


class CustomExceptionB(Exception):
    pass


class CustomBaseTask(Task):
    def __call__(self, *args, **kwargs):
        try:
            super().__call__(*args, **kwargs)
        except ShouldNOTShowUpException:  # should NOT be sent to sentry
            # do sth
            raise SHOULDShowUpExceptions()  # SHOULD be sent to sentry
        except CustomExceptionB:
            pass


@shared_task(base=CustomBaseTask, bind=True)
def some_actual_task(self, x, y):
    if y > 10:
        raise ShouldNOTShowUpException()  # should NOT be sent to sentry
    return x + y

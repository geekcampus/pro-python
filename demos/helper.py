import functools
from time import sleep


def fake_acquire_lock(func, timeout=60):
    @functools.wraps(func)
    def inner(*args, **kwargs):
        sleep(100)
        return func(*args, **kwargs)
    return inner

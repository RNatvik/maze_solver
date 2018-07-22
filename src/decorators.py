# Collection of basic decorators
from time import time


def timed(func):
    def timed_method(*args, **kwargs):
        start_time = time()
        func(*args, **kwargs)
        end_time = time()
        total_time = end_time - start_time
        return total_time
    return timed_method


def timed_with_rv(func):
    def timed_method(*args, **kwargs):
        start_time = time()
        rv = func(*args, **kwargs)
        end_time = time()
        total_time = end_time - start_time
        return rv, total_time
    return timed_method

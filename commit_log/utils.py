import threading
from functools import wraps


def thread_safe(fn):
    lock = threading.Lock()

    @wraps(fn)
    def _fn(*args, **kwargs):
        with lock:
            return fn(*args, **kwargs)

    return _fn

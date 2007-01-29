import threading
import logging

class DummyHandler:
    _d_lock = None
    _d_values = None
    _d_logger = None

    def __init__(self):
        self._d_lock = threading.Event()
        self._d_values = []
        self._d_logger = logging.getLogger("edef.core")

    def release(self, value=None):
        self._d_logger.debug("Release wating threads with value %s"%value)
        self._d_values.append(value)
        self._d_lock.set()

    def wait(self, timeout=None):
        if len(self._d_values) > 0:
            return self._d_values.pop(0)
        self._d_lock.wait(timeout)
        self._d_lock.clear()
        return self._d_values.pop(0)



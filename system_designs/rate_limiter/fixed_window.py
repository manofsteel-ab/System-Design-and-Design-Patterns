from abc import ABC, abstractmethod

class RateLimiter(ABC):

    _max_request_per_second=None

    def __init__(self, max_request_per_second=0):
        self._max_request_per_second = max_request_per_second

    @abstractmethod
    def allow(self):
        pass

class FixedWindowRateLimiter(RateLimiter):
    def __init__(self, max_request_per_second=0):
        super().__init__(max_request_per_second)
        self._storage = {}
        print(self._max_request_per_second)

    def put(self):
        pass

    def get(self):
        pass

    def allow(self):
        pass


FixedWindowRateLimiter()

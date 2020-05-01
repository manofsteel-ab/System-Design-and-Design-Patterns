from abc import ABC, abstractmethod

class RateLimiter(ABC):

    _maxRequestPerSec=None

    @abstractmethod
    def allow(self):
        pass

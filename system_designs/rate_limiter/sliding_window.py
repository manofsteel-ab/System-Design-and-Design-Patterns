from abc import ABC, abstractmethod
import threading

import time
import random

class RateLimiterInterface(ABC):

    def __init__(self):
        self.db = {} # ex: key: user_id,  value is list of epoch time


    @abstractmethod
    def allow(self, user_id, allowed_reqest, window_in_second):
        pass

    def get_current_time(self):
        return int(time.time())

    def set_value(self, key, value):
        self.db[key] = value


class SlidingWindowRateLimiter(RateLimiterInterface):
    def __init__(self):
        super().__init__()
        self._lock = threading.Lock()

    def _previous_requests(self, key):
        return sorted(self.db.get(key,[]), reverse=True)

    def allow(self, user_id, allowed_reqest, window_in_second=10):
        self._lock.acquire()
        current_time = self.get_current_time()
        previous_requests = self._previous_requests(user_id)
        req_in_window = []
        for time in previous_requests:
            diff = current_time-time
            if diff<window_in_second:
                req_in_window.append(time)
            else:
                break
        print(previous_requests, ">>>>", req_in_window," + ", current_time)
        if len(req_in_window)>=allowed_reqest:
            self._lock.release()
            return False
        else:
            req_in_window.append(current_time)
            self.set_value(key=user_id, value=req_in_window)
            self._lock.release()
        return True


class SendRequest:

    _request_id=1

    @classmethod
    def request_task(cls):
        users = ['user_1']
        rate_limiter = SlidingWindowRateLimiter()
        while True:
            id = users[(random.randint(1, 100))%1]
            print(
                "Thread {}".format(threading.currentThread().getName()),
                cls._request_id,
                rate_limiter.allow(user_id=id, allowed_reqest=5)
            )
            cls._request_id+=1
            time.sleep(1)


class TestMe:
    pass


if __name__ == '__main__':
    t1 = threading.Thread(name='t1',target=SendRequest.request_task)
    t2 = threading.Thread(name='t2',target=SendRequest.request_task)
    t3 = threading.Thread(name='t3',target=SendRequest.request_task)
    t1.start()
    t2.start()
    t3.start()

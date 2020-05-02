from abc import ABC, abstractmethod
import threading

import time
import random

class RateLimiterInterface(ABC):

    def __init__(self):
        self.db = {} # ex: key: user_id,  value {freq:starttime}


    @abstractmethod
    def allow(self, user_id, allowed_reqest, rate):
        pass

    def get_current_time(self):
        return int(time.time())


class FixedWindowRateLimiter(RateLimiterInterface):

    def __init__(self):
        super().__init__()
        self._lock = threading.Lock()

    def allow(self, user_id, allowed_reqest, in_second=10):
        try:
            self._lock.acquire()
            current_time = self.get_current_time()
            stored_freq = self.db.get(user_id)
            allowed = True
            if not stored_freq:
                self.db[user_id] = (1, current_time)
                self._lock.release()
                return allowed

            diff = current_time - stored_freq[1]
            if diff > in_second:
                self.db[user_id] = (1, current_time)
            elif diff < in_second and stored_freq[0]<allowed_reqest:
                self.db[user_id]=(stored_freq[0]+1, stored_freq[1])
            else:
                allowed = False
            self._lock.release()
            return allowed
        except Exception as e:
            print(str(e))



class SendRequest:
    _request_id=1

    @classmethod
    def request_task(cls):
        users = ['user_1']
        rate_limiter = FixedWindowRateLimiter()
        while True:
            id = users[(random.randint(1, 100))%1]
            print(
                "Thread {}".format(threading.currentThread().getName()),
                cls._request_id,
                rate_limiter.allow(user_id=id, allowed_reqest=5)
            )
            cls._request_id+=1
            time.sleep(1)


if __name__ == '__main__':
    t1 = threading.Thread(name='t1',target=SendRequest.request_task)
    t2 = threading.Thread(name='t2',target=SendRequest.request_task)
    t3 = threading.Thread(name='t3',target=SendRequest.request_task)
    t1.start()
    t2.start()
    t3.start()


"""
What are some of the problems with our algorithm?

- boundary burst
- in case of distributed environment, race condition
- memory - ex suppose user_id takes 8 byte, 2 byte to store the freq and 4 byte
            to starttime - total = 14 byte, if we assume 20 byte for hashtable
            then total = 34byte for 1M user total space = 34*1M = 34MB(million byte)




"""

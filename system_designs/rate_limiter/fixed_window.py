from abc import ABC, abstractmethod
import threading

import time
import random

class RateLimiterInterface(ABC):

    def __init__(self):
        self.db_1 = {} # ex: key: user_id,  value {freq:starttime}


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
            stored_freq = self.db_1.get(user_id)
            allowed = True
            if not stored_freq:
                self.db_1[user_id] = (1, current_time)
                self._lock.release()
                return allowed

            diff = current_time - stored_freq[1]
            print(current_time,stored_freq[1],diff)
            if diff > in_second:
                self.db_1[user_id] = (1, current_time)
            elif diff < in_second and stored_freq[0]<allowed_reqest:
                self.db_1[user_id]=(stored_freq[0]+1, stored_freq[1])
            else:
                allowed = False
            self._lock.release()
            return allowed
        except Exception as e:
            print(str(e))



class SendRequest:

    @classmethod
    def request_task(cls,counter):
        users = ['user_1']
        rate_limiter = FixedWindowRateLimiter()
        while True:
            id = users[(random.randint(1, 100))%1]
            print("Thread {}".format(threading.currentThread().ident))
            print(counter,rate_limiter.allow(user_id=id, allowed_reqest=5))
            counter+=1
            time.sleep(1)


if __name__ == '__main__':
    counter = 1
    t1 = threading.Thread(target=SendRequest.request_task, args=(counter,))
    t2 = threading.Thread(target=SendRequest.request_task, args=(counter,))
    t3 = threading.Thread(target=SendRequest.request_task, args=(counter,))
    t1.start()
    # t2.start()
    # t3.start()

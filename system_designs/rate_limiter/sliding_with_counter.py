from abc import ABC,abstractmethod
import time
import threading
import random

class Storage:

    def __init__(self):
        self.db = {}

    def get(self, key):
        return self.db.get(key)

    def set(self, key, value):
        self.db[key] = value


class RateLimiter(ABC):

    @abstractmethod
    def is_allowed(self, user_id):
        pass


class SlidingWindowCounterStrategy(RateLimiter):
    REQUESTS = "requests" # key in the metadata representing the max number of requests
    WINDOW_TIME = "window_time" # key in the metadata representing the window time
    METADATA_SUFFIX = "_metadata" # metadata suffix
    BUCKETS = "_buckets" #  buckets suffix

    def __init__(self, storage, bucket_size=10):
        self._storage = storage
        self._lock = threading.Lock()
        self._bucket_size = bucket_size

    def is_allowed(self, user_id):
        # fetch config
        allowed_requests, window_time_in_second = self.get_user_config(user_id)
        # initalization
        current_timestamp = self.get_timestamp_in_second()
        buckets =  self.get_user_buckets(user_id) or {}
        print(buckets)
        oldest_timestamp = current_timestamp - window_time_in_second
        deletable_bucket_keys = []
        total = 0

        # find total valid request count and deletable buckets
        for bucket_starttime, count in buckets.items():
            if bucket_starttime<=oldest_timestamp:
                deletable_bucket_keys.append(bucket_starttime)
            else:
                total+=count

        # delete invalid bucket
        for key in deletable_bucket_keys:
            del buckets[key]

        # validate total proccessed request count in given window
        print(total)
        if total>=allowed_requests:
            return False
        else:
            current_bucket =  self.get_bucket(current_timestamp,window_time_in_second)
            buckets[current_bucket] = buckets.get(current_bucket,0)+1
            self.update_user_bucket(user_id, buckets)
            return True

    def get_bucket(self, timestamp, window_time_in_second):
        factor = window_time_in_second / self._bucket_size
        return ((timestamp // factor) * factor)

    def get_user_buckets(self, user_id):
        hash_key = user_id+self.BUCKETS
        val = self._storage.get(hash_key)
        return val

    def update_user_bucket(self, user_id, value):
        hash_key = user_id+self.BUCKETS
        self._storage.set(hash_key, value)

    def get_user_config(self, user_id):
        hash_key = user_id+self.METADATA_SUFFIX
        val = self._storage.get(hash_key)
        if val is None:
            raise Exception("Invalid user")

        return (val[self.REQUESTS], val[self.WINDOW_TIME])

    def add_user_config(self, user_id, allowed_requests=100, window_time_in_second=60):
        hash_value = {
            self.REQUESTS: allowed_requests,
            self.WINDOW_TIME: window_time_in_second
        }
        self._storage.set(
            key = user_id+self.METADATA_SUFFIX,
            value = hash_value
        )


    def remover_user(self, user_id): #TODO
        pass

    def get_timestamp_in_second(self):
        return int(round(time.time()))


class RequestHandler:

    def __init__(self, storage):
        self._request_id = 1
        self.rate_limiter = SlidingWindowCounterStrategy(storage)

    def add_sample_users(self):
        self.rate_limiter.add_user_config('user_1')
        self.rate_limiter.add_user_config('user_2')

    def request_task(self):
        users = ['user_1', 'user_2']

        while True:
            id = users[(random.randint(1, 100))%1]
            print(
                "Thread {}".format(threading.currentThread().getName()),
                self._request_id,
                self.rate_limiter.is_allowed(user_id=id)
            )
            self._request_id+=1
            time.sleep(1)

if __name__ == '__main__':
    storage = Storage()
    request_handler =  RequestHandler(storage)
    request_handler.add_sample_users()
    t1 = threading.Thread(name='t1',target=request_handler.request_task)
    t2 = threading.Thread(name='t2',target=request_handler.request_task)
    t3 = threading.Thread(name='t3',target=request_handler.request_task)
    t1.start()
    # t2.start()
    # t3.start()

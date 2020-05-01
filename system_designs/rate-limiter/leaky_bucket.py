import threading

import time
import random

class LeakyBucket:

    def __init__(self, drain_rate, capacity):
        invalidation = [
            not isinstance(drain_rate, (float, int)),
            drain_rate<1,
            not isinstance(capacity, int),
        ]
        if any(invalidation):
            raise TypeError('Invalid type')

        self._capacity = capacity
        self._queue = []
        self._lock = threading.Lock()

    def refill(self, id):
        if len(self._queue) >= self._capacity:
            print("Request {} - Discarded".format(id))
            return
        self._queue.append(id)
        print("Request {} - accepted".format(id))

    def consume(self):
        if self._queue:
            reqest = self._queue.pop(0)
            print('consumed > {} '.format(reqest))

def request_task(bucket):

    while True:
        id = random.randint(1, 1000)
        bucket.refill(id)
        time.sleep(random.randint(1, 2))

def consumer_task(bucket):
    while True:
        bucket.consume()
        time.sleep(random.randint(1, 4))


if __name__ == '__main__':
    bucket = LeakyBucket(drain_rate=1, capacity=10)

    t1 = threading.Thread(target=request_task, args=(bucket,))
    t2 = threading.Thread(target=consumer_task, args=(bucket,))


    t1.start()
    t2.start()


    # wait until threads finish their job
    t1.join()
    t2.join()

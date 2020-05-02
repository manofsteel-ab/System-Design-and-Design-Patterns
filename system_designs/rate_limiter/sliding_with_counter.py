import time
import threading

class RequestCounter:
    def __init__(self, allowed_requests, window_time_in_second, bucket_size):
        self.allowed_requests = allowed_requests
        self.window_time_in_second = window_time_in_second
        self.bucket_size = bucket_size
        self.counter = {}
        self.total_counts = 0
        self.lock = threading.Lock()

    def get_bucket(self, timestamp):
        pass

    def get_oldest_bucket(self, current_timestamp):
        pass

    def remove_older_buckets(self, current_timestamp):
        pass

class SlidingWindowCounterRateLimiter:
    def __init__(self):
		self.lock = threading.Lock()
		self.rate_limiter = {}

    def add_user_config(self):
        pass

    def remover_user(self, user_id):
        pass

    def get_timestamp_in_second(self):
        pass

    def is_allowed(self, user_id):
        pass

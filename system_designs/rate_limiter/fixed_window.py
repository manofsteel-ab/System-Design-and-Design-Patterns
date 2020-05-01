from abc import ABC, abstractmethod
import threading

import time
import random


# Rate limit(per minut) Configuration api level, user level
class Configuration:
    def __init__(self):
        self.total_call = 50
        self.api = {'api_1': 10, 'api_2': 10}
        self.user = {'user_1': 10, 'user_2':20}
        self.user_api = {
            'user_1_api_1': 5, 'user_2_api_1':10,
            'user_1_api_2': 5, 'user_2_api_2':10,
        }

class RateLimiterInterface(ABC):

    def __init__(self):
        self.api_db = {} # ex: key=api_1_12:00 and value will be freq
        self.user_db = {} # ex. key=user_1_12:00 and value will be freq
        self.user_api_db = {} # ex. key=user_1_api_1_12:00 and value will be freq
        self.total_call_db = {} # ex. key=12:00 and value will be freq

    @abstractmethod
    def allow(self):
        pass

    def get_current_time(self):
        return int(time.time())



class FixedWindowRateLimiter(RateLimiterInterface):

    def __init__(self):
        super().__init__()

    def allow(self):
        pass

class SendRequest:

    @classmethod
    def request_task(cls):
        users = ['user_1', 'user_2']
        apis = ['api_1', 'api_2']

        while True:
            user = (random.randint(1, 100))%2
            api = (random.randint(1, 100))%2

import time

class SimpleCache(object):

    def __init__(self, capacity=1000):
        self.cache = {}
        self.capacity = capacity
        self.used_keys = {}

    def get(self, key):
        if key in self.cache:
            self.used_keys[key] = int(time.time())
            return self.cache[key]
        return None

    def set(self, key, value):
        if len(self.cache) >= self.capacity:
            least_used_key = min(self.used_keys.keys(), key=lambda k:self.used_keys[k])
            del self.cache[least_used_key]
            del self.used_keys[least_used_key]

        self.cache[key] = value
        self.used_keys[key] = int(time.time())

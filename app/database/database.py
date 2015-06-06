from pymongo import MongoClient

class MongoConnection(object):
    _instance = None
    def __init__(self):
        if not self._instance:
            self._instance = MongoClient().test_db

    def get_connection(self):
        return self._instance

mongo_connection = MongoConnection()

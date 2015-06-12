from motor import MotorClient
from tornado.concurrent import Future
from bson.objectid import ObjectId
import copy

DATABASE = {}


class ToList(object):
    def __init__(self, database, name):
        self.database = database
        self.name = name
        self.slice = slice(0, 10, None)

    def __getitem__(self, value):
        self.slice = value
        return self

    def to_list(self, aux):
        future = Future()
        result = self.database[self.name][self.slice.start:self.slice.stop]
        future.set_result(copy.deepcopy(result))
        return future

class Collection(object):

    def __init__(self, database, name):
        self.database = database
        self.name = name
        self.database[self.name] = []

    def find(self):
        return ToList(self.database, self.name)

    def insert(self, value):
        future = Future()
        id = ObjectId()
        value['_id'] = id
        self.database[self.name].append(value)
        future.set_result(id)
        return future

    def count(self):
        future = Future()
        count = len(self.database[self.name])
        future.set_result(count)
        return future

    def remove(self, query):
        future = Future()
        value_query = query.values()[0]
        key_query = query.keys()[0]
        element = [ele for ele in self.database[self.name] if ele.get(key_query) == value_query]
        self.database[self.name].remove(element[0])
        future.set_result(True)
        return future

    def find_one(self, query):
        future = Future()
        value_query = query.values()[0]
        key_query = query.keys()[0]
        element = [ele for ele in self.database[self.name] if ele.get(key_query) == value_query]
        if element == []:
            future.set_result(None)
        else:
            future.set_result(element[0])
        return future

    def update(self, query, modifier):
        future = Future()
        value_query = query.values()[0]
        key_query = query.keys()[0]
        element = [ele for ele in self.database[self.name] if ele.get(key_query) == value_query]

        modifier_key = modifier.keys()[0]
        modifier_value = modifier.values()[0]

        if modifier_key == "$set":
            element[0][modifier_value.keys()[0]] = modifier_value.values()[0]
        elif modifier_key == "$push":
            element[0][modifier_value.keys()[0]].append(modifier_value.values()[0])
        elif modifier_key == "$pull":
            delete_key = modifier_value.values()[0].keys()[0]
            delete_value = modifier_value.values()[0].values()[0]
            to_delete = [ele for ele in element[0][modifier_value.keys()[0]] if ele.get(delete_key) == delete_value]
            element[0][modifier_value.keys()[0]].remove(to_delete[0])

        future.set_result(True)
        return future






class FakeDatabase(object):

    def __init__(self):
        print "Creating Fake Database"
        self.Playlists = Collection(DATABASE, 'Playlists')

    def __getitem__(self, name):
        return self.Playlists

client = MotorClient()

def get_connection(db, c):
    def deal_connection(alive, error):
        if error:
            db = FakeDatabase()
        else:
            db = client.test_db
        return c(db)

    client.admin.command('ping', callback=deal_connection)

print "Getting db"

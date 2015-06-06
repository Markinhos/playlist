from app.database.database import mongo_connection

class User(object):
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def save(self):
        user = {
            'username': self.username,
            'password': self.password
        }
        return mongo_connection.get_connection().users.insert_one(user).inserted_id

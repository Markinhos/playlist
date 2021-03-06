from app.database.database import mongo_connection
from bson.objectid import ObjectId

class Playlist(object):
    def __init__(self, name):
        self.name = name
        self.songs = []
        self.id = None

    def save(self):
        playlist = {
            'name': self.name,
            'songs': self.songs
        }
        if self.id:
            return mongo_connection.get_connection().Playlists.find_one_and_update(
                    {'_id': ObjectId(self.id)},
                    {'$set':
                        {'name': self.name}
                    })
        else:
            return mongo_connection.get_connection().Playlists.insert_one(playlist).inserted_id

    def add_song(self, song):
        result = mongo_connection.get_connection().Playlists.find_one_and_update(
            {'_id': ObjectId(self.id)},
            {'$pushAll':
                {'songs' : [{
                    'spotify_id': song['song_id'],
                    'name': song['song_name']
                    }
                ]}
            })
        return result

    def delete_song(self, song_id):
        result = mongo_connection.get_connection().Playlists.find_one_and_update(
            {'_id': ObjectId(self.id)},
            {'$pull':
                {'songs' : {
                    'spotify_id': song_id,
                    }
                }
            })
        return result


    def serialize(self):
        return {
            'name': self.name,
            'songs': self.songs,
            'id': self.id
        }


    @classmethod
    def get(cls, id):
        json = mongo_connection.get_connection().Playlists.find_one({'_id': ObjectId(id)})
        playlist = Playlist(json['name'])
        playlist.id = str(json['_id'])
        playlist.songs = json['songs']
        return playlist

    @classmethod
    def delete(cls, id):
        return mongo_connection.get_connection().Playlists.delete_one({'_id': ObjectId(id)})

    @classmethod
    def get_all(cls):
        cursor = mongo_connection.get_connection().Playlists.find()
        for result in cursor:
            yield result

    @classmethod
    def list(cls):
        results = []
        for result in Playlist.get_all():
            result['id'] = str(result['_id'])
            del result['_id']
            print "Result {}".format(result)
            results.append(result)
        return results

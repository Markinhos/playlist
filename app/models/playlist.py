from bson.objectid import ObjectId
from tornado.concurrent import TracebackFuture

from app.models import base_model

class Playlist(base_model.BaseModel):
    COLLECTION = 'Playlists'

    def __init__(self, db, name, id=None, songs=None):
        self.db = db
        self.name = name
        self.songs = [] if songs is None else songs
        self.id = id

    def save(self):
        playlist = {
            'name': self.name,
            'songs': self.songs
        }
        if self.id:
            return self.db.Playlists.update(
                    {'_id': ObjectId(self.id)},
                    {'$set':
                        {'name': self.name}
                    })
        else:
            return self.db.Playlists.insert(playlist)

    def add_song(self, song):
        return self.db.Playlists.update(
            {'_id': ObjectId(self.id)},
            {'$push':
                {'songs' : {
                    'spotify_id': song['song_id'],
                    'name': song['song_name']
                    }
                }
            })

    def delete_song(self, song_id):
        return self.db.Playlists.update(
            {'_id': ObjectId(self.id)},
            {'$pull':
                {'songs' : {
                    'spotify_id': song_id,
                    }
                }
            })

    def serialize(self):
        return {
            'name': self.name,
            'songs': self.songs,
            'id': self.id
        }

    @classmethod
    def get(cls, db, id):
        future = TracebackFuture()
        def handle_response(response, error):
            playlist = Playlist(db, response['name'], id=str(response['_id']), songs=response['songs'])
            future.set_result(playlist)
        db.Playlists.find_one({'_id': ObjectId(id)}, callback=handle_response)
        return future

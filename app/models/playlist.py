from bson.objectid import ObjectId
from tornado.concurrent import TracebackFuture

class Playlist(object):
    def __init__(self, db, name):
        self.db = db
        self.name = name
        self.songs = []
        self.id = None

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
            playlist = Playlist(db, response['name'])
            playlist.id = response['_id']
            playlist.songs = response['songs']
            future.set_result(playlist)
        db.Playlists.find_one({'_id': ObjectId(id)}, callback=handle_response)
        return future

    @classmethod
    def delete(cls, db, id):
        return db.Playlists.remove({'_id': ObjectId(id)})

    @classmethod
    def list(cls, db):
        future = TracebackFuture()
        def handle_response(response, error):
            if error:
                print "Error"
            else:
                results = []
                for result in response:
                    result['id'] = str(result['_id'])
                    del result['_id']
                    results.append(result)
                future.set_result(results)
        db.Playlists.find().to_list(None, callback=handle_response)
        return future

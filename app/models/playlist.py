from bson.objectid import ObjectId
from tornado.concurrent import TracebackFuture

class BaseModel(object):
    """Base Model class for manipulating records in the db"""

    @classmethod
    def delete(cls, db, id):
        return db[cls.COLLECTION].remove({'_id': ObjectId(id)})

    @classmethod
    def list(cls, db):
        future = TracebackFuture()
        # Handles the response from the db. Replaces _id:ObjectId for id:str
        def handle_response(response, error):
            if error:
                print "Error! {}".format(error)
            else:
                results = []
                for result in response:
                    result['id'] = str(result['_id'])
                    del result['_id']
                    results.append(result)
                future.set_result(results)
        db[cls.COLLECTION].find().to_list(None, callback=handle_response)
        return future

class Playlist(BaseModel):
    """Playlist model to perform CRUD actions and atomic adds/deletes over fields"""
    COLLECTION = 'Playlists'

    def __init__(self, db, name, id=None, songs=None):
        self.db = db
        self.name = name
        self.songs = [] if songs is None else songs
        self.id = id

    def save(self):
        """Save the object into the database
            if the object has an id updates otherwise inserts"""
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
        """Add a song into the collections of songs.
            Performs the operation atomically so there is no problem of
            concurrency"""
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
        """Deletes a song from the collections of songs.
            Performs the operation atomically so there is no problem of
            concurrency"""
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
        """Get a record from the db and returns an object"""
        future = TracebackFuture()
        # Handle the response of the playlists db access
        def handle_response(response, error):
            playlist = Playlist(db, response['name'], id=str(response['_id']), songs=response['songs'])
            future.set_result(playlist)
        db.Playlists.find_one({'_id': ObjectId(id)}, callback=handle_response)
        return future

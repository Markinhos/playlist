from bson.objectid import ObjectId
from tornado.concurrent import Future

class BaseModel(object):
    """Base Model class for manipulating records in the db"""

    @classmethod
    def delete(cls, db, id):
        """Deletes a document from the db.
            Args:
                db: the database driver
                id: the id of the document to be deleted

            Returns:
                Future. Holds the id of the document deleted
        """
        return db[cls.COLLECTION].remove({'_id': ObjectId(id)})

    @classmethod
    def list(cls, db, offset=0, limit=20):
        """Gets all the records from the db
            Args:
                db: the database driver

            Returns:
                Future. Holds a list of dicts with the values
        """
        future = Future()
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

        if offset == 0:
            db[cls.COLLECTION].find()[:limit].to_list(None, callback=handle_response)
        else:
            db[cls.COLLECTION].find()[offset:(offset * limit)].to_list(None, callback=handle_response)
        return future

    @classmethod
    def count(cls, db):
        """Gets the count of elements of this collection"""

        return db[cls.COLLECTION].count()

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
            if the object has an id updates otherwise inserts.

            Returns:
                Future. Holds the id of the document inserted.
        """
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
            concurrency.

            Args:
                song (dict): Dict with the fields to be inserted in the db

            Returns:
                Future: Holds the id of the document updated
        """
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
            concurrency

            Args:
                song_id (str): Id of the song to be deleted.

            Returns:
                Future. Holds the id of the deleted song."""
        return self.db.Playlists.update(
            {'_id': ObjectId(self.id)},
            {'$pull':
                {'songs' : {
                    'spotify_id': song_id,
                    }
                }
            })

    def serialize(self):
        """Returns a dict with the attributes of the object"""

        return {
            'name': self.name,
            'songs': self.songs,
            'id': self.id
        }

    @classmethod
    def get(cls, db, id):
        """Get a record from the db and returns an object

            Args:
                db: The database driver used.
                id (str): The id of the playlist to be retrieved
        """

        future = Future()
        # Handle the response of the playlists db access
        def handle_response(response, error):
            playlist = Playlist(db, response['name'], id=str(response['_id']), songs=response['songs'])
            future.set_result(playlist)
        db.Playlists.find_one({'_id': ObjectId(id)}, callback=handle_response)
        return future

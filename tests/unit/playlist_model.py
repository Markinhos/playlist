import unittest
import tornado.testing
from tornado.testing import AsyncTestCase
from tornado.gen import coroutine, Return
from tornado.concurrent import Future
from bson.objectid import ObjectId

from app.models import playlist
from mock import MagicMock, patch

class MyTestCase(AsyncTestCase):

    @tornado.testing.gen_test
    def test_delete(self):
        future = Future()
        future.set_result('Ok!')
        return_mock = MagicMock()
        return_mock.remove.return_value = future
        db = {'Playlists' : return_mock }
        response = yield playlist.Playlist.delete(db, "556f146fcf01fd499c7affc1")
        db['Playlists'].remove.assert_called_once_with({ '_id': ObjectId("556f146fcf01fd499c7affc1")})

    @patch('app.models.playlist.Playlist._list')
    @tornado.testing.gen_test
    def test_list(self, _list_mock_pass):
        future = Future()
        future.set_result([
            {
                '_id': ObjectId("5579e044ecbc55234af148cf"),
                'name': 'test'
            },
            {
                '_id': ObjectId("5579e044ecbc55234af148ca"),
                'name': 'test2'
            }
        ])

        _list_mock_pass.return_value = future
        response = yield playlist.Playlist.list("Fake db", "556f146fcf01fd499c7affc1")
        playlist.Playlist._list.assert_called_once_with("Fake db", offset=0, limit=20)
        assert response == [
            {
                'id': "5579e044ecbc55234af148cf",
                'name': 'test'
            },
            {
                'id': "5579e044ecbc55234af148ca",
                'name': 'test2'
            }
        ], response

    @tornado.testing.gen_test
    def test_count(self):
        future = Future()
        future.set_result('Ok!')
        return_mock = MagicMock()
        return_mock.count.return_value = future
        db = {'Playlists' : return_mock }
        response = yield playlist.Playlist.count(db)
        db['Playlists'].remove.assert_called_once()


    @tornado.testing.gen_test
    def test_add_song(self):
        future = Future()
        future.set_result('Ok!')
        return_mock = MagicMock()
        return_mock.update.return_value = future
        db = {'Playlists' : return_mock }

        _playlist = playlist.Playlist(db, "test", "5579e044ecbc55234af148ca")
        response = yield _playlist.add_song({
            'song_id': "1234",
            'song_name': "test_song"
        })
        db['Playlists'].update.assert_called_once_with({'_id': ObjectId("5579e044ecbc55234af148ca")},
            {'$push':
                {'songs' : {
                    'spotify_id': "1234",
                    'name': "test_song"
                    }
                }
            })

    @tornado.testing.gen_test
    def test_delete_song(self):
        future = Future()
        future.set_result('Ok!')
        return_mock = MagicMock()
        return_mock.update.return_value = future
        db = {'Playlists' : return_mock }

        _playlist = playlist.Playlist(db, "test", "5579e044ecbc55234af148ca")
        response = yield _playlist.delete_song("1234")

        db['Playlists'].update.assert_called_once_with({'_id': ObjectId("5579e044ecbc55234af148ca")},
            {'$pull':
                {'songs' : {
                    'spotify_id': "1234"
                    }
                }
            })

    @tornado.testing.gen_test
    def test_update(self):
        future = Future()
        future.set_result('Ok!')
        return_mock = MagicMock()
        return_mock.update.return_value = future
        db = {'Playlists' : return_mock }

        _playlist = playlist.Playlist(db, "test", "5579e044ecbc55234af148ca")
        _playlist.name = "test2"
        response = yield _playlist.save()

        db['Playlists'].update.assert_called_once_with({'_id': ObjectId("5579e044ecbc55234af148ca")},
            {'$set':
                { 'name' : "test2" }
            })

    @tornado.testing.gen_test
    def test_create(self):
        future = Future()
        future.set_result('Ok!')
        return_mock = MagicMock()
        return_mock.insert.return_value = future
        db = {'Playlists' : return_mock }

        _playlist = playlist.Playlist(db, "test")
        response = yield _playlist.save()

        db['Playlists'].insert.assert_called_once_with({
            'name': "test",
            'songs': []
        })

    @patch('app.models.playlist.Playlist._find_one')
    @tornado.testing.gen_test
    def test_get(self, _get_mock_pass):
        future = Future()
        future.set_result(
            {
                '_id': ObjectId("5579e044ecbc55234af148cf"),
                'name': 'test',
                'songs': []
            }
        )

        _get_mock_pass.return_value = future
        response = yield playlist.Playlist.get("Fake db", "556f146fcf01fd499c7affc1")
        playlist.Playlist._find_one.assert_called_once_with("Fake db", "556f146fcf01fd499c7affc1")
        assert type(response) == playlist.Playlist

if __name__ == '__main__':
    unittest.main()

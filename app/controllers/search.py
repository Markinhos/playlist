import json
import urllib
from app.models.search import Search
from app.models.playlist import Playlist
from tornado import gen, httpclient
import tornado.web

class SearchTracksHandler(tornado.web.RequestHandler):

    @tornado.gen.coroutine
    def get(self):
        db = self.settings['db']
        playlist_id = self.get_argument('playlist_id')
        query = self.get_argument('q')
        tracks, playlist = yield [Search.get_tracks(query), Playlist.get(db, playlist_id)]
        self.render('playlists/get.html', search=tracks, playlist=playlist.serialize())

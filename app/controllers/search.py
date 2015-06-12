import json
import urllib
from app.models.search import Search
from app.models.playlist import Playlist
from tornado import gen, httpclient
import tornado.web

class SearchTracksHandler(tornado.web.RequestHandler):

    @tornado.gen.coroutine
    def get(self):
        """Get tracks from the API"""
        db = self.settings['db']
        playlist_id = self.get_argument('playlist_id')
        query = self.get_argument('q')
        # return tracks and playlist in parallel
        try:
            tracks, playlist = yield [Search.get_tracks(query), Playlist.get(db, playlist_id)]
        except Exception as error:
            print "Error {}".format(error)
            raise tornado.web.HTTPError(500, 'Oops, something is broken')

        self.render('playlists/get.html', search=tracks, playlist=playlist.serialize())

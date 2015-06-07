import json
import urllib
from tornado import gen, httpclient
import tornado.web

from tornado import gen
from tornado.concurrent import TracebackFuture

SPOTIFY_API_ENDPOINT='https://api.spotify.com/v1/'
SEARCH_ENDPOINT=SPOTIFY_API_ENDPOINT+'search/'
TRACKS_ENDPOINT=SPOTIFY_API_ENDPOINT+'tracks/'

CACHE = {}
class Search(object):

    @classmethod
    def get(self, query):

        future = TracebackFuture()

        if query in CACHE:
            tracks = CACHE[query]
            future.set_result(tracks)
        else:
            http_client = httpclient.AsyncHTTPClient()
            tracks_url = "{}?{}".format(SEARCH_ENDPOINT, urllib.urlencode({'q': query, 'type': 'track'}))

            def handle_response(response):
                tracks = json.loads(response.body)['tracks']['items']
                CACHE[query] = tracks
                future.set_result(tracks)

            http_client.fetch(tracks_url, callback=handle_response)

        return future

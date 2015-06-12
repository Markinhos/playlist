import json
import urllib
from tornado import gen, httpclient
import tornado.web
from tornado.web import gen

from tornado import gen
from tornado.concurrent import Future

SPOTIFY_API_ENDPOINT='https://api.spotify.com/v1/'
SEARCH_ENDPOINT=SPOTIFY_API_ENDPOINT+'search/'
TRACKS_ENDPOINT=SPOTIFY_API_ENDPOINT+'tracks/'

CACHE = {}
class Search(object):

    @classmethod
    @gen.coroutine
    def get_tracks(cls, query):
        """Search tracks in the Spotify API the query gotten from the parameter.
            Checks if it is in the cache before making the http call.

            Args:
                query (string): query term to be used in the API search

            Returns:
                Future. When resolved the future holds the tracks found.
        """

        if query in CACHE:
            tracks = CACHE[query]
        else:
            response = yield cls._fetch(query)
            tracks = cls._handle_search_response(response)
            CACHE[query] = tracks

        raise gen.Return(tracks)

    @classmethod
    def _handle_search_response(cls, response):
        return json.loads(response.body)['tracks']['items']

    @classmethod
    def _fetch(cls, query):
        http_client = httpclient.AsyncHTTPClient()
        tracks_url = "{}?{}".format(SEARCH_ENDPOINT, urllib.urlencode({'q': query, 'type': 'track'}))
        return http_client.fetch(tracks_url)

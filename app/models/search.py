import json
import urllib
from tornado import gen, httpclient
import tornado.web

from tornado import gen
from tornado.concurrent import Future

SPOTIFY_API_ENDPOINT='https://api.spotify.com/v1/'
SEARCH_ENDPOINT=SPOTIFY_API_ENDPOINT+'search/'
TRACKS_ENDPOINT=SPOTIFY_API_ENDPOINT+'tracks/'

CACHE = {}
class Search(object):

    @classmethod
    def get_tracks(self, query):
        """Search tracks in the Spotify API the query gotten from the parameter.
            Checks if it is in the cache before making the http call.

            Args:
                query (string): query term to be used in the API search

            Returns:
                Future. When resolved the future holds the tracks found.               
        """
        future = Future()

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

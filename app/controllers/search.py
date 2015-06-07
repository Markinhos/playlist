import urllib
import json

SPOTIFY_API_ENDPOINT='https://api.spotify.com/v1/'
SEARCH_ENDPOINT=SPOTIFY_API_ENDPOINT+'search/'
TRACKS_ENDPOINT=SPOTIFY_API_ENDPOINT+'tracks/'

def search(query):
    results = {}
    tracks = urllib.urlopen("{}?{}".format(SEARCH_ENDPOINT, urllib.urlencode({'q': query, 'type': 'track'}))).read()
    results.update(json.loads(tracks))
    albums = urllib.urlopen("{}?{}".format(SEARCH_ENDPOINT, urllib.urlencode({'q': query, 'type': 'album'}))).read()
    results.update(json.loads(albums))
    artists = urllib.urlopen("{}?{}".format(SEARCH_ENDPOINT, urllib.urlencode({'q': query, 'type': 'artist'}))).read()
    results.update(json.loads(artists))
    return results

def get(spotify_id):
    song = urllib.urlopen("{}{}".format(TRACKS_ENDPOINT,spotify_id)).read()
    return json.loads(song)

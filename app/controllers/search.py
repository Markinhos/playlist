import urllib
import json
from app.models.playlist import Playlist
from flask import render_template, request, redirect, url_for
from werkzeug.contrib.cache import SimpleCache
cache = SimpleCache()

SPOTIFY_API_ENDPOINT='https://api.spotify.com/v1/'
SEARCH_ENDPOINT=SPOTIFY_API_ENDPOINT+'search/'
TRACKS_ENDPOINT=SPOTIFY_API_ENDPOINT+'tracks/'

def search():
    playlist_id = request.args.get('playlist_id')
    playlist = Playlist.get(playlist_id)
    query = request.args.get('q')
    tracks = cache.get(query)
    if tracks is None:
        tracks = json.loads(urllib.urlopen("{}?{}".format(SEARCH_ENDPOINT, urllib.urlencode({'q': query, 'type': 'track'}))).read())
        cache.set(query, tracks, timeout=5*60)
    return render_template('playlists/get.html', search=tracks['tracks']['items'], playlist=playlist)

def get(spotify_id):
    song = json.loads(urllib.urlopen("{}{}".format(TRACKS_ENDPOINT,spotify_id)).read())
    playlists = Playlist.list()
    return render_template('songs/get.html', song=song, playlists=playlists)

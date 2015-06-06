import urllib

SPOTIFY_API_ENDPOINT='https://api.spotify.com/v1/search/'

def search(query):
    r = urllib.urlopen("{}?{}".format(SPOTIFY_API_ENDPOINT, urllib.urlencode({'q': query, 'type': 'artist'})))
    return r.read()

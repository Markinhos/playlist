from app.models.playlist import Playlist

def list():
    return Playlist.list()

def insert(name):
    playlist = Playlist(name)
    return playlist.save()

def find_one(id):
    return Playlist.find(id).serialize()

def delete(id):
    return Playlist.delete(id)

def edit(id, name):
    playlist = Playlist.find(id)
    playlist.name = name
    return playlist.save()

def add_song(id, song):
    playlist = Playlist.find(id)
    return playlist.add_song(song)

def delete_song(id, song_id):
    playlist = Playlist.find(id)
    return playlist.delete_song(song_id)

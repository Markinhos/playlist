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

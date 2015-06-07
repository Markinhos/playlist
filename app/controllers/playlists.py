from flask import render_template, request, redirect, url_for
from app.models.playlist import Playlist

def list():
    return render_template('playlists/list.html', playlists=Playlist.list())

def create(name):
    name = request.form.get('name')
    playlist = Playlist(name)
    playlist.save()
    return redirect(url_for('playlists'))

def get(id):
    playlist = Playlist.get(id).serialize()
    return render_template('playlists/get.html', playlist=playlist)

def delete(id):
    return Playlist.delete(id)

def edit(id, name):
    playlist = Playlist.get(id)
    playlist.name = name
    return playlist.save()

def add_song(id, song):
    playlist = Playlist.get(id)
    return playlist.add_song(song)

def delete_song(id, song_id):
    playlist = Playlist.get(id)
    return playlist.delete_song(song_id)

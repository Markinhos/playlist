from flask import render_template, request, redirect, url_for
from app.models.playlist import Playlist

def list():
    return render_template('playlists/list.html', playlists=Playlist.list())

def create():
    name = request.form.get('name')
    playlist = Playlist(name)
    playlist.save()
    return redirect(url_for('playlists'))

def get(id):
    playlist = Playlist.get(id).serialize()
    return render_template('playlists/get.html', playlist=playlist)

def delete(id):
    Playlist.delete(id)
    return redirect(url_for('playlists'))

def edit(id):
    name = request.form.get('name')
    playlist = Playlist.get(id)
    playlist.name = name
    playlist.save()
    return redirect(url_for('playlist', id=id))

def add_song():
    playlist_id = request.form.get('playlist_id')
    song_name = request.form.get('song_name')
    song_id = request.form.get('song_id')
    playlist = Playlist.get(playlist_id)
    playlist.add_song({
        'song_id': song_id,
        'song_name': song_name
    })
    return redirect(url_for('playlist', id=playlist_id))

def delete_song(playlist_id):
    song_id = request.form.get('song_id')
    playlist = Playlist.get(playlist_id)
    playlist.delete_song(song_id)
    return redirect(url_for('playlist', id=playlist.id))

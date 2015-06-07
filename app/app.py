from flask import Flask, send_from_directory, jsonify
from flask import render_template, request, redirect, url_for

from controllers import playlists as playlist_controller
from controllers import search as search_controller

app = Flask(__name__)

@app.route("/")
def index():
    return redirect(url_for('playlists'))

@app.route("/static/<path:path>")
def send_static(path):
    return send_from_directory('static', path)

@app.route("/playlists/", methods=['GET', 'POST'])
def playlists():
    if request.method == 'POST':
        return playlist_controller.create()
    elif request.method == 'GET':
        return playlist_controller.list()


@app.route("/playlists/<id>")
def playlist(id):
    return playlist_controller.get(id)


@app.route("/delete_playlist/<id>", methods=['POST'])
def delete_playlist(id):
    return playlist_controller.delete(id)


@app.route("/edit_playlist/<id>", methods=['POST', 'GET'])
def edit_playlist(id):
    if request.method == 'GET':
        playlist = playlist_controller.get(id)
        return render_template('playlists/edit.html', playlist=playlist)
    elif request.method == 'POST':
        return playlist_controller.edit(id)

@app.route("/add_song", methods=['POST'])
def add_song():
    return playlist_controller.add_song()


@app.route("/delete_song/<playlist_id>", methods=['POST'])
def delete_song(playlist_id):
    return playlist_controller.delete_song(playlist_id)


@app.route("/search")
def search():
    return search_controller.search()


# @app.route("/songs/<spotify_id>")
# def get_song(spotify_id):
#     return search_controller.get(spotify_id)

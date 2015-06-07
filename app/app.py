from flask import Flask, send_from_directory, jsonify
from flask import render_template, request, redirect, url_for

from controllers import playlists as playlist_controller
from controllers import search as search_controller

from bson import json_util

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
        name = request.form.get('name')
        playlist_controller.insert(name)
        return redirect(url_for('playlists'))
    elif request.method == 'GET':
        return render_template('playlists/list.html', playlists=playlist_controller.list())


@app.route("/playlists/<id>")
def playlist(id):
    if request.method == 'PUT':
        playlist_controller.insert(name)
        return redirect(url_for('playlists'))
    elif request.method == 'GET':
        playlist = playlist_controller.find_one(id)
        print "PLAYLIST {}".format(playlist)
        return render_template('playlists/get.html', playlist=playlist)


@app.route("/delete_playlist/<id>", methods=['POST'])
def delete_playlist(id):
    status = playlist_controller.delete(id)
    return redirect(url_for('playlists'))


@app.route("/edit_playlist/<id>", methods=['POST', 'GET'])
def edit_playlist(id):
    if request.method == 'GET':
        playlist = playlist_controller.find_one(id)
        return render_template('playlists/edit.html', playlist=playlist)
    elif request.method == 'POST':
        name = request.form.get('name')
        playlist_controller.edit(id, name)
        return redirect(url_for('playlist', id=id))

@app.route("/add_song", methods=['POST'])
def add_song():
    playlist_id = request.form.get('playlist')
    song_name = request.form.get('song_name')
    song_id = request.form.get('song_id')
    playlist_controller.add_song(playlist_id, {
        'song_id': song_id,
        'song_name': song_name
    })
    return redirect(url_for('playlist', id=playlist_id))


@app.route("/delete_song/<playlist_id>", methods=['POST'])
def delete_song(playlist_id):
    song_id = request.form.get('song_id')
    playlist_controller.delete_song(playlist_id, song_id)
    return redirect(url_for('playlist', id=playlist_id))


@app.route("/search")
def search():
    query = request.args.get('q')
    # print "Result {}".format(search_controller.search(query))
    result = search_controller.search(query)
    return render_template('search.html', playlists=playlists, artists=result['artists']['items'], albums=result['albums']['items'], songs=result['tracks']['items'])
    # return jsonify(result)


@app.route("/songs/<spotify_id>")
def get_song(spotify_id):
    song = search_controller.get(spotify_id)
    playlists = playlist_controller.list()
    return render_template('songs/get.html', song=song, playlists=playlists)


@app.route("/api/v1/playlists/", methods=['GET', 'POST'])
def api_playlists():
    if request.method == 'POST':
        data = request.get_json()
        playlist_controller.insert(data['name'])
        return '', 201
    elif request.method == 'GET':
        return jsonify(result=playlist_controller.list())

@app.route("/api/v1/playlists/<id>", methods=['GET', 'PUT'])
def api_playlist(id):
    if request.method == 'PUT':
        playlist_controller.insert(name)
        return redirect(url_for('playlists'))
    elif request.method == 'GET':
        return jsonify(result=playlist_controller.find_one(id))

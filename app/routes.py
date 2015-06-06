from flask import send_from_directory, jsonify
from flask import render_template, request, redirect, url_for

from controllers import users as user_controller
from controllers import playlists as playlist_controller

from bson import json_util

@app.route("/")
def index():
    return render_template('index.html', playlists=playlists)

@app.route("/static/<path:path>")
def send_static(path):
    return send_from_directory('static', path)


@app.route("/users/", methods=['GET', 'POST'])
def users():
    if request.method == 'POST':
        data = request.get_json()
        id = str(user_controller.insert_user(data['username'], data['password']))
        return redirect(url_for('index'))


@app.route("/playlists/", methods=['GET', 'POST', 'DELETE', 'PUT'])
def playlists():
    if request.method == 'POST':
        name = request.form.get('name')
        playlist_controller.insert(name)
        return redirect(url_for('playlists'))
    elif request.method == 'GET':
        return render_template('index.html', playlists=playlist_controller.list())

@app.route("/api/v1/playlists/", methods=['GET', 'POST', 'DELETE', 'PUT'])
def api_playlists():
    if request.method == 'POST':
        data = request.get_json()
        playlist_controller.insert(data['name'])
        return '', 201
    elif request.method == 'GET':
        return render_template('index.html', playlists=playlist_controller.list())

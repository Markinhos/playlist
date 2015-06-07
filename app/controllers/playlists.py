from flask import render_template, request, redirect, url_for
from app.models.playlist import Playlist

import tornado.web

class PlaylistHandler(tornado.web.RequestHandler):

    @tornado.gen.coroutine
    def get(self, id):
        db = self.settings['db']
        playlist = yield Playlist.get(db, id)
        self.render('playlists/get.html', playlist=playlist.serialize(), search=[])

    @tornado.gen.coroutine
    def post(self, id):
        db = self.settings['db']
        playlist = yield Playlist.get(db, id)
        playlist.name = self.get_argument('name')
        yield playlist.save()
        self.redirect('/playlists/{}'.format(id))

class PlaylistsHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self):
        db = self.settings['db']
        results = yield Playlist.list(db)
        self.render('playlists/list.html',playlists=results)

    @tornado.gen.coroutine
    def post(self):
        db = self.settings['db']
        name = self.get_argument('name')
        playlist = Playlist(db, name)
        yield playlist.save()
        self.redirect('/playlists/')

class DeletePlaylistHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def post(self, id):
        db = self.settings['db']
        yield Playlist.delete(db, id)
        self.redirect('/playlists/')

class AddSongHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def post(self, id):
        db = self.settings['db']
        song_id = self.get_argument('song_id')
        song_name = self.get_argument('song_name')
        playlist = yield Playlist.get(db, id)
        yield playlist.add_song({
            'song_id': song_id,
            'song_name': song_name
        })
        self.redirect('/playlists/{}'.format(id))

class DeleteSongHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def post(self, id):
        db = self.settings['db']
        song_id = self.get_argument('song_id')
        playlist = yield Playlist.get(db, id)
        yield playlist.delete_song(song_id)
        self.redirect('/playlists/{}'.format(id))

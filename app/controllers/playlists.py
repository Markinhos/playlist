from flask import render_template, request, redirect, url_for
from app.models.playlist import Playlist

import tornado.web

"""Access model to get the information and setup the proper answer"""

LIMIT_PAGINATION = 10

class PlaylistHandler(tornado.web.RequestHandler):
    """Controller for a concrete playlists."""
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
    """Controller for playlists"""
    @tornado.gen.coroutine
    def get(self):
        db = self.settings['db']
        offset = self.get_argument('offset', default=0)
        limit = self.get_argument('limit', default=LIMIT_PAGINATION)
        results = yield Playlist.list(db, int(offset), int(limit))
        count = yield Playlist.count(db)
        self.render('playlists/list.html',playlists=results, count=count, limit=LIMIT_PAGINATION)

    @tornado.gen.coroutine
    def post(self):
        db = self.settings['db']
        name = self.get_argument('name')
        playlist = Playlist(db, name)
        yield playlist.save()
        self.redirect('/playlists/')

class DeletePlaylistHandler(tornado.web.RequestHandler):
    """Controller for a delete operation in the Playlists collection.
        Used POST as is intented to use with html forms"""
    @tornado.gen.coroutine
    def post(self, id):
        db = self.settings['db']
        yield Playlist.delete(db, id)
        self.redirect('/playlists/')

class AddSongHandler(tornado.web.RequestHandler):
    """Add song controller"""
    @tornado.gen.coroutine
    def post(self, id):
        db = self.settings['db']
        song_id, song_name = self._get_songs_arguments()
        playlist = yield Playlist.get(db, id)
        yield playlist.add_song({
            'song_id': song_id,
            'song_name': song_name
        })
        self.redirect('/playlists/{}'.format(id))

    def _get_songs_arguments(self):
        return self.get_argument('song_id'), self.get_argument('song_name')

class DeleteSongHandler(tornado.web.RequestHandler):
    """Delete song controller"""
    @tornado.gen.coroutine
    def post(self, id):
        db = self.settings['db']
        song_id = self.get_argument('song_id')
        playlist = yield Playlist.get(db, id)
        yield playlist.delete_song(song_id)
        self.redirect('/playlists/{}'.format(id))

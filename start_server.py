from datetime import date
import tornado.ioloop
import tornado.web
import os
from motor import MotorClient

from app.controllers import playlists, search
from app.database import database

application = tornado.web.Application([
    (r"/", tornado.web.RedirectHandler,
        dict(url="/playlists/")),
    (r"/playlists/(.+)", playlists.PlaylistHandler),
    (r"/playlists/", playlists.PlaylistsHandler),
    (r"/delete_playlist/(.*)", playlists.DeletePlaylistHandler),
    (r"/delete_song/(?P<id>[^\/]+)?", playlists.DeleteSongHandler),
    (r"/add_song/(?P<id>[^\/]+)?", playlists.AddSongHandler),
    (r"/search", search.SearchTracksHandler)
],
    template_path=os.path.join(os.path.dirname(__file__), "app/templates"),
    debug=True,
)

def assign_database(_db):
    application.settings['db'] = _db

db = None
database.get_connection(db, assign_database)

if __name__ == "__main__":
    application.listen(5000)
    tornado.ioloop.IOLoop.instance().start()

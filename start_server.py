from datetime import date
import tornado.escape
import tornado.ioloop
import tornado.web
import os
from motor import MotorClient

from app.controllers import playlists, search

client = MotorClient()
db = client.test_db

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
    db=db
)

if __name__ == "__main__":
    application.listen(5000)
    tornado.ioloop.IOLoop.instance().start()

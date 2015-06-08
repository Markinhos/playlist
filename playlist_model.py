import unittest
import tornado.testing
from tornado.testing import AsyncTestCase

import app


class MyTestCase(AsyncTestCase):
    @tornado.testing.gen_test
    def test_http_fetch(self):
        response = yield playlists.list({})
        # Test contents of response
        self.assertIn("FriendFeed", response.body)

if __name__ == '__main__':
    unittest.main()

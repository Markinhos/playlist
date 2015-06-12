import unittest
import tornado.testing
from tornado.testing import AsyncTestCase
from tornado.gen import coroutine, Return
from tornado.concurrent import Future

from app.models import search
from mock import MagicMock, patch


class ResponseFetch(object):
    def __init__(self, result):
        self.body = result

class MyTestCase(AsyncTestCase):

    @patch('app.models.search.Search._fetch')
    @tornado.testing.gen_test
    def test_search(self, _fetch_mock_pass):
        future = Future()

        future.set_result(ResponseFetch('{"tracks": {"items": [{"id": "5579e044ecbc55234af148cf", "name": "song1"}]}}'))

        _fetch_mock_pass.return_value = future
        response = yield search.Search.get_tracks("the who")
        search.Search._fetch.assert_called_once_with("the who")
        assert response == [
            {
                'id': "5579e044ecbc55234af148cf",
                'name': 'song1'
            }
        ]

if __name__ == '__main__':
    unittest.main()

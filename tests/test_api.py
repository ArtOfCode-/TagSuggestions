import api
from unittest import TestCase


class TestApi(TestCase):
    apiRequester = None

    def test_init(self):
        self.apiRequester = api.APIRequester("stackoverflow")
        self.assertTrue(isinstance(self.apiRequester, api.APIRequester))
        self.assertEqual("stackoverflow", self.apiRequester.site)

    def test_request_without_data(self):
        try:
            response, has_more, backoff = self.apiRequester.request("/questions", None)
        except:
            self.fail("APIRequester.request throws unexpected error")

    def test_request_api_error(self):
        try:
            response, has_more, backoff = self.apiRequester.request("/nosuchmethod", None)
        except api.APIException as ex:
            self.assertTrue(ex.id is not None and ex.message is not None and ex.name is not None)
        else:
            self.fail("API did not provide error on nonexistent method")

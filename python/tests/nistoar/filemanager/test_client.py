import unittest
import responses
from nistoar.filemanager.client import BaseClient
from nistoar.filemanager.client import WebDavClient
from tests.nistoar.filemanager.webdav_server import WebDavTestServer


class ClientTest(unittest.TestCase):
    def setUp(self):
        self.client = BaseClient(base_url="http://127.0.0.1:8880")

    def tearDown(self):
        pass

    def test_construct_url(self):
        client = BaseClient(
            base_url="https://nextcloud.com/test/client", api_url="sharing"
        )
        full_url = client.construct_url(extra_url="files")
        expected_url = "https://nextcloud.com/test/client/sharing/files"
        self.assertTrue(full_url == expected_url)

    @responses.activate
    def test_get_using_responses_lib(self):
        responses.add(
            **{
                "method": responses.GET,
                "url": "http://example.com/api",
                "body": '{"status": "up"}',
                "status": 200,
                "content_type": "application/json",
            }
        )

        client = BaseClient(base_url="http://example.com", api_url="api")
        response = client.get()

        self.assertTrue(response.json() == {"status": "up"})
        self.assertTrue(client.construct_url() == "http://example.com/api")
        self.assertTrue(response.status_code == 200)

    def test_get(self):
        with WebDavTestServer(blocking=False) as server:
            response = self.client.get()
            self.assertTrue(response.status_code == 200)


class WebDavClientTest(unittest.TestCase):
    def setUp(self):
        self.webdav_client = WebDavClient(base_url="http://127.0.0.1:8880")

    def tearDown(self):
        pass

    def test_mkcol(self):
        with WebDavTestServer(blocking=False) as server:
            response = self.webdav_client.make_collection(url="my_collection")
            self.assertTrue(response.status_code == 201)


if __name__ == "__main__":
    unittest.main()

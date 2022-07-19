from lib2to3.pytree import Base
from urllib import response
import responses
from nistoar.filemanager.client import BaseClient


def test_construct_url():
    client = BaseClient(base_url="https://nextcloud.com/test/client", api_url="sharing")
    full_url = client.construct_url(extra_url="files")
    expected_url = "https://nextcloud.com/test/client/sharing/files"
    assert full_url == expected_url


@responses.activate
def test_get():
    responses.add(**{
      'method'         : responses.GET,
      'url'            : 'http://example.com/api',
      'body'           : '{"status": "up"}',
      'status'         : 200,
      'content_type'   : 'application/json'
    })

    client = BaseClient(base_url="http://example.com", api_url="api")
    response = client.get()

    assert response.json() == {"status": "up"}
    assert client.construct_url() == "http://example.com/api"
    assert response.status_code == 200
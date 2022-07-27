from http import client
import unittest
import docker

from tests.nistoar.filemanager.webdav_server import Container

CONTAINER_OPTIONS = {
    "image": "bytemark/webdav",
    "name": "webdav_testserver",
    "ports": {"80/tcp": 8095},
    "volumes": ["/Users/one1/webdav:/var/lib/dav"],
    "env": ["AUTH_TYPE=Basic", "USERNAME=login", "PASSWORD=password"],
    "detach": True,
    "auto_remove": True,
}


class TestContainer(unittest.TestCase):
    def setUp(self) -> None:
        self.client = docker.from_env()
        self.container = Container(**CONTAINER_OPTIONS)
        self.container.start()
        return super().setUp()

    def tearDown(self) -> None:
        self.container.stop()
        self.client.close()
        return super().tearDown()

    def get_ids(self, containers):
        return [c.id for c in containers]

    def test_run(self):
        self.assertTrue(
            self.container.id in self.get_ids(self.client.containers.list())
        )

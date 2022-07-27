import uvicorn
import docker
from loguru import logger
from multiprocessing import Event, Process
from wsgidav.wsgidav_app import WsgiDAVApp
from wsgidav.fs_dav_provider import FilesystemProvider

from nistoar.filemanager.util import create_test_folder
from nistoar.filemanager.util import initialize_logger


class BaseTestServer:
    """Base WebDav test server class."""

    def __init__(self) -> None:
        raise NotImplementedError("Should implement this!")

    def start(self):
        raise NotImplementedError("Should implement this!")

    def stop(self):
        raise NotImplementedError("Should implement this!")

    def __enter__(self):
        raise NotImplementedError("Should implement this!")

    def __exit__(self):
        raise NotImplementedError("Should implement this!")


class Container(BaseTestServer):
    """BaseTestServer implmentation using a container from the Docker SDK."""

    DEFAUL_IMAGE = "bytemark/webdav"
    DEFAULT_NAME = "webdav_testserver"
    DEFAULT_VOLUMES = ["/Users/one1/webdav:/var/lib/dav"]
    DEFAUL_ENV = ["AUTH_TYPE=Basic", "USERNAME=login", "PASSWORD=password"]
    DEFAULT_PORTS = {"80/tcp": 8095}

    def __init__(
        self,
        image=DEFAUL_IMAGE,
        name=DEFAULT_NAME,
        volumes=DEFAULT_VOLUMES,
        env=DEFAUL_ENV,
        ports=DEFAULT_PORTS,
        detach=True,
        auto_remove=True,
    ):

        self.options = {
            "image": image,
            "name": name,
            "volumes": volumes,
            "environment": env,
            "ports": ports,
            "detach": detach,
            "auto_remove": auto_remove,
        }

        self.client = docker.from_env()
        self.container = self.client.containers.create(**self.options)

    @property
    def id(self):
        """ID of the container."""
        return self.container.id
    
    @property
    def status(self):
        """Status of the container."""
        return self.container.status

    def start(self):
        """Start the container."""
        return self.container.start()

    def stop(self):
        """Stop the container."""
        if self.container:
            return self.container.stop()

    def remove(self):
        if not self.options["auto_remove"] and self.container:
            return self.container.remove()
        self.client.close()

    def __enter__(self):
        """Implement the __enter__() method for context manager.

        Starts the container.

        :return: the container
        """
        return self.start()

    def __exit__(self):
        """Implement the __exit__() method for context manager."""
        return self.stop()

    def __del__(self):
        return self.remove()


class WebDavTestServer:
    def __init__(self, config=None, provider=None, blocking=False) -> None:
        self.config = config
        if not config:
            self.config = self._get_default_config(provider)
        self.provider = provider
        self.blocking = blocking
        self.process = None
        self._ready = Event()
        self.ready_timeout = 5
        self.stop_timeout = 5

    def _run_server(self, provider=None, **kwargs):

        app = WsgiDAVApp(self.config)
        server_args = {
            "host": self.config["host"],
            "port": self.config["port"],
            "interface": "wsgi",
            "lifespan": "auto",
            "callback_notify": self.callback_notify,
        }
        uvicorn.run(app, **server_args)

    async def callback_notify(self):
        # run by uvicorn, periodically
        self._ready.set()

    @property
    def url(self):
        host = self.config["host"]
        port = self.config["port"]
        return str(f"http://{host}:{port}")

    def start(self):
        if self.blocking:
            self._run_server()
        else:
            # run the WebDavTestServer in a separate process
            kwargs = {
                "provider": self.provider,
            }
            self.process = Process(
                target=self._run_server,
                kwargs={"callback_notify": self.callback_notify, **kwargs},
            )
            self.process.daemon = True
            self.process.start()

            if not self._ready.wait(self.ready_timeout):
                raise TimeoutError(
                    f"WebDavTestServer timed out after {self.ready_timeout} seconds"
                )
            logger.info(f"WebDavTestServer is running on {self.url}...")

        return self

    def stop(self):
        if self.process:
            self.process.terminate()
            self.process.join(self.stop_timeout)
            self.process = None
        logger.info(f"WebDavTestServer stopped.")

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

    def _get_default_config(self, provider=None):
        tmp_dir = create_test_folder()
        if not provider:
            provider = FilesystemProvider(tmp_dir)
        config = {
            "host": "127.0.0.1",
            "port": 8880,
            "provider_mapping": {"/": provider},
            "verbose": 1,
            "simple_dc": {"user_mapping": {"*": True}},  # allow anonymous access
            "logging": {
                "enable_loggings": [],
            },
        }
        return config


def main():
    wd_test_server = WebDavTestServer(blocking=True)
    wd_test_server.start()


if __name__ == "__main__":
    initialize_logger(__name__, "DEBUG")
    main()

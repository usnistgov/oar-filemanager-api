import uvicorn
import sys
import logging
from loguru import logger
from multiprocessing import Event, Process
from wsgidav.wsgidav_app import WsgiDAVApp
from wsgidav.fs_dav_provider import FilesystemProvider

from nistoar.filemanager.util import create_test_folder
from nistoar.filemanager.util import initialize_logger


class WebDavTestServer:
    def __init__(self, config=None, provider=None, blocking=False) -> None:
        self.config = config
        self.provider = provider
        self.blocking = blocking
        self.process = None
        self.start_delay = 1  # second
        self._ready = Event()
        self.ready_timeout = 5
        self.stop_timeout = 5

    def _run_server(self, provider=None, **kwargs):
        if not self.config:
            self.config = self._get_default_config(provider)

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
        port = self.config["host"]
        return f"http://{host}:{port}"

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
            logger.info(f"WebDavTestServer is running...")

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
        if not self.provider:
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

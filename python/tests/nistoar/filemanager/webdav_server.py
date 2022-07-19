import uvicorn
import tempfile
import os
from wsgidav.wsgidav_app import WsgiDAVApp
from wsgidav.fs_dav_provider import FilesystemProvider


def create_test_folder(name="testfolder"):
    sys_tmp = tempfile.gettempdir()
    test_tmp = os.path.join(sys_tmp, name)
    if not os.path.exists(test_tmp):
        os.makedirs(test_tmp)
    tmp_dir = tempfile.mkdtemp(dir=test_tmp)
    print(tmp_dir)
    return tmp_dir


def get_default_config(provider=None):
    tmp_dir = create_test_folder()
    provider = FilesystemProvider(tmp_dir)
    config = {
        "host": "127.0.0.1",
        "port": 8090,
        "provider_mapping": {"/": provider},
        "verbose": 1,
        "logging": {
            "enable_loggers": [],
        },
    }
    return config


def setup_app(config):
    app = WsgiDAVApp(config)
    server_args = {
        "host": config["host"],
        "port": config["port"],
        "interface": "wsgi",
        "lifespan": "auto",
    }
    return app, server_args


class WebdavTestServer:
    def __init__(self, config=None) -> None:
        if not config:
            self.config


def main():
    config = get_default_config()
    app, args = setup_app(config=config)
    uvicorn.run(app, **args)


if __name__ == "__main__":
    main()

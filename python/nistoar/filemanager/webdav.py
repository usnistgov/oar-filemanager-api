import webdav3.client as wd


class WebDavMethod:
    PROPFIND = "PROPFIND"
    PROPPATCH = "PROPPATCH"
    MKCOL = "MKCOL"
    MOVE = "MOVE"
    COPY = "COPY"
    LOCK = "LOCK"
    UNLOCK = "UNLOCK"


DEFAULT_OPTIONS = {
    "webdav_hostname": "http://localhost:8095",
    "webdav_login": "login",
    "webdav_password": "password",
}


class Client:
    def __init__(self, options=DEFAULT_OPTIONS, verify=False) -> None:
        self._client = wd.Client(options)
        self._client.verify = verify

    def build_url(self, path):
        """Builds url using the given uri path.

        :param path: uri path.

        :return: the constructed url string.
        """
        return f"{self._client.webdav.hostname}{self._client.webdav.root}{path}"

    def info(self, path):
        """Get information about the resource on WebDAV server.

        :param path: the path to the resource.

        :return: a dictionary contained following information about the resource:
                 `created`: date when the resource was created,
                 `name`: name of the resource,
                 `size`: size of the resource,
                 `modified`: date the resource was last modified,
                 `etag`: etag of the resource,
                 `content_type`: content type of the resource.
        """
        return self._client.info(path)

    def list_resources(self, path=None, with_info=False):
        """Returns list of files and directories on the WebDAV server for given directory path.

        :param remote_path: path to remote directory.
        :param with_info: return full details about requested resources.

        :return: if with_info=False, names of resources
                 if with_info=True, details about each resource like self.info()
        """
        if not path:
            return self._client.list()
        return self._client.list(path=path, get_info=with_info)

    def create_directory(self, path=None):
        """Create a new directory on WebDAV server.

        :param path: path to the directory to create.

        :return: True if request executed with code 200 or 201 and False otherwise.
        """
        return self._client.mkdir(path)

    def request(self, action, path, data=None, extra_headers=None):
        """Generate a raw request to WebDAV server using given action and path and execute it.

        :param action: the action to excute.
        :param path: the path to the resource.
        :param data: optional. data to send in the body of the request.

        :return: HTTP response of request.
        """
        return self._client.execute_request(
            action=action, path=path, data=data, headers_ext=extra_headers
        )


def main():
    webdavClient = Client()
    print(webdavClient.create_directory("dir"))
    print(webdavClient.list_resources())


if __name__ == "__main__":
    main()

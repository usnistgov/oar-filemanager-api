import requests
from nistoar.filemanager.webdav import WebDavMethod


class BaseClient:
    """Base HTTP clients, wrapper around requests library."""

    def __init__(self, base_url, api_url=None):
        self.base_url = base_url
        self.api_url = None
        if api_url:
            self.api_url = api_url if str(api_url).startswith("/") else "/" + api_url
        # TODO: add headers. What headers we need?
        self.get_headers = {}
        self.post_headers = {}

    def construct_url(self, extra_url=None):
        full_url = self.base_url
        if self.api_url:
            full_url += self.api_url
        if extra_url:
            extra_url = extra_url if str(extra_url).startswith("/") else "/" + extra_url
            full_url += extra_url
        # TODO: validate url here
        return full_url

    def get(self, url=None, headers=None, params=None):
        full_url = self.construct_url(extra_url=url)
        if not headers:
            headers = self.get_headers
        res = requests.get(url=full_url, headers=headers, params=params)
        return res

    def post(self, url="", headers=None, data=None):
        full_url = self.construct_url(extra_url=url)
        if not headers:
            headers = self.post_headers
        res = requests.post(url=full_url, headers=headers, data=data)
        return res

    def put(self, url="", headers=None, data=None):
        full_url = self.construct_url(extra_url=url)
        if not headers:
            headers = self.post_headers
        res = requests.put(url=full_url, headers=headers, data=data)
        return res

    def head(self, url="", headers=None, params=None):
        full_url = self.construct_url(extra_url=url)
        if not headers:
            headers = self.get_headers
        res = requests.head(url=full_url, headers=headers, params=params)
        return res

    def delete(self, url="", headers=None, data=None):
        full_url = self.construct_url(extra_url=url)
        if not headers:
            headers = self.post_headers
        res = requests.delete(url=full_url, headers=headers, data=data)
        return res


class WebDavClient(BaseClient):
    """Extension of HTTP clients, to include WEBDAV additional operations."""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def prop_find(self, url="", headers=None, data=None):
        full_url = self.construct_url(extra_url=url)

        res = requests.request(
            WebDavMethod.PROPFIND, url=full_url, headers=headers, data=data
        )
        return res

    def prop_patch(self, url="", headers=None, data=None):
        full_url = self.construct_url(extra_url=url)

        res = requests.request(
            WebDavMethod.PROPPATCH, url=full_url, headers=headers, data=data
        )
        return res

    def make_collection(self, url=""):
        full_url = self.construct_url(extra_url=url)

        res = requests.request(WebDavMethod.MKCOL, url=full_url)
        return res

    def move(self, url, destination, overwrite=False):
        full_url = self.construct_url(extra_url=url)
        destination_url = self.construct_url(extra_url=destination)
        if not headers:
            headers = {}
        headers["Destination"] = destination_url
        headers["Overwrite"] = "T" if overwrite else "F"
        res = requests.request(WebDavMethod.MOVE, url=full_url)
        return res

    def copy(self, url, destination, overwrite=False, headers=None):
        full_url = self.construct_url(extra_url=url)
        destination_url = self.construct_url(extra_url=destination)
        if not headers:
            headers = {}
        headers["Destination"] = destination_url
        headers["Overwrite"] = "T" if overwrite else "F"
        res = requests.request(WebDavMethod.COPY, url=full_url, headers=headers)
        return res

    def lock(self, url, headers=None):
        full_url = self.construct_url(extra_url=url)
        res = requests.request(WebDavMethod.LOCK, url=full_url, headers=headers)
        return res

    def unlock(self, url, headers=None):
        full_url = self.construct_url(extra_url=url)
        res = requests.request(WebDavMethod.UNLOCK, url=full_url, headers=headers)
        return res

    def download(self, url="", headers=None, params=None):
        full_url = self.construct_url(extra_url=url)
        if not headers:
            headers = self.get_headers
        res = requests.get(url=full_url, headers=headers, params=params)
        return res

# oar-filemanager-api
Filemanager Service API


## Run WebDav Test Server

Using Docker:

```
docker run --restart always -v /path/to/folder:/var/lib/dav -e AUTH_TYPE=Basic -e USERNAME=login -e PASSWORD=password  --publish 8095:80 -d bytemark/webdav
```
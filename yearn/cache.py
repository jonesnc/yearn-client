from typing import Union
from urllib.parse import urlparse
from xmlrpc.client import Server as HTTPServerProxy

from .scgi import SCGIServerProxy

ServerProxy = Union[HTTPServerProxy, SCGIServerProxy]


class ServerCache(object):
    """Caches the server.

    Subclass this for any object that needs access to the ServerProxy.
    """

    _server: ServerProxy

    def __init__(self, *args, uri: str = None, server: ServerProxy = None,
                 **kwargs):

        if server:
            self._server = server

        elif uri:
            schema = urlparse(uri)[0]
            if schema == 'scgi':
                self._server = SCGIServerProxy(uri)
            elif schema in ['http', 'https']:
                self._server = HTTPServerProxy(uri)
            else:
                raise NotImplementedError()
        else:
            raise ValueError('MISSING KWARG: uri or server is required!')

        super().__init__()

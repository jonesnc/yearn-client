from yearn.cache import ServerCache


class MethodAPIMixin(ServerCache):

    def set_key(self, name, key, definition=''):
        self._server.method.set_key('', name, key, definition)

    def keys(self, name):
        return self._server.method.list_keys('', name)

    def has_key(self, name, key):
        result = self._server.method.has_key('', name, key)
        return result == 1

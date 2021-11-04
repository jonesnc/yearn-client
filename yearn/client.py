import xmlrpc.client

from yearn.download import DownloadAPIMixin
from yearn.load import LoadAPIMixin
from yearn.method import MethodAPIMixin
from yearn.system import SystemAPIMixin
from yearn.torrent import Torrent


class Client(
    SystemAPIMixin,
    DownloadAPIMixin,
    LoadAPIMixin,
    MethodAPIMixin,
):

    def get_torrent(self, torrent_hash: str) -> Torrent:
        return Torrent(server=self._server, torrent_hash=torrent_hash)

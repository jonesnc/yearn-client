from typing import Dict, List, Optional, Union

from yearn.cache import ServerCache
from yearn.exceptions import XmlrpcResultTypeException
from yearn.torrent import Torrent

TorrentHashDict = Dict[str, Torrent]


class DownloadAPIMixin(ServerCache):
    """Download methods that don't make sense in the Torrent class."""

    def torrents_info(
        self,
        # TODO: put these attrs in an Enum/pydantic model
        torrent_attrs: List[str]=['d.hash=', 'd.name=', 'd.directory=',
                       'd.base_filename=', 'd.base_path=',
                       'd.directory_base='],
        as_dict: bool=False,
        view: str='main'
    ) -> Optional[Union[List[Torrent], TorrentHashDict]]:
        results = self._server.d.multicall2('', view, *torrent_attrs)

        clean_attrs: List[str] = [
            x.replace('d.', '').replace('=', '')
            for x in torrent_attrs
        ]

        if isinstance(results, list):
            if as_dict:
                torrents_dict: TorrentHashDict = {}
                for result in results:
                    res_dict = dict(zip(clean_attrs, result))
                    torrent = Torrent(server=self._server, **res_dict)
                    hash = torrent.hash
                    torrents_dict[hash] = torrent
                return torrents_dict

            else:
                torrents_list: List[Torrent] = []
                for result in results:
                    res_dict = dict(zip(clean_attrs, result))
                    torrent = Torrent(server=self._server, **res_dict)
                    torrents_list.append(torrent)
                return torrents_list
        return None

    def info_hashes(self, view='main') -> List[str]:
        results = self._server.download_list('', view)
        if isinstance(results, list):
            return results
        raise XmlrpcResultTypeException(
            f'Expected type list, got {type(results)}')

    def check_hash(self, hash):
        self._server.d.check_hash(hash)

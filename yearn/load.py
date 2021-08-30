from time import time
from typing import Optional
from xmlrpc import client

from torrentool.api import Torrent as Torrentool  # type: ignore

from yearn.cache import ServerCache
from yearn.torrent import Torrent


class LoadAPIMixin(ServerCache):

    def load_torrent(self, torrent_file, directory=None,
                     use_dir_as_base=False, perform_check_hash=False,
                     set_addtime=False
    ) -> Optional[Torrent]:
        try:
            print(f'torrent_file={torrent_file}')
            with open(torrent_file, 'rb') as f:
                raw_torrent_data = client.Binary(f.read())
                load_args = ['', raw_torrent_data]
                if use_dir_as_base:
                    directory_cmd = f'd.directory_base.set={directory}'
                else:
                    directory_cmd = f'd.directory.set={directory}'

                load_args.append(directory_cmd)
                if perform_check_hash:
                    perform_check_hash_cmd = 'd.check_hash='
                    load_args.append(perform_check_hash_cmd)

                if set_addtime:
                    now = int(time())
                    set_custom_addtime_cmd = f'd.custom.set=addtime,{now}'
                    load_args.append(set_custom_addtime_cmd)
                self._server.load.raw_verbose(*load_args)
                torrent_hash = Torrentool.from_file(torrent_file).info_hash
                return Torrent(server=self._server, hash=torrent_hash)
        except OSError as e:
            print(f'Unable to load file: {torrent_file}')
            print(e)
            return None

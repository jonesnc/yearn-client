import math
import os
from enum import Enum
from pprint import pprint
from time import time
from typing import Optional, Sequence
from xmlrpc import client

import bencodepy
from torrentool.api import Torrent as Torrentool  # type: ignore

from yearn.cache import ServerCache
from yearn.torrent import Torrent


class FilePriorities(Enum):
    OFF = 0
    NORMAL = 1
    HIGH = 2


class LoadAPIMixin(ServerCache):

    def load_torrent(self, torrent_file, directory=None,
                     use_dir_as_base=False, perform_check_hash=False,
                     set_addtime=False, add_started=False, set_completed=False
    ) -> Optional[Torrent]:

        with open(torrent_file, 'rb') as f:
            raw_torrent_data = client.Binary(f.read())
            load_args = ['', raw_torrent_data]

            directory = directory.replace('"', '\\"')

            if use_dir_as_base:
                directory_cmd = f'd.directory_base.set="{directory}"'.encode('utf-8')
            else:
                directory_cmd = f'd.directory.set="{directory}"'.encode('utf-8')

            load_args.append(directory_cmd)
            if perform_check_hash:
                perform_check_hash_cmd = 'd.check_hash='
                load_args.append(perform_check_hash_cmd)

            if set_addtime:
                now = int(time())
                set_custom_addtime_cmd = f'd.custom.set=addtime,{now}'
                load_args.append(set_custom_addtime_cmd)

            tt_class = Torrentool.from_file(torrent_file)

            if set_completed:
                chunk_size = tt_class._struct['info']['piece length']
                files = []
                total_size = tt_class.total_size

                if 'files' in tt_class._struct['info']:
                    tt_files = tt_class._struct['info']['files']
                else:
                    tt_files = [{
                        'path': [
                            tt_class._struct['info']['name']
                        ],
                        'length': tt_class._struct['info']['length']
                    }]

                for file in tt_files:
                    file_length = file['length']
                    host_torrent_file_dir = os.path.dirname(torrent_file)
                    local_file_path = os.path.join(
                        host_torrent_file_dir,
                        # for files in sub-dir, 'path' will have multiple
                        # elements
                        *file['path']
                    )
                    try:
                        stat = os.stat(local_file_path)
                        mtime = math.trunc(stat.st_mtime)

                        resume = {
                            'completed': math.ceil(file_length / chunk_size),
                            'mtime': mtime,
                            'priority': FilePriorities.OFF.value,
                        }
                    except FileNotFoundError:
                        resume = {
                            'completed': 0,
                            'mtime': 0,
                            'priority': FilePriorities.OFF.value,
                        }
                    files.append(resume)

                bitfield = math.ceil(total_size / chunk_size)
                libtorrent_resume = {
                    'bitfield': bitfield,
                    'files': files
                }

                torrent_file_data = tt_class._struct.copy()
                torrent_file_data['libtorrent_resume'] = libtorrent_resume

                raw_data_with_resume = bencodepy.encode(torrent_file_data)

                load_args[1] = raw_data_with_resume

            if add_started:
                self._server.load.raw_start_verbose(*load_args)
            else:
                self._server.load.raw_verbose(*load_args)

            torrent = Torrent(
                server=self._server,
                torrent_hash=tt_class.info_hash)

            return torrent

from datetime import datetime
from typing import List

import humanfriendly  # type: ignore

from yearn.cache import ServerCache
from yearn.exceptions import XmlrpcResultTypeException
from yearn.tracker import Tracker


class Torrent(ServerCache):

    def __init__(self, server, hash, name=None, base_filename=None,
                 base_path=None, directory=None, directory_base=None):
        # TODO: should this be simplified to only require the hash on init?
        super().__init__(server=server)

        # TODO: move these to property's
        self.hash: str = hash
        self.name: str = name
        self.base_filename: str = base_filename
        self.base_path: str = base_path
        self.directory: str = directory
        self.directory_base: str = directory_base

    def __str__(self):
        return f'Torrent (hash={self.hash},name={self.name})'

    def __repr__(self):
        return self.__str__()

    def open(self):
        return self._server.d.open(self.hash)

    def resume(self):
        return self._server.d.resume(self.hash)

    def close(self):
        return self._server.d.close(self.hash)

    def start(self):
        return self._server.d.start(self.hash)

    def erase(self):
        return self._server.d.erase(self.hash)

    @property
    def accepting_seeders(self):
        result = self._server.d.accepting_seeders(self.hash)
        if isinstance(result, int):
            return result == 1
        raise XmlrpcResultTypeException(
            f'Expected type int, got {type(result)}')

    @accepting_seeders.setter
    def accepting_seeders(self, accepting_seeders: bool):
        if accepting_seeders:
            self._server.d.accepting_seeders.enable(self.hash)
        else:
            self._server.d.accepting_seeders.disable(self.hash)

    @property
    def bitfield(self):
        result = self._server.d.bitfield(self.hash)
        if isinstance(result, str):
            return result
        else:
            raise XmlrpcResultTypeException(
                f'Expected type str, got {type(result)}')

    @property
    def size_bytes(self):
        result = self._server.d.size_bytes(self.hash)
        if isinstance(result, int):
            return result
        else:
            raise XmlrpcResultTypeException(
                f'Expected type int, got {type(result)}')

    @property
    def chunk_size(self):
        result = self._server.d.chunk_size(self.hash)
        if isinstance(result, int):
            return humanfriendly.format_size(result)
        else:
            raise XmlrpcResultTypeException(
                f'Expected type int, got {type(result)}')

    @property
    def chunk_size_bytes(self):
        result = self._server.d.chunk_size(self.hash)
        if isinstance(result, int):
            return result
        else:
            raise XmlrpcResultTypeException(
                f'Expected type int, got {type(result)}')

    @property
    def size_chunks(self):
        result = self._server.d.size_chunks(self.hash)
        if isinstance(result, int):
            return result
        else:
            raise XmlrpcResultTypeException(
                f'Expected type int, got {type(result)}')

    @property
    def bytes_done(self):
        return self._server.d.bytes_done(self.hash)

    @property
    def bytes_left(self):
        return self._server.d.left_bytes(self.hash)

    @property
    def timestamp_start(self):
        time_result = self._server.d.timestamp.started(self.hash)
        if isinstance(time_result, int):
            datetime_time = datetime.fromtimestamp(float(time_result))
            return datetime_time
        return None

    @property
    def is_paused(self) -> bool:
        return (
            self._server.d.is_open(self.hash) == 1 and
            not self._server.d.is_active(self.hash) == 1 and
            not self._server.d.state(self.hash) == 1)

    @property
    def complete(self) -> bool:
        return self._server.d.complete(self.hash) == 1

    @property
    def is_hash_checked(self) -> bool:
        return self._server.d.is_hash_checked(self.hash) == 1

    @property
    def is_hash_checking(self) -> bool:
        return self._server.d.is_hash_checking(self.hash) == 1

    @property
    def is_multi_file(self) -> bool:
        return self._server.d.is_multi_file(self.hash) == 1

    @property
    def trackers(self) -> List[Tracker]:
        trackers_results = self._server.t.multicall(self.hash, '', 't.url=')
        tracker_list = []
        if isinstance(trackers_results, list):
            for idx, tracker_url in enumerate(trackers_results):
                tracker = Tracker(self._server, self.hash, tracker_url, idx)
                tracker_list.append(tracker)
            return tracker_list
        else:
            raise XmlrpcResultTypeException(
                f'Expected type list, got {type(trackers_results)}')

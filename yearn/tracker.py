from datetime import datetime
from enum import Enum

from yearn.cache import ServerCache
from yearn.exceptions import XmlrpcResultTypeException


class TrackerType(Enum):
    HTTP = 1
    UDP = 2
    DHT = 3


class Tracker(ServerCache):
    def __init__(self, server, hash, url, index):
        super().__init__(server=server)

        self.hash = hash
        self.url = url
        self.index = index

    @property
    def target(self):
        return f'{self.hash}:t{self.index}'

    @property
    def tracker_type(self) -> TrackerType:
        result = self._server.t.type(self.target)
        if isinstance(result, int):
            return TrackerType(result)
        raise XmlrpcResultTypeException(
            f'Expected type int, got {type(result)}')

    @property
    def activity_time_last(self) -> datetime:
        result = self._server.t.activity_time_last(self.target)
        if isinstance(result, int):
            datetime_result = datetime.fromtimestamp(float(result))
            return datetime_result
        else:
            raise XmlrpcResultTypeException(
                f'Expected type int, got {type(result)}')

    @property
    def activity_time_next(self) -> datetime:
        result = self._server.t.activity_time_next(self.target)
        if isinstance(result, int):
            datetime_result = datetime.fromtimestamp(float(result))
            return datetime_result
        raise XmlrpcResultTypeException(
            f'Expected type int, got {type(result)}')

    @property
    def can_scrape(self) -> bool:
        result = self._server.t.can_scrape(self.target)
        if isinstance(result, int):
            return result == 1
        raise XmlrpcResultTypeException(
            f'Expected type int, got {type(result)}')

    @property
    def is_usable(self) -> bool:
        result = self._server.t.is_usable(self.target)
        return result == 1

    @property
    def enabled(self) -> bool:
        result = self._server.t.is_enabled(self.target)
        return result == 1

    def enable(self):
        self._server.t.enable('', self.target)

    def disable(self):
        self._server.t.disable('', self.target)

    def __str__(self):
        return f'Tracker(url={self.url})'

    def __repr__(self):
        return self.__str__()

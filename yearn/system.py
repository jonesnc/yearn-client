from datetime import datetime
from typing import List, Optional, Union

import humanfriendly

from yearn.cache import ServerCache
from yearn.exceptions import XmlrpcResultTypeException
from yearn.schema import Capabilities, Version


class SystemAPIMixin(ServerCache):

    @property
    def version(self) -> Version:
        version = Version(
            rtorrent=self._server.system.client_version(),
            libtorrent=self._server.system.library_version(),
            api=self._server.system.api_version(),
        )
        return version

    @property
    def capabilities(self) -> Capabilities:
        result = self._server.system.capabilities()
        if isinstance(result, dict):
            capabilities = Capabilities(
                facility=result['facility'],
                version_major=result['version_major'],
                version_minor=result['version_minor'],
                version_point=result['version_point'],
                protocol_version=result['protocol_version'],
            )
            return capabilities
        raise XmlrpcResultTypeException(
            f'Expected type int, got {type(result)}')

    @property
    def cwd(self) -> str:
        return str(self._server.system.cwd())

    @cwd.setter
    def cwd(self, cwd):
        self._server.system.cwd.set('', cwd)

    @property
    def pid(self) -> int:
        pid = self._server.system.pid()
        if isinstance(pid, int):
            return pid
        raise XmlrpcResultTypeException(
            f'Expected type int, got {type(pid)}')

    @property
    def hostname(self) -> str:
        result = self._server.system.hostname()
        if isinstance(result, str):
            return result
        raise XmlrpcResultTypeException(
            f'Expected type str, got {type(result)}')

    def env(self, env_val):
        result = self._server.system.env('', env_val)
        if result == '':
            return None
        return result

    @property
    def file_allocate(self):
        return bool(self._server.system.file.allocate())

    @file_allocate.setter
    def file_allocate(self, file_allocate: bool):
        file_allocate_1_or_0 = 1 if file_allocate else 0
        self._server.system.file.allocate.set('', file_allocate_1_or_0)

    @property
    def file_max_size(self) -> str:
        result = self._server.system.file.max_size()
        if isinstance(result, int):
            return humanfriendly.format_size(result)
        raise XmlrpcResultTypeException(
            f'Expected type int, got {type(result)}')

    @file_max_size.setter
    def file_max_size(self, file_max_size: Union[int, str]):
        if isinstance(file_max_size, str):
            file_max_size = humanfriendly.parse_size(file_max_size)

        # Convert file_max_size to str to work around int size limits
        self._server.system.file.max_size.set('', str(file_max_size))

    @property
    def file_max_size_bytes(self) -> int:
        result = self._server.system.file.max_size()
        if isinstance(result, int):
            return result
        raise XmlrpcResultTypeException(
            f'Expected type int, got {type(result)}')

    @property
    def daemon(self):
        return bool(self._server.system.daemon())

    @daemon.setter
    def daemon(self, daemon: bool):
        daemon_1_or_0 = 1 if daemon else 0
        self._server.system.daemon.set('', daemon_1_or_0)

    @property
    def all_methods(self) -> List[str]:
        list_methods = self._server.system.listMethods()
        if isinstance(list_methods, list):
            return list_methods
        return []

    @property
    def time(self) -> Optional[datetime]:
        time_result = self._server.system.time()
        if isinstance(time_result, int):
            datetime_time = datetime.fromtimestamp(float(time_result))
            return datetime_time
        return None

    def method_exists(self, method: str) -> bool:
        return bool(self._server.system.methodExist(method))

    def method_help(self, method: str) -> str:
        return str(self._server.system.methodHelp(method))

    def method_signature(self, method: str) -> str:
        return str(self._server.system.methodSignature(method))

    @property
    def get_capabilities(self) -> str:
        return str(self._server.system.get_capabilities())

    def shutdown(self, quick=False):
        if not quick:
            self._server.system.shutdown.normal()
        else:
            self._server.system.shutdown.quick()

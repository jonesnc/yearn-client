import xmlrpc.client

from yearn.download import DownloadAPIMixin
from yearn.load import LoadAPIMixin
from yearn.method import MethodAPIMixin
from yearn.system import SystemAPIMixin


class Client(
    SystemAPIMixin,
    DownloadAPIMixin,
    LoadAPIMixin,
    MethodAPIMixin,
):
    pass

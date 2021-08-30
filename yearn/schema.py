from pydantic import BaseModel

from .torrent import Torrent


class Version(BaseModel):
    libtorrent: str
    rtorrent: str
    api: int


class Capabilities(BaseModel):
    facility: str
    version_major: int
    version_minor: int
    version_point: int
    protocol_version: int

from datetime import datetime

from yearn import Client
from yearn.schema import Capabilities

sock_uri = 'scgi:///home/nathanjones/Projects/yearn-client/rtorrent/config/.local/share/rtorrent/rtorrent.sock'

client = Client(uri=sock_uri)

def test_version():
    assert client.version.libtorrent == '0.13.8'
    assert client.version.rtorrent == '0.9.8'
    assert type(client.version.api) == int

def test_cwd_and_setter():
    client.cwd = '/'
    assert client.cwd == '/'
    client.cwd = '/config/.local/share/rtorrent/download'
    assert client.cwd == '/config/.local/share/rtorrent/download'

def test_daemon_and_setter():
    assert client.daemon == True
    client.daemon = False
    assert client.daemon == False
    client.daemon = True
    assert client.daemon == True

def test_file_allocate_and_setter():
    assert client.file_allocate == False
    client.file_allocate = True
    assert client.file_allocate == True
    client.file_allocate = False
    assert client.file_allocate == False

def test_hostname():
    assert type(client.hostname) == str

def test_env():
    assert client.env('HOME') == '/config'
    assert client.env('SDFLKJ') is None

def test_file_allocate():
    assert client.file_allocate == False

def test_all_methods():
    assert isinstance(client.all_methods, list)

def test_pid():
    assert client.pid is not None
    assert isinstance(client.pid, int)

def test_time():
    assert client.time is not None
    assert isinstance(client.time, datetime)

def test_capabilities():
    assert isinstance(client.capabilities, Capabilities)

# def test_shutdown():
    # TODO: figure out a stable method of testing this without blowing up
    # the rest of the tests
    # client.shutdown()


def test_file_max_size_and_setter():
    assert isinstance(client.file_max_size, str)
    client.file_max_size = '2 GB'
    assert client.file_max_size == '2 GB'
    client.file_max_size = '1 GB'
    assert client.file_max_size == '1 GB'


def test_file_max_size_bytes_and_setter():
    assert isinstance(client.file_max_size_bytes, int)
    client.file_max_size = '1000000000'
    assert client.file_max_size_bytes == 1000000000
    client.file_max_size = '5000000000'
    assert client.file_max_size_bytes == 5000000000

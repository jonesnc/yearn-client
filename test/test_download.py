from yearn import Client

sock_uri = 'scgi:///home/nathanjones/Projects/yearn-client/rtorrent/config/.local/share/rtorrent/rtorrent.sock'

client = Client(uri=sock_uri)


def test_accepting_seeders():
    for torrent in client.torrents_info():
        torrent.erase()

    client.load_torrent(
        '/home/nathanjones/Projects/yearn-client/test/torrent_files/KNOPPIX_V9.1CD-2021-01-25-DE.torrent',
        '/config/.local/share/rtorrent/download')
    new_torrent = client.torrents_info()[0]
    assert type(new_torrent.accepting_seeders) == bool

    new_torrent.accepting_seeders = True
    assert new_torrent.accepting_seeders == True

    new_torrent.accepting_seeders = False
    assert new_torrent.accepting_seeders == False


def test_bitfield():
    for torrent in client.torrents_info():
        torrent.erase()

    client.load_torrent(
        '/home/nathanjones/Projects/yearn-client/test/torrent_files/KNOPPIX_V9.1CD-2021-01-25-DE.torrent',
        '/config/.local/share/rtorrent/download')

    new_torrent = client.torrents_info()[0]

    assert type(new_torrent.bitfield) == str


def test_chunk_size():
    for torrent in client.torrents_info():
        torrent.erase()

    client.load_torrent(
        '/home/nathanjones/Projects/yearn-client/test/torrent_files/KNOPPIX_V9.1CD-2021-01-25-DE.torrent',
        '/config/.local/share/rtorrent/download')

    new_torrent = client.torrents_info()[0]

    assert type(new_torrent.chunk_size) == str
    assert type(new_torrent.chunk_size_bytes) == int

from yearn import Client

sock_uri = 'scgi:///home/nathanjones/Projects/yearn-client/rtorrent/config/.local/share/rtorrent/rtorrent.sock'

client = Client(uri=sock_uri)

def test_insert_key():
    name = 'event.download.finished'
    key = 'new_event'
    definition = 'execute = /bin/ash /config/.local/share/rtorrent/event.sh'
    client.set_key(name, key)
    client.set_key(name, key, definition)
    keys = client.keys('event.download.finished')

    print(keys)
    assert client.has_key(name, key) == True

    for torrent in client.torrents_info():
        torrent.erase()
    new_torrent_hash = client.load_torrent(
        '/home/nathanjones/Projects/yearn-client/test/torrent_files/KNOPPIX_V9.1CD-2021-01-25-DE.torrent',
        '/config/.local/share/rtorrent/download')

    client.torrents_info()[0].start()

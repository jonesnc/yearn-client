from datetime import datetime

from yearn import Client
from yearn.tracker import TrackerType

sock_uri = 'scgi:///home/nathanjones/Projects/yearn-client/rtorrent/config/.local/share/rtorrent/rtorrent.sock'

client = Client(uri=sock_uri)


def test_activity_timestamps():
    for torrent in client.torrents_info():
        torrent.erase()
    new_torrent_hash = client.load_torrent(
        '/home/nathanjones/Projects/yearn-client/test/torrent_files/KNOPPIX_V9.1CD-2021-01-25-DE.torrent',
        '/config/.local/share/rtorrent/download')
    trackers = client.torrents_info()[0].trackers
    for tracker in trackers:
        assert type(tracker.activity_time_next) == datetime
        assert type(tracker.activity_time_last) == datetime


def test_can_scrape():
    for torrent in client.torrents_info():
        torrent.erase()
    new_torrent_hash = client.load_torrent(
        '/home/nathanjones/Projects/yearn-client/test/torrent_files/KNOPPIX_V9.1CD-2021-01-25-DE.torrent',
        '/config/.local/share/rtorrent/download')
    trackers = client.torrents_info()[0].trackers
    for tracker in trackers:
        assert type(tracker.can_scrape) == bool


def test_is_usable():
    for torrent in client.torrents_info():
        torrent.erase()
    new_torrent_hash = client.load_torrent(
        '/home/nathanjones/Projects/yearn-client/test/torrent_files/KNOPPIX_V9.1CD-2021-01-25-DE.torrent',
        '/config/.local/share/rtorrent/download')
    trackers = client.torrents_info()[0].trackers
    for tracker in trackers:
        assert type(tracker.is_usable) == bool


def test_is_enabled():
    for torrent in client.torrents_info():
        torrent.erase()
    new_torrent_hash = client.load_torrent(
        '/home/nathanjones/Projects/yearn-client/test/torrent_files/KNOPPIX_V9.1CD-2021-01-25-DE.torrent',
        '/config/.local/share/rtorrent/download')
    trackers = client.torrents_info()[0].trackers
    for tracker in trackers:
        assert type(tracker.enabled) == bool


def test_tracker_type():
    for torrent in client.torrents_info():
        torrent.erase()
    new_torrent_hash = client.load_torrent(
        '/home/nathanjones/Projects/yearn-client/test/torrent_files/KNOPPIX_V9.1CD-2021-01-25-DE.torrent',
        '/config/.local/share/rtorrent/download')
    trackers = client.torrents_info()[0].trackers
    for tracker in trackers:
        assert type(tracker.tracker_type) == TrackerType

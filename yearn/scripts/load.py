import os
import re

import click
import torrentool
from torrentool.api import Torrent as Torrentool

from yearn import Client
from yearn.torrent import Torrent


def get_all_torrent_files(path):
    for root, _dirs, files in os.walk(path, topdown=False):
        torrent_dir = os.path.abspath(root)
        for name in files:
            if '.torrent' in name:
                yield (torrent_dir, name)


def load(path, scgi, mount=None):
    if mount:
        host_base_dir, mount_base_dir = mount.split(':')
    client = Client(uri=scgi)
    torrent_hashes = client.info_hashes()

    if os.path.isdir(path):
        for dir, torrent_file in get_all_torrent_files(path):
            full_host_torrent_file_path = os.path.join(dir, torrent_file)
            try:
                torrent = Torrentool.from_file(full_host_torrent_file_path)
            except torrentool.exceptions.BencodeDecodingError:
                click.echo(
                    f'Invalid torrent file: {full_host_torrent_file_path}')
                continue
            torrent_hash = torrent.info_hash.upper()

            if torrent_hash not in torrent_hashes:

                mount_full_path = dir.replace(host_base_dir, mount_base_dir)

                click.echo(f'Adding {torrent_file}')
                client.load_torrent(
                    torrent_file=full_host_torrent_file_path,
                    directory=mount_full_path,
                    use_dir_as_base=True,
                    perform_check_hash=False,
                    set_addtime=True,
                    add_started=True,
                    set_completed=True,
                )

            else:
                torrent_in_rtorrent = client.get_torrent(
                    torrent_hash=torrent_hash)
                if not torrent_in_rtorrent.complete:
                    print((
                        f'{torrent_in_rtorrent.name} '
                        f'({torrent_in_rtorrent.hash}) is incomplete!'))
    elif os.path.isfile(path):
        pass
    else:
        click.echo('path is a special file! Skipping.')

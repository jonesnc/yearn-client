import click

from yearn.scripts.load import load as script_load


@click.group()
def cli():
    pass


@cli.command()
@click.argument('path', default='.')
@click.option('--scgi', default=None)
@click.option('--mount', default=None)  # TODO: support multiple mounts
def load(path, scgi, mount):
    click.echo('Loading torrent files...')
    click.echo(f'Using SCGI: {scgi}')
    click.echo(f'Using path: {path}')
    click.echo(f'Using mount: {mount}')
    script_load(path, scgi, mount)

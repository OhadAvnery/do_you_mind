import click
from .server import run_server


@click.group()
def main():
    pass


@main.command('run-server')
@click.option('--host', '-h', default='127.0.0.1', type=str)
@click.option('--port', '-p', default=8000, type=int)
@click.argument('publish', type=str)
@click.option('--database', '-db', default='mongodb://127.0.0.1:27017',
              type=str)
def run_server_cli(host, port, publish, database):
    run_server(host, port, publish, database)


if __name__ == '__main__':
    main()

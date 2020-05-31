import click
from .server import run_server

@click.group()
def main():
    pass

@main.command('run-server')
@click.option('--host', '-h', default='127.0.0.1', type=str)
@click.option('--port', '-p', default=8000, type=int)
@click.option('--database', '-db', default='mongodb://127.0.0.1:27017', type=str)
@click.argument('publish', type=str)
def run_server_cli(host, port, database, publish):
    run_server(host, port, database, publish)

if __name__ == '__main__':
    main()
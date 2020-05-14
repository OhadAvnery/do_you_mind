import click

from .api import run_api_server

@click.group()
def main():
    pass

@main.command()
@click.option('--host', '-h', default='127.0.0.1', type=str)
@click.option('--port', '-p', default=5000, type=int)
@click.option('--database', '-d', 
    default='mongodb://127.0.0.1:27017', type=str)
def run_server(host, port, database):
    return run_api_server(host, port, database)

if __name__ == '__main__':
    main()

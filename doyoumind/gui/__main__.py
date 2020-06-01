import click
from .gui import run_server


@click.group()
def main():
    pass


@main.command('run-server')
@click.option('--host', '-h', default='127.0.0.1', type=str)
@click.option('--port', '-p', default=8080, type=int)
@click.option('--api-host', '-H', default='127.0.0.1', type=str)
@click.option('--api-port', '-P', default=5000, type=int)
def run_server_cli(host, port, api_host, api_port):
    run_server(host, port, api_host, api_port)


if __name__ == '__main__':
    main()

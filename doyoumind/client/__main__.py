import click
from .client import upload_sample

@click.group()
def main():
    pass


@main.command('upload-sample')
@click.option('--host', '-h', default='127.0.0.1', type=str)
@click.option('--port', '-p', default=8000, type=int)
@click.argument('path', type=str)
def upload_sample_cli(host, port, path):
    print(f"client host- {host}, client port- {port}")
    return upload_sample(host, port, path)


if __name__ == '__main__':
    #print(f"client main: {main.commands}")
    main()
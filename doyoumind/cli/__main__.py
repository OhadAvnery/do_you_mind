import click
from furl import furl
import requests

from ..api import api

@click.group()
def main():
    pass

def get_answer(host, port, path):
    '''
    '''
    f = furl()
    f.set(scheme='http',host=host,port=port,path=path)
    url = f.url
    print(f"cli.main: out request- {url}")
    answer = requests.get(url)
    print("cli.main: done get")
    return answer.json()

@main.command()
@click.option('--host', '-h', default='127.0.0.1', type=str)
@click.option('--port', '-p', default=5000, type=int)
def get_users(host, port):
    '''
    returns a list of all users.
    Each entry contains the user id and username.
    '''
    print(get_answer(host, port, 'users'))

@main.command()
@click.option('--host', '-h', default='127.0.0.1', type=str)
@click.option('--port', '-p', default=5000, type=int)
@click.argument('user_id', type=int)
def get_user(host, port, user_id):
    '''
    returns a users' details (not including the snapshots).
    '''
    print(get_answer(host, port, f'users/{user_id}'))

@main.command()
@click.option('--host', '-h', default='127.0.0.1', type=str)
@click.option('--port', '-p', default=5000, type=int)
@click.argument('user_id', type=int)
def get_snapshots(host, port, user_id):
    '''
    return the users' snapshots (only their timestamps).
    '''
    print(get_answer(host, port, f'users/{user_id}/snapshots'))


@main.command()
@click.option('--host', '-h', default='127.0.0.1', type=str)
@click.option('--port', '-p', default=5000, type=int)
@click.argument('user_id', type=int)
@click.argument('timestamp', type=float)
def get_snapshot(host, port, user_id, timestamp):
    '''
    return the given topics for a snapshot.
    The snapshot is given by the id of its user, and by its timestamp.
    WARNING: it probably dosen't support snapshots made before 1970
    '''
    print(get_answer(host, port, f'users/{user_id}/snapshots/{timestamp}'))

@main.command()
@click.option('--host', '-h', default='127.0.0.1', type=str)
@click.option('--port', '-p', default=5000, type=int)
@click.argument('user_id', type=int)
@click.argument('user_id', type=float)
@click.argument('result_name', type=str)
def get_result(host, port, user_id, timestamp, result_name):
    print(get_answer(host, port, f'/users/{user_id}/snapshots/{timestamp}/{result_name}'))

if __name__ == '__main__':
    main()
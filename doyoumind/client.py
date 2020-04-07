import time
import struct
import socket
#from . import cli
from .cli import CommandLineInterface

from .utils.connection import Connection

import click

cli = CommandLineInterface()



def send_hello(connection, path):

@cli.command
def upload_sample(host, port, path):
    with Connection.connect(host, port) as connection:
        pass #need to fix

        send_hello()


#@click.command()
@cli.command
def upload_thought(address, user, thought):
    """
    uploads the thought to the given address.
    address- a string of the form ip:port.
    user- a string representing the user id.
    thought- the user's thought as string.
    """
    n = len(thought)
    ip_address, port = address.split(":")
    port = int(port)

    user_id_bytes = struct.pack("Q", int(user))
    timestamp = struct.pack("Q", int(time.time()))
    thought_size = struct.pack("I", n)
    thought_data = struct.pack("{:d}s".format(n), str.encode(thought))

    binary_data = user_id_bytes + timestamp + \
                  thought_size + thought_data


    sock = socket.socket()
    sock.connect((ip_address, port))
    conn = Connection(sock)
    conn.send(binary_data)
    conn.close()
    print('done')


"""def main(argv):
    if len(argv) != 4:
        print(f'USAGE: {argv[0]} <address> <user_id> <thought>')
        return 1
    try:
        address, user_id, thought = argv[1:]
        ip_address, port = address.split(":")
        fixed_address = (ip_address, int(port))
        upload(fixed_address, int(user_id), thought)
        print('done')

    except Exception as error:
        print(f'ERROR: {error}')
        return 1"""


if __name__ == '__main__':
    cli.main()


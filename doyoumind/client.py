import click
import time
import struct
import socket



from .utils.connection import Connection
from .readers.reader import Reader
from . import protocol
from .constants import ALL_FIELDS



@click.group()
def main():
    pass

#IDEA: these three functions only work at the connection level (so they're really short), 
#and don't use any (de)serialization.
def send_hello(conn, hello_msg):
    conn.send_message(hello_msg)
def get_config(conn):
   return conn.receive_message()
def send_snapshot(conn, snap_msg):
    conn.send_message(snap_msg)

def filter_snapshot(snap, config):
    """
    Update the snapshot so it'll only have the fields described in config
    """
    for field in ALL_FIELDS:
        if field not in config:
            snap.ClearField(field)

@main.command()
@click.option('--host', '-h', default='127.0.0.1', type=str)
@click.option('--port', '-p', default=8000, type=int)
@click.argument('path', type=str)
def upload_sample(host, port, path, read_type='protobuf'):
    with Connection.connect(host, port) as conn:
        zipped = (path.endswith(".gz"))
        r = Reader(path, read_type, zipped)
        #print("reading hello")
        hello = r.read_hello()
        hello_bytes = hello.SerializeToString()
        num_snapshot = 1
        for snap in r:
            #print(f"client: sending snapshot {debug_counter}...")
            send_hello(conn, hello_bytes)
            config_bytes = get_config(conn)
            config = protocol.Config.deserialize(config_bytes)
            filter_snapshot(snap, config)
            send_snapshot(conn, snap.SerializeToString())
            #print(f"client: done sending snapshot {debug_counter}")
            num_snapshot += 1

if __name__ == '__main__':
    #print(f"client main: {main.commands}")
    main()


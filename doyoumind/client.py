import click
import time
import struct
import socket



from .utils.connection import Connection
from .readers.reader import Reader
from . import protocol



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
    if 'translation' not in config:
        snap.pose.ClearField("translation")
    if 'rotation' not in config:
        snap.pose.ClearField("rotation")
    if 'color_image' not in config:
        snap.ClearField("color_image")
    if 'depth_image' not in config:
        snap.ClearField("depth_image")
    if 'feelings' not in config:
        snap.ClearField("feelings")


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


print("CLIENT.PY: TODO- REMOVE UPLOAD_THOUGHT! (do it after implementing the API)")
#@main.command
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


if __name__ == '__main__':
    print(f"client main: {main.commands}")
    main()


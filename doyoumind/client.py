import time
import struct
import socket
#from . import cli
from cli import CommandLineInterface

from utils.connection import Connection
from readers.reader import Reader
from readers import cortex_pb2
import protocol

import click

cli = CommandLineInterface()


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

@cli.command
def upload_sample(host, port, path, read_type='protobuf'):
    with Connection.connect(host, int(port)) as conn:
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

        #print("done!")
 


        """send_hello(conn, hello.SerializeToString())
        print("reading config")
        config_bytes = get_config(conn)
        print(f"the config bytes that client got: {config_bytes}")
        config = protocol.Config.deserialize(config_bytes)
        print(f"upload_sample- config is: {config.fields}")
        #config = protocol.Config.deserialize(get_config(conn))
        for snap in r:
            print("upload_sample: sending snap!!!")
            filter_snapshot(snap, config)
            send_snapshot(conn, snap.SerializeToString())
            print("upload_sample: snapshot sent ;)")
            break"""




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


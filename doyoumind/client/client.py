
import time
import struct
import socket



from ..utils.connection import Connection
from ..readers.reader import Reader
from .. import protocol
from .constants import ALL_FIELDS





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
    Update the snapshot so it'll only have the fields described in config.
    :param snap: the snapshot about to be sent to the server 
    :type snap: doyoumind_pb2.Snapshot
    :param config: the configuration of available topics
    :type config: protocol.Config
    """
    for field in ALL_FIELDS:
        if field not in config:
            snap.ClearField(field)


def upload_sample(host, port, path, read_type='protobuf'):
    """
    Upload the sample from the file to the server, using the hello-->config-->snapshot protocol.
    WARNING: only the protobuf reader has been tested- this may lead to problems
    when using a binary reader!

    :param host: the server's host, defaults to '127.0.0.1' in the CLI
    :type host: str, optional
    :param port: the server's port, defaults to 8000 in the CLI
    :type port: int, optional
    :param path: the path for the sample path
    :type path: str
    :param read_type: the type of reader for the file, defaults to 'protobuf'
    :type read_type: str, optional
    """
    with Connection.connect(host, port) as conn:
        zipped = (path.endswith(".gz"))
        r = Reader(path, read_type, zipped)
        #print("reading hello")
        hello = r.read_hello()
        hello_bytes = hello.SerializeToString()
        num_snapshot = 1
        for snap in r:
            send_hello(conn, hello_bytes)
            config_bytes = get_config(conn)
            config = protocol.Config.deserialize(config_bytes)
            filter_snapshot(snap, config)
            send_snapshot(conn, snap.SerializeToString())
            num_snapshot += 1




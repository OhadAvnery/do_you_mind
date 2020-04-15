import datetime
import time
import struct
import socket
import sys
import threading
from pathlib import Path
import os
from cli import CommandLineInterface
from protocol import Config
from parsers.main_parser import MainParser, Context
from readers import cortex_pb2
from utils.connection import Connection
#from readers.reader import read_hello

"""
NOTE!!!!! -
my server doesn't use the Listener and Connection classes yet, as I'm still not sure
how to use it in a 'correct' way.
"""

cli = CommandLineInterface()
MAX_CONN = 1000

SUPPORTED_FIELDS = ["translation", "rotation", "feelings", "color_image", "depth_image"]
class Handler(threading.Thread):
    lock = threading.Lock()
    def __init__(self, connection, data_dir):
        super().__init__()
        self.connection = connection
        self.dir = Path(data_dir)

    def get_hello(self):
        return self.connection.receive_message()

    def send_config(self, config_msg):
        self.connection.send_message(config_msg)

    def get_snapshot(self):
        return self.connection.receive_message()

    def run(self):
        while True:
            hello_msg = self.get_hello()
            hello = cortex_pb2.User()       
            hello.ParseFromString(hello_msg)
           
            user_id = hello.user_id

            config = Config(SUPPORTED_FIELDS)
            config_msg = config.serialize()
            #print(f"sending config, bytes: {config_msg}, num. fields: {len(config.fields)}")
            self.send_config(config_msg)
            snap = cortex_pb2.Snapshot()
            snap.ParseFromString(self.get_snapshot())
            #print("server/run: done parsing")

            #example format: 2019-12-04_12-00-00-500000
            time_epoch = snap.datetime // 1000 #converting milliseconds to seconds
            time_string = datetime.datetime.fromtimestamp(time_epoch).strftime("%Y-%m-%d_%H-%M-%S-%f")

            context = Context(self.dir / f"{user_id}" / time_string)
            main_parser = MainParser(SUPPORTED_FIELDS)
            main_parser.parse(context, snap)
        #print("server/run: done run")

        try:
            pass
        except Exception as e:
            print(e)

@cli.command
def run_server(address, data):
    """
    address - the server's address, given as a string host:port
    data - the data directory in which to write the thoughts
    """
    ip_address, port = address.split(":")
    port = int(port)
    server = socket.socket()
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((ip_address, port))
    server.listen(MAX_CONN)
    
    try:
        while True:
            conn, addr = server.accept()
            handler = Handler(Connection(conn), data)
            handler.start()

    except KeyboardInterrupt:
        sys.exit()
    finally:
        server.close()


if __name__ == '__main__':
    cli.main()
    

        

        
        
        

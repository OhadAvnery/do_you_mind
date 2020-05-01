import datetime
import struct
import socket
import sys
import threading
import time
from pathlib import Path
import os

from google.protobuf.json_format import MessageToDict
import numpy as np
import json

from cli import CommandLineInterface
from parsers.main_parser import MainParser, Context
from protocol import Config
from mq.publisher import publish_by_url
from readers import cortex_pb2
from utils.connection import Connection
from constants import SUPPORTED_FIELDS

#from readers.reader import read_hello



cli = CommandLineInterface()
MAX_CONN = 1000


class Handler(threading.Thread):
    lock = threading.Lock()
    def __init__(self, connection, data_dir, publish):
        """
        publish- a function that takes a message and publishes it
        """
        super().__init__()
        self.connection = connection
        self.dir = Path(data_dir)

        #publish should be a string.
        #if it's a string like 'rabbitmq://127.0.0.1:5672/',
        #we turn it to a function. 
        if isinstance(publish, str):
            self.publish = lambda msg, context: publish_by_url(publish, msg, context)
        else: 
            self.publish = publish

    def get_hello(self):
        return self.connection.receive_message()

    def send_config(self, config_msg):
        self.connection.send_message(config_msg)

    def get_snapshot(self):
        return self.connection.receive_message()

    def run(self):
        num_snapshot = 1
        while True:
            #print(f"server: proccessing message {debug_counter}...")
            hello_msg = self.get_hello()
            if not hello_msg:
                break
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
            time_epoch = snap.datetime / 1000 #converting milliseconds to seconds
            time_string = datetime.datetime.fromtimestamp(time_epoch).strftime("%Y-%m-%d_%H-%M-%S-%f")
            snapshot_dir = self.dir / f"{user_id}" / time_string
            context = Context(snapshot_dir)
            snapshot_json = self.snapshot_to_json(snap, context) 
            self.publish(snapshot_json, context)

            #print(f"server: done proccessing message {debug_counter}")
            num_snapshot += 1
        #print("server/run: done run")



    def snapshot_to_json(self, snapshot, context):
        """
        converts the snapshot object to a json string.
        In order to not make the json file too big, we save the image+depth data into a temp file,
        and in the json, save the file's path.
        """
        Handler.lock.acquire()

        context.make_dir()

        color_image_filename = 'color_image.raw'
        context.save(color_image_filename, snapshot.color_image.data)

        depth_image_filename = 'depth_image.raw'
        #create new file and save the depth image's float list in it
        with open(context.path(depth_image_filename), "wb+") as f:
            np.save(f, list(snapshot.depth_image.data)) 


        Handler.lock.release()

        snap_dict = MessageToDict(snapshot, preserving_proto_field_name=True)
        print(snap_dict.keys())

        snap_dict['color_image']['data'] = str(context.path(color_image_filename))
        snap_dict['depth_image']['data'] = str(context.path(depth_image_filename))

        return json.dumps(snap_dict)


@cli.command
def run_server(address, data, publish):
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
            handler = Handler(Connection(conn), data, publish)
            handler.start()

    except KeyboardInterrupt:
        sys.exit()
    finally:
        server.close()


if __name__ == '__main__':
    cli.main()
    

        

        
        
        

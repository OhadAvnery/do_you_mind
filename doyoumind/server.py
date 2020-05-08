import click
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

from .constants import SUPPORTED_FIELDS
from .mq.constants import SERVER_EXCHANGE
from .mq.publisher_parser import PublisherParser
from .protocol import Config
from .readers import cortex_pb2
from .saver.saver import Saver
from .utils.connection import Connection
from .utils.context import Context 






#from readers.reader import read_hello

@click.group()
def main():
    pass

#cli = CommandLineInterface()
MAX_CONN = 1000


class Handler(threading.Thread):
    lock = threading.Lock()
    def __init__(self, connection, database, data_dir, publish):
        """
        publish- a function that takes a message and publishes it
        """
        super().__init__()
        self.connection = connection
        self.dir = Path(data_dir)
        self.database = database

        #publish should be a string.
        #if it's a string like 'rabbitmq://127.0.0.1:5672/',
        #we turn it to a function. 
        if isinstance(publish, str):
            publisher = PublisherParser(publish)
            self.publish = publisher.publish
            print(f"our publish function: {self.publish}")
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

           
            saver = Saver(self.database)
            hello_dict = MessageToDict(hello, preserving_proto_field_name=True, \
                including_default_value_fields=True)
            #weird bug: somehow this isn't an int!!!!! 
            hello_dict['user_id'] = int(hello_dict['user_id'])
            #print("server/run:", hello_dict)
            saver.save('user', json.dumps(hello_dict))

           
            user_id = hello.user_id #an int
            config = Config(SUPPORTED_FIELDS)
            config_msg = config.serialize()
            #print(f"sending config, bytes: {config_msg}, num. fields: {len(config.fields)}")
            self.send_config(config_msg)
            snap = cortex_pb2.Snapshot()
            snap.ParseFromString(self.get_snapshot())

            #example format: 2019-12-04_12-00-00-500000
            time_epoch = snap.datetime / 1000 #converting milliseconds to seconds
            time_string = datetime.datetime.fromtimestamp(time_epoch).strftime("%Y-%m-%d_%H-%M-%S-%f")
            snapshot_dir = self.dir / f"{user_id}" / time_string
            context = Context(snapshot_dir)
            snapshot_json = self.snapshot_to_json(snap, context, user_id) 
            print("server: going to publish...")
            self.publish(snapshot_json)

            #print(f"server: done proccessing message {debug_counter}")
            num_snapshot += 1
        #print("server/run: done run")



    def snapshot_to_json(self, snapshot, context, user_id):
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

        snap_dict = MessageToDict(snapshot, preserving_proto_field_name=True, \
            including_default_value_fields=True)

        snap_dict['user_id'] = user_id
        snap_dict['snapshot_dir'] = context.dir.absolute().as_posix()
        snap_dict['color_image']['data'] = str(context.path(color_image_filename))
        snap_dict['depth_image']['data'] = str(context.path(depth_image_filename))
        snap_dict['datetime'] = int(snap_dict['datetime']) / 1000 #convert it to seconds from miliseconds
        return json.dumps(snap_dict)


@main.command()
@click.option('--host', '-h', default='127.0.0.1', type=str)
@click.option('--port', '-p', default=8000, type=int)
@click.option('--database', '-db', default='mongodb://127.0.0.1:27017', type=str)
@click.argument('publish', type=str)
def run_server(host, port, database, publish, data="/home/user/test2"):
    """
    host,port - the server's address
    database- the database in which we save the users' data, given as a url.
    defaults to mongodb.
    NOTE: this should have the same connection as the run-saver.
    publish- a function to 
    data - the data directory in which to write the thoughts.
    """
    server = socket.socket()
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((host, port))
    server.listen(MAX_CONN)
    
    try:
        while True:
            conn, addr = server.accept()
            handler = Handler(Connection(conn), database, data, publish)
            handler.start()

    except KeyboardInterrupt:
        sys.exit()
    finally:
        server.close()


if __name__ == '__main__':
    print(f"server main: {main.commands}")
    main()
    

        

        
        
        

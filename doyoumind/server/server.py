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

from ..constants import SUPPORTED_FIELDS
from ..mq.constants import SERVER_EXCHANGE
from ..mq.publisher_parser import PublisherParser
from ..readers import doyoumind_pb2
from ..saver.saver import Saver
from ..utils.protocol import Config
from ..utils.connection import Connection
from ..utils.context import Context 



MAX_CONN = 1000


class Handler(threading.Thread):
    lock = threading.Lock()
    def __init__(self, connection, database, data_dir, publish):
        """
        Create a new handler.

        :param connection: an object representing the server+client connection.
        :type connection: utils.connection.Connection
        :param database: the database's drive url (currently only supports mongodb)
        :type database: str
        :param data_dir: the data directory to write the snapshots in
        :type data_dir: str
        :param publish: a function that takes a message and publishes it.
        (or a str, representing a message queue to publish to)
        :type publish: function/str
        :returns: handler object
        :rtype: Handler
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
        '''
        runs the server, waiting for connections from clients.
        '''

        num_snapshot = 1
        while True:
            #print(f"server: proccessing message {debug_counter}...")
            hello_msg = self.get_hello()
            if not hello_msg:
                break
            hello = doyoumind_pb2.User()       
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
            snap = doyoumind_pb2.Snapshot()
            snap.ParseFromString(self.get_snapshot())

            #example format: 2019-12-04_12-00-00-500000
            time_epoch = snap.datetime / 1000 #converting milliseconds to seconds
            time_string = datetime.datetime.fromtimestamp(time_epoch).strftime("%Y-%m-%d_%H-%M-%S-%f")
            snapshot_dir = self.dir / f"{user_id}" / time_string
            context = Context(snapshot_dir)
            snapshot_json = self.snapshot_to_json(snap, context, user_id) 
            #print(f"server: the snapshot to be published: {snapshot_json}")
            self.publish(snapshot_json)

            #print(f"server: done proccessing message {debug_counter}")
            num_snapshot += 1
        #print("server/run: done run")



    def snapshot_to_json(self, snapshot, context, user_id):
        """
        Converts the snapshot object to a json string.
        In order to not make the json file too big, we save the image+depth data into a temp file,
        and in the json, save the file's path.

        :param snapshot: the snapshot read from the client
        :type snapshot: doyoumind.Snapshot
        :param context: the snapshot's context
        :type context: protocol.Context
        :returns: json string
        :rtype: str
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


def run_server(host, port, database, publish, data="/home/user/test"):
    """
    Run the server at the given host+port, listening to clients, reading their snapshots
    and sending them to consumers.
    NOTE: the server also directly connects to the database,
    in order to save the user's details.

    :param host: the server's host, defaults to '127.0.0.1' in the CLI
    :type host: str, optional
    :param port: the server's port, defaults to 8000 in the CLI
    :type port: int, optional
    :param database: the database's drive url, defaults to 'mongodb://127.0.0.1:27017' in the CLI
    (currently only supports mongodb)
    :type database: str, optional
    :param publish: a function that's activated on any read snapshot.
    in the API, expects a function object.
    in the CLI, expects a message queue drive url to publish the snapshots to.
    :type publish: function/str
    :param data: the data directory to write the snapshots in, defaults to a test folder.
    :type data: str, optional
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
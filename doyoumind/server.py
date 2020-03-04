import time
import struct
import socket
import sys
import threading
from pathlib import Path
import os
from do_you_mind.cli import CommandLineInterface

"""
NOTE!!!!! -
my server doesn't use the Listener and Connection classes yet, as I'm still not sure
how to use it in a 'correct' way.
"""

cli = CommandLineInterface()
MAX_CONN = 1000

class Handler(threading.Thread):
    lock = threading.Lock()
    def __init__(self, connection, data_dir):
        super().__init__()
        self.connection = connection
        self.data_dir = data_dir
    def run(self):
        try:
            data = b''
            while True:
                temp_data = self.connection.recv(1024)
                if not temp_data:
                    break
                data += temp_data


            offset = 0
            
            user_id = struct.unpack_from("Q", data, offset)[0]
            offset += struct.calcsize("Q")
            
            timestamp = struct.unpack_from("Q", data, offset)[0]
            offset += struct.calcsize("Q")

            thought_size = struct.unpack_from("I", data, offset)[0]
            offset += struct.calcsize("I")

            thought_data = struct.unpack_from("{:d}s".format(thought_size), \
                                             data, offset)[0].decode()

            time_date_format = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime(timestamp))

            # thought_path = "{}/{}/{}.txt".format(self.data_dir, user_id, time_date_format)
            thought_path = "{}/{}".format(self.data_dir, user_id)
            filename = "{}.txt".format(time_date_format)

            # We need to check if thought_path exists, and if not, create the needed directories
            p = Path(thought_path)
            p_file = p / filename

            self.lock.acquire()
            try:
                if not p.exists():
                    p.mkdir(parents=True)
                if not p_file.exists():
                    p_file.touch()
                thought_file = p_file.open('a') # mode 'a' so it appends instead of writing over previous thoughts
                is_file_nonempty = p_file.stat().st_size > 0
                if is_file_nonempty:
                    thought_file.write('\n')
                thought_file.write(thought_data)
                thought_file.close()
            finally:
                self.lock.release()

            
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
            handler = Handler(conn, data)
            handler.start()

    except KeyboardInterrupt:
        sys.exit()
    finally:
        server.close()

"""def main(argv):
    if len(argv) != 3:
        print(f'USAGE: {argv[0]} <ip_address>:<port> <data_dir>')
        return 1
    try:
        address, data_dir = argv[1:]
        ip_address, port = address.split(":")
        fixed_address = (ip_address, int(port))
        run_server(fixed_address, data_dir)
        print('done')
    except Exception as error:
        print(f'ERROR: {error}')
        return 1"""


if __name__ == '__main__':
    cli.main()
    

        

        
        
        

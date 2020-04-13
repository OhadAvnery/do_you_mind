import socket
import struct

class Connection:
    def __init__(self, socket):
        self.socket = socket

    def __repr__(self):
        local_addr, local_port = self.socket.getsockname()
        peer_addr, peer_port = self.socket.getpeername()

        return f'<Connection from {local_addr}:{local_port} to {peer_addr}:{peer_port}>'

    #context methods
    def __enter__(self):
        return self
    def __exit__(self, exception, error, traceback):
        self.close()

    def send(self, data):
        self.socket.sendall(data)

    @classmethod
    def connect(cls, host, port):
        sock = socket.socket()
        sock.connect((host, port))
        return cls(sock)



    def receive(self, size):
        """
        receives at most size bytes of information
        """

        """data = b''
        while True:
            temp_data = self.socket.recv(1024)
            if not temp_data:
                break
            data += temp_data"""


        #Maybe change this in the future
        data = self.socket.recv(size)
        if len(data) < size:
            raise Exception

        return data

    def close(self):
        self.socket.close()

    def send_message(self, msg):
        """
        sends the message to the server, stating with the string's length.
        NOTE- it works both if msg has type str and if it has type bytes.
        """
        msg_len_bytes = struct.pack("<I", len(msg))
        if isinstance(msg, str):
            msg = msg.encode()
        self.socket.sendall(msg_len_bytes + msg)

    def receive_message(self):
        """
        returns a bytes object.
        """
        msg_len_bytes = self.socket.recv(struct.calcsize("<I"))
        msg_len, = struct.unpack("<I", msg_len_bytes)
        msg = self.socket.recv(msg_len)
        if len(msg) < msg_len:
            raise Exception

        return msg


import socket
import struct

class Connection:
    '''
    A class representing an abstract connection.
    The connection works above a regular socket, with a simplification-
    all messages sent using Connection start with 
    a declaration of the number of bytes to be sent.
    :param socket: the socket we're communicating over
    :type socket: socket.socket
    '''
    def __init__(self, socket):
        self.socket = socket

    def __repr__(self):
        local_addr, local_port = self.socket.getsockname()
        peer_addr, peer_port = self.socket.getpeername()

        return f'<Connection from {local_addr}:{local_port} to {peer_addr}:{peer_port}>'

    # context methods
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
        receives size bytes of information.
        :param size: the number of bytes to receive
        :type size: int
        :returns: the received data
        :rtype: bytes
        """

        data = b''
        num_bytes_left = size
        while num_bytes_left:
            temp_data = self.socket.recv(num_bytes_left)
            if not temp_data:
                break
            data += temp_data
            num_bytes_left -= len(temp_data)

        return data

    def close(self):
        self.socket.close()

    def send_message(self, msg):
        """
        sends the message to the server, stating with the string's length.
        NOTE- it works both if msg has type str and if it has type bytes.
        :param msg: the message to be sent
        :type msg: str/bytes
        """
        msg_len_bytes = struct.pack("<I", len(msg))
        if isinstance(msg, str):
            msg = msg.encode()
        self.socket.sendall(msg_len_bytes + msg)

    def receive_message(self):
        """
        returns a bytes object containing the received message.
        if no message was received, returns None.
        :raises Exception: exception if the length of the received message is less than msg_len
        :returns: the received message
        :rtype: bytes 
        """

        msg_len_bytes = self.receive(struct.calcsize("<I"))
        if not msg_len_bytes:
            return None

        msg_len, = struct.unpack("<I", msg_len_bytes)
        msg = self.receive(msg_len)
        if len(msg) < msg_len:
            raise Exception

        return msg

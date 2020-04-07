from .connection import Connection
import socket

class Listener:
    def __init__(self, port, host='0.0.0.0', backlog=1000, reuseaddr=True):
        self.port = port
        self.host = host
        self.backlog = backlog
        self.reuseaddr = reuseaddr

        self.server = socket.socket()
        if self.reuseaddr:
            self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((host, port))


    #context methods
    def __enter__(self):
        self.start()
        return self
    def __exit__(self, exception, error, traceback):
        self.stop()


    def __repr__(self):
        return f'Listener(port={self.port}, host={self.host!r}, backlog={self.backlog}, reuseaddr={self.reuseaddr})'

    def start(self):
        self.server.listen(self.backlog) 

    def accept(self):
        conn, addr = self.server.accept()
        return Connection(conn)

    def stop(self):
        self.server.close()
from . import binary_reader
from . import protobuf_reader
from . import hello_pb2

class Reader:
    def __init__(self, path, format, zipped=True):
        if format=='binary':
            self.reader = binary_reader.Reader(path, zipped)
        elif format == 'protobuf':
            self.reader = protobuf_reader.Reader(path, zipped)
    
    def read_user(self):
        return self.reader.read_user()

    #we implement read_hello using read_user,
    #if they'll become different we'll implement them differently, and use the hello class from hello.proto.
    def read_hello(self):
        return self.reader.read_user()

    def read_snapshot(self):
        return self.reader.read_snapshot()

    def __iter__(self): 
        return self._snapshots_generator()

    def _snapshots_generator(self):
        filesize = self.reader.path.stat().st_size
        while self.reader.offset < filesize:
            yield self.read_snapshot()
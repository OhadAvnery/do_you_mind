from . import binary_reader
from . import protobuf_reader

class Reader:
    def __init__(self, path, format, zipped=True):
        if format=='binary':
            self.reader = binary_reader.Reader(path, zipped)
        elif format == 'protobuf':
            self.reader = protobuf_reader.Reader(path, zipped)
    
    def read_user(self):
        return self.reader.read_user()

    def read_snapshot(self):
        return self.reader.read_snapshot()

    def __iter__(self): 
        return self._snapshots_generator()

    def _snapshots_generator(self):
        filesize = self.reader.path.stat().st_size
        while self.reader.offset < filesize:
            yield self.read_snapshot()
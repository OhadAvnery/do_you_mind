import gzip
import struct
from PIL import Image
from pathlib import Path

from . import doyoumind_pb2
from ..utils.reader_utils import *


class Reader:
    """An implementation of the reader for files in protobuf format.
    For full documentation on the functions, see the main Reader class.
    """
    def __init__(self, path, zipped=True):
        self.offset = 0
        self.path = Path(path)
        if zipped:
            self.open_func = lambda p: gzip.open(p, 'rb')
        else:
            self.open_func = lambda p: open(p, 'rb')

    def read_user(self):
        user = doyoumind_pb2.User()
        with (self.open_func)(self.path) as file:  
            size = unpack_format(file, '<I')    
            user.ParseFromString(file.read(size))
            self.offset = file.tell()
        return user

    def read_snapshot(self):
        snap = doyoumind_pb2.Snapshot()
        with (self.open_func)(self.path) as file:
            file.seek(self.offset)
            size = unpack_format(file, '<I')        
            snap.ParseFromString(file.read(size))
            self.offset = file.tell()

        return snap

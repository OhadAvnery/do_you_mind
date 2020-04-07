import gzip
import struct
from PIL import Image
from pathlib import Path

from . import cortex_pb2
from utils.reader_utils import *


#from .utils.reader_utils import *

class Reader:
    def __init__(self, path, zipped=True):
        self.offset = 0
        self.path = Path(path)
        if zipped:
            self.open_func = lambda p: gzip.open(p, 'rb')
        else:
            self.open_func = lambda p: open(p, 'rb')
        #self.file = (self.open_func)(path)
        #self.user = cortex_pb2.User()
        #with (self.open_func)(self.path) as file:            
         #   self.user.ParseFromString(file.read())

    def read_user(self):
        user = cortex_pb2.User()
        with (self.open_func)(self.path) as file:  
            size = unpack_format(file, '<I')        
            user.ParseFromString(file.read(size))
            self.offset = file.tell()
        return user

    def read_snapshot(self):
        snap = cortex_pb2.Snapshot()
        with (self.open_func)(self.path) as file:  
            file.seek(self.offset)   
            size = unpack_format(file, '<I')         
            snap.ParseFromString(file.read(size))
            self.offset = file.tell()

        """#ugly trick- change the snap's color image to actually be an Image object
        color_image = snap.color_image
        snap.color_image = Image.frombytes("RGB", (color_image.width, color_image.height), color_image.data)
        depth_image = snap.depth_image
        snap.depth_image = Image.frombytes("L", (depth_image.width, depth_image.height), depth_image.data)"""

        return snap
            
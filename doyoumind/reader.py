import gzip
import struct
from PIL import Image
from pathlib import Path


from .utils.reader_utils import *

class User:
    def __init__(self, user_id, username, birthdate, gender):
        self.user_id = user_id
        self.username = username
        self.birthdate = birthdate
        self.gender = gender

    def __str__(self):
        return f"ID: {self.user_id}, username: {self.username}, age: {self.birthdate}, gender: {self.gender}"

class Snapshot:
    def __init__(self, timestamp, translation, rotation, color_image, \
        depth_image, user_feelings):
        self.timestamp = timestamp
        self.translation = translation
        self.rotation = rotation
        self.color_image = color_image
        self.depth_image = depth_image
        self.user_feelings = user_feelings
    

"""class Image:
    #img_type- 'd' (for depth) or 'c' (for color)
    def __init__(self, height, width, vals, img_type):
        self.height = height
        self.width = width
        self.vals = vals
        self.img_type = img_type"""

class UserFeelings:
    """
    4 floats between -1 and 1 representing the feelings
    """
    def __init__(self, hunger, thirst, exhaustion, happiness):
        self.hunger = hunger
        self.thirst = thirst
        self.exhaustion = exhaustion
        self.happiness = happiness

class Reader:
    """Note about formats:
    'uint64':'Q', 'uint32':'L', 'double':'d', 'char':'c', 'float':'f'
    """
    def __init__(self, path, zipped=True):
        
        #self.user_id = 0
        #self.username = ""
        #self.__file = open(path, 'rb')
        self.offset = 0
        self.path = Path(path)
        if zipped:
            self.open_func = lambda p: gzip.open(p, 'rb')
        else:
            self.open_func = lambda p: open(p, 'rb')
        #self.file = (self.open_func)(path)
        with (self.open_func)(self.path) as file:
            user_id = unpack_format(file, '<Q')
            username_length = unpack_format(file, '<L') 
            username = unpack_string(file, username_length)
            birthdate = unpack_format(file, '<L')
            gender = unpack_format(file, 'c')
            self.offset = file.tell()


        self.user = User(user_id, username, birthdate, gender)
        #print(self.user)


    
    def __iter__(self): 
        return self._snapshots_generator()

    def _snapshots_generator(self):
        filesize = self.path.stat().st_size
        while self.offset < filesize:
            yield self._get_next_snapshot()

    #returns the next snapshot
    def _get_next_snapshot(self):
        with (self.open_func)(self.path) as file:
            file.seek(self.offset)

            timestamp = unpack_format(file, '<Q')
            translation = unpack_format(file, 'ddd')
            rotation = unpack_format(file, 'dddd')

            c_height = unpack_format(file, '<L')
            c_width = unpack_format(file, '<L')
            print(f"color img dimensions: {c_height}x{c_width}")
            c_vals = file.read(c_height*c_width*3)
            color_image = Image.frombytes("RGB", (c_width, c_height), c_vals)

            d_height = unpack_format(file, '<L')
            d_width = unpack_format(file, '<L')
            print(f"depth img dimensions: {c_height}x{c_width}")
            d_vals = file.read(d_height*d_width*struct.calcsize('f'))
            depth_image = Image.frombytes("L", (d_width, d_height), d_vals)

            hunger, thirst, exaustion, happiness = unpack_format(file, 'ffff')
            user_feelings = UserFeelings(hunger, thirst, exaustion, happiness)

            self.offset = file.tell()

            snap = Snapshot(timestamp, translation, rotation, color_image, \
            depth_image, user_feelings)
        return snap

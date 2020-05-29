import gzip
import struct
from PIL import Image
from pathlib import Path


from ..utils.reader_utils import *

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
        self.datetime = timestamp
        self.translation = translation
        self.rotation = rotation
        self.color_image = color_image
        self.depth_image = depth_image
        self.user_feelings = user_feelings
    

class ReaderImage:
    '''img_type- 'd' (for depth) or 'c' (for color)'''
    def __init__(self, width, height, vals, img_type):
        self.height = height
        self.width = width
        self.data = vals
        self.img_type = img_type

class UserFeelings:
    """
    4 floats between -1 and 1 representing the feelings.
    """
    def __init__(self, hunger, thirst, exhaustion, happiness):
        self.hunger = hunger
        self.thirst = thirst
        self.exhaustion = exhaustion
        self.happiness = happiness

class Reader:
    """An implementation of the reader for files in binary format.
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
        with (self.open_func)(self.path) as file:
            user_id = unpack_format(file, '<Q')
            username_length = unpack_format(file, '<L') 
            username = unpack_string(file, username_length)
            birthdate = unpack_format(file, '<L')
            gender = unpack_format(file, 'c')
            self.offset = file.tell()

        #self.user = User(user_id, username, birthdate, gender)
        return User(user_id, username, birthdate, gender)

                                    
    #returns the next snapshot
    def read_snapshot(self):
        with (self.open_func)(self.path) as file:
            file.seek(self.offset)

            timestamp = unpack_format(file, '<Q')
            translation = unpack_format(file, 'ddd')
            rotation = unpack_format(file, 'dddd')

            c_height = unpack_format(file, '<L')
            c_width = unpack_format(file, '<L')
            #print(f"color img dimensions: {c_height}x{c_width}")
            c_vals = file.read(c_height*c_width*3)
            color_image = ReaderImage(c_width, c_height, c_vals, 'c')
            #color_image = Image.frombytes("RGB", (c_width, c_height), c_vals)

            d_height = unpack_format(file, '<L')
            d_width = unpack_format(file, '<L')
            #print(f"depth img dimensions: {c_height}x{c_width}")
            d_vals = file.read(d_height*d_width*struct.calcsize('f'))
            depth_image = ReaderImage(d_width, d_height, d_vals, 'd')
            #depth_image = Image.frombytes("L", (d_width, d_height), d_vals)

            hunger, thirst, exaustion, happiness = unpack_format(file, 'ffff')
            user_feelings = UserFeelings(hunger, thirst, exaustion, happiness)

            self.offset = file.tell()

            snap = Snapshot(timestamp, translation, rotation, color_image, \
            depth_image, user_feelings)
        return snap

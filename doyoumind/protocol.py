import struct
from utils.reader_utils import PackedString
from readers import hello_pb2

"""class Hello:
    def __init__(self, user_id, username, birthdate, gender):
        self.user_id = user_id
        self.username = username
        self.birthdate = birthdate
        self.gender = gender

    def serialize(self):
        \"""
        turns the Hello object into a message string 
        \"""
        hello_msg = b''
        hello_msg += struct.pack('<Q', self.user_id)
        hello_msg += struct.pack('<L', self.username_length) 
        hello_msg += struct.pack(f'{self.username_length}s', self.username)
        hello_msg += struct.pack('<L', self.birthdate)
        hello_msg += struct.pack('c', self.gender)
        return hello_msg


    @classmethod
    def deserialize(msg):
        \"""
        turns the message string into a Hello object
        \"""
        packed_msg = PackedString(msg)

        user_id, = packed_msg.unpack('<Q')
        username_length, = packed_msg.unpack('<L')
        username = packed_msg.unpack(f'{username_length}s')
        birthdate, = packed_msg.unpack('<L')
        gender, = packed_msg.unpack('c')

        return Hello(user_id, username, birthdate, gender)"""

class Config:
    #field - a list of strings
    def __init__(self, fields):
        self.fields = fields 

    def __contains__(self, field):
        return field in self.fields

    def serialize(self):
        """
        turns the Config object into a message string
        """
        config_msg = b''
        num_fields = len(self.fields)
        config_msg += struct.pack('<L', num_fields)
        for field in self.fields:
            config_msg += struct.pack('<L', len(field))
            config_msg += struct.pack(f'{len(field)}s', field.encode())

        return config_msg

    @staticmethod
    def deserialize(msg):
        """
        turns the message string into a Config object
        """
        packed_msg = PackedString(msg)
        fields = []

        num_fields, = packed_msg.unpack('<L')
        print("number of fields: ", num_fields)

        for _ in range(num_fields):
            field_len, = packed_msg.unpack('<L')
            print(f"field len: {field_len}")
            field, = packed_msg.unpack(f'{field_len}s')
            fields.append(field.decode())

        return Config(fields)

class Snapshot:
    pass
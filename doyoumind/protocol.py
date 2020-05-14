import struct
from .utils.reader_utils import PackedString
from .readers import hello_pb2



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
        #print("number of fields: ", num_fields)

        for _ in range(num_fields):
            field_len, = packed_msg.unpack('<L')
            #print(f"field len: {field_len}")
            field, = packed_msg.unpack(f'{field_len}s')
            fields.append(field.decode())

        return Config(fields)

class Snapshot:
    pass
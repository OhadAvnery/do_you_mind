import struct
from .utils.reader_utils import PackedString
from .readers import hello_pb2



class Config:
    """
    A class representing the snapshot's supported fields.
    :param fields: a list of supported fields for the snapshot
    :type fields: List[str]

    """
    def __init__(self, fields):
        """
        makes a new Config object with the given fields.
        :param fields: a list of supported fields for the snapshot
        :type fields: List[str]
        """
        self.fields = fields 

    def __contains__(self, field):
        return field in self.fields

    def serialize(self):
        """
        turns the Config object into a message string.
        :returns: a message representing the supported fields
        :rtype: str
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
        turns the message string into a Config object.
        :param msg: the string with the supported fields
        :type msg: str
        :returns: a Config object with the given fields
        :rtype: Config
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


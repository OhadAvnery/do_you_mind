import struct

from . import binary_reader
from . import protobuf_reader
from . import hello_pb2


DRIVERS = {'binary': binary_reader, 'protobuf': protobuf_reader}
class Reader:
    '''
    A class representing an objects that reads the client's sample.
    :param reader: the implemented reader
    :type reader: dynamic
    :param zipped: True iff the sample is compressed
    :type zipped: bool
    :param path: the path of the sample to read from
    :type path: str
    '''
    def __init__(self, path, format, zipped=True):
        '''
        Create a new reader object.
        
        :param path: the path of the sample to read from
        :type path: str
        :param format: the reader's format (binary or protobuf)
        :type format: str
        :param zipped: True iff the sample is compressed, defaults to True
        :type zipped: bool, optional
        :returns: a reader object
        :rtype: Reader
        '''
        if format=='binary':
            print("WARNING: binary reader has been deprecated and may"
                  "not behave well- use protobuf instead!")
        self.path = path
        self.zipped = zipped
        self.reader = DRIVERS[format].Reader(path, zipped)
    
    def read_user(self):
        '''
        Read the next user from the sample.

        :return: the user
        :rtype: doyoumind_pb2.User
        '''
        return self.reader.read_user()

    def read_hello(self):
        '''
        read the 'hello' message.
        NOTE: we implement read_hello using read_user,
        since they have the same content exactly.
        if they'll become different we'll implement them differently, 
        and use the Hello class from hello.proto.

        :return: hello object
        :rtype: doyoumind_pb2.User
        '''
        return self.reader.read_user()

    def read_snapshot(self):
        '''
        Read the next snapshot from the sample.

        :return: the snapshot
        :rtype: doyoumind_pb2.Snapshot
        '''
        return self.reader.read_snapshot()

    def __iter__(self): 
        return self._snapshots_generator()

    def __size(self):
        '''
        Returns the size of the uncompressed file.
        :returns: uncompressed file size
        :rtype: int
        '''
        if self.zipped:
            with open(self.path, 'rb') as f:
                f.seek(-4, 2)
                return struct.unpack('I', f.read(4))[0]
        return self.path.stat().st_size

    def _snapshots_generator(self):
        filesize = self.__size()
        while self.reader.offset < filesize:
            yield self.read_snapshot()
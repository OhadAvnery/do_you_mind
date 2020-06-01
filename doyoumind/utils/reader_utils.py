import struct


def unpack_format(file, fmt):
    '''
    Unpacks the format from the file using struct.unpack,
    to the correct number of bytes, and returns the result.
    :param file: the file to read from
    :type file: Path
    :param fmt: the format to read
    :type fmt: str
    :returns: the result of the read
    :rtype: str/List(str)
    '''
    vals = struct.unpack(fmt, file.read(struct.calcsize(fmt)))
    if len(vals) == 1:  # vals is a tuple of the form (x,)
        return vals[0]
    else: 
        return vals


def unpack_string(file, str_len):
    return struct.unpack("{:d}s".format(str_len), file.read(str_len))[0].decode()


fmt = {'uint64': 'Q', 'uint32': 'L', 'double': 'd'}
size = {st:struct.calcsize(val) for st, val in fmt.items()}


class PackedString:
    '''
    an object representing a string, together with an offset that saves
    where we read from last.
    :param msg: The message string
    :type msg: str
    :param offset: the offset of the string we're reading
    :type offset: int
    '''
    def __init__(self, msg):
        self.msg = msg
        self.offset = 0

    def unpack(self, fmt):
        val = struct.unpack_from(fmt, self.msg, self.offset)
        self.offset += struct.calcsize(fmt)
        return val

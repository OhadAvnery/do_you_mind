import struct

#fmt = {'uint64':'Q', 'uint32':'L', 'double':'d', 'char':'c', 'float':'f'}
#size = {st:struct.calcsize(val) for st,val in fmt.items()}

"""def unpack_format(file, fmt_str):
    return struct.unpack(fmt[fmt_str], file.read(size[fmt_str]))"""

def unpack_format(file, fmt):
    #int_fmts = {'Q', 'L'}
    vals = struct.unpack(fmt, file.read(struct.calcsize(fmt)))
    if len(vals) == 1: #vals is a tuple of the form (x,)
        return vals[0]
    else: 
        return vals

def unpack_string(file, str_len):
    return struct.unpack("{:d}s".format(str_len), \
                                         file.read(str_len) )[0].decode()


fmt = {'uint64':'Q', 'uint32':'L', 'double':'d'}
size = {st:struct.calcsize(val) for st,val in fmt.items()}



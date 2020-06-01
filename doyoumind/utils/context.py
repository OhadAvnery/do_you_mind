import json
import os
from pathlib import Path 

class Context:
    '''
    An object representing the directory a certain object is using.
    :param dir: a PosixPath object representing the path
    :type dir: PosixPath
    :param dir_string: a string represnting the path
    :type dir_string: str
    '''
    def __init__(self, dir_name):
        """
        Create a new Context object with the given directory.
        :param dir_name: a string/Path object for the directory
        :type dir_name: str/PosixPath
        :returns: new Context object
        :rtype: Context
        """
        if isinstance(dir_name, str):
            self.dir = Path(dir_name)
            self.dir_string = dir_name
        else:  # if it's a PosixPath
            self.dir = dir_name
            self.dir_string = dir_name.absolute().as_posix()

    def make_dir(self):
        os.makedirs(self.dir, exist_ok=True)

    def path(self, filename):
        return self.dir / filename

    def save(self, filename, data=""):
        """
        create a new file with the given filename, and write to it the given data.
        If no data parameter is given, create a new empty file.
        :param filename: filename of file to create
        :type filename: PosixPath
        :param data: data to write, defaults to ""
        :type data: str/bytes, optional
        """
        open_fmt = 'wb+' if isinstance(data, bytes) else 'w+'        
        with open(self.dir / filename, open_fmt) as f:
            f.write(data)


def context_from_snapshot(snapshot):
    """
    given a json string representing a snapshot, return a Context object of the snapshot's dir.
    :param snapshot: json string representing a snapshot
    :type snapshot: str
    :returns: a Context object of the snapshot's dir
    :rtype: Context
    """
    snap_dict = json.loads(snapshot)
    return Context(snap_dict['snapshot_dir'])

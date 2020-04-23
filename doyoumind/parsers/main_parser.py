import os
from pathlib import Path

from .__init__ import __parsers__



class MainParser:
    def __init__(self, fields):
        self.fields = fields

    
    def parse(self, context, snapshot):
        for parse_func in __parsers__:
            for field in parse_func.fields:
                if field not in self.fields:
                    continue
            parse_func(context, snapshot)

class Context:
    def __init__(self, dir_name):
        """
        dir - a PosixPath object
        """
        self.dir = dir_name
    def make_dir(self):
        os.makedirs(self.dir, exist_ok=True)
    def path(self, filename):
        return self.dir / filename
    def save(self, filename, string=""):
        """create a new file with the given filename, and put in it the given string.
        If no string parameter is given, create a new empty file."""
        open_fmt = 'wb+' if isinstance(string, bytes) else 'w+'        
        with open(self.dir / filename, open_fmt) as f:
            f.write(string)




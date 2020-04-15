import os
from pathlib import Path

from .__init__ import __parsers__
"""from .color_image import *
from .depth_image import *
from .feelings import *
from .pose import *
from .location import *"""


class MainParser:
    def __init__(self, fields):
        self.fields = fields
        #self.dir = working_dir #working directory

    
    def parse(self, context, snapshot):
        for parse_func in __parsers__:
            for field in parse_func.fields:
                if field not in self.fields:
                    continue
            parse_func(context, snapshot)

        """for field in self.fields:
            func_name = f'parse_{field}'
            parse_func = globals()[func_name]
            parse_func(context, snapshot)"""


class Context:
    def __init__(self, dir_name):
        """
        dir - a PosixPath object
        """
        self.dir = dir_name
    def path(self, filename):
        return self.dir / filename
    def save(self, filename, string):
        os.makedirs(self.dir, exist_ok=True)
        with open(self.dir / filename, "w+") as f:
            f.write(string)



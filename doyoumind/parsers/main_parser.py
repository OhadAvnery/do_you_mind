from .color_image import *
from .depth_image import *
from .feelings import *
from .rotation import *
from .translation import *

#PARSERS_DIR = ""
class MainParser:
    def __init__(self, fields, working_dir):
        self.fields = fields
        self.dir = working_dir #working directory

    def parse(self, context, snapshot):
        for field in self.fields:
            func_name = f'parse_{field}'
            parse_func = globals()[func_name]
            parse_func(context, snapshot)


class Context:
    def __init__(self, dir_name):
        """
        dir - a PosixPath object
        """
        self.dir = dir_name
    def path(filename):
        return self.dir / filename
    def save(filename, string):
        with open(self.dir / filename, "wb") as f:
            f.write(string)



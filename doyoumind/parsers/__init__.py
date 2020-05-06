from importlib import import_module
from inspect import getmembers, isfunction
import os
from pathlib import Path
import sys

from .constants import __parsers__
from ..constants import SUPPORTED_FIELDS

#PARSERS_DIR = "/home/user/do_you_mind/doyoumind/parsers"
PARSERS_DIR = os.path.dirname(__file__)
PARSERS_DIR_SHORT = PARSERS_DIR.split('/')[-1]
PARSERS_DIR_PARENT = str(Path(PARSERS_DIR).parent)
PARENT_NAME = Path(PARSERS_DIR).parent.name
UNWANTED_FILES = ['__init__.py', 'constants.py', '__main__.py']


def collect_parsers():
    """
    only collects the parsers for which we support all of their fields.
    """
    sys.path.insert(0, PARSERS_DIR_PARENT)
    my_filename = Path(__file__).name
    for filename in os.listdir(PARSERS_DIR):
        if filename in UNWANTED_FILES or not filename.endswith(".py"):
            continue
        
        short_filename = filename[:-3] #ignoring the .py suffix
        #print(f"import_module({PARSERS_DIR_PARENT}.{PARSERS_DIR_SHORT}.{short_filename})")
        #/home/user/do_you_mind/doyoumind.parsers.feelings
        parse_module = import_module(f"{PARENT_NAME}.{PARSERS_DIR_SHORT}.{short_filename}")
        print("collect_parsers:", parse_module)
        for obj_name,obj in getmembers(parse_module):
            #we only need one function from each module.
            #we only care for the parse_X function, and we check if its supported.
            if isfunction(obj) and obj_name.startswith("parse_"):
                if all([field in SUPPORTED_FIELDS for field in obj.fields]):
                    __parsers__.add(obj)
                break 


collect_parsers()

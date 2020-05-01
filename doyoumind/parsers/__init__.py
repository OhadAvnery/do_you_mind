from importlib import import_module
from inspect import getmembers, isfunction
import os
from pathlib import Path
import sys

from .constants import __parsers__

#PARSERS_DIR = "/home/user/do_you_mind/doyoumind/parsers"
PARSERS_DIR = os.path.dirname(__file__)
PARSERS_DIR_SHORT = PARSERS_DIR.split('/')[-1]
PARSERS_DIR_PARENT = str(Path(PARSERS_DIR).parent)
PARENT_NAME = Path(PARSERS_DIR).parent.name
UNWANTED_FILES = ['__init__.py', 'main_parser.py', 'constants.py']


def collect_parsers():
    sys.path.insert(0, PARSERS_DIR_PARENT)
    my_filename = Path(__file__).name
    parse_func = None
    for filename in os.listdir(PARSERS_DIR):
        if filename in UNWANTED_FILES:
            continue
        
        short_filename = filename[:-3] #ignoring the .py suffix
        #print(f"collect_parsers- short filename: {PARSERS_DIR_SHORT}.{short_filename}, parent: {PARSERS_DIR_PARENT}")
        #parse_module = import_module(f".{short_filename}", PARSERS_DIR_SHORT)
        #parse_module = import_module(f"{PARSERS_DIR_SHORT}.{short_filename}", package=PARSERS_DIR_SHORT)
        print(f"collect_parsers: {PARSERS_DIR_PARENT}.{PARSERS_DIR_SHORT}.{short_filename}")
        parse_module = import_module(f"{PARENT_NAME}.{PARSERS_DIR_SHORT}.{short_filename}")
        for obj_name,obj in getmembers(parse_module):
            if isfunction(obj) and obj_name.startswith("parse_"):
                __parsers__.add(obj)
                #we only need one function from each module
                break 


collect_parsers()
#print(__parsers__)

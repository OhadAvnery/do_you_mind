from importlib import import_module
from inspect import getmembers, isfunction
import os
from pathlib import Path

from .constants import __parsers__

PARSERS_DIR = "/home/user/do_you_mind/doyoumind/parsers"
PARSERS_DIR_SHORT = PARSERS_DIR.split('/')[-1]
UNWANTED_FILES = ['__init__.py', 'main_parser.py', 'constants.py']

def collect_parsers():
    my_filename = Path(__file__).name
    parse_func = None
    for filename in os.listdir(PARSERS_DIR):
        if filename in UNWANTED_FILES:
            continue
        
        short_filename = filename[:-3] #ignoring the .py suffix
        parse_module = import_module(f".{short_filename}", PARSERS_DIR_SHORT)
        for obj_name,obj in getmembers(parse_module):
            if isfunction(obj) and obj_name.startswith("parse_"):
                __parsers__.add(obj)
                #we only need one function from each module
                break 


collect_parsers()
from importlib import import_module
from inspect import getmembers, isfunction
import os
from pathlib import Path

__parsers__ = set()
PARSERS_DIR = "/home/user/do_you_mind/doyoumind/parsers"
PARSERS_DIR_SHORT = "parsers"
UNWANTED_FILES = ['__init__.py', 'main_parser.py']

def collect_parsers():
    my_filename = Path(__file__).name
    parse_func = None
    for filename in os.listdir(PARSERS_DIR):
        if filename in UNWANTED_FILES:
            continue
        
        short_filename = filename[:-3]
        
        parse_module = import_module(f".{short_filename}", PARSERS_DIR_SHORT)
        #print(f"collect_parsers: successfully imported {parse_module}")
        for obj_name,obj in getmembers(parse_module):
            if isfunction(obj) and obj_name.startswith("parse_"):
                __parsers__.add(obj)
                break

        """command = f"parse_func = {short_filename}.parse_{short_filename}"
        print(f"collect_parsers command: {command}")
        exec(command)
        __parsers__.add(parse_func)"""

collect_parsers()
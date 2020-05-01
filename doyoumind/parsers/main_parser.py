import os
from pathlib import Path

from ..constants import SUPPORTED_FIELDS
from .constants import __parsers__


class MainParser:
    def __init__(self, fields):
        self.fields = fields

    
    def parse(self, context, snapshot):
        for parse_func in __parsers__:
            for field in parse_func.fields:
                if field not in self.fields:
                    continue
            parse_func(context, snapshot)





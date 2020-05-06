import click
from furl import furl
import pika

from .constants import __parsers__
from ..mq.constants import SERVER_EXCHANGE, SAVER_EXCHANGE


@click.group()
def main():
    pass

def run_parser(parser_type, data):
    """
    Runs the parser with the given topic on the given data.
    Returns a string, to be later saved in the saver as the value of the topic. 
    """
    for parser in __parsers__:
        if parser.__name__ == f'parse_{parser_type}':
            return parser(data)

@main.command('parse')
@click.argument('parser_type', type=str)
@click.argument('path', type=str)
def parse_cli(parser_type, path):
    with open(path, 'rb') as f:
        data = f.read()
    print(run_parser(parser_type, data))

@main.command('run-parser')
@click.argument('parser_type', type=str)
@click.argument('url', type=str)
def run_parser_cli(parser_type, url):
    pass
print("parsers/main: is name==main?", __name__ == '__main__')
main()
import click
from furl import furl
import pika

from .constants import __parsers__
from ..mq.consumer_parser_atomic import ConsumerParserAtomic
from ..mq.publisher_saver_atomic import PublisherSaverAtomic
from ..utils.context import context_from_snapshot


@click.group()
def main():
    pass

def run_parser(parser_type, data):
    '''
    Runs the parser with the given topic on the given data.
    Returns a string, to be later saved in the saver as the value of the topic. 

    :param parser_type: the topic to be parsed (for example, 'depth_image')
    :type parser_type: str
    :param data: the snapshot data to be parsed (in json format)
    :type data: str
    :return: the result of the parser (in json format)
    :rtype: str
    '''
    for parser in __parsers__:
        if parser.__name__ == f'parse_{parser_type}':
            return parser(context_from_snapshot(data), data)

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
    publisher = PublisherSaverAtomic(url, parser_type)
    publish = publisher.publish #takes data as parameter
    consumer = ConsumerParserAtomic(url, parser_type, publish)
    consumer.consume()

main()
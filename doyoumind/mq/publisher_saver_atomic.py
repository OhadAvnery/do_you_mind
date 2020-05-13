from furl import furl
import json
import pika

from .constants import SAVER_EXCHANGE
#from ..parsers import run_parser
from ..parsers.constants import __parsers__
from ..utils.context import context_from_snapshot

def run_parser(parser_type, data):
    """
    Runs the parser with the given topic on the given data.
    Returns a string, to be later saved in the saver as the value of the topic. 
    """
    for parser in __parsers__:
        if parser.__name__ == f'parse_{parser_type}':
            return parser(context_from_snapshot(data), data)

class PublisherSaverAtomic:
    def __init__(self, url, topic):
        f = furl(url)
        self.url = f
        self.publish = PUBLISHER_SAVER_ATOMIC_SETUPS[f.scheme](f, topic)


def make_rabbitmq_publisher_saver_atomic(f, topic):
    """
    publishes the consumed parser result to the saver's queue.
    """
    print(f"calling make_rabbitmq_publisher_saver_atomic on: {f},{topic}")

    exchange = SAVER_EXCHANGE
    params = pika.ConnectionParameters(host=f.host, port=f.port)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    channel.exchange_declare(exchange=exchange, exchange_type='direct')
    parser_name = f"parse_{topic}"
    queue_name = f"{exchange}/{parser_name}"
    channel.queue_declare(queue=queue_name, durable=True)
    channel.queue_bind(exchange=exchange, routing_key=parser_name, queue=queue_name)
    def publish(msg):
        result = run_parser(topic, msg)
        channel.basic_publish(exchange=exchange, routing_key=parser_name, body=result)
        print("publisher_saver_atomic published!")
        #print(f"PUBLISHER: published message on exchange: {exchange} for parser: {parser}. \
        #    Routing key is: {routing_key}. exhange type is: {exchange_type}")

    return publish
  

    


PUBLISHER_SAVER_ATOMIC_SETUPS = {'rabbitmq': make_rabbitmq_publisher_saver_atomic}


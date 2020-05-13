from furl import furl
import json
import pika

from .constants import SERVER_EXCHANGE, SAVER_EXCHANGE
from ..parsers.constants import __parsers__
from ..utils.context import context_from_snapshot


class PublisherParser:
    def __init__(self, url):
        f = furl(url)
        self.url = f
        self.publish = PUBLISHER_PARSER_SETUPS[f.scheme](f)


def make_rabbitmq_publisher_parser(f):
    """
    Creates a new parsers exchange, and binds it to multiple queues,
    each one representing a different parser.
    Returns a function that given a message, publishes it to the exchange using fanout.
    """
    print(f"calling make_rabbitmq_publisher_parser on: {f}")
    exchange = SERVER_EXCHANGE

    #here, we don't need a routing key, as we're using fanout.


    params = pika.ConnectionParameters(host=f.host, port=f.port)
    print(f"publisher_parser- trying to connect with: {f.host},{f.port}")
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    channel.exchange_declare(exchange=exchange, exchange_type='fanout')
    for parser in __parsers__:
        parser_name = parser.__name__
        queue_name = f"{exchange}/{parser_name}"
        channel.queue_declare(queue=queue_name, durable=True)
        channel.queue_bind(exchange=exchange, queue=queue_name) #no need for routing key
    def publish(msg):
        channel.basic_publish(exchange=exchange, routing_key='', body=msg)
        print("publisher published!")
    return publish
  



PUBLISHER_PARSER_SETUPS = {'rabbitmq': make_rabbitmq_publisher_parser}
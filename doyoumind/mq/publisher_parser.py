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
    Creates a new exchange with the given name, and binds it to multiple queues,
    each one representing a different parser.
    Returns a function that given a message, publishes it to the exchange using fanout.
    for the publisher-->consumer interaction: SERVER_EXCHANGE.
    for the consumer-->saver: SAVER_EXCHANGE.
    """
    print(f"calling make_rabbitmq_publisher_parser on: {f}")
    exchange = SERVER_EXCHANGE

    #routing_key is either a constant- '', or it depends on the parser's name.
    #in the server's exchange, we don't need a routing key, as everything is direct.
    #in the saver's exchange, we update the routing key based on the message.

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
  


'''def publish_by_url(url, msg):
    """url: a url of the form 'rabbitmq://127.0.0.1:5672/' """
    print(f"publish_by_url - url: {url}")
    f = furl(url)
    print(f"publish_by_url - f: {f}")
    print(f"publish_by_url - scheme: {f.scheme}")
    publisher_func = PUBLISHERS[f.scheme]
    print(f"scheme: {f.scheme}, publisher func: {publisher_func}")
    publisher_func(url, msg)
    #main_parser = MainParser(SUPPORTED_FIELDS)
    #main_parser.parse(context, msg)

def publish_rabbit_mq(url, msg):
    f = furl(url)
    
    #channel.queue_declare(queue=QUEUE_NAME)'''
    


PUBLISHER_PARSER_SETUPS = {'rabbitmq': make_rabbitmq_publisher_parser}
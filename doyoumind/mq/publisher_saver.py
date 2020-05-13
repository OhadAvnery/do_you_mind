from furl import furl
import json
import pika

from .constants import SAVER_EXCHANGE
#from ..parsers import run_parser
from ..parsers.constants import __parsers__
from ..utils.context import context_from_snapshot



class PublisherSaver:
    def __init__(self, url):
        f = furl(url)
        self.url = f
        self.publish = PUBLISHER_SAVER_SETUPS[f.scheme](f)


def make_rabbitmq_publisher_saver(f):
    """
    Creates a new exchange with the given name, and binds it to multiple queues,
    each one representing a different parser.
    Returns a function that given a message, publishes it to the exchange using fanout.
    for the publisher-->consumer interaction: SERVER_EXCHANGE.
    for the consumer-->saver: SAVER_EXCHANGE.
    """
    print(f"calling make_rabbitmq_publisher_saver on: {f}")

    #routing_key is either a constant- '', or it depends on the parser's name.
    #in the server's exchange, we don't need a routing key, as everything is direct.
    #in the saver's exchange, we update the routing key based on the message.
    exchange = SAVER_EXCHANGE
    params = pika.ConnectionParameters(host=f.host, port=f.port)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    channel.exchange_declare(exchange=exchange, exchange_type='direct')
    for parser in __parsers__:
        parser_name = parser.__name__
        queue_name = f"{exchange}/{parser_name}"
        channel.queue_declare(queue=queue_name, durable=True)
        channel.queue_bind(exchange=exchange, routing_key=parser_name, queue=queue_name)
    def publish(parser):
        def publish_parser(msg):
            result = parser(context_from_snapshot(msg), msg)
            channel.basic_publish(exchange=exchange, routing_key=parser.__name__, body=result)
            print("publisher_saver published!")
            #print(f"PUBLISHER: published message on exchange: {exchange} for parser: {parser}. \
            #    Routing key is: {routing_key}. exhange type is: {exchange_type}")
        return publish_parser
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
    


PUBLISHER_SAVER_SETUPS = {'rabbitmq': make_rabbitmq_publisher_saver}


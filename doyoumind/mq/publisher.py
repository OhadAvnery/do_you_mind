from furl import furl
import json
import pika

from .constants import SERVER_EXCHANGE, SAVER_EXCHANGE
from ..parsers.constants import __parsers__



class Publisher:
    def __init__(self, url, exchange_name):
        f = furl(url)
        self.url = f
        self.publish = PUBLISHER_SETUPS[f.scheme](f, exchange_name)


def make_rabbitmq_publisher(f, exchange):
    """
    Creates a new exchange with the given name, and binds it to multiple queues,
    each one representing a different parser.
    Returns a function that given a message, publishes it to the exchange using fanout.
    for the publisher-->consumer interaction: SERVER_EXCHANGE.
    for the consumer-->saver: SAVER_EXCHANGE.
    """
    print(f"calling make_rabbitmq_publisher on: {f},{exchange}")

    if exchange == SERVER_EXCHANGE:
        exchange_type = 'fanout'
        routing_key = ''

    else: #exchange==SAVER_EXCHANGE
        exchange_type = 'direct'
        routing_key = 'non-empty key'


    params = pika.ConnectionParameters(host=f.host, port=f.port)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    channel.exchange_declare(exchange=exchange, exchange_type=exchange_type)
    for parser in __parsers__:
        parser_name = parser.__name__
        queue_name = f"{exchange}/{parser_name}"
        channel.queue_declare(queue=queue_name, durable=True)
        channel.queue_bind(exchange=exchange, routing_key=parser_name, queue=queue_name)
    def publish(msg):
        nonlocal routing_key
        #in the server's exchange, we don't need a routing key, as everything is direct.
        #in the saver's exchange, we update the routing key based on the message.
        if routing_key:
            routing_key = json.loads(msg)['parser'] 

        channel.basic_publish(exchange=exchange, routing_key=routing_key, body=msg)
        print("published message!")
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
    


PUBLISHER_SETUPS = {'rabbitmq': make_rabbitmq_publisher}

